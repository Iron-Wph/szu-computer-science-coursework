#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <queue>
#include <chrono>
#define inf 4000000
using namespace std;
vector<string> files{ "smallG.txt", "mediumG.txt", "largeG.txt" };
int points = inf, edges;
// vector<bool>visit(points, false);       // visit数组
bool visit[inf];
bool tree[inf];             // 标记是否为环边
int parent[inf];
int depth[inf];
class edge
{
public:
    int begin;
    int end;
    edge(int tb = -1, int te = -1) :begin(tb), end(te) {}
};

// int graph[inf][100];      // 存储图的邻接关系
vector<vector<int>>graph;

// 边集合
vector<edge>E_set;
// 基准法优化
bool BFS_opt(int b, int e)
{
    for (int i = 0; i < points; i++)
        visit[i] = false;
    // BFS过程
    queue<int>q;
    visit[b] = true;
    q.push(b);
    while (!q.empty())
    {
        int u = q.front();
        q.pop();
        // 遍历邻接点
        for (int j : graph[u])
        {
            if (!visit[j])
            {
                // 如果遍历到终点
                if (j == e)
                {
                    return false;
                }
                visit[j] = true;
                q.push(j);
            }
        }
    }
    return true;
}

int qiao_opt()
{
    // 获取图初始的连通分支数目
    int count = BFS();
    std::cout << "连通分数为：" << count << endl;
    // 桥的个数
    int bridge = 0;
    // 遍历所有边
    for (int i = 0; i < E_set.size(); i++)
    {
        int tb = E_set[i].begin, te = E_set[i].end;
        // delete the edge
        graph[tb].erase(std::remove(graph[tb].begin(), graph[tb].end(), te), graph[tb].end()); // 删除所有值为 3 的元素
        graph[te].erase(std::remove(graph[te].begin(), graph[te].end(), tb), graph[te].end());
        // count the bridge
        if (BFS_opt(tb, te))
            bridge++;
        // add the edge
        graph[tb].push_back(te);
        graph[te].push_back(tb);
    }
    return bridge;
}

int main()
{

    string path = "D:\\作业\\算法设计与分析\\实验5\\" + files[2];
    int n = 1500;
    // string path = "D:\\作业\\算法设计与分析\\实验5\\random\\p" + to_string(n) + "e" + to_string(n*n) + ".txt";
    // string path = "D:\\作业\\算法设计与分析\\实验5\\random_point_cm" + to_string(100) + ".txt";
    // 打开文件
    ifstream file(path);
    if (!file.is_open())
    {
        cerr << "文件打开失败" << endl;
        return 1;
    }
    else
    {
        std::cout << "成功打开文件：" << path << endl;
    }

    std::string line;
    // 读取顶点个数和边数
    getline(file, line);
    istringstream iss(line);
    iss >> points;
    getline(file, line);
    iss >> edges;

    graph.resize(points);

    // 读取边集
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int pa, pb;
        iss >> pa; iss >> pb;
        // 加入邻接关系
        graph[pa].push_back(pb);
        graph[pb].push_back(pa);

        // 记录边集合
        edge t(pa, pb);
        E_set.push_back(t);             
    }
    // 执行算法
    auto start = chrono::steady_clock::now();
    cout << "桥的个数为：" << qiao()_opt << endl;
    auto end = chrono::steady_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

    std::cout << duration.count() << "ms\n";
    return 0;
}

