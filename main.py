import sys
import pygame
import json
import os
import random
from enemy import Enemy
from player import Player
from card import Card
from piles import Piles

def initialization(chara):
    save0 = 0 if not os.path.exists('data/save0.json') else 1
    save1 = 0 if not os.path.exists('data/save1.json') else 2
    save2 = 0 if not os.path.exists('data/save2.json') else 3
    # cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] #简单处理
    # player = Player("character1", 10000, 10000, cards) #简单处理
    if chara == 0:
        cards = [1, 1, 1, 2, 2, 2, 3, 9, 9, 14, 16, 16, 16]
        # cards = [7, 7, 7, 7, 7, 7]
        player = Player("刺客", 80, 80, 5, cards)
    elif chara == 1:
        cards = [1, 1, 1, 1, 2, 2, 2, 2, 3, 5, 5, 12, 12]
        player = Player("骑士", 160, 160, 4, cards)
    elif chara == 2:
        cards = [1, 1, 1, 2, 2, 2, 3, 11, 11, 16, 20, 20]
        player = Player("剑客", 120, 120, 4, cards)
    data = {
        "map": [0, 0, 0, 0, 0], 
        "player" : player.__dict__,
        "enemies_ids" : [[1], [3, 3, 3], [5], [2], [4, 5, 5]],
        "first_level_cards" : [5,6,9,11,12,13,14,16,20],
        "second_level_cards" :[3,4,7,8,10,15,17,18,19]
        }
    with open("data/data.json", "w") as f:
        json.dump(data, f, indent = 2)
    saves = {"saves" : [save0, save1, save2]}
    with open("data/saves.json", "w") as f:
        json.dump(saves, f, indent = 2)

def showContent(screen, content, color, font, width, height):
    content = font.render(content, True, color)
    rect = content.get_rect()
    rect.center = (width, height)
    screen.blit(content, rect)
    return [rect, content]

def showImage(screen, path, width, height):
    img = pygame.image.load(path).convert_alpha()
    rect = img.get_rect()
    rect.center = (width, height)
    screen.blit(img, rect)
    return [rect, img]

