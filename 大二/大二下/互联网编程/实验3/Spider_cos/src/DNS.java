import java.net.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
public class DNS {
    // 根据域名查找IP地址
    public static void DNS_find(String str) throws UnknownHostException {
        // 使用正则表达式匹配判断是否为ip地址
        String ipv4 = "\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b";
        String ipv6 = "([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}";
        Pattern pattern = Pattern.compile(ipv4 + "|" + ipv6);
        Matcher matcher = pattern.matcher(str);
        // 如果是IP地址
        if(matcher.find())
        {
            // 解析IP地址
            InetAddress address = InetAddress.getByName(str);
            // 输出域名
            System.out.println(address.getHostName());
        }
        // 如果是域名
        else
        {
            // 解析所有的IP地址
            InetAddress addresses[] = InetAddress.getAllByName(str);
            for(InetAddress address : addresses)
                System.out.println(address.getHostAddress());
        }
    }
    public static void main(String[] args) throws UnknownHostException {
        // 输入域名或IP地址
        String str = "www.17k.com";
        DNS_find(str);
        DNS_find("113.125.228.115");
    }
}
