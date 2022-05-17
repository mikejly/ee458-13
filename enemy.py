class Enemy:
    def __init__(self, name, image_path, max_HP, armor, damage, action_list, actual_list):
        self.name = name
        # self.image_path = "images/enemy/"+name+".png"
        self.image_path = image_path
        self.max_HP = max_HP
        self.armor = armor
        self.buff = [0, 0] # 伤害数值增加a点, 护甲数值增加a点
        self.debuff = [0, 0, 0] # 伤害减益剩余a回合 受伤增益剩余a回合 流血剩余a回合
        self.damage = damage
        self.HP = max_HP
        self.action_list = action_list
        self.actual_list = actual_list
    def act(self):
        # return self.cards[0]
        effect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        action = self.actual_list[0] #简单化处理
        a = self.action_list[action]
        if action == 0: #造成伤害公式	基础伤害数值*a+伤害增益
            effect[8] = self.damage * a + self.buff[0]
        elif action == 1: #造成伤害公式	（基础伤害数值+伤害增益）*a
            effect[8] = (self.damage + self.buff[0]) * a
        elif action == 2: #玩家a回合内造成伤害减少30%
            effect[0] = a
        elif action == 3: #玩家a回合内受到伤害增加50%
            effect[1] = a
        elif action == 4: #为所有怪物单位恢复a点生命值
            effect[7] = a #目前无法生效?
        elif action == 5: #获得a点伤害增益
            self.buff[0] += a
        return effect
    def affected(self, effect):
        self.HP -= effect[0]
    def isDead(self):
        return self.HP <= 0 
    
