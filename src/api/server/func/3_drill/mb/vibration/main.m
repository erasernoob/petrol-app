clear
clc
global wob WOB v V Lp Lpw Lc Lb p1 p2 p3 Dp Dpw Dc dp dpw dc Db Rb dl np npw nc Lv nv n Jp Jpw Jc Jb Kp Kpw Kpc Kcb Cp Cpw Cpc Ccb Cb miusb miucb Dv gamab uf miuS Sp Spw Sc Sb Dwell Dlp Dlpw Dlc Dlb sita3 sita100 sita200 sigma k nl 
%输入参数——————————————————————————————————————————————————————————————————————————————
%基本钻具参数————————————————————————————————————————————————————
Lb=0.24;          %钻头长度，m
Db=0.2159;        %钻头直径，m
Lp=5765.26;       %钻杆长度，m
p1=8629;          %钻杆密度，kg/m3
Dp=0.127;         %钻杆外径，m
dp=0.1086;        %钻杆内径，m
Lpw=47.26;        %加重钻杆长度，m
p3=9058;          %加重钻杆密度，kg/m3
Dpw=0.127;        %加重钻杆外径，m
dc=0.0572;        %加重钻杆内径，m
Lc=6.89;          %钻铤长度，m
p2=8518;          %钻铤密度，kg/m3
Dc=0.1715;        %钻铤外径，m
dpw=0.0762;       %钻铤内径，m
%钻井液——————————————————————————————————————————————————————————
uf=67;            %钻井液塑性粘度 mPa.s
sita3=7;          %旋转粘度计读数（3转）
sita100=41;       %旋转粘度计读数（100转）
sita200=69;       %旋转粘度计读数（200转）
%计算参数————————————————————————————————————————————————————————
wob=100;          %钻压，kN
V=90;             %转速，RPM
miusb=0.8;        %静摩擦系数
miucb=0.5;        %动摩擦系数
Lv=3306;          %垂直段长度，m
dl=500;           %质量块长度，m
TIME=50;          %计算时长，s
Dt=0.01;          %时间步长，s

% 自动计算参数
WOB=wob*1000
v=(V)/60*2*pi;                %转速 rad/s
welldepth=Lp+Lpw+Lc+Lb;     %井深
Rb=Db/2;                    %钻头半径

np=ceil(Lp/dl);    %钻杆质量块个数
npw=ceil(Lpw/dl);  %加重钻杆质量块个数
nc=ceil(Lc/dl);    %钻铤质量块个数
nv=ceil(Lv/dl);    %垂直段质量块个数
n=1+np+npw+nc;

Jp=54*p1*pi*(dl)*(Dp^4-dp^4)/32;        %转动惯量
Jpw=100*p3*pi*(Lpw)*(Dpw^4-dpw^4)/32;   
Jc=150*p2*pi*(Lc)*(Dc^4-dc^4)/32;
Jb=471;

E=210e9;            %钻柱弹性模量
nu=0.3;             %钻柱泊松比
G=E/2/(1+nu);       %钻柱剪切模量

Kp=0.36*pi*G*(Dp^4-dp^4)/(32*dl);        %刚度
Kpw=0.0079*pi*G*(Dpw^4-dpw^4)/(32*Lpw);
Kpc=0.00109*pi*G*(Dc^4-dc^4)/(32*Lc);
Kcb=907;

Cp=140;                                 %阻尼
Cpw=80;
Cpc=190;
Ccb=181;
Cb=0.7*pi*uf*Lc*Dc^3*0.5/(Db-Dc);

Dv=0.000001; % 最小滑动转速
gamab=0.9;   % 摩擦扭矩下降率

miuS=0.8;            %接触面积修正系数
Sp=miuS*pi*Dp*dl;    %接触面积
Sc=miuS*pi*Dc*Lc;
Spw=miuS*pi*Dpw*Lpw;
Sb=miuS*pi*Db*Lb; 

Dwell=Db;            %井眼直径
Dlp=(Dwell-Dp)/2;    %各段泥浆厚度
Dlpw=(Dwell-Dpw)/2;
Dlc=(Dwell-Dc)/2;
Dlb=(Dwell-0.7*Db)/2;

sigma=0.511*sita3;                                   %赫巴屈服应力
nl=3.26*log10((sita200-sita3)/(sita100-sita3));      %流度指数
k=0.511*(sita100-sita3)/(170.2^nl);                  %稠度系数

%
x0=zeros(n,1);
v0=zeros(size(x0));  % 初始化n个角位移，角速度

% 时间配置
time=TIME*10;
dt=10*Dt;
tspan=0:dt:time;


% 使用ode45求解模型
[t,y]=ode45(@(t,y)odefunc(t,y),tspan,[x0;v0]);

