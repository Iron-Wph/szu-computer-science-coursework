import java.io.*;
import java.net.*;
import java.time.LocalDateTime;

public class Server
{
    public static void main(String args[])
    {   //服务器套接字
        ServerSocket server = null;
        try
        {

            //创建服务器的套接字
            server = new ServerSocket(4333);

            // 接收客户端的套接字
            Socket ClientSocket = server.accept();
            // 当客户端都加入服务器时，创建线程
            if(ClientSocket!=null)
            {
                System.out.println("客户端成功连接");

                DataInputStream in = new DataInputStream(ClientSocket.getInputStream());
                DataOutputStream out = new DataOutputStream(ClientSocket.getOutputStream());

                // 持续监听客户端信息
                while(true)
                {
                    if(in.available()>0)
                    {   // 接收客户端的请求
                        String requeset = in.readUTF();
                        System.out.println("客户端："+requeset);
                        if(requeset.equals("Time"))
                        {
                            // 获取当前日期和时间
                            LocalDateTime currentDateTime = LocalDateTime.now();
                            out.writeUTF("服务器当前时间为："+currentDateTime);
                        }
                        else if(requeset.equals("Bye"))
                        {
                            System.out.println("客户端退出");
                            // 关闭客户端套接字
                            ClientSocket.close();
                            break;
                        }
                    }
                    Thread.sleep(100);
                }
            }
        }
        catch(IOException e)
        {
            System.out.println(""+e);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
