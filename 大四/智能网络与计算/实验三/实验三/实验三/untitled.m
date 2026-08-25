% 参数初始化
T = 10; % 时隙数
Pmax = 1; % 最大功率
a = rand(T, 1); % 生成信道状态ai

% CVX 求解最优功率分配
cvx_begin
    variable P(T) nonnegative
    maximize(sum(log(1 + P .* a)))
    subject to
        sum(P) == Pmax;
cvx_end

% 输出最优功率分配
disp('最优功率分配:');
disp(P);

% 绘图：显示功率分配
figure;
stem(1:T, P, 'filled');
xlabel('时隙 i');
ylabel('功率分配 P_i (W)');
title('CVX 求解的最优功率分配');
