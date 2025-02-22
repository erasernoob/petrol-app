function [Pyx,Plg,yssd]=Hydro(guiji,lbmx,pailiang,fluidden,n,K,miu,taof,Dw,A1,C1,A2,C2,A3,C3,Rzz,rzz,Lzz,Rzt,rzt,Lzt,L1,d1,L2,d2,L3,d3,L4,d4,Lp,Li,rzzjt,yxmd,H,jsjg);
data=guiji;
wc=lbmx;
Q=pailiang/1000/60;   %排量，m3/s
Ql=pailiang/60;       %排量，L/s
rhoi=fluidden;        %钻井液密度，kg/m3
rhoo=fluidden/1000;   %钻井液密度，kg/L
g=9.81;
Rt=Rzz/2;        %钻柱外径，m
rt=rzz/2;        %钻柱内径，m
Rtzt=Rzt/2;      %钻铤外径，m
rtzt=rzt/2;      %钻铤内径，m
Dwcm=Dw*100      %井眼直径，cm
Rzzcm=Rzz*100    %钻杆外径，cm
rzzcm=rzz*100    %钻杆内径，cm
Rztcm=Rzt*100    %钻铤外径，cm
rztcm=rzt*100    %钻铤内径，cm
d1=d1*100        %地面高压管线内径，cm
d2=d2*100        %立管内径，cm
d3=d3*100        %水龙带内径，cm
d4=d4*100        %方钻杆内径，cm

jd=guiji(:,1);
yssd=jd(end);
% num_iterations = yssd/jsjg;
num_iterations = ceil(yssd / jsjg);

Plg=zeros(num_iterations*jsjg,num_iterations);

for nnn=1:num_iterations
%     js=nnn*jsjg;
    if nnn == num_iterations
        % 最后一次迭代时使用 guiji 最后的值
        js = yssd;
    else
        % 否则按正常的间隔计算
        js = nnn * jsjg;
    end

ntrans=round(js);

%地面管汇压耗
Pdm=5.1655 * rhoo^0.8 * miu^0.2 * (L1 / d1^4.8 + L2 / d2^4.8 + L3 / d3^4.8 + L4 / d4^4.8) * Ql^1.8 / 10

%钻头压降
S1=C1*pi*(A1/2/10)^2;
S2=C2*pi*(A2/2/10)^2;
S3=C3*pi*(A3/2/10)^2;
S=S1+S2+S3
dertaPzt=(0.05*Ql^2*rhoi/1000)/(0.95^2 * S^2);

%静液柱压力
ds=1;
len=ntrans-1;
nt=len/ds;
sspan=0:ds:len;
SW=sspan';
[Mk,mk,Sk,alphak,phik]=deal_curve_data2(data,js);
[alpha,phi,ks,dks,ddks,kphis,kalphas,taos]=prepare_data(sspan,Mk,mk,Sk,alphak,phik);
PI1=zeros(ntrans,1);
PO1=zeros(ntrans,1);
PI2=zeros(ntrans,1);
PO2=zeros(ntrans,1); 
for i=1:ntrans
    PI1(i)=rhoi*g*cos(alpha(ntrans-i+1));
    PO1(i)=rhoi*g*cos(alpha(ntrans-i+1));
end
PI2(1)=PI1(1);
PO2(1)=PO1(1);
for i=2:ntrans
    PI2(i)=PI2(i-1)+PI1(i);
    PO2(i)=PO2(i-1)+PO1(i);
end
PI2=(PI2-9.81*rhoi)/10^6;  %管内静液柱压力
PO2=(PO2-9.81*rhoi)/10^6;  %环空静液柱压力

%流速
%钻柱井段
Vp=Q/(pi*rt^2);                %管内流速
Va=4*Q/(pi*(Dw^2-4*Rt^2));    %环空流速
%钻铤井段
Vpzt=Q/(pi*rtzt^2);                %管内流速
Vazt=4*Q/(pi*(Dw^2-4*Rtzt^2));    %环空流速

%钻柱接头影响系数
fjt = Lp / (Lp+Li) + Li / (Lp+Li) * (rzz / rzzjt)^4.8

