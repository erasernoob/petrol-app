function [alphas,phis,ks,dks,ddks,kphis,kalphas,taos]=prepare_data(sspan,Mk,mk,Sk,alphak,phik)
    alphas=zeros(numel(sspan),1);
    phis=zeros(numel(sspan),1);
    taos=zeros(numel(sspan),1);
    for i=1:numel(sspan)
        [alphas(i),phis(i)]=spline_interp(Mk,mk,Sk,alphak,phik,sspan(i));
    end
    kphis=diff_func(phis,sspan);        %调用求导函数进行计算
    kalphas=diff_func(alphas,sspan);
    ks=sqrt(kalphas.^2+kphis.^2.*sin(alphas).*sin(alphas));
    dks=diff_func(ks,sspan);
    ddks=diff_func(dks,sspan);
    
    for i=1:numel(sspan)
        if i==1
            alpha1=alphas(1);
            alpha2=alphas(2);
            phi1=phis(1);
            phi2=phis(2);
              ppp=abs(phi1-phi2);
        if ppp>pi&phi1<pi
            phi1=phi1+2*pi;
            elseif ppp>pi&phi1>pi
                 phi1=phi1-2*pi;
        end
            ds=sspan(2)-sspan(1);
        elseif i==numel(sspan)
            alpha1=alphas(end-1);
            alpha2=alphas(end);
            phi1=phis(end-1);
            phi2=phis(end);
              ppp=abs(phi1-phi2);
        if ppp>pi&phi1<pi
            phi1=phi1+2*pi;
            elseif ppp>pi&phi1>pi
                 phi1=phi1-2*pi;
        end
            ds=2*(sspan(2)-sspan(1));
        else
            alpha1=alphas(i-1);
            alpha2=alphas(i+1);
            phi1=phis(i);
            phi2=phis(i+1);
            ppp=abs(phi1-phi2);
        if ppp>pi&phi1<pi
            phi1=phi1+2*pi;
            elseif ppp>pi&phi1>pi
                 phi1=phi1-2*pi;
        end
            ds=sspan(2)-sspan(1);
        end
        dp=(phi2-phi1)/2;
        da=(alpha2-alpha1)/2;
        ac=(alpha1+alpha2)/2;
        edl=sqrt(da^2+dp^2*(sin(ac))^2);
        
        theta=acos(da^2/edl^2*cos(dp)-da*dp/edl^2*(sin(alpha2)*cos(alpha2)-sin(alpha1)*cos(alpha1))*sin(dp)...
            +dp^2/edl^2*sin(alpha1)*sin(alpha2)*(sin(alpha1)*sin(alpha2)+cos(alpha1)*cos(alpha2)*cos(dp)));
        theta=real(theta);
        taos(i)=theta/ds;
    end
    
    for i=1:numel(sspan)
        if isnan(taos(i))
            taos(i)=0;
        else
            taos(i)=taos(i);
        end
    end
end