from Node import Node

class Main:
    def __init__(self) -> None:
        self.nodes = self.makeGrid(16,16)
        


    def makeGrid(self, len: int, width: int) -> list:
        """ 
        creates a grid of node objects 
        and returns them in a 2d list.
        """
        grid = []
        for i in range(0, width):
            grid.append([Node(i, x) for x in range(0, len) ])
        return grid




if __name__ == "__main__":
    main = Main()
