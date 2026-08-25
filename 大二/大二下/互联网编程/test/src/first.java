public class first
{
    public static void main(String []args)
    {
        // 存储时间与金额无关
        double x = 1,init = x;
        int year = 0;
        while(true)
        {
            x *= 1.05;
            year++;
            if(x>=2 * init)
                break;
        }
        System.out.println("需要存" + year + "年");
    }
}