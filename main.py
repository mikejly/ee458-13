import sys
import pygame
import json
import os
from enemy import Enemy
from player import Player
from card import Card
from piles import Piles

def showContent(screen, content, color, font, width, height):
    content = font.render(content, True, color)
    rect = content.get_rect()
    rect.center = (width, height)
    screen.blit(content, rect)
    return [rect, content]

def showImage(screen, path, width, height):
    img = pygame.image.load(path).convert()
    rect = img.get_rect()
    rect.center = (width, height)
    screen.blit(img, rect)
    return [rect, img]

def cardAnalyzer(id):
    effect = [0]
    with open("data/cards.json", "r") as f:
        data = json.load(f)
    if data[id]["name"] == "attack":
        effect[0] = data[id]["value"]
    elif data[id]["name"] == "heavy_attack":
        effect[0] = data[id]["value"]
    return effect

def initialization():
    save0 = 0 if not os.path.exists('data/save0.json') else 1
    save1 = 0 if not os.path.exists('data/save1.json') else 2
    save2 = 0 if not os.path.exists('data/save2.json') else 3
    cards = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1] #简单化处理
    player = Player("character1", 50, 50, cards)
    data = {
        "map": [0, 0, 0, 0, 0], 
        "player" : player.__dict__,
        "enemies_ids" : [[0], [0, 0], [0, 0, 0], [0], [0]]
        }
    with open("data/data.json", "w") as f:
        json.dump(data, f, indent = 2)
    saves = {"saves" : [save0, save1, save2]}
    with open("data/saves.json", "w") as f:
        json.dump(saves, f, indent = 2)


