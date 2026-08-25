import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.net.Socket;
//控制接受信息的线程
class Input extends Thread
{
    DataInputStream in;
    // 传入接收端的套接字
    Input(Socket tem) throws IOException {
        // 根据要接受对象的套接字，初始化输入流
        in = new DataInputStream(tem.getInputStream());
    }
    @Override
    public void run()
    {
        // 是否为第一条消息
        boolean first = true;
        // 写入文件流
        BufferedWriter bw = null;
        //持续监听接收端转发的信息
        while(true)
        {
            //如果有信息则接收，避免堵塞
            try
            {
                if(in.available()>0)
                {
                    //接受、显示的信息
                    String respon = in.readUTF();
                    //线程休眠
                    Thread.sleep(100);

                    // 写入文件
                    if(first)
                    {
                        System.out.println("接收到的文件为：" + respon);

                        // 根据文件路径创建文件输出流对象
                        int index = respon.indexOf(".");
                        // 在文件名后加_new
                        respon = respon.substring(0, index) + "_new" + respon.substring(index);
                        bw = new BufferedWriter(new FileWriter(respon));

                        //
                        System.out.println("保存为：" + respon);

                    }
                    else
                    {
                        bw.write(respon);
                        bw.newLine();
                        bw.flush();
                    }
                    first = false;
                }
            }
            catch (IOException e)
            {
                throw new RuntimeException(e);
            } catch (InterruptedException e)
            {
                throw new RuntimeException(e);
            }
        }
    }
}