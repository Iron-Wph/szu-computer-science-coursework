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

int graph[inf][100];      // 存储图的邻接关系
//vector<vector<int>>graph;

// 边集合
vector<edge>E_set;

void find_lca(int u, int v)
{
    // 记录起始点
    int tu = u, tv = v;
    // 如果有重边直接结束
    if (parent[u] == v || parent[v] == u)
        return;
    // 寻找共同祖先
    while (u != v)
    {
        // 每次只移动一个节点
        if (depth[u] < depth[v])
        {
            int t = parent[v];
            // 加入环边
            tree[v] = false;
            v = t;
        }
        else if (depth[u] > depth[v])
        {
            int t = parent[u];
            // 加入环边
            tree[u] = false;
            u = t;
        }
        // 当高度一致时，同时移动
        else
        {
            int du = parent[u];
            int dv = parent[v];
            // 加入环边
            tree[u] = false;
            tree[v] = false;
            u = du;
            v = dv;
        }
    }
    // 压缩路径
    while (tu != u)
    {
        // 得到父节点
        int t = parent[tu];
        // 指向祖先节点
        parent[tu] = u;
        // 深度也要更新
        depth[tu] = depth[u] + 1;
        // 继续往上操作
        tu = t;
    }
    while (tv != v)
    {
        // 得到父节点
        int t = parent[tv];
        // 指向祖先节点
        parent[tv] = v;
        // 深度也要更新
        depth[tv] = depth[v] + 1;
        // 继续往上操作
        tv = t;
    }
}

int BFS_lca()
{
    for (int i = 0; i < points; i++)
    {
        visit[i] = false;
        depth[i] = 0;
        tree[i] = false;
    }

    int count = 0;
    for (int i = 0; i < points; i++)
    {
        if (!visit[i])
        {
            // BFS过程
            queue<int>q;
            visit[i] = true;
            depth[i] = 0;
            q.push(i);
            while (!q.empty())
            {
                int u = q.front();
                q.pop();
                int d = depth[u];
                // 遍历邻接点
                for (int j = 1; j <= graph[u][0]; j++)
                {
                    int t = graph[u][j];
                    if (!visit[t])
                    {
                        // 记录祖先节点
                        parent[t] = u;
                        depth[t] = d + 1;
                        visit[t] = true;
                        tree[t] = true;
                        q.push(t);
                    }
                }
            }
            // 
            count++;
        }
    }
    std::cout << "连通分支数：" << count << endl;
    return count;
}

int LCA()
{
    // 初始化每个结点的前驱为自身
    for (int i = 0; i < points; i++)
        parent[i] = i;
    // BFS生成树
    int count = BFS_lca();

    // 遍历所有边
    for (auto& elem : E_set)
    {
        // 环操作
        if (parent[elem.begin] != elem.end && parent[elem.end] != elem.begin)
        {
            find_lca(elem.begin, elem.end);
        }
    }

    // 统计桥的数目
    int bridge = 0;
    for (int i = 0; i < points; i++)
    {
        if (tree[i])
            bridge++;
    }
    return bridge;
}

//// 通过层次遍历计算图的连通分支数目
//int BFS()
//{
//    for (int i = 0; i < points; i++)
//        visit[i] = false;
//    int count = 0;
//    for (int i = 0; i < points; i++)
//    {
//        if (!visit[i])
//        {
//            // BFS过程
//            queue<int>q;
//            visit[i] = true;
//            q.push(i);
//            while (!q.empty())
//            {
//                int u = q.front();
//                q.pop();
//                // 遍历邻接点
//                for (int j : graph[u])
//                {
//                    if (!visit[j])
//                    {
//                        visit[j] = true;
//                        q.push(j);
//                    }
//                }
//            }
//            // 
//            count++;
//        }
//    }
//    return count;
//}
//
//int qiao()
//{
//    // 获取图初始的连通分支数目
//    int count = BFS();
//    std::cout << "连通分数为：" << count << endl;
//    // 桥的个数
//    int bridge = 0;
//    // 遍历所有边
//    for (int i = 0; i < E_set.size(); i++)
//    {
//        int tb = E_set[i].begin, te = E_set[i].end;
//        // delete the edge
//        graph[tb].erase(std::remove(graph[tb].begin(), graph[tb].end(), te), graph[tb].end()); // 删除所有值为 3 的元素
//        graph[te].erase(std::remove(graph[te].begin(), graph[te].end(), tb), graph[te].end());
//        // count the bridge
//        if (BFS() > count)
//            bridge++;
//        // add the edge
//        graph[tb].push_back(te);
//        graph[te].push_back(tb);
//    }
//    return bridge;
//}
//
//// 基准法优化
//bool BFS_opt(int b, int e)
//{
//    for (int i = 0; i < points; i++)
//        visit[i] = false;
//    // BFS过程
//    queue<int>q;
//    visit[b] = true;
//    q.push(b);
//    while (!q.empty())
//    {
//        int u = q.front();
//        q.pop();
//        // 遍历邻接点
//        for (int j : graph[u])
//        {
//            if (!visit[j])
//            {
//                // 如果遍历到终点
//                if (j == e)
//                {
//                    return false;
//                }
//                visit[j] = true;
//                q.push(j);
//            }
//        }
//    }
//    return true;
//}
//
//int qiao_opt()
//{
//    // 获取图初始的连通分支数目
//    int count = BFS();
//    std::cout << "连通分数为：" << count << endl;
//    // 桥的个数
//    int bridge = 0;
//    // 遍历所有边
//    for (int i = 0; i < E_set.size(); i++)
//    {
//        int tb = E_set[i].begin, te = E_set[i].end;
//        // delete the edge
//        graph[tb].erase(std::remove(graph[tb].begin(), graph[tb].end(), te), graph[tb].end()); // 删除所有值为 3 的元素
//        graph[te].erase(std::remove(graph[te].begin(), graph[te].end(), tb), graph[te].end());
//        // count the bridge
//        if (BFS_opt(tb, te))
//            bridge++;
//        // add the edge
//        graph[tb].push_back(te);
//        graph[te].push_back(tb);
//    }
//    return bridge;
//}

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

    //graph.resize(points);

    for (int i = 0; i < points; i++)
        graph[i][0] = 0;
    // 读取边集
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int pa, pb;
        iss >> pa; iss >> pb;
        // 加入邻接关系
        graph[pa][++graph[pa][0]] = pb;
        graph[pb][++graph[pb][0]] = pa;
        //graph[pa].push_back(pb);
        //graph[pb].push_back(pa);

        // 记录边集合
        edge t(pa, pb);
        E_set.push_back(t);             
    }
    // 执行算法
    auto start = chrono::steady_clock::now();
    // cout << "桥的个数为：" << qiao() << endl;
    std::cout << "桥的个数为：" << LCA() << endl;
    auto end = chrono::steady_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

    std::cout << duration.count() << "ms\n";
    return 0;
}

