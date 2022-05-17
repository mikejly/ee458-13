class Player:
    def __init__(self, name, max_HP, HP, cards):
        self.name = name
        self.image_path = "images/character/"+name+".png"
        self.max_HP = max_HP
        self.HP = HP #待修改
        self.cards = cards
        self.armor = 0
        self.buff = [0, 0]
        self.debuff = [0, 0, 0]
        self.extra_cards = 0
        self.cost = 1
        self.max_cost = 1
    def affected(self, effect):
        self.debuff[0] = effect[0]
        self.debuff[1] = effect[1]
        self.buff[0] = effect[2]
        self.buff[1] = effect[3]
        self.extra_cards = effect[4]
        self.cost += effect[5] #上限？
        # effect[6]
        self.HP += effect[7] #上限？
        self.HP -= effect[8]
        # effect[9], effect[10]
    def isDead(self):
        return self.HP <= 0 