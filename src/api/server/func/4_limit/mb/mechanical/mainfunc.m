function [Tjk,Mjk,aqjk]=mainfunc(guiji,zuanju,wc,T0,rhoi,Dw,tgxs,miua11,miua22,qfqd,jsjg,v,omega)
data1=guiji;
data2=zuanju;
working_condition=wc;     %工况选择：1旋转钻进；2滑动钻进；3起钻；4下钻；5倒划眼
if working_condition==1
    %输入参数————————————————————————————————————————————
    T0=T0;                   %钻压，N
    rhoi=rhoi;               %钻井液密度，kg/m3 
    Dw=Dw;                   %井眼直径，m
    tgxs=tgxs;               %套管下深，m
    miua1=miua11/30;          %套管段摩阻系数
    miua2=miua22/30;          %裸眼段摩阻系数
    miut1=miua11*1.2;        %套管段切向摩阻系数
    miut2=miua22*1.2;        %裸眼段切向摩阻系数
    qfqd=qfqd;               %钻柱屈服强度，MPa
    jsjg=jsjg;               %计算井深间隔，m
    %固定值——————————————————————————————————————————————
    M0=abs(T0*Dw/3*0.5);         %钻头扭矩
    v=v;                     %钻进速度，m/s               
    omega=omega;             %转速，rad/s
    miu=0.2;                 %钻井液塑性粘度，mPa·s
    taof=14;                 %钻井液屈服值，Pa
    sign1=1;                 %钻柱运动方向：1下入；-1上提
    sign2=1;                 %钻柱是否旋转：1旋转；0不旋转
elseif working_condition==2
    %输入参数————————————————————————————————————————————
    T0=T0;                   %钻压，N
    rhoi=rhoi;               %钻井液密度，kg/m3 
    Dw=Dw;                   %井眼直径，m
    tgxs=tgxs;               %套管下深，m
    miua1=miua11*1.165;      %套管段摩阻系数
    miua2=miua22*1.165;      %裸眼段摩阻系数
    miut1=0;                 %套管段切向摩阻系数
    miut2=0;                 %裸眼段切向摩阻系数  
    qfqd=qfqd;               %钻柱屈服强度，MPa
    jsjg=jsjg;               %计算井深间隔，m
    %固定值——————————————————————————————————————————————
    M0=0;                    %钻头扭矩
    miu=0.2;                 %钻井液塑性粘度，mPa·s
    taof=14;                 %钻井液屈服值，Pa
    v=1;                     %钻进速度，m/s
    omega=0;                 %转速，rad/s
    sign1=1;                 %钻柱运动方向：1下入；-1上提
    sign2=0;                 %钻柱是否旋转：1旋转；0不旋转
elseif working_condition==3
    %输入参数————————————————————————————————————————————               
    rhoi=rhoi;               %钻井液密度，kg/m3
    Dw=Dw;                   %井眼直径，m
    tgxs=tgxs;               %套管下深，m
    miua1=miua11*1.09;       %套管段摩阻系数
    miua2=miua22*1.09;       %裸眼段摩阻系数
    miut1=0;                 %套管段切向摩阻系数
    miut2=0;                 %裸眼段切向摩阻系数
    qfqd=qfqd;               %钻柱屈服强度，MPa
    jsjg=jsjg;               %计算井深间隔，m
    %固定值——————————————————————————————————————————————
    T0=0;                    %钻压，N
    M0=0;                    %钻头扭矩
    miu=0.2;                 %钻井液塑性粘度，mPa·s
    taof=14;                 %钻井液屈服值，Pa
    v=1;                     %上提速度，m/s
    omega=0;                 %转速，rad/s
    sign1=-1;                %钻柱运动方向：1下入；-1上提
    sign2=0;                 %钻柱是否旋转：1旋转；0不旋转
