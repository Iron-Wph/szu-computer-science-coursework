import java.io.*;
import java.net.*;
import java.util.Scanner;
//控制接受信息的线程
class InputThreadB extends Thread
{
    DataInputStream in = null;
    //传入服务器的套接字
    InputThreadB(Socket tem) throws IOException {
        //根据要接受对象的套接字，初始化输入流
        in = new DataInputStream(tem.getInputStream());
    }
    @Override
    public void run()
    {   //持续监听服务器转发的信息
        while(true)
        {
            //如果有信息则接收，避免堵塞
            try
            {
                if(in.available()>0)
                {
                    //接受ClientB的信息
                    String respon = in.readUTF();
                    //显示B用户的信息
                    System.out.println("ClientA:"+respon);
                    //线程休眠
                    Thread.sleep(100);
                }
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
//控制发送信息的线程
class OutputThreadB extends Thread
{
    Socket tem;     //服务器的套接字
    DataOutputStream out = null;
    OutputThreadB(Socket tem) throws IOException {
        //构建向服务器发送信息的输出流
        this.tem=tem;
        out = new DataOutputStream(this.tem.getOutputStream());
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
                //读取控制台输入信息
                String message = scanner.nextLine();
                //发送信息
                try
                {
                    out.writeUTF(message);
                    //线程休眠
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
public class ClientB
{
    public static void main(String args[])
    {
        Socket socketAtClient;
        try
        {
            // 与服务器端口进行连接
            socketAtClient = new Socket("localhost", 4333);

            //创建接收、发送信息的线程
            InputThreadB in = new InputThreadB(socketAtClient);
            OutputThreadB out = new OutputThreadB(socketAtClient);

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
