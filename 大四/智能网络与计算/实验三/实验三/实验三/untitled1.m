% 清理工作区
clear all;
clc;

% 设置参数
T = 10;  % 信道数
Pmax = 1; % 最大总功率(W)
Btotal = 10; % 总带宽(MHz)
a = rand(T,1); % 生成信道状态与噪声比值

% 使用CVX求解优化问题
cvx_begin
    variable P(T) % 定义功率分配变量
    variable B(T) % 定义带宽分配变量
    maximize (sum(B .* log(1 + P .* a)/log(2))); % 最大化总容量
    subject to
        P >= 0; % 功率非负约束
        B >= 0; % 带宽非负约束
        sum(P) == Pmax; % 总功率约束
        sum(B) == Btotal; % 总带宽约束
cvx_end

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