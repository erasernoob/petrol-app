clear
clc
%���������������������������������������������������������������������������������������������������������
guiji=xlsread('KL16-1-A25���۹켣_6000m.xlsx');
zuanju=xlsread('������.xlsx');
Holedia=0.2159;    %����ֱ����m
ml=2.1e5;          %��������ģ����MPa
js=6000            %���㾮�m

[fh,fs]=abcfunc4(guiji,Holedia,ml,zuanju,js);

%������������ٽ��غ�ͼ������������������������������������������������������������������������������������������������
figure;
plot(fs);
xlabel('���m��'); % x���ǩ
ylabel('���������ٽ��غɣ�kN��'); % y���ǩ
%�������������ٽ��غ����ݡ�����������������������������������������������������������������������������������������������������������
writematrix(fs, '���������ٽ��غ�.xlsx', 'Sheet', 1);
%������������ٽ��غ�ͼ������������������������������������������������������������������������������������������������
figure;
plot(fh);
xlabel('���m��'); % x���ǩ
ylabel('���������ٽ��غɣ�kN��'); % y���ǩ
%�������������ٽ��غ����ݡ�����������������������������������������������������������������������������������������������������������
writematrix(fh, '���������ٽ��غ�.xlsx', 'Sheet', 1);