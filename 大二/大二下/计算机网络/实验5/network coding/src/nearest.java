import java.io.*;
import java.util.*;
class Point
{
    double x;
    double y;
    Point(double x, double y)
    {
        this.x = x;
        this.y = y;
    }
};

public class nearest {
    static void calculateDistance(List<Point>point_set) {
        double minDis = Double.MIN_VALUE;
        for (int i = 0; i < point_set.size() - 1; i++) {
            for (int j = i + 1; j < point_set.size(); j++) {
                Point pa = point_set.get(i);
                Point pb = point_set.get(j);
                double dis = Math.sqrt(Math.pow(pa.x - pb.x, 2) + Math.pow(pa.y - pb.y, 2));
                if (dis < minDis) {
                    minDis = dis;
                }
            }
        }
        //System.out.println("mindis:"+minDis);
    }

    public static void main(String args[]) throws IOException {
        String disfile = "dis.txt";
        try(BufferedWriter dis = new BufferedWriter(new FileWriter(disfile)))
        {
            for(int i = 7; i <= 10; i++)
            {
                //
                String men = Integer.toString(i)+"0w规模\n";
                dis.write(men);
                int con = 1;
                if(i == 7)
                    con = 7;
                
                //
                for(int j = con; j <= 10; j++)
                {
                    String path = "D:/作业/算法设计与分析/实验2/random_point/random_point"+Integer.toString(i)+"0w "+Integer.toString(j)+".txt";
                    BufferedReader file = new BufferedReader(new FileReader(path));
                    System.out.println("成功打开文件 " + path);

                    // 读取点的数据
                    List<Point> pointSet = new ArrayList<>();
                    String line;
                    while ((line = file.readLine()) != null) {
                        String[] parts = line.split("\\s+"); // 假设点坐标之间由空白字符分隔
                        double x = Double.parseDouble(parts[0]);
                        double y = Double.parseDouble(parts[1]);
                        // 压入点坐标
                        Point point = new Point(x, y);
                        pointSet.add(point);
                    }
                    // 计算运行时间
                    long startTime = System.currentTimeMillis();

                    calculateDistance(pointSet);

                    long endTime = System.currentTimeMillis();
                    long totalTime = endTime - startTime;
                    System.out.println("程序运行时间: " + totalTime + "毫秒");
                    dis.write(totalTime+"\n");
                    dis.flush();    //及时写入
                }
            }
        }
    }
}



