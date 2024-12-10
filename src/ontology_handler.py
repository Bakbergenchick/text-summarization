import networkx as nx
import os

class OntologyHandler:
    def __init__(self):
        self.output_dir = "data"
        os.makedirs(self.output_dir, exist_ok=True)

    def build_ontology(self, keywords):
        ontology_graph = nx.DiGraph()
        for keyword in keywords:
            ontology_graph.add_node(keyword)

        for i in range(len(keywords) - 1):
            ontology_graph.add_edge(keywords[i], keywords[i + 1], relation="composed_of")

        return ontology_graph

    def export_ontology_formula(self, graph):
        formula_parts = []
        for edge in graph.edges(data=True):
            source, target, relation = edge[0], edge[1], edge[2]["relation"]
            if relation == "composed_of":
                formula_parts.append(f"{source} <= *{target}")
        return " ; ".join(formula_parts)

    def save_ontology(self, graph, formula):
        nx.write_gml(graph, f"{self.output_dir}/ontology_graph.gml")
        with open(f"{self.output_dir}/ontology_formula.txt", "w") as f:
            f.write(formula)
