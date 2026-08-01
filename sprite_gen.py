import pygame, os, math, random

pygame.init()
SURF = pygame.Surface((1,1))

OUT = "assets/sprites"
os.makedirs(OUT, exist_ok=True)

TW, TH = 16, 16

def save(surf, name):
    pygame.image.save(surf, os.path.join(OUT, name+".png"))
    print(f"  {name}.png")

def spr(w=16, h=16, alpha=True):
    s = pygame.Surface((w,h), pygame.SRCALPHA if alpha else 0)
    s.fill((0,0,0,0) if alpha else (0,0,0))
    return s

def tile_grass():
    s = spr()
    s.fill((40,100,40))
    for _ in range(6):
        bx,by = random.randint(0,13),random.randint(0,13)
        pygame.draw.rect(s,(50,120,50),(bx,by,3,2))
    return s

def tile_road():
    s = spr()
    s.fill((80,80,80))
    pygame.draw.rect(s,(100,100,100),(0,7,16,2))
    return s

def tile_floor():
    s = spr()
    s.fill((100,70,40))
    pygame.draw.rect(s,(90,60,35),(0,0,16,1))
    pygame.draw.rect(s,(90,60,35),(0,0,1,16))
    return s

def tile_cave():
    s = spr()
    s.fill((35,25,40))
    for _ in range(4):
        pygame.draw.rect(s,(50,40,55),(random.randint(0,12),random.randint(0,12),3,2))
    return s

def tile_factory():
    s = spr()
    s.fill((55,55,60))
    pygame.draw.rect(s,(70,70,75),(0,0,16,1))
    pygame.draw.rect(s,(70,70,75),(0,0,1,16))
    pygame.draw.rect(s,(40,40,45),(8,8,1,1))
    return s

def tile_water():
    s = spr()
    s.fill((30,60,120))
    pygame.draw.rect(s,(40,80,150),(0,8,16,3))
    pygame.draw.rect(s,(50,90,160),(3,4,4,2))
    return s

def tile_sand():
    s = spr()
    s.fill((200,170,100))
    for _ in range(4):
        pygame.draw.rect(s,(180,150,80),(random.randint(0,13),random.randint(0,13),3,1))
    return s

def tile_dirt():
    s = spr()
    s.fill((90,60,30))
    for _ in range(3):
        pygame.draw.circle(s,(70,45,20),(random.randint(2,14),random.randint(2,14)),2)
    return s

def tile_wall():
    s = spr()
    s.fill((60,60,70))
    pygame.draw.rect(s,(80,80,90),(0,0,16,16),1)
    pygame.draw.rect(s,(50,50,60),(2,2,12,5))
    pygame.draw.rect(s,(50,50,60),(2,9,12,5))
    return s

def tile_tree():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(80,50,20),(6,10,4,6))
    pygame.draw.circle(s,(30,90,30),(8,6),6)
    pygame.draw.circle(s,(50,110,50),(8,4),4)
    pygame.draw.circle(s,(40,100,40),(5,7),3)
    pygame.draw.circle(s,(40,100,40),(11,7),3)
    return s

def tile_tree_dark():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(60,35,10),(6,10,4,6))
    pygame.draw.circle(s,(15,55,15),(8,6),6)
    pygame.draw.circle(s,(25,70,25),(8,4),4)
    return s

def tile_rock():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.ellipse(s,(90,90,100),(1,4,14,10))
    pygame.draw.ellipse(s,(110,110,120),(2,5,12,8))
    pygame.draw.rect(s,(120,120,130),(4,6,3,2))
    return s

def tile_water_deep():
    s = spr()
    s.fill((15,40,90))
    pygame.draw.rect(s,(20,50,110),(0,7,16,3))
    return s

def tile_bridge():
    s = spr()
    s.fill((0,0,0,0))
    s.fill((100,70,30))
    for bx in range(0,16,4):
        pygame.draw.rect(s,(80,55,20),(bx,0,3,16))
    pygame.draw.rect(s,(120,90,50),(0,6,16,4))
    return s

def tile_dock():
    s = spr()
    s.fill((0,0,0,0))
    s.fill((80,55,25))
    pygame.draw.rect(s,(60,40,15),(0,14,16,2))
    for px in range(0,16,5):
        pygame.draw.rect(s,(60,40,15),(px,0,2,16))
    return s

