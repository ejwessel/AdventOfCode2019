class Graph:

    def __init__(self):
        self.graph = {}
        self.closure = {}

    def make_graph_file(self, file_input):

        orbits = []
        with open(file_input) as data:
            for line in data:
                line = line.rstrip()
                orbits.append(line)

        self.make_graph(orbits)

    def make_graph(self, orbit_mappings):
        for orbit in orbit_mappings:
            [parent, child] = orbit.split(")")

            if parent not in self.graph:
                self.graph[parent] = []

            if child not in self.graph:
                self.graph[child] = []

            # add child to parent
            self.graph[parent].append(child)

    def compute_transitive_closure(self, current_node, seen_list):
        self.closure[current_node] = seen_list

        for adjacent_node in self.graph[current_node]:
            self.compute_transitive_closure(adjacent_node, seen_list + [current_node])



if __name__ == "__main__":
    # GOAL: find all transitive closures

    # TEST DATA
    sol = Graph()
    input_data = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
    sol.make_graph(input_data)
    assert sol.graph == {'COM': ['B'], 'B': ['C', 'G'], 'C': ['D'], 'D': ['E', 'I'], 'E': ['F', 'J'], 'F': [], 'G': ['H'], 'H': [], 'I': [], 'J': ['K'], 'K': ['L'], 'L': []}

    sol.compute_transitive_closure('COM', [])
    total_closures = 0
    for available_nodes in sol.closure.values():
        total_closures += len(available_nodes)
    assert total_closures == 42

    # PART 1
    sol = Graph()
    sol.make_graph_file("input.txt")
    sol.compute_transitive_closure('COM', [])
    print(sol.graph)
    total_closures = 0
    for available_nodes in sol.closure.values():
        total_closures += len(available_nodes)
    assert total_closures == 295936

    #PART 2