% 提取结果
% 钻铤
AngleDisplacements_collar=y(:,n-1)*0.1;                          %角位移
AngleVelocities_collar=y(:,2*n-1);                               %角速度
AngleAcceleration_collar=zeros(size(AngleVelocities_collar));       %角加速度
% 钻头
AngleDisplacements_bit=y(:,n)*0.1;                               %角位移
AngleVelocities_bit=y(:,2*n);                                    %角速度
AngleAcceleration_bit=zeros(size(AngleVelocities_bit));          %角加速度

for i=1:numel(t)
    dydt=odefunc(t(i),y(i,:));
    AngleAcceleration_collar(i,:)=dydt(2*n-1);
    AngleAcceleration_bit(i,:)=dydt(2*n);
    if AngleAcceleration_bit(i,:)>20
        AngleAcceleration_bit(i,:)=0;
    end
    Tb=(Kcb*5*(AngleDisplacements_collar-AngleDisplacements_bit)+Ccb*(AngleVelocities_collar-AngleVelocities_bit))*10^(-3);  %钻头扭矩
    Tzp=Tb+8;                                                   %井口扭矩
end

% 计算SSI
vb_max=max(AngleVelocities_bit((0.5*time/dt):(time/dt), end));     %钻头最大角速度
vb_min=min(AngleVelocities_bit((0.5*time/dt):(time/dt), end));     %钻头最小角速度
SSI=(vb_max-vb_min)/(2*v);                         %粘滑振动等级SSI

fprintf('v: %d, WOB: %d, SSI: %.4f\n', v, WOB, SSI);

