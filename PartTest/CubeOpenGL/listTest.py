class listTest():
    def __init__(self) -> None:
        self.LIST = [0, 1, 2, 3, 4, 5]

    def alterList(self, i, val):
        self.LIST[i] = val

    def printList(self):
        print(self.LIST)

LT = listTest()

LT.printList()
LT.alterList(0, 5)
LT.alterList(1, 4)
LT.printList()