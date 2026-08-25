import java.net.*;
import java.io.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
class ClientThread implements Runnable{
    Socket ClientSocket;
    // 输入输出流
    BufferedWriter Write;
    BufferedReader Read;
    // cookie
    static String cookies = "user_id=Nuoya; port=4333";
    public ClientThread(Socket src) throws IOException {
        this.ClientSocket = src;
        Write = new BufferedWriter(new OutputStreamWriter(src.getOutputStream()));
        Read = new BufferedReader(new InputStreamReader(src.getInputStream()));
    }
    public void run()
    {
        while(true)
        {
            try {
                // 获取客户端的请求
                String quest = Read.readLine();
                System.out.println(quest);
                // 处理cookie
                if(quest.indexOf("user_id")!=-1)
                {
                    String user = quest.substring(quest.indexOf("user_id")+1,quest.indexOf(";"));
                    cookies = cookies.substring(0, 8) + user + cookies.substring(cookies.indexOf(";"));
                }
                if(quest.indexOf("port")!=-1)
                {
                    String port = quest.substring(quest.indexOf("port")+1,quest.indexOf(";"));
                    cookies = cookies.substring(0, quest.indexOf("port")+1) + port;
                }

                // 处理客户端的请求
                // 处理GET请求
                if(quest.indexOf("GET")!=-1)
                {
                    handleGET(quest);
                }
                // 处理HEAD请求
                else if(quest.indexOf("HEAD")!=-1)
                {
                    handleHEAD();
                }
                // 处理POST请求
                else if(quest.indexOf("POST")!=-1)
                {
                    handlePOST();
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
    // 处理GET请求
    public void handleGET(String path) throws IOException {
        // 发送响应
        String response = "HTTP/1.0 200 OK\r\n" +
                "Content-Type: text/html\n";
        Write.write(response);
        // 发送cookie
        Write.write(cookies);
        Write.write("Finish!");
        Write.flush();
        // 切片操作获取文件名字
        String loc = path.split(" ")[1];
        loc = loc.substring(loc.lastIndexOf("/")+1);
        // 读取文件响应给客户端
        path = "D:\\作业\\互联网编程\\实验4\\Srcpool\\data\\" + loc;
        try {
            // 访问文件的逻辑
            FileInputStream fin = new FileInputStream(path);
            OutputStream fout = ClientSocket.getOutputStream();
            int one;
            while((one = fin.read())!=-1)
            {
                fout.write(one);
            }
            // 发送终止指令
            fout.write("Finish!".getBytes());
            fout.flush();
            fin.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace(); // 输出详细的堆栈信息
            System.out.println("无法访问文件: " + e.getMessage());
        }
    }

    // 处理HEAD请求
    public void handleHEAD() throws IOException {
        //发送响应
        String response = "HTTP/1.0 200 OK\r\n" +
                "Content-Type: text/html\n";
        Write.write(response);
        Write.write(cookies);
        Write.write("Finish!");
        Write.flush();
        //
        System.out.println(response);
    }
    // 处理POST请求
    public void handlePOST() throws IOException {
        String response = "HTTP/1.0 200 OK\n";
        Write.write(response);
        Write.write(cookies);
        Write.write("Finish!");
        Write.flush();
        //
        System.out.println(response);
    }
}

public class Server{
    public static void main(String []args) throws IOException {
        // 服务器的socket，设置端口号为4333，最大请求队列为10000
        ServerSocket server = new ServerSocket(4333, 10000);
        // 客户端线程池
        ExecutorService pool = Executors.newFixedThreadPool(100);

        // 持续监听客户端的连接
        while(true)
        {
            // 接收客户端的Socket
            Socket ClientSocket = server.accept();
            if(ClientSocket!=null)
            {
                try
                {
                    // 创建服务客户端的对象
                    ClientThread Client = new ClientThread(ClientSocket);
                    // 执行客户端线程
                    pool.execute(Client);
                    System.out.println("connect");
                }
                catch(IOException e)
                {
                    e.printStackTrace();
                }
            }
        }
    }
}
