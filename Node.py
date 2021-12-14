class Node:
    def __init__(self, x, y) -> None:
        self.position = (x,y)
        self.visited = False
        self.parent = None
        self.dGlobal = 99999
        self.dLocal = 99999
        self.neighbors= []

    


