function diff_var=diff_func(vars,span)
    diff_var1=zeros(size(vars));
    for i=1:numel(vars)
        if i==1
            diff_var1(i)=(vars(i+1)-vars(i))/(span(i+1)-span(i));
        elseif i==numel(vars)
            diff_var1(i)=(vars(end)-vars(end-1))/(span(end)-span(end-1));
        else
            diff_var1(i)=(vars(i+1)-vars(i-1))/(span(i+1)-span(i-1));
        end
    end
    %�Ե������й⻬����
    diff_var=smooth(diff_var1,100);          %�������ú���Ĺ⻬���������ƹ⻬������
   
end