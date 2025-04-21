import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks
from statsmodels.tsa.filters.hp_filter import hpfilter
from pathlib import Path

# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def process_tva_column(df, show_plot=True, window_size=60, cutoff=0.1, lamb=100):
    # df = pd.read_excel(input_path, engine='openpyxl')
    print(df.head)
    if 'TVA' not in df.columns:
        raise ValueError("数据文件中未找到TVA列")

    data = df['TVA'].interpolate(method='linear', limit_direction='both')
    median = data.rolling(window_size, center=True, min_periods=1).median()
    mad = (data - median).abs().rolling(window_size, center=True, min_periods=1).median()
    threshold = 3 * 1.4826 * mad
    data = data.where((data - median).abs() <= threshold, median)

    nyq = 0.5 * 10  # 采样频率 = 10Hz
    b, a = signal.butter(5, cutoff / nyq, btype='low')
    filtered = pd.Series(signal.filtfilt(b, a, data), index=data.index)

    cycle, trend = hpfilter(filtered, lamb=lamb)

    # 直接返回去噪后的趋势数据，不保存
    return trend

def analyze_trend(tva_data):
    try:
        x = np.arange(len(tva_data))  # 时间序列

        dy = np.gradient(tva_data, x)
        d2y = np.gradient(dy, x)

        sign_changes = np.where(np.diff(np.sign(d2y)) != 0)[0]
        threshold = np.percentile(np.abs(d2y), 90)
        valid_inflections = [i for i in sign_changes if abs(d2y[i]) > threshold]

        peaks, _ = find_peaks(tva_data, prominence=0.5)
        valleys, _ = find_peaks(-tva_data, prominence=0.5)

        filtered_peaks = []
        filtered_valleys = []
        all_extrema = np.sort(np.concatenate([peaks, valleys]))
        extrema_types = [1 if ext in peaks else -1 for ext in all_extrema]

        i = 0
        while i < len(all_extrema) - 1:
            current = all_extrema[i]
            next_ = all_extrema[i + 1]
            if extrema_types[i] * extrema_types[i + 1] == -1:
                diff = abs(tva_data[current] - tva_data[next_])
                if diff >= 3:
                    if extrema_types[i] == 1:
                        filtered_peaks.append(current)
                        filtered_valleys.append(next_)
                    else:
                        filtered_valleys.append(current)
                        filtered_peaks.append(next_)
                    i += 2
                    continue
            i += 1

        filtered_peaks = np.unique(np.array(filtered_peaks))
        filtered_valleys = np.unique(np.array(filtered_valleys))

        combined = []
        combined.extend(zip(filtered_peaks, ['peak'] * len(filtered_peaks)))
        combined.extend(zip(filtered_valleys, ['valley'] * len(filtered_valleys)))
        combined_sorted = sorted(combined, key=lambda x: x[0])

        if len(combined_sorted) > 0 and combined_sorted[0][1] == 'peak':
            combined_sorted.pop(0)

        differences = []
        i = 0
        while i < len(combined_sorted) - 1:
            current_pos, current_type = combined_sorted[i]
            next_pos, next_type = combined_sorted[i + 1]
            if current_type != next_type:
                diff = abs(tva_data[current_pos] - tva_data[next_pos])
                differences.append({
                    'peak_index': current_pos if current_type == 'peak' else next_pos,
                    'valley_index': current_pos if current_type == 'valley' else next_pos,
                    'difference': diff
                })
                i += 2
            else:
                i += 1

        if len(differences) > 0:
            dynamic_thresholds = []
            danger_zones = []
            current_threshold = differences[0]['difference']
            dynamic_thresholds.append(current_threshold)

            first_diff = differences[0]['difference']
            peak_idx = differences[0]['peak_index']
            valley_idx = differences[0]['valley_index']
            start_idx = min(peak_idx, valley_idx)
            end_idx = max(peak_idx, valley_idx)
            ratio = first_diff / current_threshold
            if ratio >= 1.5:
                danger_zones.append((start_idx, end_idx, 'Ⅱ', 'red', current_threshold))
            elif ratio >= 1.2:
                danger_zones.append((start_idx, end_idx, 'Ⅰ', 'gold', current_threshold))
            else:
                dynamic_thresholds.append(first_diff)

            for i in range(1, len(differences)):
                current_diff = differences[i]['difference']
                peak_idx = differences[i]['peak_index']
                valley_idx = differences[i]['valley_index']
                start_idx = min(peak_idx, valley_idx)
                end_idx = max(peak_idx, valley_idx)
                current_threshold = np.mean(dynamic_thresholds)
                ratio = current_diff / current_threshold
                if ratio >= 1.5:
                    danger_zones.append((start_idx, end_idx, 'Ⅱ', 'red', current_threshold))
                elif ratio >= 1.0:
                    danger_zones.append((start_idx, end_idx, 'Ⅰ', 'gold', current_threshold))
                dynamic_thresholds.append(current_diff)
        else:
            danger_zones = []
        


        # # 绘图
        # plt.figure(figsize=(12, 8))
        # plt.plot(x, tva_data, label="TVA值", color="blue", alpha=0.7)  # 改为 "TVA值"
        # for zone in danger_zones:
        #     start, end, level, color, threshold = zone
        #     plt.fill_between(x[start:end + 1], tva_data[start:end + 1], color=color, alpha=0.3, label=f"危险等级 {level}")
        #     mid_point = (x[start] + x[end]) / 2
        #     plt.annotate(f'阈值: {threshold:.2f}',
        #                  xy=(x[start], tva_data[start]),
        #                  xytext=(mid_point, max(tva_data[start:end + 1]) + 5),
        #                  arrowprops=dict(arrowstyle="->", color=color),
        #                  bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8), fontsize=8, ha='center')

        # plt.scatter(x[filtered_peaks], tva_data[filtered_peaks], c="red", marker="^", s=100, label="波峰")
        # plt.scatter(x[filtered_valleys], tva_data[filtered_valleys], c="green", marker="v", s=100, label="波谷")
        # handles, labels = plt.gca().get_legend_handles_labels()
        # by_label = dict(zip(labels, handles))
        # plt.legend(by_label.values(), by_label.keys(),
        #            loc='upper center', bbox_to_anchor=(0.5, 1.05),
        #            ncol=6, frameon=False)
        # plt.xlabel("时间(s)")
        # plt.ylabel("TVA(${m^3}$)")
        # plt.grid(True, linestyle='--', alpha=0.5)
        # plt.tight_layout()
        # plt.show()

        # print("\n动态阈值详细信息：")
        # print(f"{'-' * 70}")
        # print(f"{'区间':<10}{'起始点':<12}{'结束点':<12}{'差值':<12}{'使用阈值':<15}{'预警等级':<10}")
        # print(f"{'-' * 70}")
        # if len(danger_zones) == 0:
        #     print("无危险区间检测到")
        # else:
        #     for i, zone in enumerate(danger_zones):
        #         start, end, level, color, threshold = zone
        #         diff = abs(tva_data[start] - tva_data[end])
        #         print(f"{i + 1:<10}{start:<12}{end:<12}{diff:<12.2f}{threshold:<15.2f}{level:<10}")
        # print(f"{'-' * 70}")

        return {
            "x": x.tolist(),
            "tva_data": tva_data.tolist(),
            "peaks": filtered_peaks.tolist(),
            "valleys": filtered_valleys.tolist(),
            "danger_zones": [
                {
                    "start": int(start),
                    "end": int(end),
                    "level": level,
                    "color": color,
                    "threshold": float(threshold)
                } for start, end, level, color, threshold in danger_zones
            ]
        }

    except Exception as e:
        print(f"分析过程中发生错误：{str(e)}")

if __name__ == "__main__":
    input_file = "F:\\井漏预测\\测试集\\20201205_190000_JX1-1-B38.xlsx"

    # 运行去噪后的最终趋势数据
    trend = process_tva_column(input_path=input_file, show_plot=False)

    if trend is not None:
        print("TVA数据处理完成！")
        # 使用去噪后的趋势数据进行危险区间分析
        analyze_trend(trend)
    else:
        print("TVA数据处理失败，无法进行趋势分析")
