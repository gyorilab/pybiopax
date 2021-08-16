import copy
import networkx
from .biopax import BioPaxModel, BioPaxObject


def model_to_networkx(model: BioPaxModel) -> networkx.DiGraph:
    #model = copy.deepcopy(model)
    add_reverse_links(model)
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


traverse_edges = {'component', 'controlled', 'controlled_of', 'controller',
                  'entity_reference', 'entity_reference_of',
                  'left', 'member_entity_reference', 'member_physical_entity',
                  'physical_entity', 'right'}


def paths_from_to(g, source, target):
    g = g.edge_subgraph([(e[0], e[1]) for e in g.edges(data=True)
                        if e[2]['label'] in traverse_edges])
    breakpoint()
    paths = networkx.all_simple_paths(g, source, target)
    return paths


def add_reverse_links(model: BioPaxModel) -> None:
    for uid, obj in model.objects.items():
        for attr in [a for a in dir(obj) if not a.startswith('_')
                     and a not in {'list_types', 'xml_types',
                                   'to_xml', 'from_xml', 'uid'}]:
            val = getattr(obj, attr)
            if isinstance(val, BioPaxObject):
                if attr in ['left', 'right']:
                    of_attr = 'participant_of'
                else:
                    of_attr = attr + '_of'
                if of_attr in dir(val):
                    of_attr_val = getattr(val, of_attr)
                    if of_attr_val is None:
                        setattr(val, of_attr, [obj])
                    else:
                        of_attr_val.append(obj)


def draw_object(graph: networkx.DiGraph,
                obj_uid: str, fname=None):
    nodes = list(networkx.shortest_path(graph, obj_uid).keys())
    subgraph = graph.subgraph(nodes)
    ag = networkx.nx_agraph.to_agraph(subgraph)
    # Add some visual styles to the graph
    ag.node_attr['shape'] = 'plaintext'
    ag.draw(fname, prog='dot')