def showIllustration(screen, illu_type, obj):
    font = pygame.font.Font('font/simkai.ttf', 20)
    # pygame.draw.rect(screen, (0,0,0), (250, 100, 300, 400), width=1)
    if illu_type == "card":
        showImage(screen, "images/others/说明背景框.png", 400 , 300)
        showContent(screen, obj.name, (0, 0, 0), font, 400, 150+10)
        count = 2
        texts = obj.text.split("，")
        for text in texts:
            showContent(screen, text, (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        showContent(screen, "费用："+str(obj.cost), (0, 0, 0), font, 400, 150+10+30*count)
    elif illu_type == "enemy":
        showImage(screen, "images/others/说明背景框.png", 400 , 300)
        showContent(screen, obj.name, (0, 0, 0), font, 400, 150+10)
        count = 2
        showContent(screen, "护甲："+str(obj.armor), (0, 0, 0), font, 400, 150+10+30*count)
        count += 1
        showContent(screen, "当前状态：", (0, 0, 0), font, 400, 150+10+30*count)
        count += 1
        if obj.buff[0] > 0:
            showContent(screen, "伤害增加"+str(obj.buff[0]), (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        if obj.debuff[0] > 0:
            showContent(screen, "虚弱， 持续"+str(obj.debuff[0])+"回合", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        if obj.debuff[1] > 0:
            showContent(screen, "重伤， 持续"+str(obj.debuff[1])+"回合", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        if obj.debuff[2] > 0:
            showContent(screen, "流血， 持续"+str(obj.debuff[2])+"回合", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        showContent(screen, "下次行动：", (0, 0, 0), font, 400, 150+10+30*count)
        count += 1
        effect = obj.act()
        action = obj.returnAction()
        if action == 0:
            showContent(screen, "造成"+str(effect[0])+"点伤害", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        if action == 1:
            showContent(screen, "造成"+str(effect[0])+"*"+str(effect[7])+"点伤害", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        elif action == 2:
            showContent(screen, "施加"+str(effect[1])+"回合虚弱", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        elif action == 3:
            showContent(screen, "施加"+str(effect[2])+"回合重伤", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        elif action == 4:
            showContent(screen, "群体回复"+str(effect[8])+"点生命值", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        elif action == 5:
            showContent(screen, "永久增加自身"+str(effect[3])+"点伤害", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        elif action == 6:
            showContent(screen, "群体增加"+str(effect[4])+"点护甲", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
    elif illu_type == "player":
        showImage(screen, "images/others/说明背景框.png", 400 , 300)
        showContent(screen, obj.name, (0, 0, 0), font, 400, 150+10)
        count = 2
        showContent(screen, "护甲："+str(obj.armor), (0, 0, 0), font, 400, 150+10+30*count)
        count += 1
        showContent(screen, "当前状态：", (0, 0, 0), font, 400, 150+10+30*count)
        count += 1
        if obj.buff[0] > 0:
            showContent(screen, "伤害增加"+str(obj.buff[0]), (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        if obj.debuff[0] > 0:
            showContent(screen, "虚弱， 持续"+str(obj.debuff[0])+"回合", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        if obj.debuff[1] > 0:
            showContent(screen, "重伤， 持续"+str(obj.debuff[1])+"回合", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
        if obj.debuff[2] > 0:
            showContent(screen, "流血， 持续"+str(obj.debuff[2])+"回合", (0, 0, 0), font, 400, 150+10+30*count)
            count += 1
    elif illu_type == "pile":
        showImage(screen, "images/others/说明背景框.png", 400 , 300)
        if obj[1] == 0:
            showContent(screen, "牌堆", (0, 0, 0), font, 400, 150+10)
        else:
            showContent(screen, "弃牌堆", (0, 0, 0), font, 400, 150+10)
        count = 2
        with open("data/cards.json", "rb") as f:
            cards_data = json.load(f)
        for i,card in enumerate(obj[0]):
            showContent(screen, cards_data[str(card)]["name"], (0, 0, 0), font, 320+160*(i%2), 150+10+30*(count//2))
            count += 1
    elif illu_type == "chara":
        if obj == 0:
            showImage(screen, 'images/others/角色背景框.png', 200, 300)
            text = " 刺客"
            showContent(screen, text, (0, 0, 0), font, 200, 200+30*1)
            text = "一位灵活的角色"
            showContent(screen, text, (0, 0, 0), font, 200, 200+30*3)
            text = "擅长运用流血"
            showContent(screen, text, (0, 0, 0), font, 200, 200+30*4)
            text = "折磨他的敌人"
            showContent(screen, text, (0, 0, 0), font, 200, 200+30*5)
        elif obj == 1:
            showImage(screen, 'images/others/角色背景框.png', 400, 300)
            text = "骑士"
            showContent(screen, text, (0, 0, 0), font, 400, 200+30*1)
            text = "一位坚毅的角色"
            showContent(screen, text, (0, 0, 0), font, 400, 200+30*3)
            text = "擅长攻击敌人"
            showContent(screen, text, (0, 0, 0), font, 400, 200+30*4)
            text = "同时护卫自身"
            showContent(screen, text, (0, 0, 0), font, 400, 200+30*5)
        elif obj == 2:
            showImage(screen, 'images/others/角色背景框.png', 600, 300)
            text = "剑客"
            showContent(screen, text, (0, 0, 0), font, 600, 200+30*1)
            text = "一位优雅的角色"
            showContent(screen, text, (0, 0, 0), font, 600, 200+30*3)
            text = "擅长削弱敌人"
            showContent(screen, text, (0, 0, 0), font, 600, 200+30*4)
            text = "后将其击垮"
            showContent(screen, text, (0, 0, 0), font, 600, 200+30*5)
    pygame.display.update()

def showStartInterface(screen, width, height, clock):
    showImage(screen, "images/others/主界面.png", 400 , 300)
    tfont = pygame.font.Font('font/simkai.ttf', 30)
    cfont = pygame.font.Font('font/simkai.ttf', 20)
    showContent(screen, 'Mega Frog Game', (255, 255, 255), tfont, 400, 50)
    c_rect = [None,None,None]
    c_rect[0] = showContent(screen, '开始游戏', (255, 255, 255), cfont, 400, 300)[0]
    c_rect[1] = showContent(screen, '继续游戏', (255, 255, 255), cfont, 400, 400)[0]
    c_rect[2] = showContent(screen, '退出', (255, 255, 255), cfont, 400, 500)[0]
    clock.tick(60)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            # clock.tick(60)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if c_rect[0].collidepoint(event.pos):
                    return "start"
                elif c_rect[1].collidepoint(event.pos):
                    return "continue"
                elif c_rect[2].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            else:
                for i in range(3):
                    if c_rect[i].collidepoint(pygame.mouse.get_pos()):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def showCharaInterface(screen, width, height, clock):
    tfont = pygame.font.Font('font/simkai.ttf', 30)
    while True:
        for event in pygame.event.get():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            showImage(screen, 'images/others/界面1.png', 400, 300)
            showImage(screen, 'images/others/角色背景框.png', 200, 300)
            showImage(screen, 'images/others/角色背景框.png', 400, 300)
            showImage(screen, 'images/others/角色背景框.png', 600, 300)
            showContent(screen, '请选择你的角色', (255, 255, 255), tfont, 400, 50)
            c_rect = [None,None,None]
            c_rect[0] = showImage(screen, 'images/character/刺客.png', 200, 300)[0]
            c_rect[1] = showImage(screen, 'images/character/骑士.png', 400, 300)[0]
            c_rect[2] = showImage(screen, 'images/character/剑客.png', 600, 300)[0]
            clock.tick(60)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    if c_rect[i].collidepoint(event.pos):
                        return i
            else:
                for i in range(3):
                    if c_rect[i].collidepoint(pygame.mouse.get_pos()):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        showIllustration(screen, "chara", i)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def showMapInterface(screen, width, height, clock):
    cfont = pygame.font.Font('font/simkai.ttf', 30)
    with open("data/data.json", "rb") as f:
        map_data = json.load(f)["map"]
    loc = [[195,245],[270,305],[475,350],[565,280],[570,185]]
    e = [0,0,0,0,0]
    while True:
        for event in pygame.event.get():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            showImage(screen, "images/others/大地图.png", 400 , 300)
            save = showContent(screen, '保存', (255, 255, 255), cfont, 100+15, 50+10)[0]
            load = showContent(screen, '读取', (255, 255, 255), cfont, 700-15, 50+10)[0]
            for i in range(len(e)):
                e[i] = pygame.Rect((loc[i][0]-10, loc[i][1]-10),(20,20))
                if map_data[i]:
                    showImage(screen, "images/icons/攻克.png", loc[i][0], loc[i][1])
            clock.tick(60)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(e)):
                    if e[i].collidepoint(event.pos) and (i == 0 or map_data[i-1]) and (not map_data[i]):
                        return i
                if save.collidepoint(event.pos):
                    showSaveAndLoadInterface(screen, width, height, clock, "save")
                if load.collidepoint(event.pos):
                    map_data = showSaveAndLoadInterface(screen, width, height, clock, "load")
            else:
                for i in range(len(e)):
                    if e[i].collidepoint(pygame.mouse.get_pos()):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                if save.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                if load.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def showSaveAndLoadInterface(screen, width, height, clock, state):
    #改光标
    showImage(screen, "images/others/保存界面.png", 400 , 300)
    cfont = pygame.font.Font('font/simkai.ttf', 50)
    save_dict = {0: "空", 1: "存档1", 2: "存档2", 3 : "存档3"}
    with open("data/data.json", "rb") as f:
        data = json.load(f)
    with open("data/saves.json", "rb") as f:
        saves = json.load(f)
    save0 = showContent(screen, save_dict[saves["saves"][0]], (0, 0, 0), cfont, 600, 100)[0]
    save1 = showContent(screen, save_dict[saves["saves"][1]], (0, 0, 0), cfont, 600, 300)[0]
    save2 = showContent(screen, save_dict[saves["saves"][2]], (0, 0, 0), cfont, 600, 500)[0]
    clock.tick(60)
    pygame.display.update()
    save_num = -1
    while True:
        for event in pygame.event.get():
            # clock.tick(60)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save0.collidepoint(event.pos):
                    save_num = 0
                elif save1.collidepoint(event.pos):
                    save_num = 1
                elif save2.collidepoint(event.pos):
                    save_num = 2
                if save_num >= 0:
                    if state == "save":
                        with open("data/save"+str(save_num)+".json", "w") as f:
                            json.dump(data, f, indent = 2)
                        saves["saves"][save_num] = save_num+1
                        with open("data/saves.json", "w") as f:
                            json.dump(saves, f, indent = 2)
                        return 0
                    elif state == "load":
                        with open("data/save"+str(save_num)+".json", "rb") as f:
                            data = json.load(f)
                        with open("data/data.json", "w") as f:
                            json.dump(data, f, indent = 2)
                        return data["map"]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def showBattleInterface(screen, width, height, clock, e_id):
    # pygame.mixer.music.load("bgm/battle.mp3")
    # pygame.mixer.music.play()
    cfont = pygame.font.Font('font/simkai.ttf', 15)
    font2 = pygame.font.Font('font/simkai.ttf', 10)
    #角色，卡牌，怪物初始化
    with open("data/data.json", "rb") as f:
        data = json.load(f)
        player_data = data["player"]
        enemies_ids = data["enemies_ids"][e_id]
    player = Player(
        player_data["name"], 
        player_data["max_HP"],
        player_data["HP"], 
        player_data["max_cost"], 
        player_data["cards"])
    cards_keys = player_data["cards"]
    with open("data/cards.json", "rb") as f:
        cards_data = json.load(f)
        # cards_keys = [*data]
    cards = {} #不同种类而非数量
    for key in cards_keys:
        cards[str(key)] = Card(
            cards_data[str(key)]["name"],
            cards_data[str(key)]["text"],
            cards_data[str(key)]["image"],
            cards_data[str(key)]["cost"],
            cards_data[str(key)]["object"],
            cards_data[str(key)]["type"],
            cards_data[str(key)]["trigger"],
            cards_data[str(key)]["effect"],
            )
    with open("data/enemies.json", "rb") as f:
        enemy_data = json.load(f) 
    enemies = []
    for i in enemies_ids:
        enemy = Enemy(
            enemy_data[str(i)]["name"], 
            enemy_data[str(i)]["image"],
            enemy_data[str(i)]["HP"],
            enemy_data[str(i)]["damage"],
            enemy_data[str(i)]["action_list"],
            enemy_data[str(i)]["actual_list"])
        enemies.append(enemy)
    #受击抖动相关
    player_hit = False
    player_buffed = False #强化动画？
    enemies_hit = []
    enemies_buffed = []
    for i in range(len(enemies)):
        enemies_hit.append(False)
        enemies_buffed.append(False)
    loop = 1
    shift = [0, 10, -10]
    enemies_loc = [[700, 200], [600, 250], [700, 300]]
    #点击锁定相关
    lock = False
    selected_card_key = -1  #在手牌中的位置
    prev_card_type = -1
    #牌堆初始化
    piles = Piles(cards_keys, 5) #设定初始5张手牌
    if piles.heap_num < piles.HANDMAX:
        piles.resetcard()
    piles.dealcard()
    while True:
        for event in pygame.event.get():
            for j in range(loop): #控制受击动画的循环
                # screen.fill((255, 255, 255))
                showImage(screen, "images/others/地图"+str(e_id+1)+".png", 400 , 300)
                enemies_rects = []
                if player_hit:
                    player_rect = showImage(screen, player.image_path, 100+shift[j%3], 250)[0]
                else:
                    player_rect = showImage(screen, player.image_path, 100, 250)[0]
                for i, enemy_hit in enumerate(enemies_hit):
                    if enemy_hit:
                        enemies_rects.append(showImage(
                            screen, 
                            enemies[i].image_path, 
                            enemies_loc[i][0]+50+shift[j%3], 
                            enemies_loc[i][1]
                            )[0])
                    else:
                        enemies_rects.append(showImage(
                            screen, 
                            enemies[i].image_path,  
                            enemies_loc[i][0]+50, 
                            enemies_loc[i][1]
                            )[0])
                #显示角色怪物血条，费
                showImage(screen, "images/icons/费.png", 50, 450)
                showContent(screen, str(player.cost)+'/'+str(player.max_cost), (0, 0, 0), cfont, 50, 450)
                scale = player.HP/player.max_HP
                pygame.draw.rect(screen, (255,0,0), (50, 350, 100*scale, 10), 0)
                showContent(screen, str(player.HP)+'/'+str(player.max_HP), (0, 0, 0), font2, 50+50, 350+5)
                for i in range(len(enemies)):
                    scale = enemies[i].HP/enemies[i].max_HP
                    pygame.draw.rect(screen, (255,0,0), (enemies_loc[i][0], enemies_loc[i][1]+50, 100*scale, 10), 0)
                    showContent(
                        screen, 
                        str(enemies[i].HP)+'/'+str(enemies[i].max_HP), 
                        (0, 0, 0), 
                        font2, 
                        enemies_loc[i][0]+50, 
                        enemies_loc[i][1]+50+5
                        )
                #显示角色手牌
                cards_rect = []
                for i, key in enumerate(piles.hand_pile):
                    if i == selected_card_key and lock:
                        cards_rect.append(showImage(screen, cards[str(key)].image_path, 150+100*i, 500+50-20)[0])
                    else:
                        cards_rect.append(showImage(screen, cards[str(key)].image_path, 150+100*i, 500+50)[0])
                endTurn_rect = showImage(screen, "images/icons/图标框1.png", 700, 450)[0]
                showContent(screen, "结束回合", (255,255,255), cfont, 700, 450+5)
                h_pile_rect = showImage(screen, "images/icons/牌堆.png", 50, 550)[0]
                d_pile_rect = showImage(screen, "images/icons/牌堆.png", 750, 550)[0]
                # showContent(screen, '牌堆：'+str(piles.heap_num), (0, 0, 0), cfont, 50, 550)
                # showContent(screen, '弃牌堆：'+str(piles.discard_num), (0, 0, 0), cfont, 750, 550)
                clock.tick(60)
                pygame.display.update()
            #部分参数初始化
            player_hit = False
            player_buffed = False
            for i in range(len(enemies)):
                enemies_hit[i] = False
                enemies_buffed[i] = False
            loop = 1
            all_dead = True
            #战斗结果判定
            for i in range(len(enemies)):
                if not enemies[i].isDead():
                    all_dead = False
            if all_dead:
                pygame.display.update()
                with open("data/data.json", "rb") as f:
                    data = json.load(f)
                data["map"][e_id] = 1
                data["player"]["HP"] = player.HP
                with open("data/data.json", "w") as f:
                    json.dump(data, f, indent = 2)
                return True
            elif player.isDead():
                return False
            #鼠标点击事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                #点击手牌
                for i, card_rect in enumerate(cards_rect):
                    if card_rect.collidepoint(event.pos):
                        if not lock and cards[str(piles.hand_pile[i])].cost <= player.cost:
                            lock = True
                            selected_card_key = i
                            selected_card = cards[str(piles.hand_pile[selected_card_key])]
                        else:
                            lock = False #目前点击任何其他牌都会解锁
                        break
                #点击怪物或角色头像
                flag = False
                if lock:
                    #是否有额外触发条件
                    if selected_card.trigger[0] or selected_card.trigger[1]:
                        effect = selected_card.untriggered()
                    else:
                        effect = selected_card.effect[:]
                    if selected_card.action_object != 0: #对怪物释放
                        for i in range(len(enemies)):
                            if not enemies[i].isDead():
                                if enemies_rects[i].collidepoint(event.pos):
                                    flag = True #是否影响全体怪物
                                    if selected_card.action_object == 1:
                                        enemies[i].affected(player.act(effect), "enemy")
                                        if selected_card.trigger[0] == prev_card_type:
                                            triggered = selected_card.triggered()
                                            enemies[i].affected(player.act(triggered), "enemy")
                                        elif selected_card.trigger[1] and enemies[i].isDead():
                                            triggered = selected_card.triggered()
                                            player.affected(triggered, "self")
                                        enemies_hit[i] = True
                        if flag and selected_card.action_object == 2:
                            for i in range(len(enemies)):
                                if not enemies[i].isDead():
                                    enemies[i].affected(player.act(effect), "enemy")
                                    if selected_card.trigger[0] == prev_card_type:
                                        triggered = selected_card.triggered()
                                        enemies[i].affected(player.act(triggered), "enemy")
                                    elif selected_card.trigger[1] and enemies[i].isDead():
                                        triggered = selected_card.triggered()
                                        player.affected(triggered, "self")
                                    enemies_hit[i] = True
                    else: #对自己释放
                        if player_rect.collidepoint(event.pos):
                            player.affected(effect, "self")
                            if selected_card.trigger[0] == prev_card_type:
                                triggered = selected_card.triggered()
                                player.affected(triggered, "self")
                            player_buffed = True
                            if player.extra_cards > 0:
                                if piles.heap_num < player.extra_cards:
                                    piles.resetcard()
                                piles.dealcard(player.extra_cards)
                #卡牌使用结算
                if (True in enemies_hit) or player_buffed:
                    player.cost -= selected_card.cost
                    piles.playcard(selected_card_key)
                    lock = False
                    prev_card_type = selected_card.card_type
                    if selected_card.name == "护盾打击": #临时修改，涉及底层机制,待会改
                        player.armor += 7
                #点击结束回合
                if endTurn_rect.collidepoint(event.pos):#只会有一次动画
                    lock = False
                    for i in range(len(enemies)):
                        if not enemies[i].isDead():
                            player.affected(enemies[i].act(), "enemy")
                            player_hit = True  if enemies[i].returnAction() in [0, 1, 2, 3] else False
                            enemies[i].passTurn()
                    for i in range(len(enemies)):
                        if not enemies[i].isDead():
                            for j in range(len(enemies)):
                                if j == i: #怪物对自己生效
                                    enemies[j].affected(enemies[i].act(), "self")
                                else:   #怪物对队友生效
                                    enemies[j].affected(enemies[i].act(), "ally")
                            enemies[i].passAction()
                    piles.discardcard()
                    if piles.heap_num < piles.HANDMAX:
                        piles.resetcard()
                    piles.dealcard()
                    player.passTurn()
                loop = 10
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #鼠标悬停事件
            else:
                for i, card_rect in enumerate(cards_rect):
                    if card_rect.collidepoint(pygame.mouse.get_pos()):
                        showIllustration(screen, "card", cards[str(piles.hand_pile[i])])
                for i in range(len(enemies)):
                    if enemies_rects[i].collidepoint(pygame.mouse.get_pos()):
                        showIllustration(screen, "enemy", enemies[i])
                if player_rect.collidepoint(pygame.mouse.get_pos()):
                    showIllustration(screen, "player", player)
                if h_pile_rect.collidepoint(pygame.mouse.get_pos()):
                    showIllustration(screen, "pile", [piles.heap,0])
                if d_pile_rect.collidepoint(pygame.mouse.get_pos()):
                    showIllustration(screen, "pile", [piles.discard_pile,1])

def showBonusInterface(screen, width, height, clock, map_choice):
    font2 = pygame.font.Font('font/simkai.ttf', 50)
    with open("data/data.json", "rb") as f:
        data = json.load(f)
    if map_choice < 2:
        bonus = data["first_level_cards"]
    else:
        bonus = data["second_level_cards"]
    random.shuffle(bonus)
    bonus = bonus[:6]
    with open("data/cards.json", "rb") as f:
        cards_data = json.load(f)
    cards = {} #不同种类而非数量
    for key in bonus:
        cards[str(key)] = Card(
            cards_data[str(key)]["name"],
            cards_data[str(key)]["text"],
            cards_data[str(key)]["image"],
            cards_data[str(key)]["cost"],
            cards_data[str(key)]["object"],
            cards_data[str(key)]["type"],
            cards_data[str(key)]["trigger"],
            cards_data[str(key)]["effect"],
            )
    while True:
        for event in pygame.event.get():
            showImage(screen, 'images/others/界面1.png', 400, 300)
            # screen.fill((255, 255, 255))
            showContent(screen, "你胜利了！点击获取卡牌奖励", (255, 255, 255), font2, 400, 50)[0]
            cards_rect = []
            for i, key in enumerate(bonus):
                    cards_rect.append(showImage(screen, cards[str(key)].image_path, 150+100*i, 500+50)[0])
            clock.tick(60)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, card_rect in enumerate(cards_rect):
                    if card_rect.collidepoint(event.pos):
                        data["player"]["cards"].append(bonus[i])
                        with open("data/data.json", "w") as f:
                            json.dump(data, f, indent = 2)
                        return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                for i, card_rect in enumerate(cards_rect):
                    if card_rect.collidepoint(pygame.mouse.get_pos()):
                        showIllustration(screen, "card", cards[str(bonus[i])])

def showEndInterface(screen, width, height, clock, result, map_choice):
    font1 = pygame.font.Font('font/simkai.ttf', 20)
    if result == True:
        showImage(screen, "images/icons/胜利.png",400,150)
    else:
        showImage(screen, "images/icons/失败.png",400,150)
    if map_choice == 4 or result == False:
        showContent(screen, "点击任意位置返回开始界面", (255,255,255), font1, 400, 480)[0]
    else:
        showContent(screen, "点击任意位置继续", (255,255,255), font1, 400, 480)[0]
    clock.tick(60)
    pygame.display.update()
    rect = screen.get_rect()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    width = 800
    height = 600
    pygame.init()
    pygame.mixer.init()
    # pygame.mixer.music.load("bgm/beginning.mp3")
    # pygame.mixer.music.play()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mega Frog Game")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            # clock.tick(60)
            start_choice = showStartInterface(screen, width, height, clock)
            if start_choice == "start":
                chara = showCharaInterface(screen, width, height, clock)
                initialization(chara)
            if start_choice == "continue":
                showSaveAndLoadInterface(screen, width, height, clock, "load")
            while True:
                map_choice = showMapInterface(screen, width, height, clock)
                if map_choice <= 4: #简单化处理
                    result = showBattleInterface(screen, width, height, clock, map_choice)
                    if result == True:
                        showEndInterface(screen, width, height, clock, result, map_choice)
                        if map_choice == 4:
                            break
                        showBonusInterface(screen, width, height, clock, map_choice)
                    else:
                        showEndInterface(screen, width, height, clock, result, map_choice)
                        break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
	main()