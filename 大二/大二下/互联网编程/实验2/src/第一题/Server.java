import java.io.*;
import java.net.*;
//为客户端提供服务的线程
class ClientThread implements Runnable
{
    //输入、输出流
    Input in;
    Output out;
    //src为接受的信息源，dis为发送的信息源
    ClientThread(Socket src) throws IOException {
        //根据传入的信息源，确定接受和转发对象
        in = new Input(src,"Client");
        out = new Output(src);
    }
    public void run()
    {   // 启动输入、输出流线程
        in.start();
        out.start();
        try {
            in.join();
            out.join();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}


public class Server
{
    public static void main(String args[])
    {   //服务器套接字
        ServerSocket server = null;
        try
        {

            //创建服务器的套接字
            server = new ServerSocket(4333);

            // 循环监听客户端的连接
            while(true)
            {
                // 接收客户端的套接字
                Socket ClientSocket = server.accept();
                // 当客户端都加入服务器时，创建线程
                if(ClientSocket!=null)
                {
                    System.out.println("客户端成功连接");
                    // 为每个客户端创建线程
                    ClientThread client = new ClientThread(ClientSocket);
                    client.run();
                }
            }
        }
        catch(IOException e)
        {
            System.out.println(""+e);
        }
    }
}