%输出角位移图————————————————————————————————————————————
figure;
plot(t*0.1, AngleDisplacements_bit);
xlabel('时间（s）');
ylabel('角位移（rad）');
%导出角速度数据——————————————————————————————————————————————————————
data3=[t*0.1', AngleDisplacements_bit];
writematrix(data3, '角位移.xlsx', 'Sheet', 1);
% 设置图形窗口和坐标轴的背景颜色为白色
set(gcf, 'color', 'w');  % 将图形窗口的背景颜色设置为白色
set(gca, 'color', 'w');  % 将坐标轴区域的背景颜色设置为白色

%输出角速度图————————————————————————————————————————————
figure;
plot(t*0.1, AngleVelocities_bit);
xlabel('时间（s）');
ylabel('角速度（rad/s）');
%导出角速度数据——————————————————————————————————————————————————————
data2=[t*0.1', AngleVelocities_bit];
writematrix(data2, '角速度.xlsx', 'Sheet', 1);
% 设置图形窗口和坐标轴的背景颜色为白色
set(gcf, 'color', 'w');  % 将图形窗口的背景颜色设置为白色
set(gca, 'color', 'w');  % 将坐标轴区域的背景颜色设置为白色

%输出角加速度图————————————————————————————————————————————
figure;
plot(t*0.1, AngleAcceleration_bit);
xlabel('时间（s）');
ylabel('角加速度（rad/s^2）');
%导出角加速度数据——————————————————————————————————————————————————————
data1=[t*0.1', AngleAcceleration_bit];
writematrix(data1, '角加速度.xlsx', 'Sheet', 1);
% 设置图形窗口和坐标轴的背景颜色为白色
set(gcf, 'color', 'w');  % 将图形窗口的背景颜色设置为白色
set(gca, 'color', 'w');  % 将坐标轴区域的背景颜色设置为白色

%输出钻头扭矩图————————————————————————————————————————————
figure;
plot(t*0.1, Tb);
xlabel('时间（s）');
ylabel('钻头扭矩（kN·m）');
%导出钻头扭矩数据——————————————————————————————————————————————————————
data4=[t*0.1', Tb];
writematrix(data4, '钻头扭矩.xlsx', 'Sheet', 1);
% 设置图形窗口和坐标轴的背景颜色为白色
set(gcf, 'color', 'w');  % 将图形窗口的背景颜色设置为白色
set(gca, 'color', 'w');  % 将坐标轴区域的背景颜色设置为白色

function dydt = odefunc(t,y)
global WOB v Db Rb np npw nc nv n Jp Jpw Jc Jb Kp Kpw Kpc Kcb Cp Cpw Cpc Ccb Cb miusb miucb Dv gamab Spw Sc Sb Dlb sigma k nl 
    
    dydt=zeros(2*n,1);
    x=zeros(n,1);
    d=zeros(n,1);
    
    for h=1:n
    x(h)=y(h);
    d(h)=y(h+n);
    dydt(1:n)=y(n+1:2*n);

% 钻头与岩石互作用以及钻井液阻尼
    Tab=Cb*d(n);
    Tr=(Ccb)*(d(n-1)-d(n))+Kcb*(x(n-1)-x(n))-Tab;
    Tsb=WOB*Rb*miusb;
    miub=miucb+(miusb-miucb)*exp(-gamab*abs(d(n)));
    if abs(d(n))<Dv&&abs(Tr)<Tsb
        Tfb=Tr;
        Clb=0;
    elseif abs(d(n))<Dv&&abs(Tr)>=Tsb
        Tfb=Tsb*sign(Tr);
        Clb=0;
    else 
        Tfb=WOB*Rb*miub*sign(d(n));
        Clb=Sb*(sigma/(abs(d(n))*Db/2)+k*(((abs(d(n))*Db/2)^(nl-1))/Dlb^nl));
    end
        Clbb=real(Clb)*d(n);
    end

% 动力学方程
for i=1
    dydt(n+i)=(-Kp*(x(i)-v*t)-(Cp)*(d(i)-v)-Kp*(x(i)-x(i+1))-(Cp)*(d(i)-d(i+1))-(Spw/Sb)*(real(Clbb)))/Jp;
end

for i=2:nv-1
    dydt(n+i)=(-Kp*(x(i)-x(i-1))-(Cp)*(d(i)-d(i-1))-Kp*(x(i)-x(i+1))-(Cp)*(d(i)-d(i+1))-(Spw/Sb)*(real(Clbb)))/Jp;
end

for i=nv
    dydt(n+i)=(-Kp*(x(i)-x(i-1))-(Cp)*(d(i)-d(i-1))-Kp*(x(i)-x(i+1))-(Cp)*(d(i)-d(i+1))-real(Tfb)-(Spw/Sb)*(real(Clbb)))/Jp;
end

for i=nv+1:np-1
    dydt(n+i)=(-Kp*(x(i)-x(i-1))-(Cp)*(d(i)-d(i-1))-Kp*(x(i)-x(i+1))-(Cp)*(d(i)-d(i+1))-(Spw/Sb)*(real(Clbb)))/Jp;
end

for i=np
    dydt(n+i)=(-Kp*(x(i)-x(i-1))-(Cp)*(d(i)-d(i-1))-Kpw*(x(i)-x(i+1))-(Cpw)*(d(i)-d(i+1))-real(Tfb)-(Spw/Sb)*(real(Clbb)))/Jp;
end

if npw<2
    for i=np+1
        dydt(n+i)=(-Kpw*(x(i)-x(i-1))-(Cpw)*(d(i)-d(i-1))-Kpc*(x(i)-x(i+1))-(Cpc)*(d(i)-d(i+1))-(Spw/Sb)*(real(Clbb)))/Jpw;
    end
elseif npw>1
    for i=np+1:np+npw-1
        dydt(n+i)=(-Kpw*(x(i)-x(i-1))-(Cpw)*(d(i)-d(i-1))-Kpw*(x(i)-x(i+1))-(Cpw)*(d(i)-d(i+1))-(Spw/Sb)*(real(Clbb)))/Jpw;
    end
end

for i=np+npw
    dydt(n+i)=(-Kpw*(x(i)-x(i-1))-(Cpw)*(d(i)-d(i-1))-Kpc*(x(i)-x(i+1))-(Cpc)*(d(i)-d(i+1))-real(Tfb)-(Spw/Sb)*(real(Clbb)))/Jpw;
end

if nc<2
    for i=np+npw+1
        dydt(n+i)=(-Kpc*(x(i)-x(i-1))-(Cpc)*(d(i)-d(i-1))-Kcb*(x(i)-x(i+1))-(Ccb)*(d(i)-d(i+1))-real(Tfb)-(Sc/Sb)*(real(Clbb)))/Jc;
    end
elseif nc>1
    for i=np+npw+1:np+npw+nc-1
        dydt(n+i)=(-Kpc*(x(i)-x(i-1))-(Cpc)*(d(i)-d(i-1))-Kpc*(x(i)-x(i+1))-(Cpc)*(d(i)-d(i+1))-real(Tfb)-(Sc/Sb)*(real(Clbb)))/Jc;
    end
end

for i=np+npw+nc
    dydt(n+i)=(-Kpc*(x(i)-x(i-1))-(Cpc)*(d(i)-d(i-1))-Kcb*(x(i)-x(i+1))-(Ccb)*(d(i)-d(i+1))-real(Tfb)-(Sc/Sb)*(real(Clbb)))/Jc;
end

for i=n
    dydt(n+i)=(Kcb*(x(i-1)-x(i))+(Ccb)*(d(i-1)-d(i))-Tab-real(Tfb)-(real(Clb)*d(i)))/Jb;
end
    disp(['Time: ', num2str(t), ' d: ', num2str(d(n)) ]);   %命令行窗口展示时间、钻头转速
end