def tile_pipe():
    s = spr()
    s.fill((70,80,70))
    pygame.draw.rect(s,(90,100,90),(2,5,12,6))
    pygame.draw.rect(s,(110,120,110),(3,6,10,4))
    return s

def tile_pillar():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(100,100,120),(4,0,8,16))
    pygame.draw.rect(s,(140,140,160),(5,1,6,14))
    pygame.draw.rect(s,(80,80,100),(4,0,8,2))
    pygame.draw.rect(s,(80,80,100),(4,14,8,2))
    return s

def tile_algo_node():
    s = spr()
    s.fill((5,5,20))
    pygame.draw.rect(s,(0,200,255),(3,3,10,10))
    pygame.draw.rect(s,(0,150,200),(4,4,8,8))
    pygame.draw.rect(s,(0,255,255),(6,6,4,4))
    pygame.draw.rect(s,(0,200,255),(3,3,10,10),1)
    return s

def tile_portal():
    s = spr()
    s.fill((0,0,0,0))
    t = pygame.time.get_ticks()
    pygame.draw.ellipse(s,(30,0,60),(1,1,14,14))
    pygame.draw.ellipse(s,(100,0,200),(2,2,12,12))
    pygame.draw.ellipse(s,(150,50,255),(4,4,8,8))
    pygame.draw.ellipse(s,(200,100,255),(5,5,6,6))
    return s

def tile_flower():
    s = spr()
    s.fill((0,0,0,0))
    s.fill((40,100,40))
    colors = [(255,80,80),(255,200,50),(200,50,255),(50,200,255)]
    for fx,fy in [(4,8),(10,6),(7,11),(12,10),(3,4)]:
        c = random.choice(colors)
        pygame.draw.circle(s,c,(fx,fy),2)
        pygame.draw.circle(s,(255,255,150),(fx,fy),1)
    return s

def tile_bush():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.circle(s,(25,80,25),(8,10),6)
    pygame.draw.circle(s,(35,95,35),(5,12),4)
    pygame.draw.circle(s,(35,95,35),(11,12),4)
    pygame.draw.circle(s,(45,110,45),(8,8),3)
    return s

def tile_lamp():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(80,80,90),(7,4,2,12))
    pygame.draw.rect(s,(80,80,90),(4,14,8,2))
    pygame.draw.circle(s,(255,220,100),(8,3),3)
    pygame.draw.circle(s,(255,240,150),(8,3),2)
    pygame.draw.circle(s,(255,255,200),(8,3),1)
    return s

def tile_chest():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(120,80,30),(2,8,12,7))
    pygame.draw.rect(s,(160,110,50),(2,8,12,4))
    pygame.draw.rect(s,(100,60,20),(2,8,12,7),1)
    pygame.draw.rect(s,(200,160,50),(6,10,4,3))
    pygame.draw.rect(s,(255,200,50),(7,11,2,2))
    return s

def tile_market():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(180,50,50),(0,2,16,2))
    pygame.draw.rect(s,(200,70,70),(2,4,12,3))
    pygame.draw.rect(s,(150,100,50),(2,7,12,8))
    pygame.draw.rect(s,(120,80,30),(2,7,12,8),1)
    pygame.draw.rect(s,(200,170,80),(4,9,3,4))
    pygame.draw.rect(s,(200,170,80),(9,9,3,4))
    return s

def tile_save():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(20,60,100),(2,2,12,12))
    pygame.draw.rect(s,(40,120,200),(3,3,10,10))
    pygame.draw.rect(s,(0,200,255),(4,4,8,8))
    pygame.draw.rect(s,(200,220,255),(5,6,6,1))
    pygame.draw.rect(s,(200,220,255),(7,4,2,4))
    return s

def tile_sign():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(80,50,10),(7,8,2,8))
    pygame.draw.rect(s,(120,80,30),(2,3,12,6))
    pygame.draw.rect(s,(100,65,25),(2,3,12,6),1)
    pygame.draw.rect(s,(200,180,130),(3,4,10,4))
    return s

def tile_door():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(100,65,25),(3,2,10,14))
    pygame.draw.rect(s,(140,100,50),(4,3,8,12))
    pygame.draw.rect(s,(80,50,10),(3,2,10,14),1)
    pygame.draw.circle(s,(200,150,50),(11,9),2)
    return s

