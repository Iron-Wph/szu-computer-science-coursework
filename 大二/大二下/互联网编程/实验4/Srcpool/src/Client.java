import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.sql.SQLOutput;
import java.util.Scanner;

public class Client {
    // 套接字
    static Socket SocketAtServer;
    // 输入输出流
    static BufferedWriter out;
    static DataInputStream in;
    // 发送GET请求，传入请求的路径
    public static void sendGET(String path) throws IOException {
        // 发送请求
        String request = "GET /index.html/" + path + " HTTP/1.0\r\n" +
                "Host: localhost:4333\r\n" +
                "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0\r\n" +
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n" +
                "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\r\n" +
                "Accept-Encoding: gzip, deflate, br, zstd\r\n" +
                "Connection: keep-alive\r\n";
        out.write(request);
        out.write("Finish!");
        out.flush();

        // 接受服务器的响应
        getResponse();

        // 保存图片或文本到本地
        FileOutputStream filew = new FileOutputStream("D:\\作业\\互联网编程\\实验4\\Srcpool\\Client\\"+path);
        byte []data = new byte[1024*1024];
        int len = -1;
        while ((len = in.read(data)) != -1) {
            String output = new String(data, 0, len, StandardCharsets.UTF_8);
            if(output.indexOf("Finish!")!=-1)
            {
                break;
            }
            filew.write(data,0, len);
        }
        filew.close();
        System.out.println("文件：" + path + "下载成功");
    }
    // 发送HEAD请求
    public static void sendHEAD() throws IOException {
        // 发送请求
        String request = "HEAD /index.html HTTP/1.0\r\n" +
                "Host: localhost:4333\r\n" +
                "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0\r\n" +
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n" +
                "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\r\n" +
                "Accept-Encoding: gzip, deflate, br, zstd\r\n" +
                "Connection: keep-alive\r\n";
        out.write(request);
        out.flush();
        // 接受服务器的响应
        getResponse();
    }
    // 发送POST请求
    public static void sendPOST() throws IOException {
        //发送POST请求
        String request = "POST /index.html HTTP/1.0\r\n" +
                "Host: localhost:4333\r\n" +
                "Content-Type: application/json\r\n" +
                "{\n" +
                "  \"name\": \"WangPeiHong\",\n" +
                "  \"email\": \"2022152021@email.szu.edu.cn\",\n" +
                "  \"age\": 20\n" +
                "}\r\n";
        out.write(request);
        out.flush();
        //接受服务器响应，并打印在控制台
        getResponse();
    }
    // 接受服务器的回应
    public static void getResponse() throws IOException {
        //接受服务器响应，并打印在控制台
        byte []data = new byte[1024*1024];
        int len = -1;
        while ((len = in.read(data)) != -1) {
            String output = new String(data, 0, len, StandardCharsets.UTF_8);
            // 退出条件
            if(output.indexOf("Finish!")!=-1)
            {
                output = output.replace("Finish!","");
                System.out.println(output);
                break;
            }
        }
        //
        // System.out.println("break");
    }
    //
    public static void main(String []args) throws IOException {
        // 获取与服务器连接的套接字
        SocketAtServer = new Socket("localhost", 4333);
        // 输入输出流
        out = new BufferedWriter(new OutputStreamWriter(SocketAtServer.getOutputStream()));
        in = new DataInputStream(SocketAtServer.getInputStream());
        //
        Scanner read = new Scanner(System.in);
        String line;
        while(true)
        {
            line = read.nextLine();
            System.out.println(line);
            if(line.equals("quit"))
            {
                break;
            }
            // 发送GET请求
            else if(line.indexOf("GET")!=-1)
            {
                // 获取请求文件
                String path = line.split(" ")[1];
                sendGET(path);
            }
            // 发送HEAD请求
            else if(line.equals("HEAD"))
            {
                sendHEAD();
            }
            // 发送POST请求
            else if(line.equals("POST"))
            {
                sendPOST();
            }
        }
    }
}
