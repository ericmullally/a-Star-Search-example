
import sys
import math
from Node import Node

from PySide6 import QtWidgets, QtGui, QtCore
from mainGrid import Ui_MainWindow

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(Main, self).__init__()
        self.setupUi(self)
        self.start = (0,0)
        self.end = (27,10)
        self.nodes = self.makeGrid(30,30)
        self.setStartAndEnd(self.start, self.end)
        self.setNeighbors()
        self.Astar(self.start, self.end )

    def makeGrid(self, len: int, width: int) -> list:
        """ 
        creates a grid of node objects 
        and returns them in a 2d list.
        """
        grid = []
        for i in range(0, len):
            innerList = []
            for j in range(0, width):  
                node = Node(i,j)
                newButton = QtWidgets.QPushButton("X")
                newButton.setStyleSheet("color:white;")
                self.mainGrid.addWidget(newButton, node.position[0],node.position[1] )
                innerList.append(node)
            grid.append(innerList)
        return grid

    def setStartAndEnd(self, start : tuple, end: tuple):
        startButton = self.mainGrid.itemAtPosition(start[0], start[1]).widget()
        endButton = self.mainGrid.itemAtPosition(end[0], end[1]).widget()
        startNode = self.nodes[start[0]][start[1]]
        endNode = self.nodes[end[0]][end[1]]
        startNode.dLocal = 0
        startNode.dGlobal = self.getDistance(startNode, endNode)
        startButton.setText("S")
        endButton.setText("E")
        startButton.setStyleSheet("background-color:green;")
        endButton.setStyleSheet("background-color:red;")
    
    def getDistance(self, startNode, endNode): 
        """
        uses pathagarian therom to get distance.
        sets the start node dGlobal variable.       
        """
        yDistance = abs( endNode.position[0] - startNode.position[0])
        xDistance = abs(endNode.position[1] - startNode.position[1])

        return math.sqrt(xDistance**2 + yDistance**2)

    def Astar(self, start:tuple, end:tuple):
        startNode = self.nodes[start[0]][start[1]]
        endNode = self.nodes[end[0]][end[1]]
        notTestedNodes = []
        notTestedNodes.append(startNode)

        while(len(notTestedNodes) > 0 ):
            notTestedNodes.sort(key= lambda x: x.dGlobal, reverse=True)
            currentNode = notTestedNodes.pop()

            if(currentNode is endNode):
                break

            if(not currentNode.visited):
               currentNode.visited = True 

               if(not currentNode is startNode): 
                    btn = self.mainGrid.itemAtPosition(currentNode.position[0], currentNode.position[1])
                    btn.widget().setStyleSheet("background-color:yellow;")

               for i in currentNode.neighbors:
                    if(not i.visited and not i in notTestedNodes):
                       notTestedNodes.append(i)

                    estmimattedLocalGoal = currentNode.dLocal + self.getDistance(currentNode, i)
                    if(estmimattedLocalGoal < i.dLocal):
                        i.dLocal = estmimattedLocalGoal
                        i.parent = currentNode
                        i.dGlobal = i.dLocal + self.getDistance(i, endNode) 
                    

        self.showPath(endNode)     
           
    def showPath(self, endNode):
        currentNode = endNode
        currentBtn = self.mainGrid.itemAtPosition(currentNode.position[0], currentNode.position[1]) 
        while currentNode.parent != None:
            if(not currentNode is endNode):
                currentBtn.widget().setText("")
                currentBtn.widget().setStyleSheet("background-color: blue;")
            currentNode = currentNode.parent
            currentBtn = self.mainGrid.itemAtPosition(currentNode.position[0], currentNode.position[1]) 
     
    def setNeighbors(self):
        """
        sets neighbors of all nodes
        if the node is on an edge it sets those neighbors to none 
        then filters them out of the final list
        """
        
        for i in range(0, len(self.nodes)):
            maxJ = len(self.nodes[i]) -1
            maxI = len(self.nodes) -1

            for j in range(0, len(self.nodes[i]) ):
                currentNode = self.nodes[i][j]
                dAbove = self.nodes[i-1][j]     if i !=0 else None 
                lAbove = self.nodes[i-1][j - 1] if i != 0 and j != 0 else None 
                rAbove = self.nodes[i-1][j + 1] if i != 0 and j != maxJ else None 
                lMid = self.nodes[i][j-1]       if j != 0 else None
                rMid = self.nodes[i][j+1]       if j != maxJ else None
                lBottom = self.nodes[i+1][j-1]  if i != maxI and j != 0 else None
                dBotttom = self.nodes[i+1][j]   if i != maxI else None 
                rBottom = self.nodes[i+1][j+1]  if i != maxI and j != maxJ else None

                neighborListToFilter = [dAbove, lAbove, rAbove, lMid, rMid, lBottom, dBotttom, rBottom]
                neighborList = [x for x in neighborListToFilter if x != None ]

                currentNode.neighbors = neighborList

                



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
