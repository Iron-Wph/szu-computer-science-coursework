import java.io.*;
import java.net.*;
public class Web {
    public static void donwload(String url) throws IOException {
        BufferedWriter writer = new BufferedWriter(new FileWriter("web.html"));
        try
        {
            URL u = new URL(url);
            URLConnection uc = u.openConnection();
            InputStream in = uc.getInputStream();
            //InputStream in = u.openStream();
            in = new BufferedInputStream(in);
            Reader r = new InputStreamReader(in);
            int c;
            while((c = r.read()) != -1) {
                System.out.print((char) c);
                writer.write(c);
                writer.flush();
            }
            System.out.println(u.getProtocol());
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
