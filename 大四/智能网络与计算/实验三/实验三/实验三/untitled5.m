T = 10;
syms k
func=0;
for i = 1:10
func = func+1/2*((1/(log(2)*k)-1/a(i))+abs((1/(log(2)*k)-1/a(i))));
end
eqn = func ==1;
lamda=double(vpasolve(eqn,k));
v = 1/((log(2)/log(exp(1)))*lamda);
z = [];
for i = 0:T-1
y = 1/a(i+1);
z = [z;i y;i+1 y];
end
figure(2);
plot(z(:,1),z(:,2));
line([0 T],[v v], 'linestyle',':');
xlabel('i');
legend('1/a','注水线');
set(gca, 'xtick', [], 'ytick',[])
text(-1.2,v,num2str(v));