function [T,M]=mainfunc(guiji,zuanju,wc,T0,rhoi,Dw,tgxs,miua11,miua22,js,v,omega)
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
    js=js;                   %计算井深，m
    %固定值——————————————————————————————————————————————
    M0=abs(T0*Dw/3*0.5);     %钻头扭矩
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
    js=js;                   %计算井深，m
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
    js=js;                   %计算井深，m
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
    js=js;                   %计算井深，m
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
    miua1=miua11/1.5;          %套管段摩阻系数
    miua2=miua22/1.5;          %裸眼段摩阻系数
    miut1=miua11*1.2;        %套管段切向摩阻系数
    miut2=miua22*1.2;        %裸眼段切向摩阻系数
    js=js;                   %计算井深，m
    %固定值——————————————————————————————————————————————
    T0=0;                    %钻压，N
    M0=0;                    %钻头扭矩，N·m
    v=v;                     %上提速度，m/s               
    omega=omega;             %转速，rad/s
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

%钻具长度确定
row_data=zuanju(4, 1:end-1);
row_sum=sum(row_data);
zuanju(4,end)=js-row_sum;

%钻具组合参数
Dtrans=zuanju(1,:);             %钻柱外径，m
dtrans=zuanju(2,:);             %钻柱内径，m
mtrans=9.81*zuanju(3,:);      %钻柱组合线重，N/m
ltrans=zuanju(4,:); 

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
[Mk,mk,Sk,alphak,phik]=deal_curve_data(guiji,js);

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

if working_condition==2 ||working_condition==3 || working_condition==4
       M(:)=0;
end

%% 输出各工况结果

%垂深计算
[Length,Xs,Ys,Zs]=deal_input_data(guiji);
cs = Xs(1)-Xs;
%垂深插值
aa=guiji(:,1);
Tzz=cs;
aacs=(1:1:max(aa))';
Tcs= interp1(aa, Tzz, aacs, 'spline');
Tcs=Tcs(1:js);