def tile_crate():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(100,80,40),(1,1,14,14))
    pygame.draw.rect(s,(140,110,60),(2,2,12,12))
    pygame.draw.rect(s,(80,60,20),(1,1,14,14),1)
    pygame.draw.line(s,(80,60,20),(1,1),(14,14),1)
    pygame.draw.line(s,(80,60,20),(14,1),(1,14),1)
    return s

def tile_barrel():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.ellipse(s,(100,70,30),(2,1,12,14))
    pygame.draw.ellipse(s,(130,95,50),(3,2,10,12))
    for by in [4,8,12]:
        pygame.draw.line(s,(70,45,15),(2,by),(13,by),1)
    return s

def tile_boat():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.polygon(s,(100,70,30),[(1,10),(15,10),(13,15),(3,15)])
    pygame.draw.rect(s,(120,90,50),(4,10,8,2))
    pygame.draw.rect(s,(80,55,20),(7,3,2,8))
    pygame.draw.polygon(s,(200,200,220),[(9,3),(9,9),(14,6)])
    return s

def tile_fish():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.ellipse(s,(50,120,200),(2,6,10,5))
    pygame.draw.polygon(s,(50,120,200),[(12,7),(15,5),(15,10)])
    pygame.draw.circle(s,(255,255,255),(5,8),1)
    return s

def tile_fence():
    s = spr()
    s.fill((0,0,0,0))
    pygame.draw.rect(s,(120,90,50),(0,4,16,3))
    for fx in [2,7,12]:
        pygame.draw.rect(s,(120,90,50),(fx,0,2,15))
    return s

def tile_stairs_down():
    s = spr()
    s.fill((50,35,20))
    for sy in range(0,16,3):
        pygame.draw.rect(s,(70,50,30),(0,sy,16,2))
        pygame.draw.rect(s,(90,65,40),(2,sy+1,12,1))
    pygame.draw.polygon(s,(200,150,50),[(7,10),(9,10),(8,14)])
    return s

def tile_stairs_up():
    s = spr()
    s.fill((50,35,20))
    for sy in range(0,16,3):
        pygame.draw.rect(s,(70,50,30),(0,sy,16,2))
        pygame.draw.rect(s,(90,65,40),(2,sy+1,12,1))
    pygame.draw.polygon(s,(200,150,50),[(7,6),(9,6),(8,2)])
    return s

def draw_player(direction="down", walk=False):
    s = spr(16, 24)
    body_col = (80,120,200)
    pygame.draw.rect(s, body_col, (4,8,8,10))
    pygame.draw.rect(s, (220,180,140), (4,2,8,8))
    pygame.draw.rect(s, (60,40,20), (4,2,8,3))

    if direction == "down":
        pygame.draw.rect(s,(255,255,255),(5,4,2,2))
        pygame.draw.rect(s,(255,255,255),(9,4,2,2))
        pygame.draw.rect(s,(150,100,80),(6,7,4,1))
        lx = 5 if walk else 4
        pygame.draw.rect(s,(60,80,160),(lx,18,3,6))
        pygame.draw.rect(s,(14-lx+5,80,160),(9,18,3,6))
        pygame.draw.rect(s,(220,180,140),(1,8,3,7))
        pygame.draw.rect(s,(220,180,140),(12,8,3,7))

    elif direction == "up":
        pygame.draw.rect(s,(60,40,20),(4,2,8,5))
        pygame.draw.rect(s,(60,80,160),(4,18,3,6))
        pygame.draw.rect(s,(60,80,160),(9,18,3,6))
        pygame.draw.rect(s,(220,180,140),(1,8,3,7))
        pygame.draw.rect(s,(220,180,140),(12,8,3,7))

    elif direction in ("left","right"):
        flip = direction == "right"
        pygame.draw.rect(s,(255,255,255),(5 if not flip else 9,4,2,2))
        pygame.draw.rect(s,(150,100,80),(5,7,5,1))
        if walk:
            pygame.draw.rect(s,(60,80,160),(4,18,3,7))
            pygame.draw.rect(s,(60,80,160),(9,16,3,7))
        else:
            pygame.draw.rect(s,(60,80,160),(4,18,3,6))
            pygame.draw.rect(s,(60,80,160),(9,18,3,6))
        pygame.draw.rect(s,(220,180,140),(0 if not flip else 13,8,3,7))
        pygame.draw.rect(s,(body_col),(13 if not flip else 0,9,3,6))

    return s

