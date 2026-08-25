import java.io.*;
import java.net.Socket;
class Contact extends Thread
{
    //创建接受、发送信息的流对象
    DataOutputStream out;
    // 读取文件
    BufferedReader in;

    public Contact(Socket socketAtClient,int i) throws IOException {
        out = new DataOutputStream(socketAtClient.getOutputStream());
        in = new BufferedReader(new FileReader("D:\\作业\\互联网编程\\实验2\\contacting\\src\\src"+ i +".txt"));
    }

    public void run()
    {
        // 整行读取文件中的信息
        String line;
        while(true)
        {
            try {
                if (!((line = in.readLine()) != null)) break;
                System.out.println(line);
                out.writeUTF(line);
                Thread.sleep(1000);
            } catch (IOException | InterruptedException e) {
                throw new RuntimeException(e);
            }



        }

        // 向服务器发送终止连接信号
        try {
            out.writeUTF("bye");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

public class Client
{
    public static void main(String args[])
    {
        Socket socketAtClient;
        try
        {
            for(int i = 1; i <= 10; i++)
            {
                // 与服务器端口进行连接
                socketAtClient = new Socket("localhost", 4333);
                // 创建线程
                Contact contact = new Contact(socketAtClient, i);
                // 启动线程
                contact.start();
            }

        }
        catch(IOException e)
        {
            System.out.println("Unable to connect to the server");
        }
    }
}
