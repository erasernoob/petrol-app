function [fh,fs]=abcfunc4(guiji,Holedia,ml,zuanju,js)
data=guiji;              %井眼轨迹hoi
Dw=Holedia;                                 %井筒直径
miut=0.17;  
miua=miut;
E=ml*1000000;%弹性模量

%钻具长度确定
row_data=zuanju(4, 1:end-1);
row_sum=sum(row_data);
zuanju(4,end)=js-row_sum

Dtrans=zuanju(1,:);             %钻柱外径，m
dtrans=zuanju(2,:);             %钻柱内径，m
mtrans=9.81*2.5*zuanju(3,:);    %钻柱组合线重，N/m
ltrans=zuanju(4,:); 

I=pi*(Dtrans(1)^4-dtrans(1)^4)/64;                                  % 极惯性矩
js=js
g=9.81;                                 %重力加速度

%%
%钻具组合参数
Ntrans=numel(Dtrans);                   %所加载的钻具组合数量
nntrans=zeros(Ntrans,1);                %即nntrans的前n项累加
ntrans=sum(ltrans);
Rt=zeros(ntrans,1);                     %各段钻具组合外半径/m
rt=zeros(ntrans,1);                     %各段钻具组合内半径/m
Aot=zeros(ntrans,1);                    %各段钻具组合外截面积/m^2
Ait=zeros(ntrans,1);                    %各段钻具组合内截面积/m^2
qt=zeros(ntrans,1);                     %各段钻具组合线重/N.m^-1
%qmt=zeros(ntrans,1);                    %各段钻具组合浮重/N.m^-1
%Kft=zeros(ntrans,1);                    %浮力系数
It=zeros(ntrans,1);                     %惯性矩
ht=zeros(ntrans,1);                     %壁厚
Pi=zeros(ntrans,1);%环空流体压力，MPa
PI1=Pi;
PI2=Pi;
Tc=PI1;
Po=zeros(ntrans,1);%管内流体压力,MPa
PO1=Po;
PO2=Pi; 
FH=zeros(ntrans,1);%正弦屈曲临界载荷,N
FS=zeros(ntrans,1);%正弦屈曲临界载荷,N

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
            Aot(j)=pi*Rt(j)^2;
            Ait(j)=pi*rt(j)^2;
            qt(j)=mtrans(i);
            %qmt(j)=qt(j)-(Aot(j)-Ait(j))*rhoi*g;
            %Kft(j)=qmt(j)/qt(j);
            It(j)=pi*(Rt(j)^4-rt(j)^4)/4;
            ht(j)=Rt(j)-rt(j);
%             thegmaa(j)=force(i)*10/(Aot(j)-Ait(j))/1000000;
        end
    else
        for j=nntrans(i-1)+1:nntrans(i)
            Rt(j)=Dtrans(i)/2;
            rt(j)=dtrans(i)/2;
            Aot(j)=pi*Rt(j).^2;
            Ait(j)=pi*rt(j).^2;
            qt(j)=mtrans(i);
            %qmt(j)=qt(j)-(Aot(j)-Ait(j))*rhoi*g;
            %Kft(j)=qmt(j)/qt(j);
            It(j)=pi*(Rt(j)^4-rt(j)^4)/4;
            ht(j)=Rt(j)-rt(j);
%             thegmaa(j)=force(i)*10/(Aot(j)-Ait(j))/1000000;
        end
    end
end

        sign1=1;
        T0=0;
        M0=0;
        sign2=0;
       
T0=-T0;
%计算参数
Dw=Dw+0.001;
ds=1;                      %步长
len=ntrans-1;              %计算长度
nt=len/ds;
sspan=0:ds:len;
SW=sspan';

%%
%处理井眼轨迹函数
[Mk,mk,Sk,alphak,phik]=deal_curve_data2(data,js);

%初始化k和tao等参数
[alpha,phi,ks,dks,ddks,kphis,kalphas,taos]=prepare_data(sspan,Mk,mk,Sk,alphak,phik);
DAL=zeros(ntrans,1);
ALpha=flipud(alpha*180/pi);
for i=1:ntrans-1
    DAL(i)=abs((ALpha(i+1)-ALpha(i))*30)*10;
end
[Length,Ys,Zs,Xs]=deal_trank(Sk,alpha,phi);      %输出从底部到井口位置的自然长度以及各点坐标
mmm=zeros(ntrans,3);
iiiii=numel(mmm(:,3));
mmm(:,3)=Xs(iiiii,1)-Xs(:,1);
mmm(:,1)=Ys(iiiii,1)-Ys(:,1);  %北坐标
mmm(:,2)=Zs(iiiii,1)-Zs(:,1);  %东坐标

%%
%识别井眼轨迹
smalpha=smooth(alpha,201);
B=mean(smalpha(1:500));
B1=mean(smalpha(1:300));
Z=mean(smalpha(end-300:end));
Ls=0;
Lc=0;
Lh=0;
if B<0.44  %若所有井斜角小于25°，则当成直井处理
    Ls=ntrans;
else
for i=1:ntrans-1
    ca(i)=abs(smalpha(end-i+1)-Z);
    Ls=i+1;%垂直井段
    if ca(i)>0.11 && smalpha(end-i+1)>0.25
        break
    end 
end
end
if B1>0.44 && B<1.23  %判断25-70°的定向井
    for i=1:ntrans-1  
       if Ls==ntrans
        break
       else
        ba(i)=abs(smalpha(i)-B1);
        Lh=i;%水平井段
        if ba(i)>0.11 && smalpha(i)<0.44 
           break  
        end   
       end     
    end
else      
for i=1:ntrans-1
    if Ls==ntrans
        break
    else
        ba(i)=abs(smalpha(i)-B);
        Lh=i;%水平井段
        if ba(i)>0.11 && smalpha(i)<1.35 
           break  
        end
    end
end
end
Lc=ntrans-Lh-Ls;   %造斜段

%  gtd=(ks*180/pi)*30;
R=zeros(ntrans,1);
R=1./ks;
RR=R.^2;
for i=1:ntrans
    if i<Lh+1
       FH(i)=-2*(2*2^0.5 - 1)*(E*It(i)*qt(i)*sin(alpha(i))/(0.5*Dw-Rt(i)))^(0.5);%斜直，水平
       FS(i)=-2*(E*It(i)*qt(i)*sin(alpha(i))/(0.5*Dw-Rt(i)))^(0.5);
    elseif i<Lh+1+Lc
       FH(i)=-7.56*E*It(i)/(Rt(i)*(0.5*Dw-Rt(i)))/(10^3);%弯曲
       FS(i)=-4*E*It(i)/(Rt(i)*(0.5*Dw-Rt(i)))/(10^3);
%        FH(i)=-12*(E*It(i)/((0.5*Dw-Rt(i))*R(i)))*(1+(1+((0.5*Dw-Rt(i))*RR(i)*qt(i)*sin(alpha(i))/(8*E*It(i))))^0.5); %弯曲
%        FS(i)=-4*(E*It(i)/((0.5*Dw-Rt(i))*R(i)))*(1+(1+((0.5*Dw-Rt(i))*RR(i)*qt(i)*sin(alpha(i))/(4*E*It(i))))^0.5);
    else
       FH(i)=-5.55*(E*It(i)*qt(i)^2)^(1/3);%垂直
       FS(i)=-2.55*(E*It(i)*qt(i)^2)^(1/3);
    end
end

fh=flipud(FH)/1000;
fs=flipud(FS)/1000;

end