def draw_npc_old():
    s = spr(16,24)
    pygame.draw.rect(s,(100,80,50),(3,8,10,12))
    pygame.draw.rect(s,(120,100,70),(4,9,8,10))
    pygame.draw.rect(s,(200,160,120),(4,2,8,8))
    pygame.draw.rect(s,(200,200,200),(4,2,8,3))
    pygame.draw.rect(s,(180,180,180),(3,4,2,2))
    pygame.draw.rect(s,(180,180,180),(11,4,2,2))
    pygame.draw.rect(s,(255,255,255),(5,4,2,2))
    pygame.draw.rect(s,(255,255,255),(9,4,2,2))
    pygame.draw.rect(s,(150,100,80),(5,7,6,1))
    pygame.draw.rect(s,(80,60,20),(13,8,2,16))
    pygame.draw.rect(s,(80,60,20),(12,8,3,2))
    pygame.draw.rect(s,(70,55,30),(4,20,3,4))
    pygame.draw.rect(s,(70,55,30),(9,20,3,4))
    return s

def draw_npc_girl():
    s = spr(16,24)
    pygame.draw.rect(s,(200,80,150),(3,8,10,12))
    pygame.draw.rect(s,(220,100,170),(4,9,8,10))
    pygame.draw.rect(s,(220,180,140),(4,2,8,8))
    pygame.draw.rect(s,(60,30,100),(3,1,10,4))
    pygame.draw.rect(s,(60,30,100),(3,5,2,6))
    pygame.draw.rect(s,(60,30,100),(11,5,2,6))
    pygame.draw.rect(s,(255,255,255),(5,4,2,2))
    pygame.draw.rect(s,(255,255,255),(9,4,2,2))
    pygame.draw.rect(s,(255,150,180),(6,7,4,1))
    pygame.draw.rect(s,(150,60,120),(4,20,3,4))
    pygame.draw.rect(s,(150,60,120),(9,20,3,4))
    return s

def draw_npc_fisherman():
    s = spr(16,24)
    pygame.draw.rect(s,(40,80,120),(3,8,10,12))
    pygame.draw.rect(s,(50,100,150),(4,9,8,10))
    pygame.draw.rect(s,(200,160,120),(4,2,8,8))
    pygame.draw.rect(s,(30,60,90),(2,1,12,3))
    pygame.draw.rect(s,(40,80,110),(4,2,8,3))
    pygame.draw.rect(s,(255,255,255),(5,4,2,2))
    pygame.draw.rect(s,(255,255,255),(9,4,2,2))
    pygame.draw.rect(s,(150,100,80),(5,7,6,1))
    pygame.draw.rect(s,(80,60,20),(13,5,2,14))
    pygame.draw.line(s,(200,200,200),(14,5),(14,16),1)
    pygame.draw.circle(s,(200,50,50),(14,16),2)
    pygame.draw.rect(s,(30,50,80),(4,20,3,4))
    pygame.draw.rect(s,(30,50,80),(9,20,3,4))
    return s

def draw_npc_engineer():
    s = spr(16,24)
    pygame.draw.rect(s,(80,80,50),(3,8,10,12))
    pygame.draw.rect(s,(100,100,70),(4,9,8,10))
    pygame.draw.rect(s,(200,160,120),(4,2,8,8))
    pygame.draw.rect(s,(200,180,50),(2,1,12,3))
    pygame.draw.rect(s,(180,160,30),(4,2,8,2))
    pygame.draw.rect(s,(255,255,255),(5,4,2,2))
    pygame.draw.rect(s,(255,255,255),(9,4,2,2))
    pygame.draw.rect(s,(60,60,80),(5,5,6,2))
    pygame.draw.rect(s,(200,200,50),(12,12,3,2))
    pygame.draw.circle(s,(200,200,50),(12,13),2)
    pygame.draw.rect(s,(60,60,40),(4,20,3,4))
    pygame.draw.rect(s,(60,60,40),(9,20,3,4))
    return s

