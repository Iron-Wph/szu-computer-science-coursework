% 绘图
z = [];
for i = 0:T - 1
    y = 1 / a(i + 1);
    z = [z;i y;i+1 y];
end

figure(1)
plot(z(:,1), z(:,2));
line([0,T], [v,v], 'linestyle', ':');
xlabel('channel index a(i)');
legend('1/a', '注水线');
set(gca, 'xtick', [], 'ytick', []);
text(-1.2, v, num2str(v));