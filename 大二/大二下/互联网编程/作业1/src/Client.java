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

            //创建接收、发送信息的线程
            String path = "D:\\作业\\互联网编程\\hw1\\src\\ClientData.txt";
            Input_Client in = new Input_Client(socketAtClient,path);
            Output out = new Output(socketAtClient,path);

            //运行控制输入、输出的线程
            in.start();
            out.start();

//            in.join();
//            out.join();
        }
        catch(IOException e)
        {
            System.out.println("Unable to connect to the server");
        }
        //catch(InterruptedException e){}
    }
}
