function [alphacal,phical]=spline_interp(Mk,mk,Sk,alphak,phik,S0)
    np=numel(Mk);
    if S0>=Sk(end)
        iter=np-1;
    else
        for i=1:np-1
            if S0>=Sk(i)&&S0<Sk(i+1)
                iter=i;
                break;
            end
        end
    end
    if S0<min(Sk)
        iter=1;
    end
    M0=Mk(iter);
    M1=Mk(iter+1);
    m0=mk(iter);
    m1=mk(iter+1);
    alpha0=alphak(iter);
    alpha1=alphak(iter+1);
    phi0=phik(iter);
    phi1=phik(iter+1);
    Sr=Sk(iter+1);
    Sl=Sk(iter);
    Lk=Sk(iter+1)-Sk(iter);
    C1=alpha1/Lk-M1*Lk/6;
    C0=alpha0/Lk-M0*Lk/6;
    c1=phi1/Lk-M1*Lk/6;
    c0=phi0/Lk-M0*Lk/6;
    alphacal=M0*(Sr-S0)^3/6/Lk+M1*(S0-Sl)^3/6/Lk+C1*(S0-Sl)+C0*(Sr-S0);
    phical=m0*(Sr-S0)^3/6/Lk+m1*(S0-Sl)^3/6/Lk+c1*(S0-Sl)+c0*(Sr-S0);
end



