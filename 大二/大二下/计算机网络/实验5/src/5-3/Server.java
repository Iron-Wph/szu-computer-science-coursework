import java.io.*;
import java.net.*;

public class Server
{
    public static void main(String args[])
    {   //服务器套接字
        ServerSocket server = null;
        try
        {

            //创建服务器的套接字
            server = new ServerSocket(4333);
            System.out.println("服务器运行开始OKOKOKO!!!");    //输出服务器正常运行信息
            int i = 0;
            // 持续监听是否有客户端连接
            while (true)
            {
                // 接收客户端的套接字
                Socket ClientSocket = server.accept();
                String path = "D:\\作业\\计算机网络\\实验5\\network coding\\szu.txt";
                //
                if(ClientSocket!=null)
                {
                    System.out.println("服务器的线程"+ i +"启动,与客户端" + i + "连接成功");
                    i++;
                    // 为每个客户端创建线程
                    Output out = new Output(ClientSocket,path);
                    out.start();
                }
            }
        }
        catch(IOException e)
        {
            System.out.println(""+e);
        }
    }
}
