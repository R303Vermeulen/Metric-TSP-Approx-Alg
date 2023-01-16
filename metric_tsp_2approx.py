import sys
import graph

def inListToEdge(inlist):
    edgeList = []
    for sting in inlist:
        cut = len(sting) - 1
        sting = sting[:cut]
        stingList = sting.split(", ")
        intList = []
        for elem in stingList:
            intList.append(int(elem))
        edgeList.append(intList)
    return edgeList

def edgesToGraph(edges):
    #gaph = graph.WeightedGraph([])
    #for edge in edges:
        #graph.add_edge(gaph, edge[0], edge[1], edge[2])
    gaph = []
    verts = []
    for edge in edges:
        if edge[0] not in verts:
            verts.append(edge[0])
        if edge[1] not in verts:
            verts.append(edge[1])
    for vert in verts:
        gaph.append([])
    for edge in edges:
        v1 = edge[0]
        v2 = edge[1]
        w = edge[2]
        gaph[v1].append([v2,w])
        gaph[v2].append([v1,w])
    return gaph


def metTSP_approx(mygraph):
    mst = minspantree(mygraph)
    path2direc = dfs(mst)
    path1direc = rectify(path2direc)
    return path1direc

def minspantree(gaph):
    tree = []
    edgesByWeight = []

    for edgesI in range(len(gaph)):
        tree.append([])
        for edge in gaph[edgesI]:
            edgesByWeight.append([edge[1], edgesI, edge[0]])

    edgesByWeight = sorted(edgesByWeight)

    curr = edgesByWeight[0]
    v1 = curr[1]
    v2 = curr[2]
    tree[v1].append([v2, curr[0]])
    tree[v2].append([v1, curr[0]])
    visited = []
    nextEdges = []
    visited.append(v1)
    visited.append(v2)
    for i in range(len(gaph[v1])):
        if v2 != gaph[v1][i][0]:
            nextEdges.append([gaph[v1][i][1], v1, gaph[v1][i][0]])
    for i in range(len(gaph[v2])):
        if v1 != gaph[v2][i][0]:
            nextEdges.append([gaph[v2][i][1], v2, gaph[v2][i][0]])

    while len(nextEdges) > 0:
        nextEdges = sorted(nextEdges)
        curr = nextEdges[0]
        v1 = curr[1]
        v2 = curr[2]
        if v2 not in visited:
            tree[v1].append([v2, curr[0]])
            tree[v2].append([v1, curr[0]])
            visited.append(v2)
            for i in range(len(gaph[v2])):
                if v1 != gaph[v2][i][0]:
                    nextEdges.append([gaph[v2][i][1], v2, gaph[v2][i][0]])
        nextEdges.pop(0)
    return tree

def dfs(must):
    path = []
    takenAlready = []
    edgeOn = [0, must[0][0][0]]
    takenAlready.append(edgeOn)
    path.append(0)
    path.append(must[0][0][0])
    oninp = 1

    while len(path) < (2*(len(must)-1) + 1):
        nonbedges = []
        bedges = []
        for edge in must[path[oninp]]:
            if [path[oninp], edge[0]] not in takenAlready:
                if edge[0] not in path:
                    nonbedges.append(edge)
                else:
                    bedges.append(edge)
        nonbedges = sorted(nonbedges)
        bedges = sorted(bedges)
        if len(nonbedges) > 0:
            edge = nonbedges[0]
        else:
            edge = bedges[0]
        edgeOn = [path[oninp], edge[0]]
        takenAlready.append(edgeOn)
        path.append(edge[0])
        oninp += 1

    return path

def rectify(pa2):
    i = 0
    path = [pa2[0]]
    while i < (len(pa2) - 1):
        c = i + 1
        v1 = pa2[i]
        v2 = pa2[c]
        if v2 not in path:
            path.append(v2)
            i += 1
        else:
            while v2 in path and c < len(pa2) - 1:
                bb = 1
                c += 1
                i += 1
                v2 = pa2[c]
            i += 1
            path.append(v2)

    return path

def findPathWeight(zepath, zegraph):
    i = 0
    w = 0
    while i < (len(zepath) - 1):
        v1 = zepath[i]
        v2 = zepath[i+1]
        edges = zegraph[v1]
        eee = None
        for edge in edges:
            if edge[0] == v2:
                eee = edge
        w += eee[1]
        i += 1
    return w

if __name__ == "__main__":
    inFile = open(sys.argv[1])
    inList = inFile.readlines()
    edgess = inListToEdge(inList)
    grap = edgesToGraph(edgess)
    pat = metTSP_approx(grap)
    weight = findPathWeight(pat, grap)
    print("Hamiltonian cycle of weight " + str(weight) + ":")
    sting = ""
    i = 0
    sting += str(pat[i])
    i += 1
    while i < len(pat):
        sting += ", "
        sting += str(pat[i])
        i += 1
    print(sting)
