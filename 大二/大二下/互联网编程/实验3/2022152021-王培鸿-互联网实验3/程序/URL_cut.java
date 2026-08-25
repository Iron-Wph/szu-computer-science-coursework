import java.net.*;
public class URL_cut {
    public static void cut_down(String str)
    {
        try {
            URL u = new URL(str);
            //
            System.out.println(u);
            System.out.println("协议类型:" + u.getProtocol());
            System.out.println("用户信息：" + u.getUserInfo());
            System.out.println("权威机构：" + u.getAuthority());
            System.out.println("主机名：" + u.getHost());
            System.out.println("端口号：" + u.getPort());
            System.out.println("默认端口号：" + u.getDefaultPort());
            System.out.println("文件：" + u.getFile());
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
    }
}