def draw_villain():
    s = spr(16,24)
    pygame.draw.rect(s,(20,20,30),(2,7,12,14))
    pygame.draw.rect(s,(35,25,45),(3,8,10,12))
    pygame.draw.rect(s,(180,150,130),(4,2,8,8))
    pygame.draw.rect(s,(10,10,20),(4,2,8,4))
    pygame.draw.rect(s,(20,15,30),(3,4,3,4))
    pygame.draw.rect(s,(20,15,30),(10,4,3,4))
    pygame.draw.rect(s,(200,50,50),(5,4,2,2))
    pygame.draw.rect(s,(200,50,50),(9,4,2,2))
    pygame.draw.rect(s,(100,0,0),(6,7,4,1))
    pygame.draw.rect(s,(15,10,25),(4,20,3,4))
    pygame.draw.rect(s,(15,10,25),(9,20,3,4))
    return s

def draw_algo():
    s = spr(32,40)
    pygame.draw.rect(s,(10,30,60),(4,8,24,26))
    pygame.draw.rect(s,(0,150,220),(6,10,20,22))
    pygame.draw.rect(s,(5,20,50),(6,2,20,8))
    pygame.draw.rect(s,(0,200,255),(8,3,16,6))
    pygame.draw.rect(s,(0,255,255),(9,4,4,4))
    pygame.draw.rect(s,(0,255,255),(19,4,4,4))
    pygame.draw.rect(s,(255,255,255),(10,5,2,2))
    pygame.draw.rect(s,(255,255,255),(20,5,2,2))
    pygame.draw.rect(s,(0,50,100),(8,12,16,12))
    pygame.draw.rect(s,(0,100,200),(9,13,14,10))
    for dy in range(14,22,2):
        pygame.draw.rect(s,(0,220,255),(10,dy,random.randint(2,12),1))
    pygame.draw.rect(s,(0,120,180),(0,8,4,20))
    pygame.draw.rect(s,(0,120,180),(28,8,4,20))
    pygame.draw.rect(s,(0,180,220),(1,9,2,18))
    pygame.draw.rect(s,(0,180,220),(29,9,2,18))
    pygame.draw.rect(s,(0,100,160),(8,34,7,6))
    pygame.draw.rect(s,(0,100,160),(17,34,7,6))
    pygame.draw.rect(s,(0,200,255),(4,8,24,26),1)
    pygame.draw.rect(s,(0,255,255),(6,2,20,8),1)
    return s

def draw_enemy_basic():
    s = spr(20,20)
    pygame.draw.ellipse(s,(100,80,150),(2,2,16,16))
    pygame.draw.ellipse(s,(130,100,180),(4,4,12,12))
    pygame.draw.rect(s,(255,255,255),(6,6,3,3))
    pygame.draw.rect(s,(255,255,255),(11,6,3,3))
    pygame.draw.arc(s,(100,150,200),(6,10,8,5),math.pi,2*math.pi,2)
    pygame.draw.rect(s,(100,150,200),(7,14,2,4))
    pygame.draw.rect(s,(100,150,200),(11,14,2,4))
    return s

def draw_enemy_shroom():
    s = spr(20,20)
    pygame.draw.ellipse(s,(200,50,50),(1,1,18,10))
    for bx,by in [(4,3),(10,2),(14,5),(7,6)]:
        pygame.draw.circle(s,(255,255,255),(bx,by),2)
    pygame.draw.rect(s,(240,220,180),(6,9,8,9))
    pygame.draw.rect(s,(200,180,140),(7,10,6,7))
    pygame.draw.rect(s,(80,50,20),(7,11,2,2))
    pygame.draw.rect(s,(80,50,20),(11,11,2,2))
    pygame.draw.rect(s,(80,50,20),(8,14,4,1))
    pygame.draw.rect(s,(200,170,120),(6,18,3,2))
    pygame.draw.rect(s,(200,170,120),(11,18,3,2))
    return s

def draw_enemy_ghost():
    s = spr(20,24)
    pygame.draw.ellipse(s,(150,150,200,180),(2,2,16,14))
    pygame.draw.rect(s,(150,150,200,180),(2,10,16,10))
    for gx in range(2,18,4):
        pygame.draw.circle(s,(0,0,0,0),(gx,20),2)
    pygame.draw.rect(s,(255,255,255),(6,6,3,3))
    pygame.draw.rect(s,(255,255,255),(11,6,3,3))
    pygame.draw.rect(s,(100,100,150),(7,11,6,2))
    return s

