import sys
import re
from itertools import combinations 

EPSILON = 0.01
ERROR_MSG = 'Error: '

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
    try:
        line = sorted(line)
        intersects = sorted(intersects)

        left_p = line[0]
        right_p = line[1]
        for i in intersects:
            if IsPointOnLineSegement(line[0], line[1], i):
                if left_p != i:
                    result.add((left_p, i))
                left_p = i

        if left_p != right_p:
            result.add((left_p,right_p))
    except:
        pass
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

    try:
        x_d = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        y_d = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        div = det(x_d, y_d)
        if div == 0:
            if if_one_line(line1[0], line1[1], line2[0]) and if_one_line(line1[0], line1[1], line2[1]):       
                if IsPointOnLineSegement(line1[0], line1[1], line2[0]) or IsPointOnLineSegement(line1[0], line1[1], line2[1]):
                    points_4 = sorted((line1[0], line1[1], line2[0], line2[1]))
                    return list(set(points_4[1:3]))
            return []

        d = (det(*line1), det(*line2))
        x = det(d, x_d) / div
        y = det(d, y_d) / div
        if IsPointOnLineSegement(line1[0], line1[1], (x,y)) and IsPointOnLineSegement(line2[0], line2[1], (x,y)):      
            return [(x, y)]
        else:
            return []
    except:
        pass

def IsPointOnLineSegement(linePointA, linePointB, point):
    try:
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
    except:
        pass
    return False


def check_self_intersect(points):
    self_intersect = False
    try:
        if len(points) != len(set(points)):
            return True
        key_count = 0
        order_count = 1
        nodes = dict()
        edges = dict()
        for x in points:
            key_count = key_count+1
            nodes[key_count]= x
            if x != points[-1]:
                edges[order_count] = (key_count, key_count+1)
            order_count += 1
        for order1, e1 in edges.items():
            for order2, e2 in edges.items():

                if order2 < order1 - 1: 
                    line1 = nodes[e1[0]],nodes[e1[1]]
                    line2 = nodes[e2[0]],nodes[e2[1]]
                    if line_segment_intersection(line1, line2):
                        self_intersect = True
    except:
        pass
  
    return self_intersect


def if_one_line(p1, p2,p3):
    if (p1[1] - p2[1]) * (p1[0] - p3[0])  == (p1[0] - p2[0]) * (p1[1] - p3[1]):
        return True
    return False


