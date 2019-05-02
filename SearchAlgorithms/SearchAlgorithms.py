from collections import deque


class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)

    def __init__(self, mazeStr, edgeCost=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        self.board = self.GetBoard(mazeStr, edgeCost)
        self.GetDirections()
        pass

    def GetBoard(self, boardStr, edgeCost):
        board = list()
        ll = self.Get2DValues(boardStr)
        count = 0

        for i in ll:
            l = list()
            for j in i:
                n = Node(j)

                if j == "S":
                    n.gOfN = 0
                if edgeCost:
                    n.edgeCost = edgeCost[count]
                else:
                    n.edgeCost = 1

                n.id = count
                l.append(n)
                count += 1
            board.append(l)
        return board

    def GetDirections(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i > 0:
                    self.board[i][j].up = self.board[i - 1][j]
                if i < len(self.board) - 1:
                    self.board[i][j].down = self.board[i + 1][j]
                if j > 0:
                    self.board[i][j].left = self.board[i][j - 1]
                if j < len(self.board[i]) - 1:
                    self.board[i][j].right = self.board[i][j + 1]

    def Get2DValues(self, boardStr):
        ll = list()
        for i in boardStr.split(" "):
            l = i.split(",")
            ll.append(l)
        return ll

    def PrintBoard(self):
        for i in self.board:
            s = ""
            for j in i:
                s += j.value + " "
            print(s)
        print("\n")

    def GetIndex(self, char):
        x = 0
        y = 0
        for i in self.board:
            x = 0
            for j in i:
                if (j.value == char):
                    return x, y
                x += 1
            y += 1

        return -1, -1

    def GetNodeIndex(self, node):
        x = 0
        y = 0
        for i in self.board:
            x = 0
            for j in i:
                if (j == node):
                    return x, y
                x += 1
            y += 1
        return -1, -1

    def GetPath(self):
        path = []
        Ex, Ey = self.GetIndex("E")
        n = self.board[Ey][Ex]
        path.append(n.id)
        while n.previousNode:
            path.append(n.previousNode.id)
            n = n.previousNode
        path.reverse()
        return path

    def DFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        Sx, Sy = self.GetIndex ( "S" )
        open = [self.board[Sy][Sx],]
        visited = []

        while open:

            node = open.pop()

            visited.append ( node )

            if (node.value) == "E":
                break

            if self.checkNeighbor(node.left, open, visited):
                node.left = self.move_BFS_DFS ( node, node.left )
                open.append ( node.left )

            if self.checkNeighbor(node.right, open, visited):
                node.right = self.move_BFS_DFS ( node, node.right )
                open.append ( node.right )

            if self.checkNeighbor(node.down, open, visited):
                node.down = self.move_BFS_DFS ( node, node.down )
                open.append ( node.down )

            if self.checkNeighbor(node.up, open, visited):
                node.up = self.move_BFS_DFS ( node, node.up )
                open.append( node.up )

        self.path = self.GetPath ()
        l = []
        for n in visited:
            l.append ( n.id )
        self.fullPath = l

        return self.path, self.fullPath


    def move_BFS_DFS(self,n1,n2):
        n2.previousNode = n1
        return n2

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        Sx, Sy = self.GetIndex("S")
        open = deque([self.board[Sy][Sx]])
        visited = []

        while open :
            node = open.popleft()
            visited.append(node)

            if(node.value) == "E":
                break

            if self.checkNeighbor(node.up, open, visited):
                node.up = self.move_BFS_DFS(node, node.up)
                open.append(node.up)

            if self.checkNeighbor(node.down, open, visited):
                node.down = self.move_BFS_DFS(node, node.down)
                open.append(node.down)

            if self.checkNeighbor(node.left, open, visited):
                node.left = self.move_BFS_DFS(node, node.left)
                open.append(node.left)

            if self.checkNeighbor(node.right, open, visited):
                node.right = self.move_BFS_DFS(node, node.right)
                open.append(node.right)

        self.path = self.GetPath()
        l = []
        for n in visited:
            l.append(n.id)
        self.fullPath = l

        return self.path, self.fullPath

    def UCS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        notvisited = []
        visited = []
        Ex, Ey = self.GetIndex("E")
        Sx, Sy = self.GetIndex("S")
        notvisited.append(self.board[Sy][Sx])
        while len(notvisited) != 0:
            notvisited.sort(key=lambda x: x.gOfN, reverse=True)
            node = notvisited.pop()
            visited.append(node)
            if node.value == "E":
                break
            if self.checkNeighbor(node.up, notvisited, visited):
                node.up = self.CostUcs(node, node.up)
                notvisited.append(node.up)
            if self.checkNeighbor(node.down, notvisited, visited):
                node.down = self.CostUcs(node, node.down)
                notvisited.append(node.down)
            if self.checkNeighbor(node.left, notvisited, visited):
                node.left = self.CostUcs(node, node.left)
                notvisited.append(node.left)
            if self.checkNeighbor(node.right, notvisited, visited):
                node.right = self.CostUcs(node, node.right)
                notvisited.append(node.right)

        self.path = self.GetPath()
        l = []
        for n in visited:
            l.append(n.id)
        self.fullPath = l
        self.totalCost = self.board[Ey][Ex].gOfN
        return self.path, self.fullPath ,self.totalCost

    def AStarEuclideanHeuristic(self):
        # Cost for a step is calculated based on edge cost of node
        # and use Euclidean Heuristic for evaluating the heuristic value
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        OPEN = []
        CLOSED = []
        Ex, Ey = self.GetIndex("E")
        Sx, Sy = self.GetIndex("S")
        OPEN.append(self.board[Sy][Sx])
        while len(OPEN) != 0:
            OPEN.sort(key=lambda x: x.heuristicFn, reverse=True)
            node = OPEN.pop()
            CLOSED.append(node)
            if node.value == "E":
                break
            if self.checkNeighbor(node.up, OPEN, CLOSED):
                node.up = self.move_AStar(node, node.up)
                OPEN.append(node.up)
            if self.checkNeighbor(node.down, OPEN, CLOSED):
                node.down = self.move_AStar(node, node.down)
                OPEN.append(node.down)
            if self.checkNeighbor(node.left, OPEN, CLOSED):
                node.left = self.move_AStar(node, node.left)
                OPEN.append(node.left)
            if self.checkNeighbor(node.right, OPEN, CLOSED):
                node.right = self.move_AStar(node, node.right)
                OPEN.append(node.right)

        self.path = self.GetPath()
        l = []
        for n in CLOSED:
            l.append(n.id)
        self.fullPath = l
        self.totalCost = self.board[Ey][Ex].heuristicFn
        return self.path, self.fullPath, self.totalCost

    def CostUcs(self, n1, n2):
        n2.previousNode = n1
        n2.gOfN = n1.gOfN + n2.edgeCost
        return n2

    def move_AStar(self, n1, n2):
        Ex, Ey = self.GetIndex("E")
        n2.previousNode = n1
        n2.gOfN = n1.gOfN + n2.edgeCost
        n2.hOfN = self.euclidean_distance(n2, self.board[Ey][Ex])
        n2.heuristicFn = n2.gOfN + n2.hOfN
        return n2


    def euclidean_distance(self, n1, n2):
        n1x, n1y = self.GetNodeIndex(n1)
        n2x, n2y = self.GetNodeIndex(n2)
        return ((n1x - n2x) ** 2 + ((n1y - n2y) ** 2)) ** (1 / 2)

    def AStarManhattanHeuristic(self):
        # Cost for a step is 1
        # and use ManhattanHeuristic for evaluating the heuristic value
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        open=[]
        closed=[]
        Ex, Ey = self.GetIndex("E")
        Sx, Sy = self.GetIndex("S")
        open.append(self.board[Sy][Sx])
        while len(open)!=0:
            open.sort(key=lambda x: x.heuristicFn, reverse=True)
            node = open.pop()
            closed.append(node)
            if node.value == "E":
                break
            if self.checkNeighbor(node.up    ,open,closed):
                node.up = self.moveManhattan(node, node.up)
                open.append(node.up)
            if self.checkNeighbor(node.down  ,open,closed):
                node.down = self.moveManhattan(node, node.down)
                open.append(node.down)
            if self.checkNeighbor(node.left  ,open,closed):
                node.left = self.moveManhattan(node, node.left)
                open.append(node.left)
            if self.checkNeighbor(node.right ,open,closed):
                node.right = self.moveManhattan(node, node.right)
                open.append(node.right)

        self.path = self.GetPath()
        l = []
        for n in closed:
            l.append(n.id)
        self.fullPath = l
        self.totalCost = self.board[Ey][Ex].heuristicFn

        return self.path, self.fullPath, self.totalCost

    def checkNeighbor(self,neighbor,open,closed):
        if neighbor is not None and neighbor.value != "#" and neighbor not in closed and neighbor not in open:
            return True

    def moveManhattan(self, n1, n2):
        Ex, Ey = self.GetIndex("E")
        n2.previousNode = n1
        n2.gOfN = n1.gOfN + n2.edgeCost
        n2.hOfN = self.distanceManhattan(n2, self.board[Ey][Ex])
        n2.heuristicFn = n2.gOfN + n2.hOfN
        return n2

    def distanceManhattan(self, n1, n2):
        n1x, n1y = self.GetNodeIndex(n1)
        n2x, n2y = self.GetNodeIndex(n2)
        return (abs(n1x - n2x)  + abs(n1y - n2y) )


def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DFS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BFS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.UCS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.AStarEuclideanHeuristic()
    print('**ASTAR with Euclidean Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')

            #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath, TotalCost = searchAlgo.AStarManhattanHeuristic()
    print('**ASTAR with Manhattan Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')


main()