%压降
if wc==1     %宾汉流体
%钻柱井段
    %管内雷诺数
    Repzz = rhoi * rzz * Vp / miu / (1 + taof * rzz / (6 * miu * Vp))
    %环空雷诺数
    Reazz = rhoi * (Dw - Rzz) * Va / miu / (1 + taof * (Dw - Rzz) / (8 * miu * Va))
    %管内压降
    if Repzz < 2000
        Ppzz = 40.7437 * miu * (1:(js-Lzt))' * Ql / rzzcm^4 + taof * (1:(js-Lzt))' / (187.5 * rzzcm)
    else
        Ppzz = 5.1655 * miu^0.2 * rhoo^0.8 * (1:(js-Lzt))' * Ql^1.8 / rzzcm^4.8
    end
    %环空压降
    if Reazz < 2000
        Pazz = 61.1155 * miu * (1:(js-Lzt))' * Ql / (Dwcm - Rzzcm)^3 / (Dwcm + Rzzcm) + 6 * 10^(-3) * taof * (1:(js-Lzt))' / (Dwcm - Rzzcm)
    else
        Pazz = 5.7503 * miu^0.2 * rhoo^0.8 * (1:(js-Lzt))' * Ql^1.8 / (Dwcm - Rzzcm)^3 / (Dwcm + Rzzcm)^1.8
    end
%钻铤井段
    %管内雷诺数
    Repzt = rhoi * rzt * Vpzt / miu / (1 + taof * rzt / (6 * miu * Vpzt))
    %环空雷诺数
    Reazt = rhoi * (Dw - Rzt) * Vazt / miu / (1 + taof * (Dw - Rzt) / (8 * miu * Vazt))
    %管内压降
    if Repzt < 2000
        Ppzt = 40.7437 * miu * (1:Lzt)' * Ql / rztcm^4 + taof * (1:Lzt)' / (187.5 * rztcm)
    else
        Ppzt = 5.1655 * miu^0.2 * rhoo^0.8 * (1:Lzt)' * Ql^1.8 / rztcm^4.8
    end
    %环空压降
    if Reazt < 2000
        Pazt = 61.1155 * miu * (1:Lzt)' * Ql / (Dwcm - Rztcm)^3 / (Dwcm + Rztcm) + 6 * 10^(-3) * taof * (1:Lzt)' / (Dwcm - Rztcm)
    else
        Pazt = 5.7503 * miu^0.2 * rhoo^0.8 * (1:Lzt)' * Ql^1.8 / (Dwcm - Rztcm)^3 / (Dwcm + Rztcm)^1.8
    end
elseif wc==2   %幂律流体
%钻柱井段
    %管内雷诺数
    Repzz = rhoi * rzz^n * Vp^(2-n) / 8^(n-1) / K / ((3*n+1) / (4*n))^n
    %环空雷诺数
    Reazz = rhoi * (Dw - Rzz)^n * Va^(2-n) / 12^(n-1) / K / ((2*n+1) / (3*n))^n
    %管内压降
    if Repzz < 3470-1370*n
        Ppzz = ((8000 * (3*n+1) * Ql) / (pi * n * rzzcm^3))^n * (1:(js-Lzt))' * K / 250 / rzzcm
    else
        Ppzz = 5.1655 * miu^0.2 * rhoo^0.8 * (1:(js-Lzt))' * Ql^1.8 / rzzcm^4.8
    end
    %环空压降
    if Reazz < 3470-1370*n
        Pazz = ((16000 * (2*n+1) * Ql) / (pi * n * (Dwcm - Rzzcm)^2 * (Dwcm + Rzzcm)))^n * (1:(js-Lzt))' * K / 250 / (Dwcm - Rzzcm)
    else
        Pazz = 5.7503 * miu^0.2 * rhoo^0.8 * (1:(js-Lzt))' * Ql^1.8 / (Dwcm - Rzzcm)^3 / (Dwcm + Rzzcm)^1.8
    end