def draw_enemy_bureaucrat():
    s = spr(20,24)
    pygame.draw.rect(s,(50,50,80),(4,8,12,14))
    pygame.draw.rect(s,(70,70,100),(5,9,10,12))
    pygame.draw.rect(s,(200,200,220),(8,9,4,5))
    pygame.draw.rect(s,(200,50,50),(9,9,2,5))
    pygame.draw.rect(s,(200,160,120),(4,2,12,8))
    pygame.draw.rect(s,(50,50,50),(5,4,4,3))
    pygame.draw.rect(s,(50,50,50),(11,4,4,3))
    pygame.draw.rect(s,(100,200,255),(6,4,3,2))
    pygame.draw.rect(s,(100,200,255),(12,4,3,2))
    pygame.draw.line(s,(50,50,50),(9,5),(11,5),1)
    pygame.draw.rect(s,(240,230,200),(13,10,5,7))
    pygame.draw.rect(s,(200,50,50),(14,11,3,1))
    pygame.draw.rect(s,(200,50,50),(14,13,3,1))
    pygame.draw.rect(s,(200,50,50),(14,15,3,1))
    pygame.draw.rect(s,(80,60,40),(4,2,12,3))
    pygame.draw.rect(s,(40,40,60),(5,22,4,2))
    pygame.draw.rect(s,(40,40,60),(11,22,4,2))
    return s

def draw_enemy_nostalgia():
    s = spr(24,24)
    pygame.draw.ellipse(s,(150,120,80,150),(2,2,20,20))
    pygame.draw.ellipse(s,(180,150,100,120),(4,4,16,16))
    for ny in range(4,20,3):
        pygame.draw.rect(s,(200,180,130,80),(4,ny,16,1))
    pygame.draw.rect(s,(220,200,160),(7,9,4,3))
    pygame.draw.rect(s,(220,200,160),(13,9,4,3))
    pygame.draw.rect(s,(100,80,60),(8,10,2,2))
    pygame.draw.rect(s,(100,80,60),(14,10,2,2))
    pygame.draw.arc(s,(100,80,60),(8,13,8,5),math.pi,2*math.pi,2)
    return s

def draw_enemy_data_thief():
    s = spr(18,22)
    pygame.draw.ellipse(s,(20,20,30),(1,1,16,16))
    pygame.draw.ellipse(s,(35,35,50),(2,2,14,14))
    pygame.draw.rect(s,(0,255,100),(5,7,3,2))
    pygame.draw.rect(s,(0,255,100),(10,7,3,2))
    pygame.draw.rect(s,(15,15,25),(2,14,14,6))
    for dy in range(16,20,1):
        pygame.draw.rect(s,(0,200,100),(3,dy,random.randint(1,8),1))
    pygame.draw.rect(s,(40,40,60),(11,14,5,5))
    pygame.draw.rect(s,(0,200,100),(12,15,3,3))
    return s

def draw_enemy_forest_spirit():
    s = spr(32,40)
    pygame.draw.rect(s,(60,100,60),(8,16,16,24))
    pygame.draw.rect(s,(80,130,80),(10,18,12,22))
    pygame.draw.circle(s,(30,100,30),(16,12),12)
    pygame.draw.circle(s,(50,130,50),(16,10),9)
    pygame.draw.circle(s,(70,150,70),(10,14),6)
    pygame.draw.circle(s,(70,150,70),(22,14),6)
    pygame.draw.rect(s,(200,255,100),(10,8,5,4))
    pygame.draw.rect(s,(200,255,100),(17,8,5,4))
    pygame.draw.circle(s,(255,255,200),(12,10),2)
    pygame.draw.circle(s,(255,255,200),(19,10),2)
    pygame.draw.rect(s,(50,30,10),(6,38,5,2))
    pygame.draw.rect(s,(50,30,10),(12,36,4,4))
    pygame.draw.rect(s,(50,30,10),(18,38,5,2))
    pygame.draw.rect(s,(50,30,10),(23,36,4,4))
    pygame.draw.rect(s,(60,80,40),(0,16,8,3))
    pygame.draw.rect(s,(60,80,40),(24,16,8,3))
    pygame.draw.rect(s,(60,80,40),(0,14,4,3))
    pygame.draw.rect(s,(60,80,40),(28,14,4,3))
    return s

