clear 
clc
%输入参数————————————————————————————————————————————
guiji=xlsread('KL16-1-A25井眼轨迹.xlsx');
zuanju=xlsread('钻具组合_4200m.xlsx');
wc=1;                    %工况选择：1旋转钻进；2滑动钻进；3起钻；4下钻；5倒划眼
v=0.00714;               %钻进速度，m/s               
omega=5*pi/3;            %转速，rad/s
T0=58900;                %钻压，N
rhoi=1170;               %钻井液密度，kg/m3 
Dw=0.2159;               %井眼直径，m
tgxs=3500;               %套管下深，m
miua11=0.15;             %套管段摩阻系数
miua22=0.20;             %裸眼段摩阻系数  
qfqd=931;                %钻柱屈服强度，MPa
jsjg=500;                %井深计算间隔，m
[Tjk,Mjk,aqjk]=mainfunc(guiji,zuanju,wc,T0,rhoi,Dw,tgxs,miua11,miua22,qfqd,jsjg,v,omega)