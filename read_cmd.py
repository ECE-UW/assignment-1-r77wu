import sys
import re
from itertools import combinations 

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
    try:
        type_match = re.search(r'^ *[a|c|r|g] *', command)
        if type_match:
            command_type = type_match.group().strip()
    except:
        pass
    return command_type

def decode_command(command, command_type):

    points_pattern = r'(\( *(-?[0-9]\d*(\.\d+)?) *, *(-?[0-9]\d*(\.\d+)?) *\) *){2,}$'

    ac_pattern = r'^ *[a|c] *"[a-zA-Z ]+" +' + points_pattern
    r_pattern = r'^ *r +"[a-zA-Z ]+" *$'
    g_pattern = r'^ *g *$'
    

    street_name = str()
    points = list()
    try:
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
                points_re = re.search(points_pattern, command)
                ## Handleing leading zeros
                # points = [eval(i+')') for i in points_str.group().split(")")[:-1]]
                points_str = points_re.group().replace("("," ")
                for p in points_str.split(")")[:-1]:
                    x, y = p.split(",")
                    x = int(x)
                    y = int(y)
                    points.append((x,y))

        else:
            sys.stderr.write(ERROR_MSG + '%s command is invalid.\n'%(command_type))
    except:
        pass
    return street_name, points