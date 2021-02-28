from snake.logic.block import BlockType


class Graph:

    def __init__(self, board):
        self.board = board
        self.nodes = {}
        self._build_graph()

    def _build_graph(self):
        for y in range(self.board.get_width()):
            for x in range(self.board.get_height()):
                b = self.board.get_block(x, y)
                if not self._is_path(b):
                    continue

                typ = None if b is None else b.type
                self.nodes[(x, y, typ)] = []
                self._build_adjacency((x, y, typ))

    def _build_adjacency(self, node):
        adjacency_list = self.nodes[node]
        x, y, typ = node

        positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for pos in positions:
            b = self.board.get_block(*pos)
            if self._is_path(b):
                typ = None if b is None else b.type
                adjacency_list.append((*pos, typ))

    def _is_path(self, b):
        return b is None or b.type in [BlockType.APPLE, BlockType.SNAKE_HEAD]

    def get_path_by_depth(self):
        max_depth = 10
        starting_node = self._get_starting_node()
        ending_node = self._get_ending_node()

        if starting_node is None or ending_node is None:
            return []

        visited_nodes = [(starting_node, self.nodes[starting_node])]
        while visited_nodes != [] and visited_nodes[-1][0] != ending_node:
            next_nodes = visited_nodes[-1][1]
            if next_nodes != [] and len(visited_nodes) < max_depth:
                next_node = next_nodes.pop()
                next_nodes_to_visit = []
                for nn in self.nodes[next_node]:
                    if nn in [n[0] for n in visited_nodes]:
                        continue
                    next_nodes_to_visit.append(nn)
                visited_nodes.append((next_node, next_nodes_to_visit))
            else:
                visited_nodes.pop()
        return [n[0] for n in visited_nodes][1:]

    def get_path_by_breadth(self):
        starting_node = self._get_starting_node()
        ending_node = self._get_ending_node()

        if starting_node is None or ending_node is None:
            return []

        visited_nodes = set()
        visited_nodes.add(starting_node)
        paths = {node: [starting_node] for node in self.nodes[starting_node]}
        while (ending_node not in paths.keys()) and paths != {}:
            next_paths = {}
            for parent in paths.keys():
                for node in self.nodes[parent] :
                    if node in visited_nodes :
                        continue
                    visited_nodes.add(node)
                    next_paths[node] = list(paths[parent])
                    next_paths[node].append(parent)
            paths = next_paths

        if paths == {} :
            return []
        path = paths[ending_node]
        path.append(ending_node)
        return path[1:]

    def _get_starting_node(self):
        for node in self.nodes.keys():
            x, y, typ = node
            if typ == BlockType.SNAKE_HEAD:
                return x, y, typ

    def _get_ending_node(self):
        for node in self.nodes.keys():
            x, y, typ = node
            if typ == BlockType.APPLE:
                return x, y, typ