def draw_enemy_data_castle():
    s = spr(32,40)
    pygame.draw.rect(s,(10,20,50),(4,8,24,30))
    pygame.draw.rect(s,(15,30,80),(6,10,20,28))
    for tx in [4,14,24]:
        pygame.draw.rect(s,(10,20,50),(tx,4,6,6))
        pygame.draw.rect(s,(15,30,80),(tx+1,5,4,5))
    pygame.draw.rect(s,(0,10,30),(11,24,10,14))
    pygame.draw.ellipse(s,(0,10,30),(11,20,10,8))
    for wx,wy in [(7,12),(19,12),(7,18),(19,18)]:
        pygame.draw.rect(s,(0,150,255),(wx,wy,4,4))
        pygame.draw.rect(s,(0,200,255),(wx+1,wy+1,2,2))
    pygame.draw.rect(s,(0,255,255),(13,13,6,2))
    pygame.draw.rect(s,(0,255,255),(14,11,2,6))
    pygame.draw.rect(s,(5,15,40),(2,36,28,4))
    return s

def draw_enemy_night_monster():
    s = spr(24,28)
    pygame.draw.ellipse(s,(10,10,20),(2,4,20,20))
    pygame.draw.ellipse(s,(20,20,40),(4,6,16,16))
    for eye_x in [(7,10),(15,10)]:
        pygame.draw.circle(s,(200,200,255),eye_x,3)
        pygame.draw.circle(s,(255,255,255),eye_x,1)
    pygame.draw.arc(s,(100,100,200),(8,14,8,6),0,math.pi,2)
    pygame.draw.polygon(s,(5,5,15),[(0,8),(10,16),(2,22)])
    pygame.draw.polygon(s,(5,5,15),[(24,8),(14,16),(22,22)])
    pygame.draw.polygon(s,(15,15,30),[(1,10),(9,16),(3,20)])
    for sx,sy in [(4,3),(18,5),(21,2),(3,20),(20,22)]:
        pygame.draw.circle(s,(200,200,255),(sx,sy),1)
    return s

def draw_heart():
    s = spr(8,8)
    pts = [(4,1),(6,0),(8,2),(8,4),(4,8),(0,4),(0,2),(2,0)]
    pygame.draw.polygon(s,(220,50,50),pts)
    pygame.draw.polygon(s,(255,80,80),[(4,2),(6,1),(7,3),(7,4),(4,7),(1,4),(1,3),(2,1)])
    return s

def draw_bullet():
    s = spr(6,6)
    pygame.draw.circle(s,(255,255,255),(3,3),3)
    pygame.draw.circle(s,(200,200,255),(3,3),2)
    return s

def draw_bullet_red():
    s = spr(8,8)
    pygame.draw.circle(s,(220,50,50),(4,4),4)
    pygame.draw.circle(s,(255,100,100),(4,4),2)
    return s

def draw_bullet_cyan():
    s = spr(6,6)
    pygame.draw.circle(s,(0,220,255),(3,3),3)
    pygame.draw.circle(s,(100,255,255),(3,3),1)
    return s

def draw_bullet_laser():
    s = spr(8,24)
    pygame.draw.rect(s,(255,50,50),(3,0,2,24))
    pygame.draw.rect(s,(255,150,150),(3,0,2,24))
    for ly in range(0,24,3):
        pygame.draw.rect(s,(255,255,100),(2,ly,4,1))
    return s