%钻铤井段
    %管内雷诺数
    Repzt = rhoi * rzt^n * Vpzt^(2-n) / 8^(n-1) / K / ((3*n+1) / (4*n))^n
    %环空雷诺数
    Reazt = rhoi * (Dw - Rzt)^n * Vazt^(2-n) / 12^(n-1) / K / ((2*n+1) / (3*n))^n
    %管内压降
    if Repzt < 3470-1370*n
        Ppzt = ((8000 * (3*n+1) * Ql) / (pi * n * rztcm^3))^n * (1:Lzt)' * K / 250 / rztcm
    else
        Ppzt = 5.1655 * miu^0.2 * rhoo^0.8 * (1:Lzt)' * Ql^1.8 / rztcm^4.8
    end
    %环空压降
    if Reazt < 3470-1370*n
        Pazt = ((16000 * (2*n+1) * Ql) / (pi * n * (Dwcm - Rztcm)^2 * (Dwcm + Rztcm)))^n * (1:Lzt)' * K / 250 / (Dwcm - Rztcm)
    else
        Pazt = 5.7503 * miu^0.2 * rhoo^0.8 * (1:Lzt)' * Ql^1.8 / (Dwcm - Rztcm)^3 / (Dwcm + Rztcm)^1.8
    end
elseif wc==3   %赫巴流体
%钻柱井段
    %管内雷诺数
    Repzz=8^(1-n) * rhoi * rzz^n * Vp^(2-n) / K / ((3*n+1)/(4*n))^n / (1 + (3*n+1) / (2*n+1) * (n/(6*n+2))^n * (rzz/Vp)^n * taof / K)
    %环空雷诺数
    Reazz=12^(1-n) * rhoi * (Dw-Rzz)^n * Va^(2-n) / K / ((2*n+1)/(3*n))^n / (1 + (2*n+1)^(1-n) / (n+1) * (n/4)^n * ((Dw-Rzz)/Va)^n * taof / K)
    %临界雷诺数
    Reczz=3470-1370*n
    %管内壁面剪切力
%     taowpzz=taof + K * (8 * Vp / rzz)^n
    taowpzz=taof + K * (8 * Q / pi / (rzz/2)^3)^n
    %环空壁面剪切力
%     taowazz=taof + K * (6 * Va / (Dw-Rzz))^n
    taowazz=taof + K * (8 * Q / pi / ((Dw/2)^3-(Rzz/2)^3))^n
    %管内摩擦系数
    if Repzz < Reczz
        fpzz=16/Repzz
    else
        equation = @(fpzz) 1/sqrt(fpzz) - (2.69/n - 2.95 + 4.53/n * log10(Repzz * fpzz^(1-0.5*n)) + 4.53/n * log10(1 - taof/taowpzz))
        fp_initial = 0.01
        options = optimoptions('fsolve', 'Display', 'off')
        fpzz = fsolve(equation, fp_initial, options)
    end
    %环空摩擦系数
    if Reazz < Reczz
        fazz=24/Reazz
    else
        equation = @(fazz) 1/sqrt(fazz) - (2.69/n - 2.95 + 4.53/n * log10(Reazz * fazz^(1-0.5*n)) + 4.53/n * log10(1 - taof/taowazz))
        fa_initial = 0.01
        options = optimoptions('fsolve', 'Display', 'off')
        fazz = fsolve(equation, fa_initial, options)
    end
    %管内压降
    Ppzz=2 * fpzz * rhoi * (1:(js-Lzt))' * Vp^2 / rzz / 10^6 * 10
    %环空压降
    Pazz=2 * fazz * rhoi * (1:(js-Lzt))' * Va^2 / (Dw - Rzz) / 10^6 * 10
%钻铤井段
    %管内雷诺数
    Repzt=8^(1-n) * rhoi * rzt^n * Vpzt^(2-n) / K / ((3*n+1)/(4*n))^n / (1 + (3*n+1) / (2*n+1) * (n/(6*n+2))^n * (rzt/Vpzt)^n * taof / K)
    %环空雷诺数
    Reazt=12^(1-n) * rhoi * (Dw-Rzt)^n * Vazt^(2-n) / K / ((2*n+1)/(3*n))^n / (1 + (2*n+1)^(1-n) / (n+1) * (n/4)^n * ((Dw-Rzt)/Vazt)^n * taof / K)
    %临界雷诺数
    Reczt=3470-1370*n
    %管内壁面剪切力
