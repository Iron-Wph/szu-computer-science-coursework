import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
//控制接受信息的线程
class Input extends Thread
{
    DataInputStream in = null;
    String text = "";
    // 传入接收端的套接字
    Input(Socket tem,String text) throws IOException {
        // 根据要接受对象的套接字，初始化输入流
        in = new DataInputStream(tem.getInputStream());
        this.text = text;
    }
    @Override
    public void run()
    {   //持续监听接收端转发的信息
        while(true)
        {
            //如果有信息则接收，避免堵塞
            try
            {
                if(in.available()>0)
                {
                    //接受、显示的信息
                    String respon = in.readUTF();
                    System.out.println(text + ":" +respon);
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
    }
}