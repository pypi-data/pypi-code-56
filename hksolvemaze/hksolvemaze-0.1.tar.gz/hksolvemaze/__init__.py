from collections import defaultdict

class Graph: 
    def __init__(self): 
        self.graph = defaultdict(list)
        self.edges = defaultdict(list)
        self.visitedVer = defaultdict(list)
        self.prev = defaultdict(list)
        self.minDistance = defaultdict(list)
        self.vertices = []

    def addEdge(self,u,v,weight=1):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.edges[(u,v)] = weight
        self.edges[(v,u)] = weight
        if u not in self.vertices:
            self.vertices.append(u)
        if v not in self.vertices:
            self.vertices.append(v)

    def pathExist(self,u,v):
        arr = []
        self.visited = defaultdict(list)
        for i in self.graph:
            self.visited[i] = False
        queue = []
        queue.append(u)
        self.visited[u] = True
        while queue:
            temp = queue.pop(0)
            if temp == v:
                return True
            for i in self.graph[temp]:
                if self.visited[i] == False:
                    queue.append(i)
                    arr.append(temp)
                    self.visited[i] = True
        return False

    def dijkstra(self,u):
        for i in self.vertices:
            self.visitedVer[i] = False
        for i in self.vertices:
            if i == u: self.minDistance[(u,i)] = 0
            else: self.minDistance[(u,i)] = 10**9
        temp = u
        while (self.visitedVer[temp] == False):
            self.visitedVer[temp] = True
            for i in self.graph[temp]:
                if self.visitedVer[i] == False and self.minDistance[(u,i)]>self.edges[(temp,i)]+self.minDistance[(u,temp)]:
                    self.minDistance[(u,i)] = self.edges[(temp,i)] + self.minDistance[(u,temp)]
                    self.prev[i] =  temp
            maximum = 10**9
            for i in self.graph[temp]:
                if self.visitedVer[i] == False and len(self.graph[i])>0 and self.minDistance[(u,i)]<maximum:
                    maximum = self.minDistance[(u,i)]
                    temp = i
            else:
                largest = 10**9
                for i in self.graph:
                    if self.visitedVer[i] == False and len(self.graph[i])>0 and self.minDistance[(u,i)]<largest:
                        largest =  self.minDistance[(u,i)]
                        temp = i
        return self.prev

    def sourceToDest(self,u,v):
        if self.pathExist(u,v):
            prev = self.dijkstra(u)
            prev = list(prev.items())
            sourceToDest = []
            temp = v
            while temp:
                sourceToDest.insert(0,temp)
                if temp == u: 
                    break
                for i in range(len(prev)):
                    if prev[i][0] == temp: 
                        temp = prev[i][1]
            sourceToDest = set(sourceToDest)
            return sourceToDest
        return -1