%     taowpzt=taof + K * (8 * Vpzt / rzt)^n
    taowpzt=taof + K * (8 * Q / pi / (rzt/2)^3)^n
    %环空壁面剪切力
%     taowazt=taof + K * (6 * Vazt / (Dw-Rzt))^n
    taowazt=taof + K * (8 * Q / pi / ((Dw/2)^3-(Rzt/2)^3))^n
    %管内摩擦系数
    if Repzt < Reczt
        fpzt=16/Repzt
    else
        equation = @(fpzt) 1/sqrt(fpzt) - (2.69/n - 2.95 + 4.53/n * log10(Repzt * fpzt^(1-0.5*n)) + 4.53/n * log10(1 - taof/taowpzt))
        fp_initial = 0.01
        options = optimoptions('fsolve', 'Display', 'off')
        fpzt = fsolve(equation, fp_initial, options)
    end
    %环空摩擦系数
    if Reazt < Reczt
        fazt=24/Reazt
    else
        equation = @(fazt) 1/sqrt(fazt) - (2.69/n - 2.95 + 4.53/n * log10(Reazt * fazt^(1-0.5*n)) + 4.53/n * log10(1 - taof/taowazt))
        fa_initial = 0.01
        options = optimoptions('fsolve', 'Display', 'off')
        fazt = fsolve(equation, fa_initial, options)
    end
    %管内压降
    Ppzt=2 * fpzt * rhoi * (1:Lzt)' * Vpzt^2 / rzt / 10^6 * 10
    %环空压降
    Pazt=2 * fazt * rhoi * (1:Lzt)' * Vazt^2 / (Dw - Rzt) / 10^6 * 10
end

Ppztt = Ppzz(end)+Ppzt
Paztt = Pazz(end)+Pazt
Ppp = [Ppzz;Ppztt]
Paa = [Pazz;Paztt]
Pp = fjt * Ppp / 10
Pa = Paa / 10

%考虑岩屑的环空压耗
S = yxmd / rhoi
%钻柱井段
if wc==1
    if Reazz < 2000
        fd=64/Reazz
    else
        fd=0.316/Reazz^0.25
    end
elseif wc==2 || wc==3
    if Reazz < 3470-1370*n
        fd=64/Reazz
    else
        fd=0.316/Reazz^0.25
    end
end
Payxzz = 0.0026068625 * H .* Pazz / 10 / fd * ( Va^2 / g / (Dw-Rzz) / (S-1) )^(-1.25) + (1 + 0.00581695 * H) .* Pazz / 10
%钻铤井段
if wc==1
    if Reazt < 2000
        fdzt=64/Reazt
    else
        fdzt=0.316/Reazt^0.25
    end
elseif wc==2 || wc==3
    if Reazt < 3470-1370*n
        fdzt=64/Reazt
    else
        fdzt=0.316/Reazt^0.25
    end
end
Payxzt = 0.0026068625 * H .* Pazt / 10 / fdzt * ( Vazt^2 / g / (Dw-Rzt) / (S-1) )^(-1.25) + (1 + 0.00581695 * H) .* Pazt / 10

Payxztt = Payxzz(end)+Payxzt
Payx = [Payxzz;Payxztt]

%考虑岩屑的环空循环压力
Phkyx=PO2+Payx

%考虑岩屑的管内循环压力
nn=ntrans;
Pgnyx=zeros(nn,1);
Pgnyx(end)=Phkyx(end)+dertaPzt;
for i=1:nn-1
    PI2yx=PI2(end+1-i)-PI2(end-i);
    Ppyx=Pp(end+1-i)-Pp(end-i);
    Pgnyx(end-i)=Pgnyx(end+1-i)-PI2yx+Ppyx;
end

%立管压力
Plg(1:length(Pgnyx), nnn) = Pgnyx;

%考虑岩屑的总循环压耗
Pyx=Plg(1,:)+Pdm

end

end