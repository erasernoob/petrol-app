function dyds=odefunc2(s,y,ksi,dksi,ddksi,kphisi,kalphasi,taosi,sspani,v1,v2,omega,taof,miu,Rti,rti,Dw,Miudi,miut,qmti...
    ,Aiti,Aoti,rhoi,rhoo,E,Iti,g,Mki,mki,Ski,alphaki,phiki,Ttemp,Mtemp,Nbtemp,Nntemp,sign1,sign2,Fs,Fh,fti,Pii,Poi)
    T=y(1);
    M=y(2);
    N=y(3);
    %计算alpha phi
    [alpha,~]=spline_interp(Mki,mki,Ski,alphaki,phiki,s);

    %利用准备的数据进行插值
    k=interp1(sspani,ksi,s);
    dk=interp1(sspani,dksi,s);
    ddk=interp1(sspani,ddksi,s);
    kphi=interp1(sspani,kphisi,s);
    kalpha=interp1(sspani,kalphasi,s);
    tao=interp1(sspani,taosi,s);
     %输入钻具组合相关数据
    a=ceil(s)+1;
    R=Rti(a);
    Ao=Aoti(a);
    Ai=Aiti(a);
    qm=qmti(a);
    I=Iti(a);
    at=Rti(a);
    bt=Rti(a);
    r=rti(a);
    miua=Miudi(a);
    Ft=0;
    FS=Fs(a);
     FH=Fh(a); 
      Nh=(0.5*Dw-R)*T^2/(4*E*I);
       Ns=(0.5*Dw-R)*T^2/(8*E*I);
       Mium=15.7*10^(-6);%流体运动粘度
       Rei=2*rhoi*v1*2*bt/Mium;
       derta=0.05; 
       if Rei<2320
          nonmda=64/Rei;
      elseif Rei<=22*(2*bt/derta)^(8/7)
          nonmda=0.316*Rei^(-0.25);
      elseif Rei<=597*(2*bt/derta)^(9/8)
          nonmda=(1.14-2*log10(derta/2/bt+21.25/Rei^0.9))^(-2);
      else 
          nonmda=0.11*(2*bt/derta)^0.25;
       end
%        Fflow=sign(v1)*rhoi*nonmda*v1^2*pi*bt/4;
%       flambdao=v2*(2*pi*at*taof/sqrt(v2^2+(at*omega)^2)+4*pi*at*miu/log(Dw/2/at))+Fflow;  
%        Nh=(0.5*Dw-R)*T^2/(4*E*I)*1.3;
    flambdao=(v2*(2*pi*at*taof/sqrt(v2^2+(at*omega)^2)+4*pi*at*miu/log(Dw/2/at))+v1*(2*pi*bt*taof/sqrt(v1^2+(bt*omega)^2)+4*pi*bt*miu/log(Dw/2/bt)))*1;
%     flambdao=32*v1*miu/(rhoi*at^2*9.8*4)+32*v2*miu/(rhoo*bt^2*9.8*4);
    
   x=fsolve(@(x)solve_func(x,M,T,k,dk,ddk,alpha,tao,kphi,kalpha,R,r,taof,v1,v2,miu,Dw,E,I,miua,miut,omega,flambdao,qm,rhoi,rhoo,Ai,Ao,g,sign1,sign2,FS,FH,Ft,Nh,Ns)...
       ,[Ttemp,Mtemp,Nntemp,Nbtemp]); 
   dyds=zeros(3,1);
   dyds(1)=x(1);
   dyds(2)=x(2);
   if T<FH
     dyds(3)=sqrt(x(3)^2+x(4)^2)+Nh;
   else
     dyds(3)=sqrt(x(3)^2+x(4)^2);  
   end
     %更新初始条件
   Ttemp=x(1);
   Mtemp=x(2);
   Nntemp=x(3);
   Nbtemp=x(4);
   err=max(abs(solve_func(x,M,T,k,dk,ddk,alpha,tao,kphi,kalpha,R,r,taof,v1,v2,miu,Dw,E,I,miua,miut,omega,flambdao,qm,rhoi,rhoo,Ai,Ao,g,sign1,sign2,FS,FH,Ft,Nh,Ns)));
   if err>1e-3
       pause(0.1);
   end
   end