def draw_logo():
    s = spr(200,40)
    s.fill((0,0,0,0))
    try:
        f = pygame.font.SysFont("Courier New", 22, bold=True)
        f2 = pygame.font.SysFont("Courier New", 10, bold=True)
    except:
        f = pygame.font.Font(None,28)
        f2 = pygame.font.Font(None,14)
    t = f.render("DURSUNVENTURE", True, (255,220,60))
    t2 = f2.render("v6.0 — DEV DÜNYA", True, (100,180,255))
    s.blit(t, (100-t.get_width()//2, 2))
    s.blit(t2,(100-t2.get_width()//2,26))
    return s

def draw_save_icon():
    s = spr(16,16)
    pygame.draw.rect(s,(20,60,100),(0,0,16,16))
    pygame.draw.rect(s,(40,120,200),(1,1,14,14))
    pygame.draw.rect(s,(0,200,255),(2,2,12,12))
    pygame.draw.rect(s,(200,220,255),(4,4,8,2))
    pygame.draw.rect(s,(200,220,255),(6,2,4,6))
    return s

def draw_icon():
    s = spr(64,64)
    s.fill((10,10,30))
    pygame.draw.circle(s,(255,220,60),(32,32),28)
    pygame.draw.circle(s,(0,0,0),(32,32),20)
    try:
        f = pygame.font.SysFont("Courier New", 14, bold=True)
        t = f.render("DV", True, (255,220,60))
        s.blit(t,(32-t.get_width()//2,32-t.get_height()//2))
    except: pass
    return s

def draw_portal():
    s = spr(32,32)
    s.fill((0,0,0,0))
    for r,col,a in [(15,(80,0,160),100),(12,(120,0,220),150),
                     (9,(160,50,255),200),(6,(200,100,255),255)]:
        ps = pygame.Surface((r*2,r*2), pygame.SRCALPHA)
        pygame.draw.ellipse(ps,(*col,a),(0,0,r*2,r*2))
        s.blit(ps,(16-r,16-r))
    return s

def generate_all():
    print("Tile sprite'ları...")
    sprites = {
        "tile_grass":    tile_grass(),
        "tile_road":     tile_road(),
        "tile_floor":    tile_floor(),
        "tile_cave":     tile_cave(),
        "tile_factory":  tile_factory(),
        "tile_water":    tile_water(),
        "tile_water_deep": tile_water_deep(),
        "tile_sand":     tile_sand(),
        "tile_dirt":     tile_dirt(),
        "tile_wall":     tile_wall(),
        "tile_tree":     tile_tree(),
        "tile_tree_dark":tile_tree_dark(),
        "tile_rock":     tile_rock(),
        "tile_fence":    tile_fence(),
        "tile_pillar":   tile_pillar(),
        "tile_pipe":     tile_pipe(),
        "tile_crate":    tile_crate(),
        "tile_barrel":   tile_barrel(),
        "tile_flower":   tile_flower(),
        "tile_bush":     tile_bush(),
        "tile_lamp":     tile_lamp(),
        "tile_bridge":   tile_bridge(),
        "tile_dock":     tile_dock(),
        "tile_chest":    tile_chest(),
        "tile_market":   tile_market(),
        "tile_save":     tile_save(),
        "tile_sign":     tile_sign(),
        "tile_door":     tile_door(),
        "tile_stairs_up":tile_stairs_up(),
        "tile_stairs_down":tile_stairs_down(),
        "tile_algo_node":tile_algo_node(),
        "tile_portal":   tile_portal(),
        "tile_boat":     tile_boat(),
        "tile_fish":     tile_fish(),
        "npc_old":       draw_npc_old(),
        "npc_girl":      draw_npc_girl(),
        "npc_fisherman": draw_npc_fisherman(),
        "npc_engineer":  draw_npc_engineer(),
        "npc_villain":   draw_villain(),
        "npc_algo":      draw_algo(),
        "player_down":        draw_player("down", False),
        "player_down_walk":   draw_player("down", True),
        "player_up":          draw_player("up",   False),
        "player_up_walk":     draw_player("up",   True),
        "player_left":        draw_player("left", False),
        "player_left_walk":   draw_player("left", True),
        "player_right":       draw_player("right",False),
        "player_right_walk":  draw_player("right",True),
        "enemy":           draw_enemy_basic(),
        "enemy_shroom":    draw_enemy_shroom(),
        "enemy_ghost":     draw_enemy_ghost(),
        "enemy_bureaucrat":draw_enemy_bureaucrat(),
        "enemy_nostalgia": draw_enemy_nostalgia(),
        "enemy_data_thief":draw_enemy_data_thief(),
        "enemy_forest_spirit": draw_enemy_forest_spirit(),
        "enemy_data_castle":   draw_enemy_data_castle(),
        "enemy_night":         draw_enemy_night_monster(),
        "heart":           draw_heart(),
        "bullet":          draw_bullet(),
        "bullet_red":      draw_bullet_red(),
        "bullet_cyan":     draw_bullet_cyan(),
        "bullet_laser":    draw_bullet_laser(),
        "logo":            draw_logo(),
        "save_icon":       draw_save_icon(),
        "icon":            draw_icon(),
        "portal":          draw_portal(),
    }
    for name, surf in sprites.items():
        save(surf, name)
    print(f"\nToplam {len(sprites)} sprite üretildi!")

if __name__ == "__main__":
    generate_all()
    pygame.quit()
