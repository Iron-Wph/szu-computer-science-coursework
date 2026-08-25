import java.io.*;
import java.net.Socket;
//控制发送信息的线程
class Output extends Thread
{
    DataOutputStream out = null;
    String path;    //文件路径
    Output(Socket tem,String path) throws IOException {
        //构建发送信息的输出流
        out = new DataOutputStream(tem.getOutputStream());
        this.path = path;
    }
    @Override
    public void run()
    {
        try {
            // 创建文件读取流对象
            BufferedReader br = new BufferedReader(new FileReader(path));
            String message;
            //
            System.out.println("要传输的文件为:" + this.path + "\n开始传输文件");
            out.writeUTF(this.path);
            //持续监听是否有信息需要发送
            while((message=br.readLine())!=null)
            {
                //如果有文件内容输入就转发，避免堵塞
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
            System.out.println("文件传输结束");
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}