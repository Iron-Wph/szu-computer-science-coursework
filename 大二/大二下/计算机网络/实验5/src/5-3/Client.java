import java.io.*;
import java.net.*;
public class Client
{
    public static void main(String args[])
    {
        Socket socketAtClient;
        try
        {
            // 与服务器端口进行连接
            socketAtClient = new Socket("localhost", 4333);

            System.out.println("与服务器连接成功");
            //创建接收、发送信息的线程
            Input in = new Input(socketAtClient);

            //运行控制输入、输出的线程
            in.start();
        }
        catch(IOException e)
        {
            System.out.println("Unable to connect to the server");
        }
    }
}
