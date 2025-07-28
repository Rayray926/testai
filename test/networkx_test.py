import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

# 创建无向空图对象
G=nx.Graph()

# 添加节点
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)

# 有向图
H=nx.DiGraph(G)

plt.figure(figsize=(12,6)) #绘制窗口大小
#子图位置:1->1行2->2列1->第一个于图的位置 第一行第一列
plt.subplot(121)
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=15, font_weight='bold', edge_color='gray')
plt.title("无向图")

# 绘制有向图 H
plt.subplot(122)
nx.draw(H, with_labels=True, node_color='lightgreen', node_size=500, font_size=15, font_weight='bold',
        edge_color='gray', arrowsize=20)
plt.title("有向图")
# 显示绘图
plt.show()