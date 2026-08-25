import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.Socket;
public class Test {
    public static void test_file()
    {
        int count=0;
        while(true){
            try{
                // 与服务器进行连接
                Client a = new Client();
                a.SocketAtServer = new Socket("localhost",4333);
                // 向服务器发送GET请求
                a.out = new BufferedWriter(new OutputStreamWriter(a.SocketAtServer.getOutputStream()));
                a.in = new DataInputStream(a.SocketAtServer.getInputStream());
                a.sendGET("Poem.txt");
                count++;
            } catch (IOException e) {
                System.out.println("Maximum capacity: "+count);
                System.exit(0);
                throw new RuntimeException(e);
            }
        }
    }
    public static void test_connect()
    {
        int count=0;
        while(true){
            try{
                // 与服务器进行连接
                new Socket("localhost",4333);
                count++;
            } catch (IOException e) {
                System.out.println("Maximum capacity: "+count);
                System.exit(0);
                throw new RuntimeException(e);
            }
        }
    }
    public static void main(String[] args) {
        // 测试最多可供多少文件提示传输
        test_file();
        // 测试最多可供多少个客户端进行连接
        test_connect();
    }
}