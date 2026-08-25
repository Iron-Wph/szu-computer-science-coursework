import java.io.*;
import java.net.*;
public class ClientB_UDP
{
    public static void main(String args[])
    {
        try
        {
            // 定义ClientB接口
            int portB = 1234;
            // 定义服务端C的接口
            int portA = 2341;

            // 运行聊天程序打开窗口
            Windows window = new Windows("ClientB",portA,portB);
            window.setVisible(true);
        }
        catch(IOException e)
        {
            System.out.println("Unable to connect to the server");
        }
        catch(InterruptedException e){}
    }
}
