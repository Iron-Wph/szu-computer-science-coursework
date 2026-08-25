import java.text.DecimalFormat;
import java.util.Scanner;

public class second {
    // 判断能否构成四边形
    public static boolean sibianxing(double a, double b, double c, double d)
    {
        // 周长
        double len = a+b+c+d;
        // 找出四条边的最大值
        double maxb = Math.max(a, b);
        maxb = Math.max(c, maxb);
        maxb = Math.max(d, maxb);
        // 如果满足条件则是四边形
        if(len > maxb * maxb)
            return true;
        else
            return false;
    }
    public static void main(String[]args)
    {
        Scanner reader = new Scanner(System.in);
        double a,b,c,d;
        // 输入四边形的边长
        a = reader.nextDouble();
        b = reader.nextDouble();
        c = reader.nextDouble();
        d = reader.nextDouble();

        // 海明定理
        if(sibianxing(a, b, c, d))
        {
            // 半周长
            double p = (a+b+c+d)/2;
            double res = Math.sqrt((p-a)*(p-b)*(p-c)*(p-c));
            DecimalFormat df = new DecimalFormat("#.##");
            System.out.println("边长为" + a + " " + b + " " + c + " "+ d + "时，最大面积为: " + df.format(res));
        }
        else
        {
            System.out.println("边长为" + a + " " + b + " " + c + " " + d + "不能构成四边形");
        }
    }
}
