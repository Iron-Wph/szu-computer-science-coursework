import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;
//控制发送信息的线程
class Output extends Thread
{
    DataOutputStream out = null;
    Output(Socket tem) throws IOException {
        //构建发送信息的输出流
        out = new DataOutputStream(tem.getOutputStream());
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