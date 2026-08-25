n = 10;
a = rand(n,1);
cvx_begin
variable x(n);
maximize(sum(log(1+x.*a)/log(2)));
subject to
x>=0;
sum(x)==1;
cvx_end