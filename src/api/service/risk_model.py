import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from torch.utils.data import Dataset, DataLoader
from scipy import signal
import pywt
from statsmodels.tsa.filters.hp_filter import hpfilter

# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 固定随机种子
torch.manual_seed(42)
np.random.seed(42)
if torch.cuda.is_available():
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# 检查GPU可用性并设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')


def preprocess_tva_data(df):
    """处理TVA数据并返回趋势"""
    original_data = df['TVA'].copy()

    # 预处理阶段
    def preprocess(data):
        data = data.interpolate(method='spline', order=3, limit_direction='both')
        window_size = 60
        median = data.rolling(window_size, center=True, min_periods=1).median()
        mad = (data - median).abs().rolling(window_size, center=True, min_periods=1).median()
        threshold = 3 * 1.4826 * mad
        data[(data - median).abs() > threshold] = np.nan
        return data.interpolate(method='linear')

    processed = preprocess(original_data)

    # 动态阈值滤波
    def dynamic_threshold_filter(data, window_size=60, n_sigma=5):
        cleaned = data.copy()
        for i in range(len(data)):
            start = max(0, i - window_size // 2)
            end = min(len(data), i + window_size // 2)
            window = data.iloc[start:end]
            if window.notna().sum() < 5:
                continue
            local_median = window.median()
            mad = (window - local_median).abs().median()
            if mad == 0:
                continue
            z_score = 0.6745 * (data.iloc[i] - local_median) / mad
            if abs(z_score) > n_sigma:
                cleaned.iloc[i] = local_median
        return cleaned

    filtered = dynamic_threshold_filter(processed)

    # 巴特沃斯低通滤波
    def butter_lowpass_filter(data, cutoff=0.1, fs=10, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype='low')
        return pd.Series(signal.filtfilt(b, a, data), index=data.index)

    lowpass_filtered = butter_lowpass_filter(filtered)

    # 小波去噪
    def wavelet_denoise(data, wavelet='db8', level=6):
        coeffs = pywt.wavedec(data, wavelet, level=level)
        sigma = np.median(np.abs(coeffs[-level])) / 0.6745
        uthresh = sigma * np.sqrt(2 * np.log(len(data)))
        coeffs[1:] = [pywt.threshold(c, value=uthresh, mode='soft') for c in coeffs[1:]]
        return pd.Series(pywt.waverec(coeffs, wavelet), index=data.index)

    wavelet_denoised = wavelet_denoise(lowpass_filtered)

    # 趋势提取
    def extract_trend(data, lamb=100):
        cycle, trend = hpfilter(data, lamb=lamb)
        return trend

    final_trend = extract_trend(wavelet_denoised)

    return final_trend


class DrillingDataset(Dataset):
    def __init__(self, features, targets, window_size=10):
        self.features = features
        self.targets = targets
        self.window_size = window_size

    def __len__(self):
        return len(self.features) - self.window_size

    def __getitem__(self, idx):
        x = self.features[idx:idx + self.window_size]
        y = self.targets[idx + self.window_size]
        return torch.FloatTensor(x), torch.FloatTensor([y])


class CNNBiLSTMAttention(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size, LSTM_nums):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(input_size, LSTM_nums, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2)
        )
        self.bilstm = nn.LSTM(LSTM_nums, hidden_size, num_layers,
                              bidirectional=True, batch_first=True)
        self.attention = nn.Sequential(
            nn.Linear(2 * hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1),
            nn.Softmax(dim=1)
        )
        self.fc = nn.Linear(2 * hidden_size, output_size)

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = self.conv(x)
        x = x.permute(0, 2, 1)
        lstm_out, _ = self.bilstm(x)
        attention_weights = self.attention(lstm_out)
        context_vector = torch.sum(attention_weights * lstm_out, dim=1)
        output = self.fc(context_vector)
        return output


def prepare_data(train_path, test_path, window_size=10):
    """直接从分开的训练集和测试集文件准备数据"""
    # 读取训练集和测试集
    # 判断是否是excel 或者 csv
    if is_csv(train_path):
        train_df = pd.read_csv(train_path)
    else:
        train_df = pd.read_excel(train_path)

    if is_csv(test_path):
        test_df = pd.read_csv(test_path)
    else:
        test_df = pd.read_excel(test_path)

    # 预处理TVA数据
    train_df['TVA_trend'] = preprocess_tva_data(train_df)
    test_df['TVA_trend'] = preprocess_tva_data(test_df)

    # 提取特征和目标
    X_train = train_df[['WOBA', 'ROPA', 'TQA', 'RPMA']].values
    y_train = train_df['TVA_trend'].values.reshape(-1, 1)

    X_test = test_df[['WOBA', 'ROPA', 'TQA', 'RPMA']].values
    y_test = test_df['TVA_trend'].values.reshape(-1, 1)

    # 标准化 - 使用训练集的统计量来标准化测试集
    scaler_x = StandardScaler()
    X_train = scaler_x.fit_transform(X_train)
    X_test = scaler_x.transform(X_test)

    scaler_y = StandardScaler()
    y_train = scaler_y.fit_transform(y_train)
    y_test = scaler_y.transform(y_test)

    # 创建DataLoader
    train_dataset = DrillingDataset(X_train, y_train, window_size)
    test_dataset = DrillingDataset(X_test, y_test, window_size)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    return train_loader, test_loader, scaler_y


def train_model(model, train_loader, criterion, optimizer, num_epochs=100):
    model.train()
    model.to(device)

    for epoch in range(num_epochs):
        total_loss = 0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {total_loss / len(train_loader):.4f}')

    # 训练完成后输出标识并保存模型
    print("✅ 训练完成！模型已训练完毕，正在保存模型...")
    torch.save(model.state_dict(), 'trained_model.pth')  # 保存训练好的模型


def load_model(model, model_path='trained_model.pth'):
    model.load_state_dict(torch.load(model_path))  # 加载训练好的模型
    model.eval()  # 切换到评估模式
    return model


def evaluate_model(model, test_loader, scaler):
    model.eval()
    model.to(device)
    y_true = []
    y_pred = []

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)

            y_true.extend(targets.cpu().numpy())
            y_pred.extend(outputs.cpu().numpy())

    y_true = np.array(y_true).reshape(-1, 1)
    y_pred = np.array(y_pred).reshape(-1, 1)

    # 检查 y_true 是否有效（没有实际值或全是NaN）
    if np.isnan(y_true).all() or len(y_true) == 0:
        print("⚠️ 测试集中没有有效的真实TVA值，指标设置为0")
        return 0, 0, 0, y_true, y_pred

    # 逆标准化
    y_true = scaler.inverse_transform(y_true)
    y_pred = scaler.inverse_transform(y_pred)

    # 计算指标
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    return mae, rmse, r2, y_true, y_pred

