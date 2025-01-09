g5_00 = {0: {1, 2, 4}, 1: {0, 2}, 2: {0, 1, 3}, 3: {2, 4}, 4: {0, 3}}
g5_01 = {0: {3, 4}, 1: {2, 3, 4}, 2: {1, 3}, 3: {0, 1, 2}, 4: {0, 1}}
g5_02 = {0: {1, 2, 4}, 1: {0, 3}, 2: {0, 3}, 3: {1, 2, 4}, 4: {0, 3}}


def combineTwo(g1, g2):
    g = {}
    n = len(g1)
    for node in g1:
        s = set()
        for neighbor in g1[node]:
            s.add(neighbor)
        g[node] = s.copy()
    for node in g2:
        s = set()
        for neighbor in g2[node]:
            s.add(neighbor + n)
        g[node + n] = s.copy()
    return g


g = combineTwo(g5_00, g5_02)
labels = {}
glabels = {}
for i in range(len(g)):
    glabels[i] = 0
glabelsCount = 1
newlabel = 1

done = False
while not (done):
    glabelsNew = {}
    glabelsCountNew = 0
    for node in g:
        label = str(glabels[node])
        s2 = []
        for neighbor in g[node]:
            s2.append(glabels[neighbor])
        s2.sort()
        for i in range(len(s2)):
            label += "_" + str(s2[i])
        if not (label in labels):
            labels[label] = newlabel
            newlabel += 1
            glabelsCountNew += 1
        glabelsNew[node] = labels[label]
    if glabelsCount == glabelsCountNew:
        done = True
    else:
        glabelsCount = glabelsCountNew
        glabels = glabelsNew.copy()
print(glabels)

g0labels = []
for i in range(len(g0)):
    g0labels.append(glabels[i])
g0labels.sort()
certificate0 = ""
for i in range(len(g0)):
    certificate0 += str(g0labels[i]) + "_"
g1labels = []
for i in range(len(g1)):
    g1labels.append(glabels[i + len(g0)])
g1labels.sort()
certificate1 = ""
for i in range(len(g1)):
    certificate1 += str(g1labels[i]) + "_"

if certificate0 == certificate1:
    test = True
else:
    test = False
print("Certificate 0:", certificate0)
print("Certificate 1:", certificate1)
print("Test yields:", test)