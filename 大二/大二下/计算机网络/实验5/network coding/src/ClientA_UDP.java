import java.io.*;
public class ClientA_UDP
{
    public static void main(String args[])
    {
        try
        {
            // 定义ClientA接口
            int portA = 1234;
            // 定义服务端C的接口
            int portB = 2341;


            // 运行聊天程序打开窗口
            Windows window = new Windows("ClientA",portA,portB);
            window.setVisible(true);

        }
        catch(IOException e)
        {
            System.out.println("Unable to connect to the server");
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
