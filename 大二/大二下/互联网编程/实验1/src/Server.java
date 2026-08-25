import java.io.*;
import java.net.*;

public class Server
{
    public static void main(String args[])
    {   //服务器套接字
        ServerSocket server = null;
        //客户端的套接字
        Socket ClientSocket = null;
        //
        try
        {
            //创建服务器的套接字
            server = new ServerSocket(4333);

            //接受客户端的套接字
            ClientSocket = server.accept();

            //当客户端都加入服务器时，创建线程
            if(ClientSocket!=null)
            {
                System.out.println("客户端成功连接");
                //分别创建服务客户的线程
                Input in = new Input(ClientSocket);
                Output out = new Output(ClientSocket);
                //启动接收、发送信息的线程
                in.start();
                out.start();
                //
                in.join();
                out.join();
            }
        }
        catch(IOException e)
        {
            System.out.println(""+e);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