def showStartInterface(screen, width, height, clock):
    screen.fill((0,0,0))
    tfont = pygame.font.Font('font/simkai.ttf', 30)
    cfont = pygame.font.Font('font/simkai.ttf', 20)
    showContent(screen, 'Mega Frog Game', (255, 255, 255), tfont, 400, 50)
    c1_rect = showContent(screen, '开始游戏', (0, 0, 255), cfont, 400, 300)[0]
    c2_rect = showContent(screen, '继续游戏', (0, 0, 255), cfont, 400, 400)[0]
    c3_rect = showContent(screen, '退出', (0, 0, 255), cfont, 400, 500)[0]
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            clock.tick(60)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if c1_rect.collidepoint(event.pos):
                    return "start"
                elif c2_rect.collidepoint(event.pos):
                    return "continue"
                elif c3_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def showMapInterface(screen, width, height, clock):
    cfont = pygame.font.Font('font/simkai.ttf', 50)
    img_paths = ["images/icons/unconquered.png", "images/icons/conquered.png"]
    with open("data/data.json", "r") as f:
        map_data = json.load(f)["map"]
    while True:
        for event in pygame.event.get():
            clock.tick(60)
            screen.fill((255, 255, 255))
            save = showContent(screen, '保存', (0, 0, 0), cfont, 200, 100)[0]
            load = showContent(screen, '读取', (0, 0, 0), cfont, 600, 100)[0]
            e0 = showImage(screen, img_paths[map_data[0]], 200 , 300)[0]
            e1 = showImage(screen, img_paths[map_data[1]], 300 , 300)[0]
            e2 = showImage(screen, img_paths[map_data[2]], 400 , 300)[0]
            e3 = showImage(screen, img_paths[map_data[3]], 500 , 300)[0]
            e4 = showImage(screen, img_paths[map_data[4]], 600 , 300)[0]
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if e0.collidepoint(event.pos) and not map_data[0]:
                    return 0
                if e1.collidepoint(event.pos) and not map_data[1]:
                    return 1
                if e2.collidepoint(event.pos) and not map_data[2]:
                    return 2
                if e3.collidepoint(event.pos) and not map_data[3]:
                    return 3
                if e4.collidepoint(event.pos) and not map_data[4]:
                    return 4
                if save.collidepoint(event.pos):
                    showSaveAndLoadInterface(screen, width, height, clock, "save")
                if load.collidepoint(event.pos):
                    map_data = showSaveAndLoadInterface(screen, width, height, clock, "load")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def showSaveAndLoadInterface(screen, width, height, clock, state):
    screen.fill((255, 255, 255))
    cfont = pygame.font.Font('font/simkai.ttf', 50)
    save_dict = {0: "空", 1: "存档1", 2: "存档2", 3 : "存档3"}
    with open("data/data.json", "r") as f:
        data = json.load(f)
    with open("data/saves.json", "r") as f:
        saves = json.load(f)
    save0 = showContent(screen, save_dict[saves["saves"][0]], (0, 0, 0), cfont, 400, 100)[0]
    save1 = showContent(screen, save_dict[saves["saves"][1]], (0, 0, 0), cfont, 400, 300)[0]
    save2 = showContent(screen, save_dict[saves["saves"][2]], (0, 0, 0), cfont, 400, 500)[0]
    pygame.display.update()
    save_num = -1
    while True:
        for event in pygame.event.get():
            clock.tick(60)
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
                        with open("data/save"+str(save_num)+".json", "r") as f:
                            data = json.load(f)
                        with open("data/data.json", "w") as f:
                            json.dump(data, f, indent = 2)
                        return data["map"]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def showBattleInterface(screen, width, height, clock, e_id):
    cfont = pygame.font.Font('font/simkai.ttf', 15)
    with open("data/data.json", "r") as f:
        data = json.load(f)
        player_data = data["player"]
        enemies_ids = data["enemies_ids"][e_id]
    player = Player(
        player_data["name"], 
        player_data["max_HP"], 
        player_data["HP"], 
        player_data["cards"])
    cards_keys = player_data["cards"]
    with open("data/cards.json", "r") as f:
        cards_data = json.load(f)
        # cards_keys = [*data]
    cards = []
    for key in cards_keys:
        cards.append(Card(
            cards_data[str(key)]["name"],
            cards_data[str(key)]["value"],
            cards_data[str(key)]["image_path"]
            ))
    with open("data/enemies.json", "r") as f:
        enemy_data = json.load(f) 
    enemies = []
    for i in enemies_ids:
        enemy = Enemy(
            enemy_data[str(i)]["name"], 
            enemy_data[str(i)]["image_path"],
            enemy_data[str(i)]["max_HP"],
            enemy_data[str(i)]["armor"],
            enemy_data[str(i)]["damage"],
            enemy_data[str(i)]["action_list"],
            enemy_data[str(i)]["actual_list"])
        enemies.append(enemy)
    player_hit = False
    enemy_hit = False
    loop = 1
    shift = [0, 10, -10]
    piles = Piles(cards_keys)
    if piles.heap_num < piles.HANDMAX:
        piles.resetcard()
    piles.dealcard()
    lock = False
    locked_card = -1
    while True:
        for event in pygame.event.get():
            for i in range(loop):
                clock.tick(60)
                screen.fill((255, 255, 255))
                if player_hit:
                    showImage(screen, player.image_path, 50+shift[i%3] , 400+50)
                    enemy_img = showImage(screen, enemies[0].image_path, 700+50, 50)
                elif enemy_hit:
                    showImage(screen, player.image_path, 50 , 400+50)
                    enemy_img = showImage(screen, enemies[0].image_path, 700+50+shift[i%3], 50)
                else:
                    showImage(screen, player.image_path, 50 , 400+50)
                    enemy_img = showImage(screen, enemies[0].image_path, 700+50, 50)
                screen.blit(enemy_img[1], enemy_img[0])
                showContent(screen, 'HP: '+str(player.HP)+'/'+str(player.max_HP), (0, 0, 0), cfont, 50, 400-10)
                showContent(screen, 'HP: '+str(enemies[0].HP)+'/'+str(enemies[0].max_HP), (0, 0, 0), cfont, 700+50, 100+10)
                cards_rect = []
                for i, key in enumerate(piles.hand_pile):
                    # print(locked_card, lock)
                    if i == locked_card and lock:
                        cards_rect.append(showImage(screen, cards[key].image_path, 50+100*i, 500+50-20)[0])
                    else:
                        cards_rect.append(showImage(screen, cards[key].image_path, 50+100*i, 500+50)[0])
                endTurn_rect = showImage(screen, "images/others/endTurn.png", 700+50, 400)[0]
                showContent(screen, '牌堆：'+str(piles.heap_num), (0, 0, 0), cfont, 50, 300)
                showContent(screen, '弃牌堆：'+str(piles.discard_num), (0, 0, 0), cfont, 750, 300)
                pygame.display.update()
            loop = 1
            player_hit = False
            enemy_hit = False
            if enemies[0].isDead():
                pygame.display.update()
                with open("data/data.json", "r") as f:
                    data = json.load(f)
                data["map"][e_id] = 1
                data["player"]["HP"] = player.HP
                with open("data/data.json", "w") as f:
                    json.dump(data, f, indent = 2)
                return True
            elif player.isDead():
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, card_rect in enumerate(cards_rect):
                    if card_rect.collidepoint(event.pos):
                        if not lock:
                            lock = True
                            locked_card = i
                        else:
                            lock = False #目前点击任何其他牌都会解锁
                        break
                if enemy_img[0].collidepoint(event.pos) and lock:
                    enemies[0].affected(cardAnalyzer(str(piles.hand_pile[i]))) #待修改,改成类相关？
                    enemy_hit = True
                    piles.playcard(i)
                    lock = False
                if endTurn_rect.collidepoint(event.pos):
                    player.affected(enemies[0].act())
                    player_hit = True
                    piles.discardcard()
                    if piles.heap_num < piles.HANDMAX:
                        piles.resetcard()
                    piles.dealcard()
                loop = 20
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def showEndInterface(screen, width, height, clock, result):
    screen.fill((255, 255, 255))
    font1 = pygame.font.Font('font/simkai.ttf', 15)
    font2 = pygame.font.Font('font/simkai.ttf', 50)
    if result == True:
        showContent(screen, "你胜利了！", (0, 0, 0), font2, 400, 300)[0]
    else:
        showContent(screen, "你输了！", (0, 0, 0), font2, 400, 300)[0]
    showContent(screen, "点击任意位置返回开始界面", (0, 0, 0), font1, 400, 500)[0]
    pygame.display.update()
    rect = screen.get_rect()
    while True:
        for event in pygame.event.get():
            clock.tick(60)
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
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mega Frog Game")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            clock.tick(60)
            start_choice = showStartInterface(screen, width, height, clock)
            if start_choice == "start":
                initialization()
            while True:
                map_choice = showMapInterface(screen, width, height, clock)
                if map_choice <= 4: #简单化处理
                    result = showBattleInterface(screen, width, height, clock, map_choice)
                    if result == True:
                        if map_choice == 4:
                            showEndInterface(screen, width, height, clock, result)
                            break
                    else:
                        showEndInterface(screen, width, height, clock, result)
                        break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
	main()