import sys
import re
from itertools import combinations 
from line_functions import *
from read_cmd import *

# YOUR CODE GOES HERE
ERROR_MSG = 'Error: '

def create_graph_from_map(street_map):
    """Generate map graph from StreetMap.

    Parameters: 
    street_map (dict)
    e.g: street_map = {'king street s': [(4, 2), (4, 8)],
                       'weber street': [(2, -1), (2, 2), (5, 5), (5, 6), (3, 8)],
                       'davenport road': [(1, 4), (5, 8)]}

    Returns: 
    nodes (dict)
    edges (dict) 

    e.g.:
    nodes = {1:(2,-1), 2:(2,2),3:(5,5),4:(5,6),5:(3,8),
                     6:(4,2),7:(4,8), 8:(1,4), 9:(5,8)
                     }
    edges = {(1,2):1,(2,3):1,(3,4):1,(4,5):1,(6,7):2,(8,9):3}
    """
    nodes = dict()
    edges = dict()
    try:
        key_count = 0
        street_code = 1
        for k, v in street_map.items():
            for x in v:
                key_count = key_count+1
                nodes[key_count]= x
                if x != v[-1]:
                    edges[key_count, key_count+1] = street_code
                else:
                    street_code = street_code + 1
    except:
        pass
    return nodes, edges

class StreetMap:
    def __init__(self):
        self.streets = dict()

    def add_street(self, street_name, points):
        # TO DO: Check if self intersect
        if street_name in self.streets:
            sys.stderr.write(ERROR_MSG + 'Steet has existed, cannot add street.\n')
        else:
            self.streets[street_name] = points
        
    def change_street(self, street_name, points):
        #TO DO: Check if self intersect
        if street_name not in self.streets:
            sys.stderr.write(ERROR_MSG + 'Street does not exist, cannot change street.\n')
        else:
            self.streets[street_name] = points

    def remove_street(self, street_name):
        if street_name not in self.streets:
            sys.stderr.write(ERROR_MSG + 'Street does not exist, cannot remove street.\n')
        else:
            del self.streets[street_name]

    def generate_graph(self):
        intersect_count = {}
        nodes, edges = create_graph_from_map(self.streets)
        for k,v in edges.items():
            intersect_count[k] = 0

        nodes_count = len(nodes)

        intersects = set()
        vertice = dict()
        graph_edges = set()
        graph_edges_repr = list()
        
        try:
            for seg1, seg2 in list(combinations(edges,2)):
                if edges[seg1] != edges[seg2]:
                    p11, p12 = nodes[seg1[0]],nodes[seg1[1]]
                    p21, p22 = nodes[seg2[0]],nodes[seg2[1]]
                    intersect = line_segment_intersection((p11, p12), (p21, p22))

                    if intersect:
                        intersect_count[seg1] += 1 
                        intersect_count[seg2] += 1
                        vertice[p11] = seg1[0]
                        vertice[p12] = seg1[1]
                        vertice[p21] = seg2[0]
                        vertice[p22] = seg2[1]
     
                        for inter in intersect:
                            intersects.add(inter)
                            if inter not in vertice:
                                nodes_count += 1
                                vertice[inter] = nodes_count
                                nodes[nodes_count] = inter

            for edge, c in intersect_count.items():
                if c == 0 and edge in edges:
                    del edges[edge]

            for e, key in edges.items():
                input_line = (nodes[e[0]], nodes[e[1]])
                intersect_segments = segment_line(input_line, intersects)
                if intersect_segments:
                    graph_edges = graph_edges.union(intersect_segments)

            for e in graph_edges:
                p1, p2 = e
                e_repr = {vertice[p1],vertice[p2]}
                if e_repr not in graph_edges_repr:
                    graph_edges_repr.append(e_repr)
        except:
            pass
        
        spaces2 = '  '
        V_graph = 'V = {\n'
        for p, k in vertice.items():
            p_x, p_y = p
            p_x = "%.2f" % p_x if isinstance(p_x, float) else str(p_x)
            p_y = "%.2f" % p_y if isinstance(p_y, float) else str(p_y)
            p_xy = '(' + p_x + ',' + p_y + ')'
            V_graph += spaces2 + str(k) + ':' + spaces2 + p_xy + '\n'
        V_graph += '}'


        E_graph = 'E = {\n'
        for i in range(len(graph_edges_repr)):
            e = list(graph_edges_repr[i])
            if i == (len(graph_edges_repr)-1):
                E_graph += spaces2 + '<' + str(e[0]) + ',' + str(e[1]) + '>\n'
            else:
                E_graph += spaces2 + '<' + str(e[0]) + ',' + str(e[1]) + '>,\n'
        E_graph += '}'
        sys.stdout.write(V_graph + '\n')
        sys.stdout.write(E_graph + '\n')

        return 0

def main():
    ### YOUR MAIN CODE GOES HERE
    street_map = StreetMap()
    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    while True:
        try:
            # command = sys.stdin.readline().strip()
            command = raw_input()
            command_type = get_command_type(command)

            if command_type == "a":
                street_name, points = decode_command(command, command_type)
                self_intersect = check_self_intersect(points)
                if self_intersect:
                    sys.stderr.write(ERROR_MSG + 'Cannot add street with self intersect points\n')
                elif street_name != '' and not self_intersect:
                    street_map.add_street(street_name.lower(), points)
            elif command_type == "c":
                street_name, points = decode_command(command, command_type)
                self_intersect = check_self_intersect(points)
                if self_intersect:
                    sys.stderr.write(ERROR_MSG + 'Cannot change street with self intersect points\n')
                elif street_name != '' and not self_intersect:
                    street_map.change_street(street_name.lower(), points)
            elif command_type == "r":
                street_name, _ = decode_command(command, command_type)
                if street_name != '':
                    street_map.remove_street(street_name.lower())
            elif command_type == "g":
                street_map.generate_graph()  
            else: ## command_type == ""
                sys.stderr.write(ERROR_MSG + 'can only recorgnize command type a / c / r / g\n')
        except EOFError:
            sys.exit(0)

if __name__ == '__main__':
    main()
