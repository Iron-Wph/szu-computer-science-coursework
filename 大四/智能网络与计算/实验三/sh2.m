syms x  % 声明一个符号x，用于后续计算
func = 0;
for i = 1:10
    % 解析解进行求和，而且保证解析解为非负，即满足(x)+ = max(0,x)
    func = func + (1 / 2) * ( ( 1/(log(2)*x) - 1/a(i) ) + abs( (1/(log(2)*x)-1/a(i) ) ) );
end
eqn = func == 1;    % 定义方程eqn，要求func == 1
lamda = double(vpasolve(eqn, x));   % 利用vpasolve函数对方程进行求解

% 计算注水线v
v = 1 / ((log(2) / log(exp(1))) * lamda);

% 反算 p2，验证注水线的正确性
for i = 1:10
    p2(i) = max(0, v - 1/a(i));
end

if all(p2 >= 0) && abs(sum(p2) - 1) < 1e-6
    disp('注水线正确');
else
    disp('注水线不正确');
end

z = []; 
for i = 0:T-1 
    y = 1/a(i+1); 
    z = [z;i y;i+1 y]; 
end 
figure(1); 
plot(z(:,1),z(:,2)); 
line([0 T],[v v],'linestyle',':'); 
xlabel('i'); 
legend('1/a','注水线'); 
set(gca,'xtick',[],'ytick',[]); 
text(-1.2,v,num2str(v)); 
