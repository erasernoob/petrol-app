function [Tjk,Mjk,aqjk]=mainfunc(guiji,zuanju,wc,T0,rhoi,Dw,tgxs,miua11,miua22,qfqd,jsjg,v,omega)
data1=guiji;
data2=zuanju;
working_condition=wc;     %����ѡ��1��ת�����2���������3���ꣻ4���ꣻ5������
if working_condition==1
    %�����������������������������������������������������������������������������������������������
    T0=T0;                   %��ѹ��N
    rhoi=rhoi;               %�꾮Һ�ܶȣ�kg/m3 
    Dw=Dw;                   %����ֱ����m
    tgxs=tgxs;               %�׹����m
    miua1=miua11/30;          %�׹ܶ�Ħ��ϵ��
    miua2=miua22/30;          %���۶�Ħ��ϵ��
    miut1=miua11*1.2;        %�׹ܶ�����Ħ��ϵ��
    miut2=miua22*1.2;        %���۶�����Ħ��ϵ��
    qfqd=qfqd;               %��������ǿ�ȣ�MPa
    jsjg=jsjg;               %���㾮������m
    %�̶�ֵ��������������������������������������������������������������������������������������������
    M0=abs(T0*Dw/3*0.5);         %��ͷŤ��
    v=v;                     %����ٶȣ�m/s               
    omega=omega;             %ת�٣�rad/s
    miu=0.2;                 %�꾮Һ����ճ�ȣ�mPa��s
    taof=14;                 %�꾮Һ����ֵ��Pa
    sign1=1;                 %�����˶�����1���룻-1����
    sign2=1;                 %�����Ƿ���ת��1��ת��0����ת
elseif working_condition==2
    %�����������������������������������������������������������������������������������������������
    T0=T0;                   %��ѹ��N
    rhoi=rhoi;               %�꾮Һ�ܶȣ�kg/m3 
    Dw=Dw;                   %����ֱ����m
    tgxs=tgxs;               %�׹����m
    miua1=miua11*1.165;      %�׹ܶ�Ħ��ϵ��
    miua2=miua22*1.165;      %���۶�Ħ��ϵ��
    miut1=0;                 %�׹ܶ�����Ħ��ϵ��
    miut2=0;                 %���۶�����Ħ��ϵ��  
    qfqd=qfqd;               %��������ǿ�ȣ�MPa
    jsjg=jsjg;               %���㾮������m
    %�̶�ֵ��������������������������������������������������������������������������������������������
    M0=0;                    %��ͷŤ��
    miu=0.2;                 %�꾮Һ����ճ�ȣ�mPa��s
    taof=14;                 %�꾮Һ����ֵ��Pa
    v=1;                     %����ٶȣ�m/s
    omega=0;                 %ת�٣�rad/s
    sign1=1;                 %�����˶�����1���룻-1����
    sign2=0;                 %�����Ƿ���ת��1��ת��0����ת
elseif working_condition==3
    %�����������������������������������������������������������������������������������������������               
    rhoi=rhoi;               %�꾮Һ�ܶȣ�kg/m3
    Dw=Dw;                   %����ֱ����m
    tgxs=tgxs;               %�׹����m
    miua1=miua11*1.09;       %�׹ܶ�Ħ��ϵ��
    miua2=miua22*1.09;       %���۶�Ħ��ϵ��
    miut1=0;                 %�׹ܶ�����Ħ��ϵ��
    miut2=0;                 %���۶�����Ħ��ϵ��
    qfqd=qfqd;               %��������ǿ�ȣ�MPa
    jsjg=jsjg;               %���㾮������m
    %�̶�ֵ��������������������������������������������������������������������������������������������
    T0=0;                    %��ѹ��N
    M0=0;                    %��ͷŤ��
    miu=0.2;                 %�꾮Һ����ճ�ȣ�mPa��s
    taof=14;                 %�꾮Һ����ֵ��Pa
    v=1;                     %�����ٶȣ�m/s
    omega=0;                 %ת�٣�rad/s
    sign1=-1;                %�����˶�����1���룻-1����
    sign2=0;                 %�����Ƿ���ת��1��ת��0����ת