%旋转钻进
if working_condition==1
  %绘制轴向力分布云图———————————————————————————————————————————————————————
    N=zeros(size(Sk));
    E=zeros(size(Sk));
    for i=2:length(Sk)
        dSk=Sk(i)-Sk(i-1);
        N(i)=N(i-1)+dSk*sind(alpha(i))*cosd(phi(i));
        E(i)=E(i-1)+dSk*sind(alpha(i))*sind(phi(i));
    end
    figure('Position',[50,50,700,450]);
    plot3(E,N,-Tcs,'LineWidth',2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('轴向力分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs),0]);
    hold on;
    scatter3(E,N,-Tcs,20,T,'filled');
    hold off;
    colormap(jet);
    colorbar;
    caxis([min(T) max(T)]);
    view(3);
  %输出轴向力分布图—————————————————————————————————————————————————————————
    figure;
    plot(T, Sk);
    xlabel('轴向力（kN）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出轴向力数据——————————————————————————————————————————————————————
    writematrix(T, '旋转钻进_轴向力.xlsx', 'Sheet', 1);
  %绘制扭矩分布云图———————————————————————————————————————————————————————
    N=zeros(size(Sk));
    E=zeros(size(Sk));
    for i=2:length(Sk)
        dSk=Sk(i)-Sk(i-1);
        N(i)=N(i-1)+dSk*sind(alpha(i))*cosd(phi(i));
        E(i)=E(i-1)+dSk*sind(alpha(i))*sind(phi(i));
    end
    figure('Position',[50,50,700,450]);
    plot3(E,N,-Tcs,'LineWidth',2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('扭矩分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs),0]);
    hold on;
    scatter3(E,N,-Tcs,20,M,'filled');
    hold off;
    colormap(jet);
    colorbar;
    caxis([min(M) max(M)]);
    view(3);
  %输出扭矩分布图—————————————————————————————————————————————————————————
    figure;
    plot(M, Sk);
    xlabel('扭矩（kN·m）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出扭矩数据——————————————————————————————————————————————————————
    writematrix(M, '旋转钻进_扭矩.xlsx', 'Sheet', 1);

%滑动钻进
elseif working_condition==2
  %绘制轴向力分布云图———————————————————————————————————————————————————————
    N=zeros(size(Sk));
    E=zeros(size(Sk));
    for i=2:length(Sk)
        dSk=Sk(i)-Sk(i-1);
        N(i)=N(i-1)+dSk*sind(alpha(i))*cosd(phi(i));
        E(i)=E(i-1)+dSk*sind(alpha(i))*sind(phi(i));
    end
    figure('Position',[50,50,700,450]);
    plot3(E,N,-Tcs,'LineWidth',2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('轴向力分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs),0]);
    hold on;
    scatter3(E,N,-Tcs,20,T,'filled');
    hold off;
    colormap(jet);
    colorbar;
    caxis([min(T) max(T)]);
    view(3);
  %输出轴向力分布图—————————————————————————————————————————————————————————
    figure;
    plot(T, Sk);
    xlabel('轴向力（kN）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出轴向力数据——————————————————————————————————————————————————————
    writematrix(T, '滑动钻进_轴向力.xlsx', 'Sheet', 1);
  %绘制扭矩分布云图———————————————————————————————————————————————————————
    M_min = min(M);
    M_max = max(M);
    if M_min == M_max
        caxis([M_min - 1e-3, M_max + 1e-3]);
    else
        caxis([M_min, M_max]);
    end
    figure('Position',[50,50,700,450]);
    plot3(E, N, -Tcs, 'LineWidth', 2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('扭矩分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs), 0]);
    hold on;
    scatter3(E, N, -Tcs, 20, M, 'filled');
    hold off;
    colormap(jet);
    colorbar;
    view(3);
  %输出扭矩分布图—————————————————————————————————————————————————————————
    figure;
    plot(M, Sk);
    xlabel('扭矩（kN·m）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出扭矩数据——————————————————————————————————————————————————————
    writematrix(M, '滑动钻进_扭矩.xlsx', 'Sheet', 1);

%起钻
elseif working_condition==3
  %绘制轴向力分布云图———————————————————————————————————————————————————————
    N=zeros(size(Sk));
    E=zeros(size(Sk));
    for i=2:length(Sk)
        dSk=Sk(i)-Sk(i-1);
        N(i)=N(i-1)+dSk*sind(alpha(i))*cosd(phi(i));
        E(i)=E(i-1)+dSk*sind(alpha(i))*sind(phi(i));
    end
    figure('Position',[50,50,700,450]);
    plot3(E,N,-Tcs,'LineWidth',2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('轴向力分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs),0]);
    hold on;
    scatter3(E,N,-Tcs,20,T,'filled');
    hold off;
    colormap(jet);
    colorbar;
    caxis([min(T) max(T)]);
    view(3);
  %输出轴向力分布图—————————————————————————————————————————————————————————
    figure;
    plot(T, Sk);
    xlabel('轴向力（kN）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出轴向力数据——————————————————————————————————————————————————————
    writematrix(T, '起钻_轴向力.xlsx', 'Sheet', 1);
  %绘制扭矩分布云图———————————————————————————————————————————————————————
    M_min = min(M);
    M_max = max(M);
    if M_min == M_max
        caxis([M_min - 1e-3, M_max + 1e-3]);
    else
        caxis([M_min, M_max]);
    end
    figure('Position',[50,50,700,450]);
    plot3(E, N, -Tcs, 'LineWidth', 2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('扭矩分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs), 0]);
    hold on;
    scatter3(E, N, -Tcs, 20, M, 'filled');
    hold off;
    colormap(jet);
    colorbar;
    view(3);
  %输出扭矩分布图—————————————————————————————————————————————————————————
    figure;
    plot(M, Sk);
    xlabel('扭矩（kN·m）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出扭矩数据——————————————————————————————————————————————————————
    writematrix(M, '起钻_扭矩.xlsx', 'Sheet', 1);

%下钻
elseif working_condition==4
  %绘制轴向力分布云图———————————————————————————————————————————————————————
    N=zeros(size(Sk));
    E=zeros(size(Sk));
    for i=2:length(Sk)
        dSk=Sk(i)-Sk(i-1);
        N(i)=N(i-1)+dSk*sind(alpha(i))*cosd(phi(i));
        E(i)=E(i-1)+dSk*sind(alpha(i))*sind(phi(i));
    end
    figure('Position',[50,50,700,450]);
    plot3(E,N,-Tcs,'LineWidth',2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('轴向力分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs),0]);
    hold on;
    scatter3(E,N,-Tcs,20,T,'filled');
    hold off;
    colormap(jet);
    colorbar;
    caxis([min(T) max(T)]);
    view(3);
  %输出轴向力分布图—————————————————————————————————————————————————————————
    figure;
    plot(T, Sk);
    xlabel('轴向力（kN）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出轴向力数据——————————————————————————————————————————————————————
    writematrix(T, '下钻_轴向力.xlsx', 'Sheet', 1);
  %绘制扭矩分布云图———————————————————————————————————————————————————————
    M_min = min(M);
    M_max = max(M);
    if M_min == M_max
        caxis([M_min - 1e-3, M_max + 1e-3]);
    else
        caxis([M_min, M_max]);
    end
    figure('Position',[50,50,700,450]);
    plot3(E, N, -Tcs, 'LineWidth', 2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('扭矩分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs), 0]);
    hold on;
    scatter3(E, N, -Tcs, 20, M, 'filled');
    hold off;
    colormap(jet);
    colorbar;
    view(3);
  %输出扭矩分布图—————————————————————————————————————————————————————————
    figure;
    plot(M, Sk);
    xlabel('扭矩（kN·m）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出扭矩数据——————————————————————————————————————————————————————
    writematrix(M, '下钻_扭矩.xlsx', 'Sheet', 1);

%倒划眼
elseif working_condition==5
  %绘制轴向力分布云图———————————————————————————————————————————————————————
    N=zeros(size(Sk));
    E=zeros(size(Sk));
    for i=2:length(Sk)
        dSk=Sk(i)-Sk(i-1);
        N(i)=N(i-1)+dSk*sind(alpha(i))*cosd(phi(i));
        E(i)=E(i-1)+dSk*sind(alpha(i))*sind(phi(i));
    end
    figure('Position',[50,50,700,450]);
    plot3(E,N,-Tcs,'LineWidth',2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('轴向力分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs),0]);
    hold on;
    scatter3(E,N,-Tcs,20,T,'filled');
    hold off;
    colormap(jet);
    colorbar;
    caxis([min(T) max(T)]);
    view(3);
  %输出轴向力分布图—————————————————————————————————————————————————————————
    figure;
    plot(T, Sk);
    xlabel('轴向力（kN）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出轴向力数据——————————————————————————————————————————————————————
    writematrix(T, '倒划眼_轴向力.xlsx', 'Sheet', 1);
  %绘制扭矩分布云图———————————————————————————————————————————————————————
    N=zeros(size(Sk));
    E=zeros(size(Sk));
    for i=2:length(Sk)
        dSk=Sk(i)-Sk(i-1);
        N(i)=N(i-1)+dSk*sind(alpha(i))*cosd(phi(i));
        E(i)=E(i-1)+dSk*sind(alpha(i))*sind(phi(i));
    end
    figure('Position',[50,50,700,450]);
    plot3(E,N,-Tcs,'LineWidth',2);
    xlabel('东/西 位移（m）');
    ylabel('南/北 位移（m）');
    zlabel('垂深（m）');
    title('扭矩分布云图');
    grid on;
    axis equal;
    zlim([min(-Tcs),0]);
    hold on;
    scatter3(E,N,-Tcs,20,M,'filled');
    hold off;
    colormap(jet);
    colorbar;
    caxis([min(M) max(M)]);
    view(3);
  %输出扭矩分布图—————————————————————————————————————————————————————————
    figure;
    plot(M, Sk);
    xlabel('扭矩（kN·m）'); % X轴标签
    ylabel('井深（m）'); % Y轴标签
    set(gca, 'YDir', 'reverse'); % Y轴反转，使井深从下到上变化
  %导出扭矩数据——————————————————————————————————————————————————————
    writematrix(M, '倒划眼_扭矩.xlsx', 'Sheet', 1);
end

end