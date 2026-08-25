import java.io.*;
import java.net.*;
class Input_UDP extends Thread
{
    // 数据存储的空间，数据包data以及当前代表当前客户端的套接字
    byte b[] = new byte[1000];
    DatagramPacket data;
    DatagramSocket mail_in;
    // 传入当前客户端的套接字
    Input_UDP(DatagramSocket tSocket) {
        //根据要接受对象的套接字，初始化数据包
        data = new DatagramPacket(b, b.length);
        mail_in = tSocket;
    }
    @Override
    public void run()
    {   //持续监听服务器转发的信息
        while(true)
        {
            //如果有信息则接收，避免堵塞
            try
            {
                // 接收信息
                mail_in.receive(data);
                // 输出信息，用trim去掉空格
                String str = new String(data.getData(),0, data.getLength());
                str = str.trim();

                System.out.println("接收到的信息为："+str);
                // 接口回调获得信息
                Windows.getInputdata(str);

                // 线程休眠0.1s进行缓冲
                Thread.sleep(100);
            }
            catch (IOException e)
            {
                throw new RuntimeException(e);
            } catch (InterruptedException e)
            {
                throw new RuntimeException(e);
            }
        }
    }
}
