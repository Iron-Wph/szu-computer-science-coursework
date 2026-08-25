import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.net.DatagramSocket;
import java.net.SocketException;
import java.time.LocalDateTime;

class Windows extends JFrame
{

    //
    volatile static boolean flag = false;
    static int portB;
    JTextArea to_send;    //文本对象
    static JTextArea talking;
    static String readmessage = "";     //显示的消息
    static String writermessage = "";   //发送的消息
    static String message = "";     //聊天信息..
    JTextField me;    //显示发送者的身份
    JButton send,exit,clear;    //按钮对象
    Box box_button,basebox; //box盒子布局
    Windows(String s,int portA, int portB) throws InterruptedException, IOException {
        //设置窗体名字，窗体初始大小
        super(s);
        setBounds(100,100,800,600);
        setVisible(true);   //显示窗体


        //
        this.portB = portB;
        DatagramSocket SocketA = new DatagramSocket(portA);
        Input_UDP in = new Input_UDP(SocketA);
        // 发送信息的线程应该传入服务端的接口portC
        Output_UDP out = new Output_UDP(portB,SocketA);


        //运行控制输入、输出的线程
        in.start();
        out.start();

//        in.join();
//        out.join();

        //

        //文本对象初始化
        to_send = new JTextArea("请输入信息",10,15);
        talking = new JTextArea(message,20,30);
        talking.setEditable(false);

        me = new JTextField(Integer.toString(portA),15);    //待修改
        me.setEditable(false);

        //设置文本框大小以及自动换行
        to_send.setPreferredSize(new Dimension(20,1));
        talking.setPreferredSize(new Dimension(50,10));
        to_send.setLineWrap(true);talking.setLineWrap(true);
        me.setPreferredSize(new Dimension(5,1));

        //滚动条设置
        JScrollPane scroll_1 = new JScrollPane(to_send);
        JScrollPane scroll_2 = new JScrollPane(talking);

        //
        //创建按钮
        //按钮初始化名称
        send = new JButton("发送");
        exit = new JButton("退出");
        clear = new JButton("清空");

        //创建一个监听器//
        ActionListener buttonListener = e -> {
            if(e.getSource()==send)
            {
                // 获取发送文本
                writermessage = to_send.getText();

                // 按下发送键位，发送信息
                Windows.flag = true;

                // 更新聊天框中发送的信息
                talking.append("时间" + LocalDateTime.now() + "\n");
                talking.append("port:" + portA + ":\n" + writermessage + "\n");
                writermessage = "";
            }
            else if(e.getSource()==exit)
            {
                // 关闭聊天框
                this.dispose();
            }
            else if(e.getSource()==clear)
            {
                // 清空当前聊天文本
                talking.setText("");
            }

        };

        //设置按钮的显示位置以及大小
        send.setBounds(100,500,50,50);
        exit.setBounds(160,500,50,50);
        clear.setBounds(220,500,50,50);

        //添加监听器
        send.addActionListener(buttonListener);
        exit.addActionListener(buttonListener);
        clear.addActionListener(buttonListener);

        //
        //
        box_button = Box.createHorizontalBox();
        box_button.add(me);         //添加发送者的身份
        box_button.add(Box.createHorizontalStrut(10));
        box_button.add(scroll_1);       //添加待发送信息文本框
        box_button.add(Box.createHorizontalStrut(10));
        //添加按钮
        box_button.add(send);
        box_button.add(Box.createHorizontalStrut(10));
        box_button.add(clear);
        box_button.add(Box.createHorizontalStrut(10));
        box_button.add(exit);

        //显示所有组件
        basebox = Box.createVerticalBox();
        basebox.add(scroll_2);
        basebox.add(Box.createVerticalStrut(10));
        basebox.add(box_button);

        //show all componets
        FlowLayout flow = new FlowLayout();
        flow.setAlignment(FlowLayout.CENTER);
        setLayout(flow);
        this.add(basebox);
        //
        validate();
        //设置关闭方式
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
    }

    // 接口回调函数，接收信息
    public static void getInputdata(String str)
    {
        LocalDateTime now = LocalDateTime.now();
        readmessage = str;
        talking.append("时间" + now + "\n");
        talking.append("port:" + portB + ":\n" + readmessage + "\n");
    }
}