elseif working_condition==4
    %�����������������������������������������������������������������������������������������������
    rhoi=rhoi;               %�꾮Һ�ܶȣ�kg/m3
    Dw=Dw;                   %����ֱ����m
    tgxs=tgxs;               %�׹����m
    miua1=miua11*1.17;       %�׹ܶ�Ħ��ϵ��
    miua2=miua22*1.17;       %���۶�Ħ��ϵ��
    miut1=0;                 %�׹ܶ�����Ħ��ϵ��
    miut2=0;                 %���۶�����Ħ��ϵ��
    qfqd=qfqd;               %��������ǿ�ȣ�MPa
    jsjg=jsjg;               %���㾮������m
    %�̶�ֵ��������������������������������������������������������������������������������������������
    T0=0;                    %��ѹ��N
    M0=0;                    %��ͷŤ��
    miu=0.2;                 %�꾮Һ����ճ�ȣ�mPa��s
    taof=14;                 %�꾮Һ����ֵ��Pa
    v=1;                     %�·��ٶȣ�m/s               
    omega=0;                 %ת�٣�rad/s
    sign1=1;                 %�����˶�����1���룻-1����
    sign2=0;                 %�����Ƿ���ת��1��ת��0����ת
elseif working_condition==5
    %����������������������������������������������������������������������������������������������� 
    rhoi=rhoi;               %�꾮Һ�ܶȣ�kg/m3
    Dw=Dw;                   %����ֱ����m
    tgxs=tgxs;               %�׹����m
    miua1=miua11/1.5;                 %�׹ܶ�Ħ��ϵ��
    miua2=miua22/1.5;                 %���۶�Ħ��ϵ��
    miut1=miua11*1.2;        %�׹ܶ�����Ħ��ϵ��
    miut2=miua22*1.2;        %���۶�����Ħ��ϵ��
    qfqd=qfqd;               %��������ǿ�ȣ�MPa
    jsjg=jsjg;               %���㾮������m
    %�̶�ֵ��������������������������������������������������������������������������������������������
    T0=0;                    %��ѹ��N
    M0=0;                    %��ͷŤ�أ�N��m
    v=v;                     %�����ٶȣ�m/s               
    omega=omega;            %ת�٣�rad/s
    miu=0.2;                 %�꾮Һ����ճ�ȣ�mPa��s
    taof=14;                 %�꾮Һ����ֵ��Pa
    sign1=-1;                %�����˶�����1���룻-1����
    sign2=1;                 %�����Ƿ���ת��1��ת��0����ת
end

%��������
rhoo=rhoi;       %�����������ܶ�
T0=-T0;
g=9.81;          %�������ٶ�
E=2.1e11;        %��������ģ��

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
        % ���һ�ε���ʱʹ�� guiji ����ֵ
        js = yssd;
    else
        % ���������ļ������
        js = nn * jsjg;
    end

%��߳���ȷ��
row_data=data2(4, 1:end-1);
row_sum=sum(row_data);
data2(4,end)=js-row_sum

%�����ϲ���
Dtrans=data2(1,:);             %�����⾶��m
dtrans=data2(2,:);             %�����ھ���m
mtrans=9.81*data2(3,:);        %����������أ�N/m
ltrans=data2(4,:); 

%%
%�����ϲ���
Ntrans=numel(Dtrans);                   %�����ص�����������
nntrans=zeros(Ntrans,1);                %��nntrans��ǰn���ۼ�
ntrans=sum(ltrans);                     %�����ص��������ֶܷ��������㲽����
Rt=zeros(ntrans,1);                     %������������뾶/m
rt=zeros(ntrans,1);                     %�����������ڰ뾶/m
Aot=zeros(ntrans,1);                    %����������������/m^2
Ait=zeros(ntrans,1);                    %�����������ڽ����/m^2
qt=zeros(ntrans,1);                     %��������������/N.m^-1
qmt=zeros(ntrans,1);                    %���������ϸ���/N.m^-1
Kft=zeros(ntrans,1);                    %����ϵ��
It=zeros(ntrans,1);                     %���Ծ�
ht=zeros(ntrans,1);                     %�ں�
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
%�������
ds=1;                      %����
len=ntrans-1;              %���㳤��
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
%�����۹켣����
[Mk,mk,Sk,alphak,phik]=deal_curve_data(data1,js);