elseif working_condition==4
    %输入参数————————————————————————————————————————————
    rhoi=rhoi;               %钻井液密度，kg/m3
    Dw=Dw;                   %井眼直径，m
    tgxs=tgxs;               %套管下深，m
    miua1=miua11*1.17;       %套管段摩阻系数
    miua2=miua22*1.17;       %裸眼段摩阻系数
    miut1=0;                 %套管段切向摩阻系数
    miut2=0;                 %裸眼段切向摩阻系数
    qfqd=qfqd;               %钻柱屈服强度，MPa
    jsjg=jsjg;               %计算井深间隔，m
    %固定值——————————————————————————————————————————————
    T0=0;                    %钻压，N
    M0=0;                    %钻头扭矩
    miu=0.2;                 %钻井液塑性粘度，mPa·s
    taof=14;                 %钻井液屈服值，Pa
    v=1;                     %下放速度，m/s               
    omega=0;                 %转速，rad/s
    sign1=1;                 %钻柱运动方向：1下入；-1上提
    sign2=0;                 %钻柱是否旋转：1旋转；0不旋转
elseif working_condition==5
    %输入参数———————————————————————————————————————————— 
    rhoi=rhoi;               %钻井液密度，kg/m3
    Dw=Dw;                   %井眼直径，m
    tgxs=tgxs;               %套管下深，m
    miua1=miua11/1.5;                 %套管段摩阻系数
    miua2=miua22/1.5;                 %裸眼段摩阻系数
    miut1=miua11*1.2;        %套管段切向摩阻系数
    miut2=miua22*1.2;        %裸眼段切向摩阻系数
    qfqd=qfqd;               %钻柱屈服强度，MPa
    jsjg=jsjg;               %计算井深间隔，m
    %固定值——————————————————————————————————————————————
    T0=0;                    %钻压，N
    M0=0;                    %钻头扭矩，N·m
    v=v;                     %上提速度，m/s               
    omega=omega;            %转速，rad/s
    miu=0.2;                 %钻井液塑性粘度，mPa·s
    taof=14;                 %钻井液屈服值，Pa
    sign1=-1;                %钻柱运动方向：1下入；-1上提
    sign2=1;                 %钻柱是否旋转：1旋转；0不旋转
end

%基础参数
rhoo=rhoi;       %钻柱外流体密度
T0=-T0;
g=9.81;          %重力加速度
E=2.1e11;        %钻柱弹性模量

jd=data1(:,1);
yssd=jd(end);
% num_iterations = yssd/jsjg;
num_iterations = ceil(yssd / jsjg);

T_result=zeros(num_iterations*jsjg,num_iterations);
M_result=zeros(num_iterations*jsjg,num_iterations);
aq_result=zeros(num_iterations*jsjg,num_iterations);

for nn=1:num_iterations
%     js=nn*jsjg;
    if nn == num_iterations
        % 最后一次迭代时使用 guiji 最后的值
        js = yssd;
    else
        % 否则按正常的间隔计算
        js = nn * jsjg;
    end

%钻具长度确定
row_data=data2(4, 1:end-1);
row_sum=sum(row_data);
data2(4,end)=js-row_sum

%钻具组合参数
Dtrans=data2(1,:);             %钻柱外径，m
dtrans=data2(2,:);             %钻柱内径，m
mtrans=9.81*data2(3,:);        %钻柱组合线重，N/m
ltrans=data2(4,:); 

%%
%钻具组合参数
Ntrans=numel(Dtrans);                   %所加载的钻具组合数量
nntrans=zeros(Ntrans,1);                %即nntrans的前n项累加
ntrans=sum(ltrans);                     %所加载的钻具组合总分段数（计算步长）
Rt=zeros(ntrans,1);                     %各段钻具组合外半径/m
rt=zeros(ntrans,1);                     %各段钻具组合内半径/m
Aot=zeros(ntrans,1);                    %各段钻具组合外截面积/m^2
Ait=zeros(ntrans,1);                    %各段钻具组合内截面积/m^2
qt=zeros(ntrans,1);                     %各段钻具组合线重/N.m^-1
qmt=zeros(ntrans,1);                    %各段钻具组合浮重/N.m^-1
Kft=zeros(ntrans,1);                    %浮力系数
It=zeros(ntrans,1);                     %惯性矩
ht=zeros(ntrans,1);                     %壁厚
%计算nnntrans，便于后续计算
nntrans(1)=ltrans(1);
for i=2:Ntrans
    nntrans(i)=nntrans(i-1)+ltrans(i);
