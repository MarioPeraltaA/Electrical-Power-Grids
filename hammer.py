"""Load a toy network.

Playing around with graph theory algorithms.

For feedback: Mario.Peralta@ieee.org
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def load_grid(json_file: str) -> dict:
    """Read json dataset.

    Parameters
    ----------
    json_file : str
        Path of the .json file.
    """
    # Load json file of the network
    with open(json_file, "r") as graph:
        data = json.load(graph)

    nodes_dict = {}
    edges_dict = {}
    # Make sure keys of nodes are integers
    for node_num, attrs in data["Nodes"].items():
        nodes_dict[int(node_num)] = attrs
    # Convert string keys back to tuple keys of integers
    for str_ends, attrs in data["Edges"].items():
        tuple_ends = eval(str_ends)
        node_from = int(tuple_ends[0])
        node_to = int(tuple_ends[1])
        edges_dict[(node_from, node_to)] = attrs

    grid = {
        "Nodes": nodes_dict,
        "Edges": edges_dict
    }
    return grid


def set_network(grid: dict) -> tuple[list]:
    """Chew grid data in order to build up a MultiGraph.

    Patameters
    ----------
    grid : dict
        Electrical grid database.

    Returns
    -------
    nodes, edges : tuple[list]
        Tuple with lists of nodes and edges.
    """
    nodes_list = [(node_num, attrs)
                  for node_num, attrs in grid["Nodes"].items()]
    edges_list = [(ends[0], ends[1], attrs)
                  for ends, attrs in grid["Edges"].items()]

    return (nodes_list, edges_list)


def build_network(nodes: list, edges: list) -> nx.Graph:
    """Built up a MultiGraph object out of list of nodes and edges.

    Parameters
    ----------
    nodes : list
        list of vertices. It must not be empty.
    edges : list
        list of edges. May be empty. The notation
        for self-loops must be (v, v).

    Returns
    -------
    network : MultiGraph
        Electrical grid as
        :py:class:`networkx.classes.graph.MultiGraph`
        object.
    """
    # Create a network (MultiGraph)
    network = nx.Graph()

    # Add vertices
    network.add_nodes_from(nodes)

    # Add edges
    network.add_edges_from(edges)

    return network


def adj_matrix() -> np.ndarray:
    """Return adjacency matrix."""
    pass


def adjacency_dict(graph: dict) -> dict:
    """Return the adjacency list representation of the graph."""
    adj = {node: [] for node in graph["Nodes"]}

    for edge in graph["Edges"]:
        node1, node2 = edge[0], edge[1]
        adj[node1].append(node2)
        adj[node2].append(node1)
    return adj


def union(self: list, other: list) -> list:
    """Operate union operator between lists."""
    _ = [self.append(i) for i in other if i not in self]
    return self


def is_connected(
        grid_data: dict, root: int = 14319
) -> list:
    """Identify components in the network.

    Verify if there is a path between every pair of vertices
    i.e A graph is connected if and only if it has
    exactly one connected component.

    Patameters
    ----------
    grid_data : dict
        Electrical grid database.

    root : int
        First vertex.

    Returns
    -------
    cloud : list
        A Cloud defines a collection of vertices of another
        or other different components. i.e. Remaining
        vertices that were not traversed. If empty means
        there is only one component, the network itself, hence
        the network is connected.
    """
    path_track = []
    path_track.append(root)
    adj_dict = adjacency_dict(grid_data)
    for vertex in path_track:
        adj_vertices = adj_dict[vertex]
        union(path_track, adj_vertices)

    cloud = []
    if len(path_track) != len(adj_dict):
        for v in adj_dict:
            if v not in path_track:
                cloud.append(v)

    return cloud


def run_connectedness() -> list:
    """Run test."""
    grid_data = load_grid("../data/network.json")
    components = is_connected(grid_data, root=14319)
    return components


def split_cloud():
    """Break cloud down into components."""
    pass


def leaves():
    """Verify loads has only one conductor connected.

    See loads as leaves of a tree kind of graph.
    """
    pass


def get_clusters():
    """Retrive sub trees for each root."""
    pass


def shortest_path():
    """Get distance of a Tree. It considers weighted edges."""
    pass


def get_cycles(
        grid_data: dict, root: int = 14319
) -> list[list]:
    """Find and eeturn list of cycles basis.

    Let a "ring" be a kind of cycle basis that has the root.
    """
    spanning_tree: list[tuple] = []   # list of (parent, child)
    spanning_tree.append((-1, root))
    adj_dict = adjacency_dict(grid_data)
    visited: list = [root]
    odd_edges: list = []
    cycles: list[list] = []
    for parent, actual in spanning_tree:
        goes_to = adj_dict[actual]
        for child in goes_to:
            # One solely parent
            if (child, actual) in spanning_tree:
                continue
            # End point already visited
            if child in visited:
                if (child, actual) in odd_edges:
                    continue
                odd_edges.append((actual, child))
                continue
            visited.append(child)
            spanning_tree.append((actual, child))

    spanning_dict = {child: parent for (parent, child) in spanning_tree}
    for u, v in odd_edges:
        cycle = [u]
        u_parent = spanning_dict[u]
        comming_from = -1
        ring = False
        while u_parent != comming_from and not ring:
            comming_from = v
            v = spanning_dict[comming_from]
            cycle.append(comming_from)
            # All the way back to the root type of cycle
            if comming_from == root:
                ring = True

        # The other half
        if ring:
            half_cycle = []
            while u_parent not in cycle:
                half_cycle.append(u_parent)
                u_parent = spanning_dict[u_parent]
            cycle += half_cycle
        cycles.append(cycle)

    return spanning_tree, cycles


def main():
    """Load and Visualize network."""
    grid_data = load_grid("../data/network.json")
    network_data = set_network(grid_data)
    network = build_network(*network_data)

    # Draw the graph
    nx.draw(
        network,
        pos=nx.spring_layout(network),
        node_size=10,
        width=0.5,
        with_labels=True,
        font_size=2
    )
    # Display the graph
    plt.title('Electrical Network')
    plt.savefig("graph.pdf")
    plt.show()


def run_cycle() -> tuple[list]:
    """Run test of cycles basis."""
    grid_data = load_grid("../data/network.json")
    spanning_tree, cycles = get_cycles(grid_data, root=14319)
    return spanning_tree, cycles


if __name__ == "__main__":
    components = run_connectedness()
    spanning_tree, cycles = run_cycle()
