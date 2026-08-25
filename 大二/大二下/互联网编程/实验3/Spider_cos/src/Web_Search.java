import java.io.*;
import java.net.*;
import java.util.Scanner;
public class Web_Search {
    public static void main(String []args) throws IOException {
        BufferedWriter fw = new BufferedWriter(new FileWriter("productResult.html"));
        // 读取输入的搜索词
        Scanner read = new Scanner(System.in);
        while(read.hasNext())
        {
            String key = read.next();   // 待搜索的关键词
            try {
                // 拼接搜索URL链接
                URL u = new URL("https://search.dangdang.com/?key=" +key);
                System.out.println(u.toString());
                // 创建http连接对象，设置请求方式为get
                HttpURLConnection uc = (HttpURLConnection) u.openConnection();
                uc.setRequestMethod("GET");
                InputStream in = uc.getInputStream();
                // 创建网页内容读取对象
                in = new BufferedInputStream(in);
                Reader r = new InputStreamReader(in);
                int c;
                while((c = r.read()) != -1) {
                    System.out.print((char) c);
                    // 写入文件中
                    fw.write(c);
                    fw.flush();
                }
            } catch (MalformedURLException e) {
                throw new RuntimeException(e);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