end
%计算钻具组合各分段的半径、截面积、线重
for i=1:Ntrans
    if i==1
        for j=1:nntrans(i)
            Rt(j)=Dtrans(i)/2;  
            rt(j)=dtrans(i)/2;
            Aot(j)=pi*Rt(j).^2;
            Ait(j)=pi*rt(j).^2;
            qt(j)=mtrans(i);
            qmt(j)=qt(j)-(Aot(j)-Ait(j))*rhoi*g;
            Kft(j)=qmt(j)/qt(j);
            It(j)=pi*(Rt(j)^4-rt(j)^4)/8;
            ht(j)=Rt(j)-rt(j);
        end
    else
        for j=nntrans(i-1)+1:nntrans(i)
            Rt(j)=Dtrans(i)/2;
            rt(j)=dtrans(i)/2;
            Aot(j)=pi*Rt(j).^2;
            Ait(j)=pi*rt(j).^2;
            qt(j)=mtrans(i);
            qmt(j)=qt(j)-(Aot(j)-Ait(j))*rhoi*g;
            Kft(j)=qmt(j)/qt(j);
            It(j)=pi*(Rt(j)^4-rt(j)^4)/8;
            ht(j)=Rt(j)-rt(j);
        end
    end
end

%%
%计算参数
ds=1;                      %步长
len=ntrans-1;              %计算长度
sspan=0:ds:len;
miua=zeros(ntrans,1);
miut=zeros(ntrans,1);

for i=1:ntrans
    if i>=ntrans-tgxs
        miua(i)=miua1;
        miut(i)=miut1;
    else
        miua(i)=miua2;
        miut(i)=miut2;
    end
end

%%
%处理井眼轨迹函数
[Mk,mk,Sk,alphak,phik]=deal_curve_data(data1,js);

%%
%初始化k和tao等参数
[alpha,phi,ks,dks,ddks,kphis,kalphas,taos]=prepare_data(sspan,Mk,mk,Sk,alphak,phik);

%%
%开始计算
Ttemp=T0;
Mtemp=M0;
Nbtemp=0;
Nntemp=0;
[s,y]=ode45(@(s,y)odefunc(s,y,ks,dks,ddks,kphis,kalphas,taos,sspan,v,omega,taof,miu,Rt,Dw,miua,miut,qmt...
    ,Ait,Aot,rhoi,rhoo,E,It,g,Mk,mk,Sk,alphak,phik,Ttemp,Mtemp,Nbtemp,Nntemp,sign1,sign2),0:ds:len,[T0;M0]);
% T11=y(:,1);
% M=y(:,2);
% T11=flipud(T11);
% for i=1:ntrans
% T(i)=T11(i);
% end
% T=T';
T=y(:,1);
M=y(:,2);
T=flipud(T);
%%
%数据恢复
Nbtemp=0;
Nntemp=0;
Ttemp=T0;
Mtemp=M0;
[N,~,~]=data_recovery(s,y,ks,dks,ddks,kphis,kalphas,taos,sspan,v,omega,taof,miu,Rt,Dw,miua,miut,qmt...
    ,Ait,Aot,rhoi,rhoo,E,It,g,Mk,mk,Sk,alphak,phik,Ttemp,Mtemp,Nbtemp,Nntemp,sign1,sign2);

%%
%表达摩阻
for i=1:ntrans
    if i<28
        N(i)=N(i)*0.3157407408;
    else
        N(i)=N(i);
    end
end
F=zeros(numel(N),1);
for i=1:ntrans
    F(i)=N(i)*miua(i);
end
%原累计摩阻
Flj=zeros(numel(N),1);
Flj(1)=N(1)*miua(i);
for i=2:ntrans
    Flj(i)=Flj(i-1)+N(i)*miua(i);
end

