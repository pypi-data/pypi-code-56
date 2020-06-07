from collections import defaultdict

class Graph: 
    def __init__(self): 
        self.graph = defaultdict(list)  #   For storing vertices as key and the list of there connected vertices as value
        self.edges = defaultdict(list)  #   For storing the tuple of two vertices as key and distance b/w them as value
        self.visitedVer = defaultdict(list) #   For storing all the vertices as key and False as there default value
        self.prev = defaultdict(list)   
        #   self.prev:   For storing the vertices as key and there previous vertices as value with the shortes distance
        self.minDistance = defaultdict(list) 
        #   self.minDistance:  For storing the vertices as key and distance from starting node as value
        self.vertices = []  #   For storing all the vertices

    #   Function for connecting two vertices or adding edge to the graph
    def addEdge(self,   u,
                v,  weight=1):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.edges[(u,v)] = weight
        self.edges[(v,u)] = weight
        if u not in self.vertices:  #    Condition to check whether the same node is already present in the list or not 
            self.vertices.append(u)
        if v not in self.vertices:  #    Condition to check whether the same node is already present in the list or not
            self.vertices.append(v)

    #   Function to check whether the path exist between two nodes or not
    def pathExist(self, u, v):
        arr = []
        self.visited = defaultdict(list)
        for i in self.graph:
            self.visited[i] = False
        queue = []
        queue.append(u)
        self.visited[u] = True
        while queue:
            temp = queue.pop(0)
            if temp == v:   #   Condition to check whether the dequeued vertex is equal to the destination vertex or not
                return True
            for i in self.graph[temp]:
                if self.visited[i] == False:    #   Condition to check whether the current vertex is already visited or not.
                    queue.append(i)
                    arr.append(temp)
                    self.visited[i] = True
        return False
    
    #   Function to find the shortest path from a point to all the nodes.
    def dijkstra(self,u):
        for i in self.vertices:
            self.visitedVer[i] = False
        for i in self.vertices:
            if i == u:  #   Condition to check if the vertex present in vertices list is equals to starting node or not
                #   if the condition is true its minimum distance is assign as 0
                self.minDistance[(u,i)] = 0
            else:
                #   else the minimum distance is set as infinite or a very large value say 10**9
                self.minDistance[(u,i)] = 10**9
        temp = u
        while (self.visitedVer[temp] == False):
            self.visitedVer[temp] = True
            for i in self.graph[temp]:
                if (self.visitedVer[i] == False and
                    self.minDistance[(u,i)]>self.edges[(temp,i)]
                                            + self.minDistance[(u,temp)]):  
                    #   Condtion to check whether the vertex is already visited or not and
                    #   to check whether the distance between adjacent node of current node and starting is greater then the
                    #   sum of distace from starting node to current node and adjacent node of currnet node    
                    self.minDistance[(u,i)] = self.edges[(temp,i)]  + self.minDistance[(u,temp)]
                    self.prev[i] =  temp
            largest = 10**9
            for i in self.graph:
                if (self.visitedVer[i] == False and
                    self.minDistance[(u,i)]<largest):
                    #   Condition to check for those unvisited vertices whose distance is updated from infinite but
                    #   that is not the shortest distance from the starting vertex  
                    largest =  self.minDistance[(u,i)]
                    temp = i
        return self.prev
    
    #   Function to find the shortest distance from source to destination
    def sourceToDest(self, u, v):
        if self.pathExist(u, v):
            #   Condition to check whether the path exist between source and destination or not
            prev = self.dijkstra(u)
            prev = list(prev.items())   #   Creating a list of all the vertices connecting form source to previous element of dest.
            sourceToDest = []
            temp = v
            while temp:
                sourceToDest.insert(0,temp)
                if temp == u: # Condition to check whether the current vertex is source or not
                    break
                for i in range(len(prev)):
                    if prev[i][0] == temp: 
                        #   Conditon to check if the verext at position 0 is equals to destination or not.
                        #   if yes then temp is assign to its previous vertex
                        temp = prev[i][1]
            sourceToDest = set(sourceToDest)
            return sourceToDest
        return -1