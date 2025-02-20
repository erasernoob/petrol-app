clear 
clc
%输入参数————————————————————————————————————————————
guiji=xlsread('KL16-1-A25井眼轨迹.xlsx');
lbmx=1             %流变模型：1宾汉；2幂律；3赫巴
pailiang=1500      %排量，L/min
fluidden=1170      %钻井液密度，kg/m3   
n=0.48             %幂律指数
K=1.09             %稠度系数，pa·s^n
miu=0.021          %塑性粘度，Pa·s
taof=14            %屈服值，Pa
Dw=0.2159          %井眼直径，m
Rzz=0.127          %钻柱外径，m
rzz=0.1086         %钻柱内径，m
Lzz=4190           %钻柱长度，m
Rzt=0.15875        %钻铤外径，m
rzt=0.07144        %钻铤内径，m
Lzt=10             %钻铤长度，m
[ECD,Sk]=Hydro(guiji,lbmx,pailiang,fluidden,n,K,miu,taof,Dw,Rzz,rzz,Lzz,Rzt,rzt,Lzt);


%作ECD图————————————————————————————————————————————
figure;
plot(ECD, Sk);
xlabel('ECD（g/cm3）');
ylabel('井深（m）');
set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化

%导出ECD数据——————————————————————————————————————————————————————
writematrix(ECD, 'ECD.xlsx', 'Sheet', 1);