%%
%��ʼ��k��tao�Ȳ���
[alpha,phi,ks,dks,ddks,kphis,kalphas,taos]=prepare_data(sspan,Mk,mk,Sk,alphak,phik);

%%
%��ʼ����
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
%���ݻָ�
Nbtemp=0;
Nntemp=0;
Ttemp=T0;
Mtemp=M0;
[N,~,~]=data_recovery(s,y,ks,dks,ddks,kphis,kalphas,taos,sspan,v,omega,taof,miu,Rt,Dw,miua,miut,qmt...
    ,Ait,Aot,rhoi,rhoo,E,It,g,Mk,mk,Sk,alphak,phik,Ttemp,Mtemp,Nbtemp,Nntemp,sign1,sign2);

%%
%���Ħ��
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
%ԭ�ۼ�Ħ��
Flj=zeros(numel(N),1);
Flj(1)=N(1)*miua(i);
for i=2:ntrans
    Flj(i)=Flj(i-1)+N(i)*miua(i);
end

%%
%���
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

%% ������������
%��ת���
if working_condition==1
    %�������������ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, T_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('������������kN��'); % y���ǩ
    %�����������������ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, T_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '��ת���_����������.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�������Ť��ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, M_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('����Ť�أ�kN��m��'); % y���ǩ
    %��������Ť�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, M_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '��ת���_����Ť��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�����ȫϵ��ͼ��������������������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, aq_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('��ȫϵ��'); % y���ǩ
    %������ȫϵ�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, aq_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '��ת���_��ȫϵ��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
%�������
elseif working_condition==2
    %�������������ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, T_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('������������kN��'); % y���ǩ
    %�����������������ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, T_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '�������_����������.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�������Ť��ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, M_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('����Ť�أ�kN��m��'); % y���ǩ
    %��������Ť�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, M_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '�������_����Ť��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�����ȫϵ��ͼ��������������������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, aq_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('��ȫϵ��'); % y���ǩ
    %������ȫϵ�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, aq_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '�������_��ȫϵ��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
%����
elseif working_condition==3
    %�������������ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, T_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('������������kN��'); % y���ǩ
    %�����������������ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, T_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '����_����������.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�������Ť��ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, M_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('����Ť�أ�kN��m��'); % y���ǩ
    %��������Ť�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, M_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '����_����Ť��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�����ȫϵ��ͼ��������������������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, aq_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('��ȫϵ��'); % y���ǩ
    %������ȫϵ�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, aq_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '����_��ȫϵ��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
%����
elseif working_condition==4
    %�������������ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, T_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('������������kN��'); % y���ǩ
    %�����������������ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, T_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '����_����������.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�������Ť��ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, M_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('����Ť�أ�kN��m��'); % y���ǩ
    %��������Ť�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, M_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '����_����Ť��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�����ȫϵ��ͼ��������������������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, aq_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('��ȫϵ��'); % y���ǩ
    %������ȫϵ�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, aq_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '����_��ȫϵ��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
%������
elseif working_condition==5
    %�������������ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, T_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('������������kN��'); % y���ǩ
    %�����������������ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(T_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, T_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '������_����������.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�������Ť��ͼ����������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, M_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('����Ť�أ�kN��m��'); % y���ǩ
    %��������Ť�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(M_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, M_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '������_����Ť��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
    %�����ȫϵ��ͼ��������������������������������������������������������������������������������������������������
    figure;
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]; % ��������꣬���� jsjg ������������ yssd
    plot(x_coords, aq_result(1, :)); % ���ƾ���������ͼ
    xlabel('���m��'); % x���ǩ
    ylabel('��ȫϵ��'); % y���ǩ
    %������ȫϵ�����ݡ���������������������������������������������������������������������������������������
    x_coords = [jsjg * (1:size(aq_result, 2) - 1), yssd]'; % �����꣬���� jsjg ������������ yssd
    dataToExport = [x_coords, aq_result(1, :)']; % ��������Ͷ�Ӧ�������ϲ�Ϊ���ݱ�
    writematrix(dataToExport, '������_��ȫϵ��.xlsx', 'Sheet', 1, 'Range', 'A1'); % ����Ϊ Excel �ļ�
end

end