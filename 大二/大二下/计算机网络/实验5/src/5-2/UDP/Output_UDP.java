import java.io.*;
import java.net.*;
import java.util.Scanner;
public class Output_UDP extends Thread
{
    // 数据存储的空间，数据包data以及当前代表当前客户端的套接字
    byte b[] = new byte[1000];
    DatagramPacket data;
    DatagramSocket mail_out;
    //
    Output_UDP(int dis, DatagramSocket tSocket) throws IOException {
        //构建向服务器发送信息的输出流
        data = new DatagramPacket(b,b.length,InetAddress.getByName("localhost"),dis);
        mail_out = tSocket;
    }
    @Override
    public void run()
    {
        //获取控制台输入信息
        Scanner scanner = new Scanner(System.in);
        //持续监听是否有信息需要发送
        while(true)
        {
            // 获取待发送的信息
            String message = Windows.writermessage;
            // 按下发送键就发送
            if(Windows.flag)
            {
                Windows.flag = false;
                //发送信息
                try
                {
                    // 获取发送文本的字节格式
                    b = message.getBytes();
                    // 修改发送的信息数据包
                    data.setData(b);
                    // 发送信息
                    mail_out.send(data);
                    //线程休眠0.1s进行缓冲
                    Thread.sleep(100);
                } catch (IOException e)
                {
                    throw new RuntimeException(e);
                } catch (InterruptedException e)
                {
                    throw new RuntimeException(e);
                }
            }
        }
    }
}
