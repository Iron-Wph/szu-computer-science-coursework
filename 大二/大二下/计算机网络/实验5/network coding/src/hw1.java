import java.io.*;
import java.net.*;
public class hw1 {
    public static void main(String[] args) throws IOException {
        // 输出主机名称
        InetAddress localhost = InetAddress.getLocalHost();
        System.out.println("主机名称："+localhost.getHostName());
        // 输出主机的IP地址
        System.out.println("主机的IP地址"+localhost.getHostAddress());

        // 根据域名获取IP地址
        InetAddress csdn = InetAddress.getByName("www.csdn.net");
        byte []IP = csdn.getAddress();
        System.out.println("csdn的IP地址为：");
        for(byte ip: IP)
        {
            int tip = ip<0?ip+256:ip;
            System.out.print(tip+" ");
        }
        System.out.println();

        // 下载深圳大学首页
        URL url = new URL("http://www.szu.edu.cn");
        InputStream in = url.openStream();
        FileOutputStream file = new FileOutputStream(new File("szu.txt"));
        int a = 0;
        while(a > -1)
        {
            a = in.read();
            file.write(a);
        }
        // 输出网页的大小
        System.out.println(url.toString()+"的大小为："+url.openConnection().getContentLength()+"B");
    }
}