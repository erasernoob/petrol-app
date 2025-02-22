function [fh,fs]=abcfunc4(guiji,Holedia,ml,zuanju,js)
data=guiji;              %���۹켣hoi
Dw=Holedia;                                 %��Ͳֱ��
miut=0.17;  
miua=miut;
E=ml*1000000;%����ģ��

%��߳���ȷ��
row_data=zuanju(4, 1:end-1);
row_sum=sum(row_data);
zuanju(4,end)=js-row_sum

Dtrans=zuanju(1,:);             %�����⾶��m
dtrans=zuanju(2,:);             %�����ھ���m
mtrans=9.81*2.5*zuanju(3,:);    %����������أ�N/m
ltrans=zuanju(4,:); 

I=pi*(Dtrans(1)^4-dtrans(1)^4)/64;                                  % �����Ծ�
js=js
g=9.81;                                 %�������ٶ�

%%
%�����ϲ���
Ntrans=numel(Dtrans);                   %�����ص�����������
nntrans=zeros(Ntrans,1);                %��nntrans��ǰn���ۼ�
ntrans=sum(ltrans);
Rt=zeros(ntrans,1);                     %������������뾶/m
rt=zeros(ntrans,1);                     %�����������ڰ뾶/m
Aot=zeros(ntrans,1);                    %����������������/m^2
Ait=zeros(ntrans,1);                    %�����������ڽ����/m^2
qt=zeros(ntrans,1);                     %��������������/N.m^-1
%qmt=zeros(ntrans,1);                    %���������ϸ���/N.m^-1
%Kft=zeros(ntrans,1);                    %����ϵ��
It=zeros(ntrans,1);                     %���Ծ�
ht=zeros(ntrans,1);                     %�ں�
Pi=zeros(ntrans,1);%��������ѹ����MPa
PI1=Pi;
PI2=Pi;
Tc=PI1;
Po=zeros(ntrans,1);%��������ѹ��,MPa
PO1=Po;
PO2=Pi; 
FH=zeros(ntrans,1);%���������ٽ��غ�,N
FS=zeros(ntrans,1);%���������ٽ��غ�,N

%����nnntrans�����ں�������
nntrans(1)=ltrans(1);
for i=2:Ntrans
    nntrans(i)=nntrans(i-1)+ltrans(i);
end
%���������ϸ��ֶεİ뾶�������������
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
%�������
Dw=Dw+0.001;
ds=1;                      %����
len=ntrans-1;              %���㳤��
nt=len/ds;
sspan=0:ds:len;
SW=sspan';

%%
%�����۹켣����
[Mk,mk,Sk,alphak,phik]=deal_curve_data2(data,js);

%��ʼ��k��tao�Ȳ���
[alpha,phi,ks,dks,ddks,kphis,kalphas,taos]=prepare_data(sspan,Mk,mk,Sk,alphak,phik);
DAL=zeros(ntrans,1);
ALpha=flipud(alpha*180/pi);
for i=1:ntrans-1
    DAL(i)=abs((ALpha(i+1)-ALpha(i))*30)*10;
end
[Length,Ys,Zs,Xs]=deal_trank(Sk,alpha,phi);      %����ӵײ�������λ�õ���Ȼ�����Լ���������
mmm=zeros(ntrans,3);
iiiii=numel(mmm(:,3));
mmm(:,3)=Xs(iiiii,1)-Xs(:,1);
mmm(:,1)=Ys(iiiii,1)-Ys(:,1);  %������
mmm(:,2)=Zs(iiiii,1)-Zs(:,1);  %������

%%
%ʶ���۹켣
smalpha=smooth(alpha,201);
B=mean(smalpha(1:500));
B1=mean(smalpha(1:300));
Z=mean(smalpha(end-300:end));
Ls=0;
Lc=0;
Lh=0;
if B<0.44  %�����о�б��С��25�㣬�򵱳�ֱ������
    Ls=ntrans;
else
for i=1:ntrans-1
    ca(i)=abs(smalpha(end-i+1)-Z);
    Ls=i+1;%��ֱ����
    if ca(i)>0.11 && smalpha(end-i+1)>0.25
        break
    end 
end
end
if B1>0.44 && B<1.23  %�ж�25-70��Ķ���
    for i=1:ntrans-1  
       if Ls==ntrans
        break
       else
        ba(i)=abs(smalpha(i)-B1);
        Lh=i;%ˮƽ����
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
        Lh=i;%ˮƽ����
        if ba(i)>0.11 && smalpha(i)<1.35 
           break  
        end
    end
end
end
Lc=ntrans-Lh-Ls;   %��б��

%  gtd=(ks*180/pi)*30;
R=zeros(ntrans,1);
R=1./ks;
RR=R.^2;
for i=1:ntrans
    if i<Lh+1
       FH(i)=-2*(2*2^0.5 - 1)*(E*It(i)*qt(i)*sin(alpha(i))/(0.5*Dw-Rt(i)))^(0.5);%бֱ��ˮƽ
       FS(i)=-2*(E*It(i)*qt(i)*sin(alpha(i))/(0.5*Dw-Rt(i)))^(0.5);
    elseif i<Lh+1+Lc
       FH(i)=-7.56*E*It(i)/(Rt(i)*(0.5*Dw-Rt(i)))/(10^3);%����
       FS(i)=-4*E*It(i)/(Rt(i)*(0.5*Dw-Rt(i)))/(10^3);
%        FH(i)=-12*(E*It(i)/((0.5*Dw-Rt(i))*R(i)))*(1+(1+((0.5*Dw-Rt(i))*RR(i)*qt(i)*sin(alpha(i))/(8*E*It(i))))^0.5); %����
%        FS(i)=-4*(E*It(i)/((0.5*Dw-Rt(i))*R(i)))*(1+(1+((0.5*Dw-Rt(i))*RR(i)*qt(i)*sin(alpha(i))/(4*E*It(i))))^0.5);
    else
       FH(i)=-5.55*(E*It(i)*qt(i)^2)^(1/3);%��ֱ
       FS(i)=-2.55*(E*It(i)*qt(i)^2)^(1/3);
    end
end

fh=flipud(FH)/1000;
fs=flipud(FS)/1000;

end