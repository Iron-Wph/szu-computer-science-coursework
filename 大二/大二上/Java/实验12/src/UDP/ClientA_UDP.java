import java.io.*;
import java.net.*;
import java.util.Scanner;
//控制接受信息的线程
class InputThreadA_UDP extends Thread
{
    // 数据存储的空间，数据包data以及当前代表当前客户端的套接字
    byte b[] = new byte[1000];
    DatagramPacket data;
    DatagramSocket mail_in;
    // 传入当前客户端的套接字
    InputThreadA_UDP(DatagramSocket tSocket) throws IOException {
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

                System.out.println("ClientB:"+str);

                // 线程休眠0.1s进行缓冲
                Thread.sleep(100);
            }
            catch (IOException e)
            {
                throw new RuntimeException(e);
            }
            catch (InterruptedException e)
            {
                throw new RuntimeException(e);
            }
        }
    }
}
//控制发送信息的线程
class OutputThreadA_UDP extends Thread
{
    // 数据存储的空间，数据包data以及当前代表当前客户端的套接字
    byte b[] = new byte[1000];
    DatagramPacket data;
    DatagramSocket mail_out;
    OutputThreadA_UDP(int dis, DatagramSocket tSocket) throws IOException {
        // 构建向服务器发送信息的输出流
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
            //如果有输入就转发，避免堵塞
            if(scanner.hasNext())
            {
                //整行读取控制台的输入信息
                String message = scanner.nextLine();
                //发送信息
                try
                {
                    // 获取发送文本的字节格式
                    b = message.getBytes();
                    // 修改待发送的信息数据包
                    data.setData(b);
                    // 发送信息
                    mail_out.send(data);

                    //线程休眠0.1s进行缓冲
                    Thread.sleep(100);
                }
                catch (IOException e)
                {
                    throw new RuntimeException(e);
                }
                catch (InterruptedException e)
                {
                    throw new RuntimeException(e);
                }
            }
        }
    }
}

public class ClientA_UDP
{
    public static void main(String args[])
    {
        try
        {
            // 定义ClientA接口
            int portA = 1234;
            // 定义服务端C的接口
            int portC = 2341;

            // 客户端A的Socket
            DatagramSocket SocketA = new DatagramSocket(portA);

            // 创建接收、发送信息的线程
            // 接收信息的线程应该传入服务端的接口portC
            InputThreadA_UDP in = new InputThreadA_UDP(SocketA);
            // 发送信息的线程应该传入服务端的接口portC
            OutputThreadA_UDP out = new OutputThreadA_UDP(portC,SocketA);

            //运行控制输入、输出的线程
            in.start();
            out.start();

            in.join();
            out.join();
        }
        catch(IOException e)
        {
            System.out.println("Unable to connect to the server");
        }
        catch(InterruptedException e){}
    }
}
