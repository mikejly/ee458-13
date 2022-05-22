class Card:
    def __init__(self, name, text, image_path, cost, action_object, card_type, trigger, effect):
        self.name = name
        self.text = text
        self.image_path = image_path
        self.cost = cost
        self.action_object = action_object
        self.card_type = card_type
        self.trigger = trigger
        self.effect = effect
    def untriggered(self):
        effect = [0,0,0,0,0,0,0,1,0,0,0,0]
        effect[0] = self.effect[0]
        effect[4] = self.effect[4]
        return effect
    def triggered(self):
        effect = self.effect[:]
        effect[0] = 0
        effect[4] = 0
        return effect
        
