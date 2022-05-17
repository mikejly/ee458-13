import random

class Piles:
    def __init__(self, heap):
        self.heap_num = len(heap)
        self.MAX = self.heap_num
        self.heap = heap
        self.HANDMAX = 3
        self.hand_num = 0
        self.discard_num = 0
        self.hand_pile = []
        self.discard_pile = []
    def dealcard(self):
        num = self.HANDMAX - self.hand_num
        for i in range(0, num):
            if self.heap_num < 1:
                break
            card = random.randint(0, self.heap_num-1)
            self.hand_pile.append(self.heap[card])
            del self.heap[card]
            self.heap_num -= 1
            self.hand_num += 1
    def playcard(self, n):
        self.discard_pile.append(self.hand_pile[n])
        del self.hand_pile[n]
        self.hand_num -= 1
        self.discard_num += 1
        #调用效果函数
    def discardcard(self):
        while self.hand_num > 0:
            self.discard_pile.append(self.hand_pile[0])
            del self.hand_pile[0]
            self.hand_num -= 1
            self.discard_num += 1
    def resetcard(self):
        for i in range(0, self.discard_num):
            self.heap.append(self.discard_pile[0])
            del self.discard_pile[0]
        self.discard_num = 0
        self.heap_num = self.MAX





    