%%
%输出
alpha=flipud(alpha)*180/pi;
phi=flipud(phi)*180/pi;
T=T/1000;
M=flipud(M)/1000;
F=flipud(F);
Flj=flipud(Flj)/1000;

if working_condition==1
    Flj=Flj
elseif working_condition==2
    Flj=Flj
elseif working_condition==3
    Flj=Flj
elseif working_condition==4
    Flj=Flj
elseif working_condition==5
    Flj=Flj
end

if working_condition==2 ||working_condition==3 || working_condition==4
       M(:)=0;
end

aq=qfqd/(T(1,1)*1000/(pi*((Dtrans(end)/2)^2-(dtrans(end)/2)^2))/1000000)

T_result(1:length(T), nn) = T;
M_result(1:length(M), nn) = M;
aq_result(1:length(aq), nn) = aq;
end
Tjk=T_result(1,:)'
Mjk=M_result(1,:)'
aqjk=aq_result(1,:)'

%% 输出各工况结果
%旋转钻进
if working_condition==1
    %输出井口轴向力图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, T_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口轴向力（kN）'); % y轴标签
    %导出井口轴向力数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, T_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '旋转钻进_井口轴向力.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出井口扭矩图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, M_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口扭矩（kN·m）'); % y轴标签
    %导出井口扭矩数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, M_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '旋转钻进_井口扭矩.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出安全系数图—————————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, aq_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('安全系数'); % y轴标签
    %导出安全系数数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, aq_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '旋转钻进_安全系数.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
%滑动钻进
elseif working_condition==2
    %输出井口轴向力图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, T_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口轴向力（kN）'); % y轴标签
    %导出井口轴向力数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, T_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '滑动钻进_井口轴向力.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出井口扭矩图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, M_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口扭矩（kN·m）'); % y轴标签
    %导出井口扭矩数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, M_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '滑动钻进_井口扭矩.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出安全系数图—————————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, aq_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('安全系数'); % y轴标签
    %导出安全系数数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, aq_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '滑动钻进_安全系数.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
%起钻
elseif working_condition==3
    %输出井口轴向力图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, T_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口轴向力（kN）'); % y轴标签
    %导出井口轴向力数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, T_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '起钻_井口轴向力.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出井口扭矩图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, M_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口扭矩（kN·m）'); % y轴标签
    %导出井口扭矩数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, M_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '起钻_井口扭矩.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出安全系数图—————————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, aq_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('安全系数'); % y轴标签
    %导出安全系数数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, aq_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '起钻_安全系数.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
%下钻
elseif working_condition==4
    %输出井口轴向力图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, T_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口轴向力（kN）'); % y轴标签
    %导出井口轴向力数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, T_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '下钻_井口轴向力.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出井口扭矩图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, M_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口扭矩（kN·m）'); % y轴标签
    %导出井口扭矩数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, M_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '下钻_井口扭矩.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出安全系数图—————————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, aq_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('安全系数'); % y轴标签
    %导出安全系数数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, aq_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '下钻_安全系数.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
%倒划眼
elseif working_condition==5
    %输出井口轴向力图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, T_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口轴向力（kN）'); % y轴标签
    %导出井口轴向力数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, T_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '倒划眼_井口轴向力.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出井口扭矩图————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, M_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('井口扭矩（kN·m）'); % y轴标签
    %导出井口扭矩数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, M_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '倒划眼_井口扭矩.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
    %输出安全系数图—————————————————————————————————————————————————
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % 计算横坐标，包括 jsjg 间隔和最终深度 yssd
    plot(x_coords, aq_result(1, :)); % 绘制井口轴向力图
    xlabel('井深（m）'); % x轴标签
    ylabel('安全系数'); % y轴标签
    %导出安全系数数据————————————————————————————————————————————
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % 横坐标，包含 jsjg 间隔和最终深度 yssd
    dataToExport = [x_coords, aq_result(1, :)']; % 将横坐标和对应轴向力合并为数据表
    writematrix(dataToExport, '倒划眼_安全系数.xlsx', 'Sheet', 1, 'Range', 'A1'); % 导出为 Excel 文件
end

end