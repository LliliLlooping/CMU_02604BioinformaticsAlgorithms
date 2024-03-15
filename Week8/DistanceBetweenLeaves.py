
class DistanceBetweenLeaves():
    def __init__(self):
        pass

    def solve_distance_between_leaves(self, n, weightedEdges):
        adjacency_list = self.generate_adjacency_list_from_weighted_edges(
            weightedEdges)
        DistMatrix = []
        for i in range(n):
            distance_from_i = {i: 0}
            queue = [i]
            self.BFS(distance_from_i, queue, adjacency_list)
            DistMatrix.append([distance_from_i[j] for j in range(n)])
        return DistMatrix

    def BFS(self, distance_from_i, queue, adjacency_list):
        ori = queue.pop(0)
        current_distance = distance_from_i[ori]
        adjacency_list_from_ori = adjacency_list[ori]
        for des in adjacency_list_from_ori.keys():
            if des not in distance_from_i.keys():
                queue.append(des)
                distance_from_i[des] = current_distance + \
                    adjacency_list[ori][des]
        if len(queue) > 0:
            self.BFS(distance_from_i, queue, adjacency_list)

        return

    def generate_adjacency_list_from_weighted_edges(self, weightedEdges):
        adjacency_list = {}
        for (ori, des, weight) in weightedEdges:

            if ori not in adjacency_list:
                adjacency_list[ori] = {}
            adjacency_list[ori][des] = weight

            if des not in adjacency_list:
                adjacency_list[des] = {}
            adjacency_list[des][ori] = weight

        return adjacency_list

    def test(self):
        n = 3
        weightedEdges = [
            (0, 1, 10),
            (0, 2, 100)
        ]
        self.solve_distance_between_leaves(n, weightedEdges)
