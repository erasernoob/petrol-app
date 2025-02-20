function [Length,Xs,Ys,Zs]=deal_input_data(data)
    Xs=zeros(size(data,1),1);
    Ys=zeros(size(data,1),1);
    Zs=zeros(size(data,1),1);
    Length=zeros(size(data,1),1);
    Length=data(:,1);
    for i=2:length(Xs)
       
           
        
        alpha1=data(i-1,2)/180*pi;
        alpha2=data(i,2)/180*pi;
        phi1=data(i-1,3)/180*pi;
        phi2=data(i,3)/180*pi;
        ppp=abs(phi1-phi2);
        if ppp>pi&phi1<pi
            phi1=phi1+2*pi;
            elseif ppp>pi&phi1>pi
                 phi1=phi1-2*pi;
        end
        ds=data(i,1)-data(i-1,1);
        if alpha1~=alpha2&phi1~=phi2
            dx=ds*(cos(alpha1)-cos(alpha2))/(alpha2-alpha1)/(phi2-phi1)*(sin(phi2)-sin(phi1));
            dy=ds*(cos(alpha1)-cos(alpha2))/(alpha2-alpha1)/(phi2-phi1)*(cos(phi1)-cos(phi2));
            dz=ds/(alpha2-alpha1)*(sin(alpha2)-sin(alpha1));
        elseif alpha1==alpha2&phi1~=phi2
            dx=ds*sin(alpha1)/(phi2-phi1)*(sin(phi2)-sin(phi1));
            dy=ds*sin(alpha1)/(phi2-phi1)*(cos(phi1)-cos(phi2));
            dz=ds*cos(alpha1);
        elseif alpha1~=alpha2&phi1==phi2
            dx=ds/(alpha2-alpha1)*(cos(alpha1)-cos(alpha2))*cos(phi1);
            dy=ds/(alpha2-alpha1)*(cos(alpha1)-cos(alpha2))*sin(phi1);
            dz=ds/(alpha2-alpha1)*(sin(alpha2)-sin(alpha1));
        else
            dx=ds*sin(alpha1)*cos(phi1);
            dy=ds*sin(alpha1)*sin(phi1);
            dz=ds*cos(alpha1);
        end
        Xs(i)=Xs(i-1)+dx;
        Ys(i)=Ys(i-1)+dy;
        Zs(i)=Zs(i-1)+dz;
    end
    %变换成从井底到井口的数据
    Length=data(end,1)-Length;
%     Xs0=Xs(end:-1:1);
%     Ys0=Ys(end:-1:1);
%     Zs0=Zs(end)-Zs;
    Xs0=Xs(end)-Xs;
    Ys0=Ys(end)-Ys;
    Zs0=Zs(end)-Zs;
    %同前期xyz坐标系定义保持一致
    Xs=Zs0;
    Ys=Xs0;
    Zs=Ys0;
end