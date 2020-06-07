import sys

sys.path.append("../vrpy/")
sys.path.append("../")
from vrpy.main import VehicleRoutingProblem
from cspy import BiDirectional
from numpy import array

if __name__ == "__main__":
    import networkx as nx

    """
    G = nx.DiGraph()
    G.add_edge("Source", 1, weight=12, res_cost=array([1, 10]))
    G.add_edge(1, 2, weight=0, res_cost=array([1, 0]))
    G.add_edge(2, "Sink", weight=-12, res_cost=array([1, 0]))
    G.graph["n_res"] = 2
    min_res = [0, 0]
    max_res = [3, 35]
    alg = BiDirectional(
        G,
        max_res,
        min_res,
        direction="both",
        REF=None,  # self.get_REF(),
        method="generated",
    )
    alg.run()
    print(alg.path)
    """
    G = nx.DiGraph(directed=True, n_res=2)
    G.add_edge("Source", "A", res_cost=array([1, 2]), weight=0)
    G.add_edge("A", "B", res_cost=array([1, 0.3]), weight=0)
    G.add_edge("A", "C", res_cost=array([1, 0.1]), weight=0)
    G.add_edge("B", "C", res_cost=array([1, 3]), weight=-10)
    # G.add_edge("B", "Sink", res_cost=array([1, 2]), weight=10)
    G.add_edge("A", "Sink", res_cost=array([1, 10]), weight=0)
    max_res, min_res = [4, 20], [1, 0]
    bidirec = BiDirectional(G, max_res, min_res, direction="both")
    bidirec.run()
    print(bidirec.path)
