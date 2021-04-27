"""
- Reads a txt file of individuals (1 per line) and converts them to PNGs
- Include optional txt file of names for your PNGs
- Requires you to download graphviz (free) and add it to your system's path: https://graphviz.org/download/
- Edit 'make_nodes'/'make_edges' functions to change respective formatting (e.g. color, shapes, etc)

Sample command: python tree_vis.py individuals.txt

Written by Cameron Whaley
"""
# NOTE: You will have to download graphviz and add it to your system's path
import argparse
import pydot

# parsing args:
parser = argparse.ArgumentParser()
parser.add_argument('--tree_file_path', type=str,default="individuals.txt",help="path to text file with an individual on each line")
parser.add_argument('--name_file_path', type=str,default='', help="path to text file with naming convention for output PNGs")
args = parser.parse_args()

# reading txt file of individuals:
tree_file = args.tree_file_path
treesf = open(tree_file, 'r')
trees = [t.strip().replace(' ','') for t in treesf.readlines()]
treesf.close()

def findEnd(ind,i):
    # helper function to find the end (index) of a primitive's arguments
    paren = 1
    j=i
    while paren>0:
        j+=1 # since we're starting with paren=1, we don't want to count the one at the start
        char = ind[j]
        if char=='(':
            paren+=1
        elif char==')':
            paren-=1
    return j

def split(string, aList):
    # split primitive arguments separated by commas
    for aStr in string.split(','):
        aList.append(aStr)
    return aList

def process_string(ind,start=0,stop=None):
    # converts individual's string representation into nested lists
    # example input: "add(5,subtract(5,2))"
    # output: ["add", ["subtract", [5,2]]]
    # primitives without args are followed by an empty list
    
    result = []
    i=start
    if stop==None:
        stop=len(ind[start:])
    while i<stop:
        if ind[i] == '(':
            result = split(ind[start:i],result)
            end = findEnd(ind,i)
            result.append(process_string(ind,i+1,end))
            start=end+2 # move start to end of primitive. +2 to skip '),'
            i=end
        i+=1
    leftover = ind[start:stop] # catches arguments after final primitive
    if leftover != '':
        result = split(leftover,result)
    return result

def make_nodes(tree,namespace,graph):
    # recursively converts tree from process_string into nested lists of pydot nodes
    # adds nodes to graph
    # can change formatting in "else" code
    nodes = []
    for i in range(len(tree)):
        if type(tree[i])==list:
            subnodes, namespace = make_nodes(tree[i], namespace,graph)
            if subnodes != []:
                nodes.append(subnodes)
        else:
            #######################################################
            ############ CAN CHANGE COLORS/SHAPES HERE ############
            #######################################################
            shape = 'oval'
            if i+1<len(tree) and type(tree[i+1])==list: # 1st condition should prevent index errors
                shape = 'rect' # primitives will be rectangular in graph
            label = tree[i] # the text shown on graph
            if label in namespace.keys():
                namespace[label]+=1 
            else:
                namespace[label]=1
            name = label + str(namespace[label]) # pydot nodes need unique names
            node = pydot.Node(name, label=label, shape=shape)
            graph.add_node(node)
            nodes.append(node)
    return nodes, namespace

def make_graph(graph,nodes,parent):
    # connects nodes of graph
    for i in range(len(nodes)):
        if type(nodes[i])==list:
            make_graph(graph, nodes[i], nodes[i-1])
        else:
            graph.add_edge(pydot.Edge(parent, nodes[i]))

# creating file names:
if args.name_file_path: # if names file supplied
    name_file = args.name_file_path
    namesf = open(name_file, 'r')
    names = [n.strip() for n in namesf.readlines()]
    namesf.close()
else:
    names = [trees[i][0:trees[i].find('(')]+str(i) for i in range(len(trees))] # default name is parent node + number in queue

# creating graphs and saving to PNGs:
for i in range(len(trees)):
    graph = pydot.Dot("my_graph", graph_type='graph')
    tree = process_string(trees[i])
    nodes = make_nodes(tree,{}, graph)[0] # don't care about namespace

    make_graph(graph,nodes[1],nodes[0]) # nodes[0] is global parent node. nodes[1] is a list of its leaves and subtrees
    graph.write_png(names[i]+".png")