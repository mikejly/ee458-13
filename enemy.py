class Enemy:
    def __init__(self, name, image_path, HP, damage, action_list, actual_list):
        self.name = name
        self.image_path = image_path
        self.max_HP = HP
        self.HP = HP
        self.armor = 0
        self.buff = [0,0] # 伤害数值增加a点, 护甲数值增加a点
        self.debuff = [0, 0, 0] # 伤害减益剩余a回合 受伤增益剩余a回合 流血剩余a回合
        self.damage = damage
        self.action_list = action_list[:]
        self.actual_list = actual_list[:]
        self.current_action = 0
    def act(self):
        effect = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        action = self.actual_list[self.current_action % len(self.actual_list)]
        a = self.action_list[action]
        coef = 0.7 if self.debuff[0] > 0 else 1
        if action == 0: #造成伤害公式	基础伤害数值*a+伤害增益
            effect[0] = round((self.damage * a + self.buff[0]) * coef)
        elif action == 1: #造成伤害公式	（基础伤害数值+伤害增益）*a
            effect[0] = round(((self.damage + self.buff[0]) * a) * coef)
        elif action == 2: #玩家a回合内造成伤害减少30%
            effect[1] = a
        elif action == 3: #玩家a回合内受到伤害增加50%
            effect[2] = a
        elif action == 4: #为所有怪物单位恢复a点生命值
            effect[8] = a
        elif action == 5: #获得a点伤害增益
            effect[3] = a
        elif action == 6: #所有怪物加护甲
            effect[4] = a
        return effect
    def affected(self, effect, source):
        if not self.isDead():
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
                if self.debuff[2] > 1 and effect[11] > 0:
                    self.HP -= round(self.debuff[2] * effect[11] * coef)
                    self.debuff[2] = 0
            else:
                self.armor += effect[4] #本回合内所有护盾数值提高
                self.HP = min(self.HP+effect[8], self.max_HP) #回复a点生命值
                if source == "self":
                    self.buff[0] += effect[3] #永久提高伤害
                #effect[5], [6], [9]对怪物不生效
    def isDead(self):
        return self.HP <= 0 
    def passTurn(self):
        # self.buff = [0]
        self.armor = 0
        if self.debuff[2] > 0:
            self.HP -= self.debuff[2]
        for i, d in enumerate(self.debuff):
            if d > 0:
                self.debuff[i] -= 1
    def passAction(self):
        self.current_action += 1
    def returnAction(self):
        return self.actual_list[self.current_action % len(self.actual_list)]
        

    
