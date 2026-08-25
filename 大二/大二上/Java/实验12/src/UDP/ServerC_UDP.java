import java.io.*;
import java.net.*;
//为客户端提供服务的线程
class ServerThread_UDP extends Thread
{
    // 服务器端的数据处理Socket
    DatagramSocket mail;
    // 接收或者发送的数据存储
    byte b[] = new byte[1000];
    DatagramPacket out_data;
    DatagramPacket in_data;
    //src为接受的信息源，dis为发送的信息源, mid为传送媒介
    ServerThread_UDP(int src,int dis,DatagramSocket tsocket) throws IOException
    {
        // 初始化服务器端Socket
        mail = tsocket;
        // 根据传入的信息源，确定接受和转发对象
        out_data = new DatagramPacket(b, b.length,InetAddress.getByName("localhost"),dis);
        in_data = new DatagramPacket(b, b.length,InetAddress.getByName("localhost"),src);
    }
    public void run()
    {
        //持续监听线程
        while(true)
        {
            try
            {
                // 实时接收信息
                mail.receive(in_data);
                // 修改待转发的信息，并实时转发
                out_data.setData(b);
                mail.send(out_data);
            }catch (IOException e)
            {
                System.out.println("用户离开");
                break;
            }
        }
    }
}

public class ServerC_UDP
{
    public static void main(String args[]) throws UnknownHostException
    {
        try
        {
            // 定义ClientA和ClientB的接口
            int portA = 1234;
            int portB = 3412;

            // 定义服务端C的接口
            int portC = 2341;

            // 创建客户端的套接字
            DatagramSocket ServerC = new DatagramSocket(portC);

            // 分别创建服务客户A、B的线程
            Thread threadA = new ServerThread_UDP(portA, portB,ServerC);
            Thread threadB = new ServerThread_UDP(portB, portA,ServerC);
            threadA.start();
            threadB.start();
            
            //
            System.out.println("通信启动！！！");
        }
        catch(IOException e)
        {
            System.out.println(""+e);
        }
    }
}
