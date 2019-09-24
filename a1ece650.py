import sys
import re
from itertools import combinations 

# YOUR CODE GOES HERE
EPSILON = 0.0001;
ERROR_MSG = 'Error: '

def get_command_type(command):
    """Returns the type of a command if it is valid command.
               o.w. return ""

    Parameters: 
    command (str)

    Returns: 
    result (str): "a" or "c" or "r" or "g" or ""
    """
    command_type = ""
    type_match = re.search(r'^ *[a|c|r|g] *', command)
    if type_match:
        command_type = type_match.group().strip()
    return command_type

def decode_command(command, command_type):

    points_pattern = r'(\( *(-?[0-9]\d*(\.\d+)?) *, *(-?[0-9]\d*(\.\d+)?) *\) *){2,}$'

    ac_pattern = r'^ *[a|c] *"[a-zA-Z ]+" +' + points_pattern
    r_pattern = r'^ *r +"[a-zA-Z ]+" *$'
    g_pattern = r'^ *g *$'
    

    street_name = str()
    points = list()

    if command_type in ["a", "c"]:
        command_valid = re.match(ac_pattern, command)
    elif command_type == "r":
        command_valid = re.match(r_pattern, command)
    else: #command_type == "g"
        command_valid = re.match(g_pattern, command)

    if command_valid:
        name_s = command.find('"')
        name_e = command.find('"', name_s+1)
        street_name = command[name_s:name_e+1]
        if command_type in ["a", "c"]:
            points_str = re.search(points_pattern, command)
            ## TO DO: handing leading zeros
            points = [eval(i+')') for i in points_str.group().split(")")[:-1]]
    else:
        sys.stderr.write(ERROR_MSG + '%s command is invalid.\n'%(command_type))
    return street_name, points


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
    return nodes, edges

def segment_line(line, intersects):
    """Returns line segments divide by intersect points

    Parameters:
    line (tuple of two tuples)
    intersects (set)

    e.g.
    line = ((4, 2), (4,8))
    intersects = {(4,4),(4,7)}

    Returns:
    result (set)

    e.g.
    result: {
                ((4, 2), (4,4)),  
                ((4, 4), (4,7)),
                ((4, 7), (4,8))
              }
    """
    result = set()
    line = sorted(line)
    intersects = sorted(intersects)

    left_p = line[0]
    right_p = line[1]
    for i in intersects:
        if IsPointOnLineSegement(line[0], line[1], i):
            result.add((left_p, i))
            left_p = i
    
    result.add((left_p,right_p))
    return result


def line_segment_intersection(line1, line2):
    """ Returns intersect(a,b) for two lines if there is one
                o.w. return ()

    Parameters: 
    line1 (list): e.g. line1 = ((2, 2), (5,5)) 
    line2 (list): e.g. line2 = ((4, 2), (4,8))

    Returns: 
    result (list): [a,b] if there is intersection else []

    """
    def det(c, d):
        return c[0] * d[1] - c[1] * d[0]

    x_d = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_d = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(x_d, y_d)
    if div == 0:
        return ()

    d = (det(*line1), det(*line2))
    x = det(d, x_d) / div
    y = det(d, y_d) / div
    if IsPointOnLineSegement(line1[0], line1[1], (x,y)) and IsPointOnLineSegement(line2[0], line2[1], (x,y)):      
        return (x, y)
    else:
        return ()

def IsPointOnLineSegement(linePointA, linePointB, point):
    if linePointA[0] == linePointB[0]:
        min_y = min(linePointA[1],linePointB[1])
        max_y = max(linePointA[1],linePointB[1])
        return min_y <= point[1] and point[1] <= max_y
    else:
        a = (linePointB[1] - linePointA[1]) / (linePointB[0] - linePointA[0])
        b = linePointA[1] - a * linePointA[0]
        if ( abs(point[1] - (a*point[0]+b)) < EPSILON):
            min_x = min(linePointA[0],linePointB[0])
            max_x = max(linePointA[0],linePointB[0])
            return min_x <= point[0] and point[0] <= max_x
    return False


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

                    if intersect not in vertice:
                        nodes_count += 1
                        vertice[intersect] = nodes_count
                        nodes[nodes_count] = intersect
                        intersects.add(intersect)

        for edge, c in intersect_count.items():
            if c == 0 and edge in edges:
                del edges[edge]

        for e, key in edges.items():
            input_line = (nodes[e[0]], nodes[e[1]])
            intersect_segments = segment_line(input_line, intersects)
            if intersect_segments:
                graph_edges = graph_edges.union(intersect_segments)

        ## TO DO
        graph_edges_repr = set()
        for e in graph_edges:
            p1, p2 = e
            graph_edges_repr.add((vertice[p1],vertice[p2]))
        # print('-----edges: ', edges)
        # print('-----graph_edges: ', graph_edges)
        sys.stdout.write('V = ' + str(vertice) + '\n')
        sys.stdout.write('E = ' + str(graph_edges_repr) + '\n')
        # print('-----graph_edges_repr: ', graph_edges_repr)
        # print('-----vertice: ', vertice)

        return 0


    


def main():
    ### YOUR MAIN CODE GOES HERE
    street_map = StreetMap()
    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    while True:
        command = sys.stdin.readline().strip()
        command_type = get_command_type(command)

        if command_type == "a":
            street_name, points = decode_command(command, command_type)
            if street_name != '' and points != list():
                street_map.add_street(street_name.lower(), points)
        elif command_type == "c":
            street_name, points = decode_command(command, command_type)
            if street_name != '' and points != list():
                street_map.change_street(street_name.lower(), points)
        elif command_type == "r":
            street_name, _ = decode_command(command, command_type)
            if street_name != '':
                street_map.remove_street(street_name.lower())
        elif command_type == "g":
            street_map.generate_graph()  
        else: ## command_type == ""
            sys.stderr.write(ERROR_MSG + 'can only recorgnize command type a / c / r / g\n')
            #TO DO:
            # break


    print 'Finished reading input'
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
