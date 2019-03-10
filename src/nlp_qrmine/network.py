import textacy.network


class Network(object):

    def __init__(self):
        self._sents = []
        self._terms = []
        self._graph = None
        self._axis = None

    def sents_to_network(self, sents):
        self._graph = textacy.network.sents_to_semantic_network(sents, normalize='lemma', edge_weighting='cosine')
        return self._graph

    def terms_to_network(self, terms):
        self._graph = textacy.network.terms_to_semantic_network(terms, normalize='lemma', edge_weighting='cosine')
        return self._graph

    def draw_graph(self, draw=False):
        self._axis = textacy.viz.network.draw_semantic_network(self._graph, node_weights=None, spread=3.0,
                                                               draw_nodes=draw,
                                                               base_node_size=300, node_alpha=0.25, line_width=0.5,
                                                               line_alpha=0.1,
                                                               base_font_size=12, save=False)
        return self._axis
