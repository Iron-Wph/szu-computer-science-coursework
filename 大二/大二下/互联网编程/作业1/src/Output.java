import java.io.*;
import java.net.Socket;
//控制发送信息的线程
class Output extends Thread
{
    DataOutputStream out = null;
    // 读取的文件路径
    String path;
    Output(Socket tem,String path) throws IOException {
        //构建发送信息的输出流
        out = new DataOutputStream(tem.getOutputStream());
        this.path = path;
    }
    @Override
    public void run()
    {
        // 创建文件的输入流对象
        try {
            BufferedReader br = new BufferedReader(new FileReader(this.path));
            //持续监听是否有信息需要发送
            String message;
            while((message = br.readLine())!=null)
            {
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
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}