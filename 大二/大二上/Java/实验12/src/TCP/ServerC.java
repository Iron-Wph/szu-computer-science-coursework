import java.io.*;
import java.net.*;
//为客户端提供服务的线程
class ServerThread extends Thread
{
    //输入、输出流
    DataInputStream in = null;
    DataOutputStream out = null;
    //src为接受的信息源，dis为发送的信息源
    ServerThread(Socket src,Socket dis) throws IOException {
        //根据传入的信息源，确定接受和转发对象
        in = new DataInputStream(src.getInputStream());
        out = new DataOutputStream(dis.getOutputStream());
    }
    public void run()
    {   //持续监听线程
        while(true)
        {
            try
            {
                //实时转发信息，避免造成堵塞
                if(in.available()>0)
                {
                    //获取信息
                    String mesg = in.readUTF();
                    //转发信息
                    out.writeUTF(mesg);
                    System.out.println(mesg);
                }
            }catch (IOException e)
            {
                System.out.println("用户离开");
                break;
            }
        }
    }
}

public class ServerC
{
    public static void main(String args[])
    {   //服务器套接字
        ServerSocket server = null;
        //客户端A、B的套接字
        Socket ClientSocketA = null;
        Socket ClientSocketB = null;
        //
        try
        {
            //创建服务器的套接字
            server = new ServerSocket(4333);

            //接受两个客户的套接字
            ClientSocketA = server.accept();
            ClientSocketB = server.accept();

            //当两个客户都加入服务器时，创建线程
            if(ClientSocketA!=null&&ClientSocketB!=null)
            {
                //分别创建服务客户A、B的线程
                Thread threadA = new ServerThread(ClientSocketA,ClientSocketB);
                Thread threadB = new ServerThread(ClientSocketB,ClientSocketA);
                threadA.start();
                threadB.start();
            }
        }
        catch(IOException e)
        {
            System.out.println(""+e);
        }
    }
}