def is_csv(filename):
    try:
        pd.read_csv(filename)
        return True
    except Exception:
        return False

def train_main(
    train_path,
    test_path,
    LSTM_nums = 64, # LSTM个数
    LSTM_layers = 2, # LSTM层数
    neuron_cnt = 128,
    window_size = 30,
    lr = 0.001,
    num_epochs = 50, # 训练批次
):
    input_size = 4  # 特征数量，注意只包括 WOBA, ROPA, TQA, RPMA（TVA 是目标）
    output_size = 1
    window_size = 30

    # test_path = "F:\\pertrol\\井漏风险预测\\录井数据-标签\\JX-1-1-B38\\20201205_190000_JX1-1-B38.csv"
    # train_path = "F:\\pertrol\\井漏风险预测\\录井数据-标签\\JX-1-1-B38\\20201205_190000_JX1-1-B38.csv"
    
    # 准备数据
    train_loader, test_loader, scaler_y = prepare_data(train_path, test_path, window_size)

    # 初始化模型
    model = CNNBiLSTMAttention(input_size, neuron_cnt, LSTM_layers, output_size, LSTM_nums)
    model_obj = CNNBiLSTMAttention(input_size, neuron_cnt, LSTM_layers, output_size, LSTM_nums)
    criterion = nn.L1Loss()
    optimizer = optim.Adam(model.parameters(), lr)

    # 训练模型
    print("正在训练模型...")
    model = train_model(model, train_loader, criterion, optimizer, num_epochs)
    return model_obj, test_loader, scaler_y

def generate_predict(model, test_loader, scaler_y):
    # 加载训练好的模型
    print("正在加载训练好的模型...")
    model = load_model(model)

    # 测试模型
    print("\n正在测试模型...")
    mae, rmse, r2, y_true, y_pred = evaluate_model(model, test_loader, scaler_y)
    print(f'\n📊 测试指标:\nMAE: {mae:.4f}\nRMSE: {rmse:.4f}\nR²: {r2:.4f}')

    #  返回预测值和测试指标
    return {
        "TVA": y_pred,
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "R": round(r2, 4),
    }

    # # 绘制预测曲线（不显示真实值）
    # plt.figure(figsize=(12, 6))
    # plt.plot(y_pred, label='TVA预测值', alpha=0.7)  # 仅绘制预测值
    # plt.xlabel('时间（s）')
    # plt.ylabel('TVA(${m^3}$)')
    # plt.legend()
    # plt.show()
