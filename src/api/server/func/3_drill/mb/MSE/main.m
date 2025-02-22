clear
clc
%导入参数————————————————————————————————————————————————————————
canshu=xlsread('BZ29-6-A26H.xlsx');

Depth=canshu(:,1);       %井深
WOB=canshu(:,2);         %钻压
Db=canshu(:,3);          %直径
RPM=canshu(:,4);         %转速
ROP=canshu(:,5);         %机械钻速

wob=WOB
rpm=RPM
rop=ROP
u=0.5;
WOB=WOB*1000/4.448222;                    %钻压单位转换
Db=Db/25.4;                               %直径单位转换
Ab=pi*(Db.^2)/4;                          %面积
T=(1/36)*u*WOB.*Db;                       %扭矩
ROP=ROP/0.3048;                           %机械钻速单位转换
MSE=(WOB./Ab)+(120*pi*RPM.*T./(Ab.*ROP));
MSE=MSE*0.0068947;                        %单位转换为MPa

%输出MSE图——————————————————————————————————————————————————————
figure('Position', [100, 100, 500, 800]); % [left, bottom, width, height]
plot(MSE, Depth, '-'); % 只绘制线，不绘制点
xlabel('MSE (MPa)');
ylabel('井深 (m)');
set(gca, 'YDir', 'reverse'); % 井深从上到下增加
%导出MSE数据——————————————————————————————————————————————————————
writematrix(MSE, 'MSE.xlsx', 'Sheet', 1);

%输出钻压图——————————————————————————————————————————————————————
figure('Position', [100, 100, 500, 800]); % [left, bottom, width, height]
plot(wob, Depth, '-'); % 只绘制线，不绘制点
xlabel('钻压 (kN)');
ylabel('井深 (m)');
set(gca, 'YDir', 'reverse'); % 井深从上到下增加

%输出转速图——————————————————————————————————————————————————————
figure('Position', [100, 100, 500, 800]); % [left, bottom, width, height]
plot(rpm, Depth, '-'); % 只绘制线，不绘制点
xlabel('转速 (RPM)');
ylabel('井深 (m)');
set(gca, 'YDir', 'reverse'); % 井深从上到下增加

%输出机械钻速图——————————————————————————————————————————————————————
figure('Position', [100, 100, 500, 800]); % [left, bottom, width, height]
plot(rop, Depth, '-'); % 只绘制线，不绘制点
xlabel('机械钻速 (m/h)');
ylabel('井深 (m)');
set(gca, 'YDir', 'reverse'); % 井深从上到下增加
