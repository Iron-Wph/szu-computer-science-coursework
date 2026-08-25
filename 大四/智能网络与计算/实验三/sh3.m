% 清理工作区
clear all;
clc;

% 设置参数
T = 10;  % 时隙数
Pmax = 1; % 最大总功率
a = rand(T,1); % 生成信道状态与噪声比值

% 使用CVX求解优化问题
cvx_begin
    variable P(T) % 定义功率分配变量
    maximize (sum(log(1 + P .* a)/log(2))); % 最大化总容量，注意log2转换为自然对数
    subject to
        P >= 0; % 功率非负约束
        sum(P) == Pmax; % 总功率约束
cvx_end

% 显示结果
disp('信道状态与噪声比值 a:');
disp(a');
disp('最优功率分配 P:');
disp(P');
disp(['总容量: ' num2str(sum(log(1 + P .* a)/log(2))) ' bits/s/Hz']);

% 绘制结果
figure;
subplot(2,1,1);
stem(a);
title('信道状态与噪声比值 a');
xlabel('时隙');
ylabel('a_i');
grid on;

subplot(2,1,2);
stem(P);
title('最优功率分配 P');
xlabel('时隙');
ylabel('P_i (W)');
grid on;