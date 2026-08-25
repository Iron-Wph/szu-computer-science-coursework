import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.net.Socket;
//控制接受信息的线程
class Input_Client extends Thread
{
    DataInputStream in = null;
    String path;
    // 传入接收端的套接字
    Input_Client(Socket tem,String path) throws IOException {
        // 根据要接受对象的套接字，初始化输入流
        in = new DataInputStream(tem.getInputStream());
        this.path = path;
    }
    @Override
    public void run()
    {
        try {
            BufferedWriter bw = new BufferedWriter(new FileWriter(this.path));
            //持续监听接收端转发的信息
            int i = 1;
            while(true)
            {
                //如果有信息则接收，避免堵塞
                try
                {
                    if(in.available()>0)
                    {
                        //接受、显示的信息
                        String respon = in.readUTF();
                        System.out.println(respon);
                        //将服务器发来的信息改写并写入文件
                        respon = Integer.toString(i) + ":" + respon;
                        bw.write(respon + "\n");
                        bw.flush();
                        i++;
                        //线程休眠
                        Thread.sleep(100);
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
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}