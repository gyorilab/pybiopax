import networkx
from .biopax import BioPaxModel, BioPaxObject


def model_to_networkx(model: BioPaxModel):
    g = networkx.DiGraph()
    nodes = []
    edges = []
    for uid, obj in model.objects.items():
        for attr in [a for a in dir(obj) if not a.startswith('_')
                     and a not in {'list_types', 'xml_types',
                                   'to_xml', 'from_xml', 'uid'}]:
            node_data = {}
            node_edges = []
            val = getattr(obj, attr)
            if val is None:
                continue
            if isinstance(val, list):
                for v in val:
                    if isinstance(v, BioPaxObject):
                        node_edges.append((uid, v.uid, {'label': attr}))
                    else:
                        if attr not in node_data:
                            node_data[attr] = [v]
                        else:
                            node_data[attr].append(v)
            else:
                if isinstance(val, BioPaxObject):
                    node_edges.append((uid, val.uid, {'label': attr}))
                else:
                    node_data[attr] = val
            nodes.append((uid, node_data))
            edges += node_edges
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g
