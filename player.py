class Player:
    def __init__(self, name, max_HP, HP, max_cost, cards):
        self.name = name
        self.image_path = "images/character/"+name+".png"
        self.max_HP = max_HP
        self.HP = max_HP
        self.armor = 0
        self.buff = [0, 0]
        self.debuff = [0, 0, 0]
        self.extra_cards = 0
        self.max_cost = max_cost
        self.cost = max_cost
        self.cards = cards #可能需要改成深拷贝
    def act(self, effect):
        coef = 0.7 if self.debuff[0] > 0 else 1
        temp = effect[:]
        temp[0] = (effect[0] + self.buff[0]) * coef
        return temp
    def affected(self, effect, source):
        coef = 1.5 if self.debuff[1] > 0 else 1
        if source == "enemy":
            damage = round(effect[0] * effect[7] * coef)
            if self.armor >= damage:
                self.armor -= damage
            else:
                self.HP -= (damage - self.armor)
            self.debuff[0] += max(effect[1], 0)
            self.debuff[1] += max(effect[2], 0)
            self.debuff[2] += max(effect[10], 0)
            if self.debuff[2] > 1  and effect[11] > 0:
                self.HP -= round(self.debuff[2] * effect[11] * coef)
                self.debuff[2] = 0
            # return True #决定是否有受击动画
        else:
            self.buff[0] += max(effect[3], 0) #本回合内所有伤害牌伤害数值提高
            self.armor += effect[4] #本回合内所有护盾数值提高
            self.HP = min(self.HP+effect[8], self.max_HP) #回复a点生命值
            #以下仅对玩家生效
            self.extra_cards = effect[5]
            # self.cost = min(self.cost+effect[6], self.max_cost)
            self.cost = self.cost+effect[6]
            self.HP -= effect[9]
            # return False
    def isDead(self):
        return self.HP <= 0 
    def passTurn(self):
        self.buff = [0, 0]
        self.armor = 0
        if self.debuff[2] > 0:
            self.HP -= self.debuff[2]
        for i, d in enumerate(self.debuff):
            if d > 0:
                self.debuff[i] -= 1
        self.cost = self.max_cost