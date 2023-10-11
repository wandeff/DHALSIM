import sys
import networkx as nx
import matplotlib.pyplot as plt


def draw_topology(topo):
    G = nx.MultiGraph()  # 使用MultiGraph来支持多重边

    # 从传递进来的拓扑对象中获取节点和边信息
    nodes = topo.g.nodes()
    edges = topo.g.edges()

    # 添加节点和边到NetworkX图中
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # 绘制网络拓扑图
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500, font_size=20, font_weight='bold')
    print(G.edges)
    plt.show()


if __name__ == "__main__":
    # 获取传递进来的拓扑数据
    topo_data = sys.argv[1]

    # 在这里解析拓扑数据（如果需要的话）

    # 调用绘制拓扑图的函数
    draw_topology(topo_data)
