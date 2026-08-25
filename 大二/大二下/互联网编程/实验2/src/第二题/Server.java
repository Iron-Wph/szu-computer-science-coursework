import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.DigestInputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Formatter;
import java.util.HexFormat;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

//为客户端提供服务的线程
class ClientThread implements Runnable
{
    //输入、输出流
    DataInputStream in;
    BufferedWriter out;
    //保存通信记录的文件地址
    String path;
    //src为接受的信息源，dis为发送的信息源
    ClientThread(Socket src,String path) throws IOException {
        //根据传入的信息源，确定接受和转发对象
        this.path = path;
        out = new BufferedWriter(new FileWriter(path));
        in = new DataInputStream(src.getInputStream());
    }
    public void run()
    {
        // 逐步监听信息
        while(true)
        {
            try {
                // 如果有信息则接收，避免堵塞
                if(in.available()>0)
                {
                    //接受客户端发送的信息
                    String respon = in.readUTF();

                    if(respon.equals("bye"))
                    {
                        // 调用计算函数
                        Server.calcute(path);
                        //关闭输入输出流
                        in.close();
                        out.close();
                        break;
                    }
                    else
                    {
                        //向通信记录文件写入客户端发送的信息
                        out.write(respon + "\n");
                        out.flush();
                    }
                    //线程休眠
                    Thread.sleep(100);
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } catch (NoSuchAlgorithmException e) {
                throw new RuntimeException(e);
            }
        }
    }
}


public class Server
{
    // 保存通信信息的文件
    public static String filename = "SafeAbstract.txt";
    public static BufferedWriter cal;
    public static void main(String args[]) throws IOException {
        cal = new BufferedWriter(new FileWriter(filename));
        try
        {
            //创建服务器的套接字
            ServerSocket server = new ServerSocket(4333);
            // 创建线程池
            ExecutorService pool = Executors.newFixedThreadPool(10);
            // 与客户端通信的文件
            int i = 0;  // 用于文件名的编号
            // 循环监听客户端的连接
            while(true)
            {
                // 接收客户端的套接字
                Socket ClientSocket = server.accept();
                // 当客户端都加入服务器时，创建线程
                if(ClientSocket!=null)
                {
                    System.out.println(ClientSocket);
                    i++;
                    // 与客户端通信的文件
                    String path = "第" + i + "个通信记录.txt";
                    System.out.println("客户端成功连接");
                    // 为每个客户端创建线程
                    ClientThread client = new ClientThread(ClientSocket, path);
                    // 执行客户端线程
                    pool.execute(client);
                }
            }
        }
        catch(IOException e)
        {
            System.out.println(""+e);
        }
    }

    public static  synchronized void calcute(String path) throws IOException, NoSuchAlgorithmException {
        FileInputStream in = new FileInputStream(path);
        // 初始化安全摘要对象
        MessageDigest sha = MessageDigest.getInstance("SHA-256");
        DigestInputStream din = new DigestInputStream(in, sha);
        // 读取文件获取安全摘要
        while(din.read()!=-1) {}
        din.close();
        byte []digest = sha.digest();
        // 写入文件信息和安全摘要
        cal.write(path + " ");
        // 将摘要转换为16进制字符串
        Formatter formatter = new Formatter();
        for(byte b:digest)
        {
            formatter.format("%02x", b);
        }
        cal.write(formatter + "\n");
        cal.flush();
    }
}
