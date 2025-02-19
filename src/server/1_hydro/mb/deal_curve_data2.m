function [Mk,mk,Sk,alphak,phik]=deal_curve_data2(data1)
%%  去除井眼轨迹中的重复值，并且按升序排序
    sortedData = sortrows(round(data1), 1); % 按第一列进行升序排序
   [~, uniqueIndices] = unique(sortedData(:, 1), 'stable'); % 获取第一列的唯一索引
   data = sortedData(uniqueIndices, :); % 通过索引获取唯一的行数据 
 %%
    S=round(data(:,1));
    alphaa=data(:,2);
    phia=data(:,3);
    n=round(S(end));
    alphas=zeros(n,1);
    phis=zeros(n,1);    
    for i=1:n
        alphas(i)=abs(interp1(S,alphaa,i,'spline'));
        phis(i)=abs(interp1(S,phia,i,'spline'));
    end
    for i=1:n
        alphas(i)=mod(alphas(i),360);
        phis(i)=mod(phis(i),360);
    end

    S=(1:1:n);
    S=S';
    alpha=alphas;
    phi=phis;
    np=numel(S);            %点数目
    A=zeros(np,np);
    D1=zeros(np,1);
    D2=zeros(np,1);
    Ls=S(2:end)-S(1:end-1);
    alpha=flipud(alpha)*pi/180;
    phi=flipud(phi)*pi/180;
    for i=2:np-1
        Lk0=Ls(i-1);
        Lk1=Ls(i);
        alphak1=alpha(i+1);
        alphak0=alpha(i);
        alphak00=alpha(i-1);
        phik1=phi(i+1);
        phik0=phi(i);
        phik00=phi(i-1);
        D1(i)=6/(Lk0+Lk1)*((alphak1-alphak0)/Lk1-(alphak0-alphak00)/Lk0);
        D2(i)=6/(Lk0+Lk1)*((phik1-phik0)/Lk1-(phik0-phik00)/Lk0);
        lamk=Lk1/(Lk0+Lk1);
        miuk=1-lamk;
        A(i,i-1:i+1)=[miuk,2,lamk];
    end
    Mk=zeros(np,1);
    mk=zeros(np,1);
    Mk(2:end-1)=A(2:end-1,2:end-1)\D1(2:end-1);
    mk(2:end-1)=A(2:end-1,2:end-1)\D2(2:end-1);
    Sk=S;
    alphak=alpha;
    phik=phi;
end