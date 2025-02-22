function [N,Nn,Nb]=data_recovery(sall,yall,ks,dks,ddks,kphis,kalphas,taos,sspan,v,omega,taof,miu,Rt,Dw,amiu,tmiu,qmt...
    ,Ait,Aot,rhoi,rhoo,E,It,g,Mk,mk,Sk,alphak,phik,Ttemp,Mtemp,Nbtemp,Nntemp,sign1,sign2)
    N=zeros(size(sall));
    Nb=N;
    Nn=N;

    for i=1:numel(sall)
        s=sall(i);
        y=yall(i,:);
        T=y(1);
        M=y(2);             %提取状态变量
        
        %计算alpha phi
        [alpha,~]=spline_interp(Mk,mk,Sk,alphak,phik,s);
    
        %利用准备的数据进行插值
        k=interp1(sspan,ks,s);
        dk=interp1(sspan,dks,s);
        ddk=interp1(sspan,ddks,s);
        kphi=interp1(sspan,kphis,s);
        kalpha=interp1(sspan,kalphas,s);
        tao=interp1(sspan,taos,s);
        
        %输入钻具组合相关数据
        a=ceil(s)+1;
        R=Rt(a);
        Ao=Aot(a);
        Ai=Ait(a);
        qm=qmt(a);
        I=It(a);
        at=Rt(a);
        miua=amiu(a);
        miut=tmiu(a);
        flambda=v*(2*pi*at*taof/sqrt(v^2+(at*omega)^2)+4*pi*at*miu/log(Dw/2/at));
    
         x=fsolve(@(x)solve_func(x,M,T,k,dk,ddk,alpha,tao,kphi,kalpha,R,taof,v,miu,Dw,E,I,miua,miut,omega,flambda,qm,rhoi,rhoo,Ai,Ao,g,sign1,sign2)...
       ,[Ttemp,Mtemp,Nntemp,Nbtemp]); 
         Nn(i)=x(3);
         Nb(i)=x(4);
         N(i)=sqrt(x(3)^2+x(4)^2);
         Ttemp=x(1);
         Mtemp=x(2);
         Nntemp=x(3);
         Nbtemp=x(4);
         err=max(abs(solve_func(x,M,T,k,dk,ddk,alpha,tao,kphi,kalpha,R,taof,v,miu,Dw,E,I,miua,miut,omega,flambda,qm,rhoi,rhoo,Ai,Ao,g,sign1,sign2)));
         if err>1e-3
             pause(0.1);
         end
    end
end