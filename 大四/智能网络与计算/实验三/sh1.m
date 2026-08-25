% 清理工作区
clear all;
clc;

% 设置参数
T = 10;               % 信道数
Pmax = 1;             % 最大总功率(W)
Btotal = 10;          % 总带宽(MHz)
a = rand(T,1);        % 信道状态与噪声比值
Pmin = 0.0;           % 每个信道最小功率（可调整）
Bmin = 0.0;           % 每个信道最小带宽（可调整）
% 检查约束可行性（总最小资源 ≤ 总资源）
if T*Pmin > Pmax || T*Bmin > Btotal
    error('最小资源约束过紧，无法满足总资源限制');
end

% 使用迭代方法求解优化问题
max_iter = 1000;       % 最大迭代次数
tolerance = 1e-3;     % 收敛容差

% 关键修改：随机初始化功率和带宽（满足总约束和最小约束）
% 1. 随机初始化功率（确保非负且总和为Pmax）
P_rand = rand(T,1);   % 生成随机向量（0~1之间）
P = Pmin + (P_rand / sum(P_rand)) * (Pmax - T*Pmin);  % 归一化并满足总功率约束

% 2. 随机初始化带宽（确保非负且总和为Btotal）
B_rand = rand(T,1);   % 生成随机向量（0~1之间）
B = Bmin + (B_rand / sum(B_rand)) * (Btotal - T*Bmin);  % 归一化并满足总带宽约束

% 迭代优化
for iter = 1:max_iter
    % 固定带宽分配，优化功率分配
    cvx_begin 
        variable P_new(T)
        maximize (sum(B .* log(1 + P_new .* a)/log(2)))
        subject to
            P_new >= Pmin;               % 最小功率约束
            sum(P_new) == Pmax;          % 总功率约束
    cvx_end

    % 固定功率分配，优化带宽分配
    cvx_begin quiet
        variable B_new(T)
        maximize (sum(B_new .* log(1 + P .* a)/log(2)))
        subject to
            B_new >= Bmin;               % 最小带宽约束
            sum(B_new) == Btotal;        % 总带宽约束
    cvx_end

    % 计算变化量
    P_change = norm(P_new - P, inf);
    B_change = norm(B_new - B, inf);

    % 更新变量
    P = P_new;
    B = B_new;

    % 检查收敛
    if max(P_change, B_change) < tolerance
        fprintf('在第 %d 次迭代后收敛\n', iter);
        break;
    end

    if iter == max_iter
        fprintf('达到最大迭代次数 %d\n', max_iter);
    end
end

% 显示结果
disp('信道状态与噪声比值 a:');
disp(a');
disp('最优功率分配 P:');
disp(P');
disp('最优带宽分配 B:');
disp(B');
disp(['总容量: ' num2str(sum(B .* log(1 + P .* a)/log(2))) ' bits/s']);

% 绘制结果
figure;
subplot(3,1,1);
stem(a);
title('信道状态与噪声比值 a');
xlabel('信道');
ylabel('a_i');
grid on;

subplot(3,1,2);
stem(P);
title('最优功率分配 P');
xlabel('信道');
ylabel('P_i (W)');
grid on;

subplot(3,1,3);
stem(B);
title('最优带宽分配 B');
xlabel('信道');
ylabel('B_i (MHz)');
grid on;