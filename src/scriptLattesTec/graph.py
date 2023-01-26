#!/usr/bin/python
# encoding: utf-8
#
#
# scriptLattesTec
# https://github.com/raphaeldeaquino/scriptLattesTec
#
# Este programa é um software livre; você pode redistribui-lo e/ou
# modifica-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença, ou (na sua opinião) qualquer versão.
#
# Este programa é distribuído na esperança que possa ser util,
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
# MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

class Graph:

    def __init__(self):
        self.vertices = []
        self.edges = {}

    def add_edge(self, author1, author2):
        index = next((i for i, item in enumerate(self.vertices) if item['name'] == author1['name']), None)

        if index is None:
            self.vertices.append(author1)

        index = next((i for i, item in enumerate(self.vertices) if item['name'] == author2['name']), None)

        if index is None:
            self.vertices.append(author2)

        name1 = author1['name']
        name2 = author2['name']

        if name1 in self.edges:
            adj_index = None
            for i in range(len(self.edges[name1])):
                if self.edges[name1][i]['name'] == name2:
                    adj_index = i
            if adj_index is not None:
                adj_node = self.edges[name1][adj_index]
                del self.edges[name1][adj_index]
                adj_node['w'] = adj_node['w'] + 1
                self.edges[name1].append(adj_node)
            else:
                adj = {'name': name2, 'w': 1}
                self.edges[name1].append(adj)
        elif name2 in self.edges:
            adj_index = None
            for i in range(len(self.edges[name2])):
                if self.edges[name2][i]['name'] == name1:
                    adj_index = i
            if adj_index is not None:
                adj_node = self.edges[name2][adj_index]
                del self.edges[name2][adj_index]
                adj_node['w'] = adj_node['w'] + 1
                self.edges[name2].append(adj_node)
            else:
                adj = {'name': name1, 'w': 1}
                self.edges[name2].append(adj)
        else:
            adj = {'name': name2, 'w': 1}
            self.edges[name1] = [adj]

    def get_vertex(self, name):
        for v in self.vertices:
            if v['name'] == name:
                return v

        return None

    def get_edges_from(self, name):
        if name in self.edges:
            return self.edges[name]
        else:
            return None

    def to_csv(self):
        s = 'nome 1\tlinha 1\tnome 2\tlinha 2\n'

        for name in self.edges.keys():
            vertex_from = self.get_vertex(name)
            for edge in self.edges[name]:
                vertex_to = self.get_vertex(edge['name'])
                for i in range(edge['w']):
                    s += vertex_from['name'] + '\t' + vertex_from['line'] + '\t' + vertex_to['name'] + '\t' + vertex_to['line'] + '\n'

        return s

    def __str__(self):
        return 'V=' + str(self.vertices) + ', E=' + str(self.edges)


if __name__ == '__main__':
    g = Graph()
    a1 = {'name': 'a', 'line': 'l1'}
    a2 = {'name': 'b', 'line': 'l2'}
    a3 = {'name': 'c', 'line': 'l2'}
    g.add_edge(a1, a2)
    g.add_edge(a1, a3)
    g.add_edge(a1, a2)
    g.add_edge(a3, a1)
    g.add_edge(a2, a1)
    print(g)
