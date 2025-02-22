function [ECD,Sk]=Hydro(guiji,lbmx,pailiang,fluidden,n,K,miu,taof,Dw,Rzz,rzz,Lzz,Rzt,rzt,Lzt);
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
ntrans=round(data(end,1));

%静液柱压力
ds=1;
len=ntrans-1;
nt=len/ds;
sspan=0:ds:len;
SW=sspan';
[Mk,mk,Sk,alphak,phik]=deal_curve_data2(data);
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

%压降
if wc==1     %宾汉流体
%钻柱井段
    %管内雷诺数
    Repzz = rhoi * rzz * Vp / miu / (1 + taof * rzz / (6 * miu * Vp))
    %环空雷诺数
    Reazz = rhoi * (Dw - Rzz) * Va / miu / (1 + taof * (Dw - Rzz) / (8 * miu * Va))
    %管内压降
    if Repzz < 2000
        Ppzz = 40.7437 * miu * (1:Lzz)' * Ql / rzzcm^4 + taof * (1:Lzz)' / (187.5 * rzzcm)
    else
        Ppzz = 5.1655 * miu^0.2 * rhoo^0.8 * (1:Lzz)' * Ql^1.8 / rzzcm^4.8
    end
    %环空压降
    if Reazz < 2000
        Pazz = 61.1155 * miu * (1:Lzz)' * Ql / (Dwcm - Rzzcm)^3 / (Dwcm + Rzzcm) + 6 * 10^(-3) * taof * (1:Lzz)' / (Dwcm - Rzzcm)
    else
        Pazz = 5.7503 * miu^0.2 * rhoo^0.8 * (1:Lzz)' * Ql^1.8 / (Dwcm - Rzzcm)^3 / (Dwcm + Rzzcm)^1.8
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
        Ppzz = ((8000 * (3*n+1) * Ql) / (pi * n * rzzcm^3))^n * (1:Lzz)' * K / 250 / rzzcm
    else
        Ppzz = 5.1655 * miu^0.2 * rhoo^0.8 * (1:Lzz)' * Ql^1.8 / rzzcm^4.8
    end
    %环空压降
    if Reazz < 3470-1370*n
        Pazz = ((16000 * (2*n+1) * Ql) / (pi * n * (Dwcm - Rzzcm)^2 * (Dwcm + Rzzcm)))^n * (1:Lzz)' * K / 250 / (Dwcm - Rzzcm)
    else
        Pazz = 5.7503 * miu^0.2 * rhoo^0.8 * (1:Lzz)' * Ql^1.8 / (Dwcm - Rzzcm)^3 / (Dwcm + Rzzcm)^1.8
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
    Ppzz=2 * fpzz * rhoi * (1:Lzz)' * Vp^2 / rzz / 10^6 * 10
    %环空压降
    Pazz=2 * fazz * rhoi * (1:Lzz)' * Va^2 / (Dw - Rzz) / 10^6 * 10
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


Paztt = Pazz(end)+Pazt
Paa = [Pazz;Paztt]
Pa = Paa / 10

%垂深插值
[Length,Xs,Ys,Zs]=deal_input_data(data)
cs = Xs(1)-Xs
aa=data(:,1);
T=cs;
aacs=(1:1:max(aa))';
Tcs= interp1(aa, T, aacs, 'spline');
Tcs=Tcs;

%ECD
ECD=Pa*10^6/9.81/1000./Tcs+rhoi/1000

end