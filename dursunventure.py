import pygame, sys, math, random, os, json, ast
from dialogues import NPC_DIALOGUES, DUMAN_DIALOGUES, ALGO_DIALOGUES, \
    SIGN_DIALOGUES, ENDING_SLIDES, SHOP_DIALOGUES, YENI_DUSMAN_DIALOGUES
from systems   import QuestLog, Cutscene, CutsceneFrame, \
    make_intro_cutscene, make_duman_defeat_cutscene, \
    make_algo_defeat_cutscene, make_chapter2_cutscene, \
    PuzzleRoom, EXTRA_BOSSES, \
    get_time_of_day, get_day_alpha, get_ambient_overlay, \
    get_npc_night_bonus, DAY_CYCLE_TICKS

SCALE   = 3
TW, TH  = 16, 16
VCOLS, VROWS = 26, 20
VW = TW * VCOLS
VH = TH * VROWS
SW = VW * SCALE
SH = VH * SCALE
MAP_W, MAP_H = 120, 80

if not os.environ.get('SDL_VIDEODRIVER'):
    os.environ['SDL_VIDEODRIVER'] = 'x11' if os.environ.get('DISPLAY') else 'dummy'
pygame.init()
try:    pygame.mixer.init(22050,-16,2,1024); AUDIO_OK=True
except: AUDIO_OK=False

def set_screen(fs=True):
    global screen
    try:    screen=pygame.display.set_mode((SW,SH),(pygame.FULLSCREEN|pygame.SCALED) if fs else 0)
    except: screen=pygame.display.set_mode((SW,SH))
screen=None; set_screen(True)
canvas=pygame.Surface((VW,VH))
pygame.display.set_caption("DURSUNVENTURE v6.0")
clock=pygame.time.Clock(); FPS=60

BASE=os.path.dirname(os.path.abspath(__file__))
def fpath(*p): return os.path.join(BASE,*p)
SAVE_FILE=fpath("save.json")

BLACK=(0,0,0);    WHITE=(255,255,255); YELLOW=(255,220,60)
GRAY=(100,100,100);DGRAY=(40,40,40);   RED=(220,50,50)
GREEN=(50,200,80);BLUE=(60,120,220);   CYAN=(60,220,220)
PINK=(255,120,180);ORANGE=(240,140,40);PURPLE=(160,60,200)
TEAL=(40,160,160);BROWN=(120,80,40);   CREAM=(240,220,180)
NIGHT_BLUE=(10,10,40); DAWN=(200,120,80)

def mfont(sz,bold=True):
    for n in ["Courier New","Courier","monospace"]:
        try:
            f=pygame.font.SysFont(n,sz,bold=bold)
            if f: return f
        except: pass
    return pygame.font.Font(None,sz+4)

fsm=mfont(8); fmd=mfont(11); flg=mfont(16)
fxl=mfont(20); fttl=mfont(26)

sounds={}
def load_sounds():
    d=fpath("assets","sounds")
    if not os.path.exists(d): return
    for f in os.listdir(d):
        if f.endswith(".wav"):
            k=f[:-4]
            try: sounds[k]=pygame.mixer.Sound(fpath("assets","sounds",f))
            except: pass
load_sounds()

def play(name,vol=0.7):
    if not AUDIO_OK: return
    s=sounds.get("sfx_"+name) or sounds.get(name)
    if s:
        s.set_volume(vol)
        try: s.play()
        except: pass

sprites={}
def load_sprites():
    d=fpath("assets","sprites")
    if not os.path.exists(d): return
    for f in os.listdir(d):
        if f.endswith(".png"):
            try: sprites[f[:-4]]=pygame.image.load(fpath("assets","sprites",f)).convert_alpha()
            except: pass
load_sprites()

def spr(name,fb=(180,50,180)):
    if name in sprites: return sprites[name]
    s=pygame.Surface((16,16),pygame.SRCALPHA)
    s.fill((*fb,200)); return s

TILE_SPRITE={
    'G':'tile_grass','R':'tile_road','F':'tile_floor',
    'D':'tile_dirt', 'N':'tile_sand','C':'tile_cave',
    'I':'tile_factory','w':'tile_water','W2':'tile_water_deep',
    'W':'tile_wall', 'T':'tile_tree','K':'tile_rock',
    'f':'tile_fence','cr':'tile_crate','P':'tile_pillar',
    'Pi':'tile_pipe','Ba':'tile_barrel','d':'tile_door',
    'ch':'tile_chest','S':'tile_sign','sv':'tile_save',
    'M':'tile_market','b':'tile_bush','Fl':'tile_flower',
    'L':'tile_lamp','Br':'tile_bridge','Dk':'tile_dock',
    'Bo':'tile_boat','Fi':'tile_fish','An':'tile_algo_node',
    'Po':'tile_portal','sd':'tile_stairs_down','su':'tile_stairs_up',
    'n':'tile_grass',
    'B':'tile_grass',
}
DARK_TREE_ZONE=lambda tx,ty: (0<=tx<50 and 40<=ty<80)

SOLID={'W','T','K','f','W2','cr','P','Pi','Ba','W'}

def load_map():
    p=fpath("map_data.json")
    if not os.path.exists(p):
        import subprocess
        subprocess.run(["python3",fpath("mapgen.py")],cwd=BASE)
    with open(p,encoding="utf-8") as f:
        data=json.load(f)
    id2char=data["tile_ids"]
    grid=[]
    for row in data["grid"]:
        grid.append([id2char[str(c)] for c in row])
    return grid, data

MAP_GRID, MAP_DATA = load_map()

def tile_at(tx,ty):
    if 0<=ty<MAP_H and 0<=tx<MAP_W:
        return MAP_GRID[ty][tx]
    return 'W'

def is_solid(tx,ty):
    return tile_at(tx,ty) in SOLID

def draw_map_view(surface, cam_x, cam_y, frame=0):
    t_ms=pygame.time.get_ticks()
    start_tx=max(0,cam_x); start_ty=max(0,cam_y)
    for ry in range(VROWS+1):
        for rx in range(VCOLS+1):
            tx=start_tx+rx; ty=start_ty+ry
            if tx>=MAP_W or ty>=MAP_H: continue
            ch=MAP_GRID[ty][tx]
            sx=(tx-cam_x)*TW; sy=(ty-cam_y)*TH

            sname=TILE_SPRITE.get(ch,'tile_grass')
            if ch=='T' and DARK_TREE_ZONE(tx,ty):
                sname='tile_tree_dark'
            ts=spr(sname)

            if ch=='w':
                off=int(2*math.sin(t_ms*0.002+tx*0.4+ty*0.3))
                surface.blit(ts,(sx,sy+off))
                wv=pygame.Surface((TW,2),pygame.SRCALPHA)
                wv.fill((50,100,180,80))
                surface.blit(wv,(sx,sy+TH//2+off))
                continue
            elif ch=='An':
                pulse=int(3*math.sin(t_ms*0.004+tx+ty))
                ns=pygame.transform.scale(ts,(TW+pulse,TH+pulse))
                surface.blit(ns,(sx-pulse//2,sy-pulse//2))
                continue
            elif ch=='Po':
                angle=(t_ms*0.1+tx*30)%360
                ps=pygame.transform.rotate(ts,angle)
                surface.blit(ps,(sx-(ps.get_width()-TW)//2,sy-(ps.get_height()-TH)//2))
                continue
            elif ch=='L':
                surface.blit(ts,(sx,sy))
                glow=pygame.Surface((TW*3,TH*3),pygame.SRCALPHA)
                br=int(30+15*math.sin(t_ms*0.003))
                pygame.draw.circle(glow,(255,220,100,br),(TW*3//2,TH*3//2),TW)
                surface.blit(glow,(sx-TW,sy-TH))
                continue
            elif ch=='Fi':
                if (t_ms//500+tx*7)%20<2:
                    surface.blit(ts,(sx,sy-2))
                continue

            surface.blit(ts,(sx,sy))

class Camera:
    def __init__(self):
        self.x=0; self.y=0
        self.shake=0; self.shake_x=0; self.shake_y=0

    def update(self, px, py):
        target_x=int(px)-VCOLS//2
        target_y=int(py)-VROWS//2
        target_x=max(0,min(MAP_W-VCOLS,target_x))
        target_y=max(0,min(MAP_H-VROWS,target_y))
        self.x+=(target_x-self.x)*0.12
        self.y+=(target_y-self.y)*0.12
        if self.shake>0:
            self.shake-=1
            self.shake_x=random.randint(-2,2)
            self.shake_y=random.randint(-2,2)
        else:
            self.shake_x=0; self.shake_y=0

    def tile_x(self): return int(self.x)+self.shake_x
    def tile_y(self): return int(self.y)+self.shake_y

    def world_to_screen(self,wx,wy):
        return ((wx-self.x)*TW+self.shake_x*TW,
                (wy-self.y)*TH+self.shake_y*TH)

def wrap(text,font,maxw):
    words=text.split(' '); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if font.size(test)[0]>maxw:
            if cur: lines.append(cur)
            cur=w
        else: cur=test
    if cur: lines.append(cur)
    return lines

class DialogueBox:
    def __init__(self):
        self.active=False; self.lines=[]; self.cur=0
        self.ch=0; self.timer=0; self.spd=2
        self.speaker=""; self.cb=None; self.col=WHITE
        self.portrait=None; self.blip=0

    def show(self,spk,lines,cb=None,portrait=None,col=WHITE):
        self.active=True; self.speaker=spk
        self.lines=lines if isinstance(lines,list) else [lines]
        self.cur=0; self.ch=0; self.timer=0
        self.cb=cb; self.portrait=portrait; self.col=col

    def update(self):
        if not self.active: return
        self.timer+=1
        if self.timer%max(1,self.spd)==0:
            if self.cur<len(self.lines):
                ln=self.lines[self.cur]
                if self.ch<len(ln):
                    self.ch+=1; self.blip+=1
                    if self.blip%4==0: play("dialogue",0.25)

    def advance(self):
        if not self.active: return False
        ln=self.lines[self.cur] if self.cur<len(self.lines) else ""
        if self.ch<len(ln): self.ch=len(ln); return True
        self.cur+=1
        if self.cur>=len(self.lines):
            self.active=False
            if self.cb: self.cb()
            return False
        self.ch=0; play("menu_select",0.35)
        return True

    def draw(self,surf):
        if not self.active: return
        bx,by,bw,bh=8,VH-72,VW-16,64
        pygame.draw.rect(surf,BLACK,(bx+2,by+2,bw,bh))
        pygame.draw.rect(surf,BLACK,(bx-1,by-1,bw+2,bh+2))
        pygame.draw.rect(surf,self.col,(bx,by,bw,bh),2)
        pygame.draw.rect(surf,DGRAY,(bx+2,by+2,bw-4,bh-4))
        if self.speaker:
            nw=fmd.size(self.speaker)[0]+10
            pygame.draw.rect(surf,BLACK,(bx,by-16,nw+4,16))
            pygame.draw.rect(surf,self.col,(bx,by-16,nw+4,16),1)
            pygame.draw.rect(surf,DGRAY,(bx+2,by-14,nw,12))
            surf.blit(fmd.render(self.speaker,True,self.col),(bx+5,by-14))
        off=0
        if self.portrait:
            ps=spr(self.portrait)
            psc=pygame.transform.scale(ps,(32,48))
            surf.blit(psc,(bx+4,by+8)); off=38
        if self.cur<len(self.lines):
            shown=self.lines[self.cur][:self.ch]
            for i,ln in enumerate(wrap(shown,fmd,bw-16-off)[:3]):
                surf.blit(fmd.render(ln,True,WHITE),(bx+8+off,by+10+i*14))
        cur_ln=self.lines[self.cur] if self.cur<len(self.lines) else ""
        if self.ch>=len(cur_ln):
            if (pygame.time.get_ticks()//400)%2:
                pygame.draw.polygon(surf,self.col,
                    [(bx+bw-12,by+bh-10),(bx+bw-6,by+bh-10),(bx+bw-9,by+bh-5)])

class ShopScreen:
    def __init__(self):
        self.active=False; self.sel=0; self.msg=""; self.mt=0
        self.items=list(SHOP_DIALOGUES["urun_listesi"].items())

    def open(self): self.active=True; self.sel=0; self.msg=""; play("shop_open")

    def update(self,kj):
        if not self.active: return
        if self.mt>0: self.mt-=1; return
        n=len(self.items)
        if kj.get(pygame.K_UP):   self.sel=(self.sel-1)%n; play("menu_select")
        if kj.get(pygame.K_DOWN): self.sel=(self.sel+1)%n; play("menu_select")
        if kj.get(pygame.K_x) or kj.get(pygame.K_ESCAPE):
            self.active=False; play("menu_select")
        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN): self._buy()

    def _buy(self):
        name,data=self.items[self.sel]
        cost=data.get("fiyat",99)
        if player.get("gold",0)<cost:
            self.msg=SHOP_DIALOGUES["para_yok"]; self.mt=90; play("shop_no_gold",0.5); return
        player["gold"]-=cost
        if "heal" in data:
            player.setdefault("items",[]).append({"name":name,"heal":data["heal"]})
        elif "atk" in data:
            player["atk_bonus"]=player.get("atk_bonus",0)+data["atk"]
            self.msg=f"{name} takıldı! ATK+{data['atk']}"; self.mt=90; play("shop_buy"); return
        elif "def" in data:
            player["def_bonus"]=player.get("def_bonus",0)+data["def"]
            self.msg=f"{name} takıldı! DEF+{data['def']}"; self.mt=90; play("shop_buy"); return
        self.msg=SHOP_DIALOGUES["satin_alindi"]; self.mt=80; play("shop_buy")

    def draw(self,surf):
        if not self.active: return
        ov=pygame.Surface((VW,VH),pygame.SRCALPHA); ov.fill((0,0,0,190)); surf.blit(ov,(0,0))
        bx,by,bw,bh=20,20,VW-40,VH-40
        pygame.draw.rect(surf,DGRAY,(bx,by,bw,bh))
        pygame.draw.rect(surf,YELLOW,(bx,by,bw,bh),2)
        surf.blit(flg.render("★ HÜSREV'İN MAĞAZASI ★",True,YELLOW),
                  (bx+bw//2-flg.size("★ HÜSREV'İN MAĞAZASI ★")[0]//2,by+6))
        surf.blit(fmd.render(f"Altın: {player.get('gold',0)}G",True,YELLOW),(bx+bw-80,by+6))
        for i,(name,data) in enumerate(self.items):
            y=by+28+i*22; sel=i==self.sel
            if sel: pygame.draw.rect(surf,(40,40,0),(bx+4,y,bw-8,20))
            ct=fmd.render(f"{'▶ ' if sel else '  '}{name}",True,YELLOW if sel else WHITE)
            surf.blit(ct,(bx+10,y+2))
            pt=fmd.render(f"{data.get('fiyat',0)}G",True,YELLOW if sel else GRAY)
            surf.blit(pt,(bx+bw-55,y+2))
            if sel:
                dt=fsm.render(data.get("desc",""),True,(200,200,150))
                surf.blit(dt,(bx+14,y+12))
        if self.msg:
            mt=fmd.render(self.msg,True,GREEN if "alındı" in self.msg or "takıldı" in self.msg else RED)
            surf.blit(mt,(bx+bw//2-mt.get_width()//2,by+bh-26))
        surf.blit(fsm.render("Z=Al  X=Çıkış",True,GRAY),(bx+bw//2-30,by+bh-12))

from dialogues import YENI_DUSMAN_DIALOGUES
ENEMIES={
    "Ağlak Varlık":       {"spr":"enemy","hp":30,"atk":5,"gold":5,"xp":10,
        "desc":"Anlamadığı şeyler için ağlıyor.","spare_cond":"",
        "spare_lines":["İki kez merci!","Affediyorum..."],"defeat_line":"Eridi.",
        "bullets":["rain"],"spare_sound":"spare"},
    "Yanlış Yer Mantarı": {"spr":"enemy_shroom","hp":25,"atk":7,"gold":8,"xp":15,
        "desc":"Yanlış yerde büyümüş.","spare_cond":"talk",
        "spare_lines":["Önce konuş!","Şimdi merci!"],"defeat_line":"Şapkası düştü.",
        "bullets":["side","diagonal"],"spare_sound":"spare"},
    "Panik Ruhu":         {"spr":"enemy_ghost","hp":40,"atk":9,"gold":12,"xp":20,
        "desc":"Her şeyden panikliyor.","spare_cond":"shout",
        "spare_lines":["BAĞIR!","Tekrar!"],"defeat_line":"Dağıldı.",
        "bullets":["circle","rain"],"spare_sound":"spare"},
    "Kafakarışık Bürokrat":{"spr":"enemy_bureaucrat","hp":50,"atk":8,"gold":18,"xp":25,
        "desc":"47 formu var. Hiçbirini bilmiyor.","spare_cond":"talk",
        "spare_lines":YENI_DUSMAN_DIALOGUES["Kafakarışık Bürokrat"]["spare_lines"],
        "defeat_line":"Formlar uçtu.","bullets":["side","rain"],"spare_sound":"spare"},
    "Nostalji Canavarı":  {"spr":"enemy_nostalgia","hp":45,"atk":11,"gold":15,"xp":30,
        "desc":"Eskiden her şey daha iyiydi...","spare_cond":"",
        "spare_lines":YENI_DUSMAN_DIALOGUES["Nostalji Canavarı"]["spare_lines"],
        "defeat_line":"Dinlendi.","bullets":["circle","rain"],"spare_sound":"spare"},
    "Veri Hırsızı":       {"spr":"enemy_data_thief","hp":35,"atk":13,"gold":20,"xp":35,
        "desc":"Ne yapacağını bilmiyor.","spare_cond":"talk",
        "spare_lines":YENI_DUSMAN_DIALOGUES["Veri Hırsızı"]["spare_lines"],
        "defeat_line":"Pişman oldu.","bullets":["diagonal","circle"],"spare_sound":"spare"},
    "Gece Canavarı":      {"spr":"enemy_night","hp":90,"atk":14,"gold":15,"xp":45,
        "desc":"Sadece gece çıkar.","spare_cond":"talk","night_only":True,
        "spare_lines":EXTRA_BOSSES["Gece Canavarı"]["spare_lines"],
        "defeat_line":"Sabahı bekledi.","bullets":["rain","diagonal","circle"],"spare_sound":"spare"},
    "Duman":              {"spr":"npc_villain","hp":120,"atk":15,"gold":0,"xp":50,
        "desc":"Kötülüğü meslek edinmiş.","spare_cond":"memory","is_boss":True,
        "spare_lines":DUMAN_DIALOGUES["duman_savaş_merci"],
        "defeat_line":"Duman dağıldı.",
        "bullets":["rain","side","circle","diagonal"],"spare_sound":"good_end_sfx",
        "phases":[
            {"hp_pct":100,"label":"DUMAN","color":RED,"atk":15,"speed":1.0},
            {"hp_pct":50, "label":"DUMAN - ÖFKE","color":ORANGE,"atk":22,"speed":1.4},
        ]},
    "Duman 2.0":          {"spr":"npc_villain","hp":200,"atk":22,"gold":0,"xp":100,
        "desc":"Upgrade edildi.","spare_cond":"memory","is_boss":True,
        "spare_lines":DUMAN_DIALOGUES["duman2_merci"],
        "defeat_line":"Duman 2.0 çöktü.",
        "bullets":["rain","side","circle","diagonal","laser"],"spare_sound":"spare",
        "phases":[
            {"hp_pct":100,"label":"DUMAN 2.0 - v1","color":RED,"atk":22,"speed":1.0},
            {"hp_pct":50, "label":"DUMAN 2.0 - v2","color":ORANGE,"atk":30,"speed":1.4},
            {"hp_pct":20, "label":"DUMAN 2.0 - MELTDOWN","color":PURPLE,"atk":38,"speed":1.8},
        ]},
    "Orman Ruhu":         {"spr":"enemy_forest_spirit","hp":180,"atk":18,"gold":0,"xp":80,
        "desc":"Ormanın koruyucusu.","spare_cond":"talk","is_boss":True,
        "spare_lines":EXTRA_BOSSES["Orman Ruhu"]["spare_lines"],
        "defeat_line":"Orman Ruhu dağıldı.",
        "bullets":["circle","rain","diagonal","laser"],"spare_sound":"empathy",
        "phases":[
            {"hp_pct":100,"label":"ORMAN RUHU - UYANIK","color":(40,140,60),"atk":18,"speed":1.0},
            {"hp_pct":50, "label":"ORMAN RUHU - ÖFKELI","color":(140,60,20),"atk":26,"speed":1.5},
            {"hp_pct":20, "label":"ORMAN RUHU - SON","color":(200,200,80),"atk":32,"speed":1.9},
        ]},
    "Veri Kalesi":        {"spr":"enemy_data_castle","hp":250,"atk":25,"gold":0,"xp":150,
        "desc":"THE ALGO'nun zırhı.","spare_cond":"empathy","is_boss":True,
        "spare_lines":EXTRA_BOSSES["Veri Kalesi"]["spare_lines"],
        "defeat_line":"Veri Kalesi çöktü.",
        "bullets":["grid","laser","circle","rain","diagonal"],"spare_sound":"empathy",
        "phases":[
            {"hp_pct":100,"label":"VERİ KALESİ - AKTİF","color":BLUE,"atk":25,"speed":1.1},
            {"hp_pct":60, "label":"VERİ KALESİ - SALDIRI","color":PURPLE,"atk":33,"speed":1.4},
            {"hp_pct":25, "label":"VERİ KALESİ - ÇÖKÜŞ","color":YELLOW,"atk":40,"speed":1.8},
        ]},
    "THE ALGO":           {"spr":"npc_algo","hp":300,"atk":20,"gold":0,"xp":200,
        "desc":"[VERİ İŞLENİYOR...]","spare_cond":"empathy","is_boss":True,
        "spare_lines":ALGO_DIALOGUES["merci_cevaplari"],
        "defeat_line":"SİSTEM KAPANIYOR...",
        "bullets":["rain","side","circle","diagonal","laser","grid"],"spare_sound":"empathy",
        "phases":[
            {"hp_pct":100,"label":"FAZ I - ANALİZ","color":CYAN,"atk":20,"speed":1.0},
            {"hp_pct":60, "label":"FAZ II - HESAP","color":PURPLE,"atk":28,"speed":1.3},
            {"hp_pct":30, "label":"FAZ III - ÇÖKÜŞ","color":RED,"atk":35,"speed":1.6},
        ]},
}

NORMAL_POOL=["Ağlak Varlık","Yanlış Yer Mantarı","Panik Ruhu",
             "Kafakarışık Bürokrat","Nostalji Canavarı","Veri Hırsızı"]
CAVE_POOL  =["Panik Ruhu","Nostalji Canavarı","Veri Hırsızı"]
FACTORY_POOL=["Kafakarışık Bürokrat","Veri Hırsızı","Nostalji Canavarı"]

class Battle:
    def __init__(self,ekey):
        e=ENEMIES.get(ekey,ENEMIES["Ağlak Varlık"])
        self.ekey=ekey; self.ename=ekey
        self.ehp=e["hp"]; self.emax=e["hp"]; self.eatk=e["atk"]
        self.edesc=e["desc"]; self.espr=e["spr"]
        self.spare_cond=e["spare_cond"]
        self.spare_lines=list(e["spare_lines"])
        self.defeat_line=e["defeat_line"]
        self.bpats=e.get("bullets",["rain"])
        self.is_boss=e.get("is_boss",False)
        self.phases=e.get("phases",None)
        self.cur_phase=0
        self.gold=e["gold"]; self.xp=e["xp"]

        self.php=player["hp"]; self.pmax=player["max_hp"]
        self.pdef=player.get("def_bonus",0)
        self.patk=player.get("atk_bonus",0)

        self.phase="intro" if self.is_boss else "menu"
        self.menu_sel=0; self.menu_items=["SALDIR","EŞYA","MERCİ","KAÇ"]
        self.msg=""; self.mt=0
        self.hx=VW//2; self.hy=VH//2+20
        self.hvx=0;    self.hvy=0
        self.hinvuln=0
        self.bullets=[]; self.btime=0; self.bdur=240
        self.talked=False; self.mercy_cnt=0; self.mercy_idx=0
        self.items=list(player.get("items",[]))
        self.shake=0; self.eanim=0
        self.result=""
        self.empathy=0
        self.bg=BLACK; self.target_bg=BLACK
        self.turn=0
        self.intro_lines=[]; self.intro_idx=0

        if self.is_boss:
            if ekey=="Duman 2.0":
                self.intro_lines=DUMAN_DIALOGUES.get("duman2_giris",{}).get("lines",["DUMAN 2.0!"])
            elif ekey=="THE ALGO":
                n=player.get("name","???"); lv=player.get("lv",1)
                hp=player["hp"]; mhp=player["max_hp"]
                k=player.get("kills",0); s=player.get("spares",0)
                self.intro_lines=[l.format(n,n,lv,hp,mhp,k,s) if '{}'in l else l
                                  for l in ALGO_DIALOGUES["ilk_giris"]["lines"]]
            elif ekey in ("Orman Ruhu","Veri Kalesi"):
                self.intro_lines=[f"{ekey} belirdi!",self.edesc,"Dur.","Seni bekleyen bir güç var."]
            else:
                self.intro_lines=DUMAN_DIALOGUES.get("ilk_karsilasma",{}).get("lines",["Boss!"])
            play("battle_start",0.9)

    def _phase_data(self):
        if not self.phases: return None,0
        pct=self.ehp/self.emax*100
        for i in range(len(self.phases)-1,-1,-1):
            if pct<=self.phases[i]["hp_pct"]: return self.phases[i],i
        return self.phases[0],0

    def _check_phase(self):
        if not self.phases: return
        _,idx=self._phase_data()
        if idx!=self.cur_phase:
            self.cur_phase=idx
            ph=self.phases[idx]
            self.intro_lines=[f"{ph['label']}!","Sistem güncelleniyor..."]
            self.intro_idx=0; self.phase="intro"
            self.target_bg=ph.get("color",BLACK)
            play("boss_phase",0.8)
            cam.shake=12

    def update(self,kp,kj):
        self.eanim+=1
        if self.shake>0: self.shake-=1
        if self.hinvuln>0: self.hinvuln-=1
        for i in range(3):
            diff=self.target_bg[i]-self.bg[i]
            if diff:
                s=1 if diff>0 else -1
                self.bg=tuple(self.bg[j]+s if j==i else self.bg[j] for j in range(3))

        if self.phase=="intro":
            if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN):
                self.intro_idx+=1
                if self.intro_idx>=len(self.intro_lines):
                    self.phase="menu"; play("battle_start",0.7)
                else: play("menu_select",0.3)
            return

        if self.phase=="menu":
            if kj.get(pygame.K_LEFT):  self.menu_sel=(self.menu_sel-1)%4; play("menu_select")
            if kj.get(pygame.K_RIGHT): self.menu_sel=(self.menu_sel+1)%4; play("menu_select")
            if kj.get(pygame.K_UP):    self.menu_sel=(self.menu_sel-2)%4; play("menu_select")
            if kj.get(pygame.K_DOWN):  self.menu_sel=(self.menu_sel+2)%4; play("menu_select")
            if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN): self._action()

        elif self.phase=="bullet":
            self._upd_bullets(kp); self.btime+=1
            if self.btime>=self.bdur: self.phase="menu"; self.bullets=[]

        elif self.phase in ("result","enemy_turn","spare_talk","death_anim"):
            if self.phase in ("result","enemy_turn","spare_talk","death_anim"):
                self.mt=max(0,self.mt-1)
            if self.phase=="enemy_turn" and self.mt<=0:
                self.phase="bullet"; self._spawn()
            elif self.phase in ("spare_talk","result") and self.mt<=0:
                if self.phase=="death_anim":
                    self.result="win"; self.phase="result"; self.mt=70

    def _action(self):
        sel=self.menu_items[self.menu_sel]; play("menu_select"); self.turn+=1
        if sel=="SALDIR":
            lv=player.get("lv",1)
            dmg=random.randint(8,18)+lv*2+self.patk
            self.ehp-=dmg; self.shake=8; self._check_phase()
            play("boss_hit" if self.is_boss else "attack")
            if self.ehp<=0:
                self.ehp=0; self.msg=self.defeat_line
                self.phase="death_anim"; self.mt=90; self.result="kill"
                player["kills"]=player.get("kills",0)+1
                player["gold"]=player.get("gold",0)+self.gold
                self._xp(self.xp); play("enemy_defeat")
            else:
                self.msg=f"{dmg} hasar!"; self.phase="enemy_turn"; self.mt=80

        elif sel=="EŞYA":
            if self.items:
                it=self.items.pop(0); heal=it.get("heal",20)
                self.php=min(self.pmax,self.php+heal)
                player["hp"]=self.php; player["items"]=self.items
                self.msg=f"{it['name']} yendi! +{heal} HP"; play("spare",0.5)
            else: self.msg="Çantanda hiçbir şey yok!"
            self.phase="enemy_turn"; self.mt=70

        elif sel=="MERCİ":
            can=not self.spare_cond or self.talked
            if self.spare_cond=="empathy":
                self.empathy+=1; can=self.empathy>=8
            self.mercy_cnt+=1
            if can and self.mercy_cnt>=2:
                self.msg=f"{self.ename} affedildi!"
                self.phase="death_anim"; self.mt=90; self.result="spare"
                player["spares"]=player.get("spares",0)+1
                player["gold"]=player.get("gold",0)+self.gold//2
                self._xp(self.xp//2); play(ENEMIES.get(self.ekey,{}).get("spare_sound","spare"))
            else:
                idx=min(self.mercy_idx,len(self.spare_lines)-1)
                self.msg=self.spare_lines[idx]; self.mercy_idx+=1
                self.phase="enemy_turn"; self.mt=90

        elif sel=="KAÇ":
            if self.is_boss: self.msg="Buradan kaçış yok!"; self.phase="enemy_turn"; self.mt=60; return
            if random.random()<0.5+player.get("lv",1)*0.05:
                self.msg="Kaçtın!"; self.result="fled"; self.phase="result"; self.mt=60; play("flee")
            else:
                self.msg="Kaçamadın!"; self.phase="enemy_turn"; self.mt=70; play("player_hurt",0.4)

    def _xp(self,amt):
        player["xp"]=player.get("xp",0)+amt
        need=player.get("lv",1)*50
        if player["xp"]>=need:
            player["lv"]=player.get("lv",1)+1
            player["xp"]-=need; player["max_hp"]+=10
            player["hp"]=player["max_hp"]
            self.php=player["hp"]; self.pmax=player["max_hp"]; play("level_up")

    def _spawn(self):
        self.bullets=[]; self.btime=0
        self.hx=VW//2; self.hy=VH//2+20; self.hvx=0; self.hvy=0
        ph,_=self._phase_data(); spd=(ph["speed"] if ph else 1.0)*1.4
        pats=self.bpats
        if self.is_boss:
            p=self.cur_phase
            if p==0: pats=["rain","side"]
            elif p==1: pats=["rain","side","circle","diagonal"]
            else: pats=pats
        pat=random.choice(pats); cnt=random.randint(6,14 if self.is_boss else 9)
        for i in range(cnt):
            delay=i*18
            if pat=="rain":
                self.bullets.append({"x":random.randint(82,VW-82),"y":62,"vx":0,"vy":spd,"delay":delay,"sz":3,"col":WHITE})
            elif pat=="side":
                sd=random.choice([-1,1])
                self.bullets.append({"x":82 if sd<0 else VW-82,"y":random.randint(70,165),"vx":sd*spd*1.2,"vy":0,"delay":delay,"sz":3,"col":CYAN})
            elif pat=="circle":
                a=(i/cnt)*math.pi*2
                self.bullets.append({"x":VW//2,"y":VH//2,"vx":math.cos(a)*spd,"vy":math.sin(a)*spd,"delay":delay,"sz":3,"col":ORANGE})
            elif pat=="diagonal":
                self.bullets.append({"x":random.randint(82,VW-100),"y":62,"vx":random.uniform(-0.6,0.6),"vy":spd*0.9,"delay":delay,"sz":3,"col":PINK})
            elif pat=="laser":
                self.bullets.append({"x":random.randint(85,VW-85),"y":62,"vx":0,"vy":spd*0.6,"delay":delay,"sz":6,"col":RED})
            elif pat=="grid":
                gx=(i%4)*42+88
                self.bullets.append({"x":gx,"y":62,"vx":0,"vy":spd*0.8,"delay":delay,"sz":4,"col":PURPLE})
                self.bullets.append({"x":gx,"y":180,"vx":0,"vy":-spd*0.8,"delay":delay+8,"sz":4,"col":PURPLE})

    def _upd_bullets(self,kp):
        spd=2.5
        if kp.get(pygame.K_LEFT):  self.hvx=-spd
        elif kp.get(pygame.K_RIGHT):self.hvx=spd
        else: self.hvx*=0.65
        if kp.get(pygame.K_UP):    self.hvy=-spd
        elif kp.get(pygame.K_DOWN):self.hvy=spd
        else: self.hvy*=0.65
        self.hx=max(84,min(VW-84,self.hx+self.hvx))
        self.hy=max(64,min(168,self.hy+self.hvy))
        for b in self.bullets:
            if b["delay"]>0: b["delay"]-=1; continue
            b["x"]+=b["vx"]; b["y"]+=b["vy"]
        if self.hinvuln==0:
            ph,_=self._phase_data()
            base_atk=ph["atk"] if ph else self.eatk
            for b in self.bullets:
                if b["delay"]>0: continue
                if math.hypot(b["x"]-self.hx,b["y"]-self.hy)<b["sz"]+3:
                    dmg=max(1,base_atk+random.randint(-2,3)-player.get("lv",1)-self.pdef)
                    self.php=max(0,self.php-dmg); player["hp"]=self.php
                    play("player_hurt",0.5); self.hinvuln=18; b["x"]=-999
                    if self.php<=0:
                        self.phase="result"; self.msg="HAYATTA KALAMADINIZ..."
                        self.mt=90; self.result="dead"; return
        self.bullets=[b for b in self.bullets if -10<b["x"]<VW+10 and -10<b["y"]<VH+10 or b["delay"]>0]

    def draw(self,surf):
        surf.fill(self.bg)
        t_ms=pygame.time.get_ticks()
        if self.is_boss and self.cur_phase>=2:
            for _ in range(4):
                pygame.draw.rect(surf,(random.randint(0,80),random.randint(0,255),random.randint(200,255)),
                    (random.randint(0,VW),random.randint(0,VH),random.randint(10,60),random.randint(1,3)))

        if self.phases:
            ph,_=self._phase_data()
            pt=fsm.render(ph["label"],True,ph.get("color",WHITE))
            surf.blit(pt,(VW//2-pt.get_width()//2,1))

        if self.spare_cond=="empathy":
            pct=min(1.0,self.empathy/8)
            pygame.draw.rect(surf,DGRAY,(8,20,VW-16,5))
            ec=(int(255*(1-pct)),int(255*pct),int(100*pct))
            pygame.draw.rect(surf,ec,(8,20,int((VW-16)*pct),5))
            surf.blit(fsm.render(f"EMPATİ: {int(pct*100)}%",True,(200,200,255)),(8,27))

        ei=spr(self.espr,(200,50,50))
        if ei.get_width()<24: ei=pygame.transform.scale(ei,(48,64))
        ox=VW//2-ei.get_width()//2
        oy=30+int(math.sin(self.eanim*0.05)*2)
        if self.shake>0:
            surf.blit(ei,(ox+random.randint(-3,3),oy))
        elif self.phase=="death_anim":
            fade=max(0,255-int((90-self.mt)*(255/90)))
            da=pygame.Surface(ei.get_size(),pygame.SRCALPHA)
            da.blit(ei,(0,0)); da.fill((255,255,255,255-fade),special_flags=pygame.BLEND_RGBA_MIN)
            surf.blit(da,(ox,oy))
        else:
            surf.blit(ei,(ox,oy))

        nc=CYAN if self.ekey=="THE ALGO" else ORANGE if "2.0" in self.ekey else WHITE
        surf.blit(fmd.render(self.ename,True,nc),(VW//2-fmd.size(self.ename)[0]//2,oy+ei.get_height()+2))

        fr=max(0,self.ehp/self.emax)
        ecol=CYAN if fr>0.6 else PURPLE if fr>0.3 else RED
        pygame.draw.rect(surf,DGRAY,(8,8,110,7))
        pygame.draw.rect(surf,ecol,(8,8,int(110*fr),7))
        pygame.draw.rect(surf,WHITE,(8,8,110,7),1)
        surf.blit(fsm.render(f"HP {max(0,self.ehp)}/{self.emax}",True,WHITE),(8,17))

        pfr=max(0,self.php/self.pmax)
        pcol=GREEN if pfr>0.5 else YELLOW if pfr>0.25 else RED
        pygame.draw.rect(surf,DGRAY,(VW-122,8,112,7))
        pygame.draw.rect(surf,pcol,(VW-122,8,int(112*pfr),7))
        pygame.draw.rect(surf,WHITE,(VW-122,8,112,7),1)
        surf.blit(fsm.render(f"{player['name']} {self.php}/{self.pmax}",True,WHITE),(VW-122,17))
        surf.blit(fsm.render(f"LV{player.get('lv',1)} DEF:{self.pdef}",True,YELLOW),(VW-122,26))

        box=pygame.Rect(78,60,VW-156,124)
        pygame.draw.rect(surf,BLACK,box)
        bcol=CYAN if self.ekey=="THE ALGO" else ORANGE if "2.0" in self.ekey else WHITE
        pygame.draw.rect(surf,bcol,box,2)

        if self.phase=="intro":
            idx=min(self.intro_idx,len(self.intro_lines)-1)
            shown=self.intro_lines[idx] if self.intro_lines else ""
            for i,ln in enumerate(wrap(shown,fmd,box.width-20)[:4]):
                surf.blit(fmd.render(ln,True,CYAN if self.ekey=="THE ALGO" else ORANGE),(box.x+10,box.y+15+i*16))
            surf.blit(fsm.render("Z: İleri",True,(60,60,60)),(box.right-42,box.bottom-12))
            return

        if self.phase=="bullet":
            if self.hinvuln==0 or (t_ms//60)%2==0:
                hs=spr("heart",(220,50,50))
                surf.blit(hs,(int(self.hx)-hs.get_width()//2,int(self.hy)-hs.get_height()//2))
            for b in self.bullets:
                if b["delay"]>0: continue
                bc=b.get("col",WHITE)
                osc=int(math.sin(t_ms*0.02+b["x"])*1) if self.is_boss else 0
                pygame.draw.rect(surf,bc,(int(b["x"])-b["sz"]+osc,int(b["y"])-b["sz"],b["sz"]*2,b["sz"]*2))
            ratio=1-self.btime/self.bdur
            pygame.draw.rect(surf,bcol,(79,box.bottom-4,int(box.width*ratio),3))

        elif self.phase=="menu":
            surf.blit(fsm.render(self.edesc,True,(160,160,160)),(box.x+4,box.y+5))
            if self.spare_cond=="empathy":
                surf.blit(fsm.render(f"★ EMPATİ BİRİKTİR ({self.empathy}/8)",True,(100,100,220)),(box.x+4,box.y+16))
            elif self.spare_cond and not self.talked:
                surf.blit(fsm.render("★ Önce konuş!",True,(120,120,60)),(box.x+4,box.y+16))
            labels=["SALDIR","EŞYA","MERCİ","KAÇ"]
            cols=[RED,GREEN,CYAN,ORANGE]
            for i,(lbl,col) in enumerate(zip(labels,cols)):
                bx2=box.x+2+(i%2)*(box.width//2); by2=box.bottom-32+(i//2)*14
                sel=i==self.menu_sel
                pygame.draw.rect(surf,col if sel else DGRAY,(bx2,by2,box.width//2-4,12))
                pygame.draw.rect(surf,WHITE,(bx2,by2,box.width//2-4,12),1 if not sel else 2)
                surf.blit(fsm.render(("▶ " if sel else "  ")+lbl,True,BLACK if sel else WHITE),(bx2+2,by2+2))

        else:
            is_good="affedildi" in self.msg or "Kaçtın" in self.msg
            is_bad="HAYATTA" in self.msg
            fc=CYAN if "SİSTEM" in self.msg or "VERİ" in self.msg else GREEN if is_good else RED if is_bad else YELLOW
            for i,ln in enumerate(self.msg.split('\n')):
                surf.blit(fmd.render(ln.strip(),True,fc),(VW//2-fmd.size(ln.strip())[0]//2,box.y+20+i*16))

    def is_over(self): return self.phase=="result" and self.mt<=0
    def won(self): return self.result in ("win","spare")
    def dead(self): return self.result=="dead"
    def fled(self): return self.result=="fled"

DEFAULT={
    "name":"Dursun","x":5.0,"y":10.0,
    "hp":80,"max_hp":80,"facing":"down",
    "kills":0,"spares":0,"gold":0,"lv":1,"xp":0,
    "atk_bonus":0,"def_bonus":0,"items":[
        {"name":"Simit","heal":20},{"name":"Çay","heal":15},
        {"name":"Baklava","heal":40},{"name":"Börek","heal":30}],
    "scene":"title","chapter":1,"global_frame":0,
    "talked":{},"flags":{},
    "quests":{},"chest_opened":[],
}
player=dict(DEFAULT)

def save_game():
    try:
        with open(SAVE_FILE,"w",encoding="utf-8") as f: json.dump(player,f,ensure_ascii=False,indent=2)
        play("save"); return True
    except: return False

def load_game():
    global player
    if not os.path.exists(SAVE_FILE): return False
    try:
        with open(SAVE_FILE,encoding="utf-8") as f: data=json.load(f)
        player.clear(); player.update(dict(DEFAULT)); player.update(data)
        if not player.get("name"): player["scene"]="title"
        return True
    except: return False

class TitleScreen:
    def __init__(self):
        self.frame=0; self.sel=0
        self.has_save=os.path.exists(SAVE_FILE)
        self.opts=["YENİ OYUN","DEVAM ET","ÇIKIŞ"] if self.has_save else ["YENİ OYUN","ÇIKIŞ"]
        self.stars=[(random.randint(0,VW),random.randint(0,VH),random.random()) for _ in range(70)]
        self.particles=[]

    def update(self,kj):
        self.frame+=1
        if self.frame%8==0:
            self.particles.append({"x":random.randint(0,VW),"y":VH,
                "vy":random.uniform(-0.8,-1.5),"life":random.randint(60,120),
                "col":(0,random.randint(100,255),random.randint(180,255))})
        for p in self.particles: p["y"]+=p["vy"]; p["life"]-=1
        self.particles=[p for p in self.particles if p["life"]>0]
        n=len(self.opts)
        if kj.get(pygame.K_UP):   self.sel=(self.sel-1)%n; play("menu_select")
        if kj.get(pygame.K_DOWN): self.sel=(self.sel+1)%n; play("menu_select")
        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN): play("menu_open"); return self.opts[self.sel]
        return None

    def draw(self,surf):
        surf.fill(BLACK)
        for sx,sy,sp in self.stars:
            br=int(80+50*math.sin(self.frame*0.04*sp))
            pygame.draw.circle(surf,(br,br,br),(int(sx),int(sy)),1 if sp<0.5 else 2)
        for p in self.particles:
            a=int(200*(p["life"]/120))
            ps2=pygame.Surface((3,3),pygame.SRCALPHA); ps2.fill((*p["col"],a))
            surf.blit(ps2,(int(p["x"]),int(p["y"])))
        logo=spr("logo",(0,0,0))
        sl=pygame.transform.scale(logo,(min(VW-20,logo.get_width()*2),min(60,logo.get_height()*2)))
        surf.blit(sl,(VW//2-sl.get_width()//2,8))
        pk=f"player_{'down' if self.frame//30%2==0 else 'down_walk'}"
        ps=pygame.transform.scale(spr(pk),(28,42))
        surf.blit(ps,(VW//2-14,76+int(math.sin(self.frame*0.08)*2)))
        sv=fsm.render("v6.0 — Dev Dünya • 7 Bölge • 66 Sprite",True,(80,80,140))
        surf.blit(sv,(VW//2-sv.get_width()//2,122))
        for i,lbl in enumerate(self.opts):
            sel=i==self.sel; col=YELLOW if sel else WHITE if lbl!="ÇIKIŞ" else (180,70,70)
            if sel: pygame.draw.rect(surf,(20,20,0),(VW//2-55,148+i*18-1,110,14))
            surf.blit(fmd.render(("▶ " if sel else "  ")+lbl,True,col),
                      (VW//2-fmd.size(("▶ " if sel else "  ")+lbl)[0]//2,148+i*18))
        if self.has_save:
            st=fsm.render("★ Kayıt mevcut",True,(80,120,80))
            surf.blit(st,(VW//2-st.get_width()//2,VH-20))

class NameEntry:
    CHARS=list("ABCDEFGHIJKLMNOPRSTUVYZÇĞİÖŞÜ")
    def __init__(self):
        self.name=""; self.r=0; self.c=0; self.frame=0; self.W=10
    def update(self,kj):
        self.frame+=1
        rows=math.ceil(len(self.CHARS)/self.W); total=rows+1
        if kj.get(pygame.K_UP):    self.r=(self.r-1)%total; play("menu_select")
        if kj.get(pygame.K_DOWN):  self.r=(self.r+1)%total; play("menu_select")
        if kj.get(pygame.K_LEFT):  self.c=(self.c-1)%self.W; play("menu_select")
        if kj.get(pygame.K_RIGHT): self.c=(self.c+1)%self.W; play("menu_select")
        if kj.get(pygame.K_BACKSPACE): self.name=self.name[:-1]
        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN):
            rc=math.ceil(len(self.CHARS)/self.W)
            if self.r<rc:
                idx=self.r*self.W+self.c
                if idx<len(self.CHARS) and len(self.name)<12:
                    self.name+=self.CHARS[idx]; play("dialogue",0.4)
            else:
                if self.c<5: self.name=self.name[:-1]
                elif self.name.strip(): return True
        return False
    def draw(self,surf):
        surf.fill(BLACK)
        surf.blit(flg.render("İSMİNİ GİR",True,YELLOW),(VW//2-40,8))
        nx,ny=50,32
        pygame.draw.rect(surf,DGRAY,(nx,ny,VW-100,18)); pygame.draw.rect(surf,WHITE,(nx,ny,VW-100,18),2)
        shown=self.name+("_" if self.frame//20%2==0 else " ")
        surf.blit(fmd.render(shown,True,WHITE),(nx+6,ny+3))
        rc=math.ceil(len(self.CHARS)/self.W)
        for i,ch in enumerate(self.CHARS):
            r,c=i//self.W,i%self.W; gx=14+c*28; gy=58+r*14
            sel=(r==self.r and c==self.c)
            if sel: pygame.draw.rect(surf,(50,50,0),(gx-2,gy-2,14,14))
            surf.blit(fmd.render(ch,True,YELLOW if sel else (160,160,160)),(gx,gy))
        sy=58+rc*14+5
        for i,(lbl,bx) in enumerate([("SİL",60),("BİTİR",150)]):
            sel=(self.r==rc and((i==0 and self.c<5)or(i==1 and self.c>=5)))
            pygame.draw.rect(surf,DGRAY,(bx-2,sy-2,65,14)); pygame.draw.rect(surf,YELLOW if sel else WHITE,(bx-2,sy-2,65,14),1)
            surf.blit(fmd.render(lbl,True,YELLOW if sel else WHITE),(bx,sy))

ENCOUNTER_ZONES={
    "forest":  lambda tx,ty: (0<=tx<50 and 42<=ty<80),
    "cave":    lambda tx,ty: (50<=tx<80 and 42<=ty<80),
    "factory": lambda tx,ty: (80<=tx<120 and 42<=ty<80),
}
NIGHT_ENCOUNTER_ZONE=lambda tx,ty: (0<=tx<80 and 0<=ty<40)

NPC_DEFS=[
    {"id":"ridvan","tx":5, "ty":6, "spr":"npc_old", "name":"Rıdvan Efendi"},
    {"id":"ayse",  "tx":13,"ty":5, "spr":"npc_girl","name":"Ayşe Harika"},
    {"id":"husrev","tx":64,"ty":17,"spr":"npc_old", "name":"Demirci Hüsrev"},
    {"id":"fatih", "tx":5, "ty":25,"spr":"npc_girl","name":"Küçük Fatih"},
    {"id":"meryem","tx":13,"ty":25,"spr":"npc_girl","name":"Meryem Nine"},
    {"id":"zeliha","tx":29,"ty":25,"spr":"npc_girl","name":"Zeliha Teyze"},
    {"id":"ahmet", "tx":82,"ty":3, "spr":"npc_fisherman","name":"Balıkçı Ahmet"},
    {"id":"fatma", "tx":82,"ty":11,"spr":"npc_fisherman","name":"Balıkçı Fatma"},
    {"id":"kaptan","tx":82,"ty":23,"spr":"npc_fisherman","name":"Yaşlı Kaptan"},
    {"id":"isci",  "tx":84,"ty":45,"spr":"npc_engineer","name":"Fabrika İşçisi"},
    {"id":"muhendis","tx":102,"ty":60,"spr":"npc_engineer","name":"Mühendis Kemal"},
]

EXTRA_DIALOGUES={
    "ahmet":   ["Balık tutmak sabır ister.","Bugün iyi avladım.","THE ALGO'yu hiç balık tutarken görmedim.","Belki o da denemelidir."],
    "fatma":   ["Şu fabrika dumanı balıkları korkutuyor.","Ama teknemi bırakmam.","Deniz temiz. İnsanlar değil.","Sen temiz görünüyorsun. İyi yolculuklar."],
    "kaptan":  ["50 yıldır bu gölde.","Her şeyi gördüm.","THE ALGO geldi, değişmeyen tek şey su oldu.","Suya bak. Cevap orada."],
    "isci":    ["Fabrika beni yordu.","Ama ne yapayım, çalışmak lazım.","Makineler artık bizi dinlemiyor.","THE ALGO programladı onları."],
    "muhendis":["Sistemleri anlıyorum ama anlayamıyorum.","THE ALGO'nun kodu... karmaşık.","Ama içinde bir mantık var.","Mantığı kırman lazım. Empatiyle."],
}

class Overworld:
    def __init__(self):
        self.frame=0; self.battle=None
        self.dialogue=DialogueBox()
        self.shop=ShopScreen()
        self.quest_log=QuestLog()
        self.cutscene=None
        self.puzzle=PuzzleRoom(solution=[2,0,3,1],title="ORMAN PUZZLEsi",
                               hint="Meryem'den ipucunu al!")
        self.save_screen=None
        self.pause_sel=0; self.pause_active=False
        self.step_t=0; self.enc_cool=0
        self.region_msg=""; self.region_t=0; self.prev_region=""
        self.hint_t=200
        self.npcs=self._init_npcs()
        self.chest_opened=set(player.get("chest_opened",[]))

    def _init_npcs(self):
        npcs=[]
        n=player.get("name","Dursun")
        for nd in NPC_DEFS:
            npc=dict(nd); npc["talk_count"]=0; npc["all_dialogues"]=[]
            nd2=NPC_DIALOGUES.get(nd["id"],{})
            for key in ["ilk_konusma","ikinci_konusma","ucuncu_konusma","dorduncu_konusma","ipucu_algo"]:
                d=nd2.get("dialogues",{}).get(key)
                if d: npc["all_dialogues"].append([l.format(n) if '{}'in l else l for l in d])
            if nd["id"] in EXTRA_DIALOGUES:
                lines=EXTRA_DIALOGUES[nd["id"]]
                npc["all_dialogues"].append(lines)
            if not npc["all_dialogues"]:
                npc["all_dialogues"]=[["Merhaba!","İyi yolculuklar."]]
            npcs.append(npc)
        return npcs

    def _get_region(self):
        tx,ty=int(player["x"]),int(player["y"])
        if 80<=tx<120 and 0<=ty<40: return "Göl Kenarı"
        if 40<=tx<80 and 0<=ty<30: return "Pazar Yeri"
        if 40<=tx<80 and 30<=ty<40: return "THE ALGO Geçişi"
        if 0<=tx<50 and 40<=ty<80: return "Gizemli Orman"
        if 50<=tx<80 and 40<=ty<80: return "Gizli Mağara"
        if 80<=tx<120 and 40<=ty<80: return "Terk Edilmiş Fabrika"
        return "Dursunköy"

    def _npc_near(self):
        px,py=int(player["x"]+0.5),int(player["y"]+0.5)
        for npc in self.npcs:
            if abs(npc["tx"]-px)<=1 and abs(npc["ty"]-py)<=1: return npc
        return None

    def _show_npc(self,npc):
        dials=npc.get("all_dialogues",[])
        if not dials: return
        night=get_npc_night_bonus(npc["id"],player.get("global_frame",0))
        if night and get_time_of_day(player.get("global_frame",0))=="gece":
            lines=night
        else:
            idx=min(npc["talk_count"],len(dials)-1)
            lines=dials[idx]
            npc["talk_count"]=min(npc["talk_count"]+1,len(dials)-1)

        col_map={"ridvan":CYAN,"meryem":CYAN,"zeliha":(200,150,80),"kaptan":TEAL}
        col=col_map.get(npc["id"],WHITE)
        self.dialogue.show(npc["name"],lines,portrait=npc["spr"],col=col)
        player.setdefault("talked",{})[npc["id"]]=True
        quest_map={"husrev":"cekic_bul","ayse":"fistik_izi","ridvan":"ridvan_simit","meryem":"algo_sifre"}
        if npc["id"] in quest_map:
            self.quest_log.start_quest(quest_map[npc["id"]])
        play("menu_select")

    def update(self,kp,kj):
        self.frame+=1
        player["global_frame"]=player.get("global_frame",0)+1
        self.hint_t=max(0,self.hint_t-1)
        self.quest_log.update(kj)

        if self.cutscene and self.cutscene.active:
            self.cutscene.update(kj)
            if self.cutscene.done: self.cutscene=None
            return

        if self.puzzle.active:
            self.puzzle.update(kj)
            if self.puzzle.solved:
                self.puzzle.active=False
                player.setdefault("flags",{})["puzzle_done"]=True
                self.dialogue.show("PUZZLE","Doğru! Orman sana kapıyı açtı.",col=GREEN)
                player.setdefault("items",[]).append({"name":"Orman Taşı","heal":60})
                play("quest_done")
            return

        if self.save_screen:
            self._upd_save(kj); return
        if self.pause_active:
            self._upd_pause(kj); return

        if self.battle:
            self.battle.update(kp,kj)
            if self.battle.is_over():
                self._battle_end(); return
            return

        if self.dialogue.active:
            self.dialogue.update()
            if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN): self.dialogue.advance()
            return

        spd=0.08; dx,dy=0,0; moved=False
        if kp.get(pygame.K_LEFT):  dx=-spd; player["facing"]="left";  moved=True
        if kp.get(pygame.K_RIGHT): dx= spd; player["facing"]="right"; moved=True
        if kp.get(pygame.K_UP):    dy=-spd; player["facing"]="up";    moved=True
        if kp.get(pygame.K_DOWN):  dy= spd; player["facing"]="down";  moved=True

        nx=player["x"]+dx; ny=player["y"]+dy
        nx=max(1,min(MAP_W-2,nx)); ny=max(1,min(MAP_H-2,ny))
        if not is_solid(int(nx+0.5),int(player["y"]+0.5)): player["x"]=nx
        if not is_solid(int(player["x"]+0.5),int(ny+0.5)): player["y"]=ny

        if moved:
            self.step_t+=1
            if self.step_t%18==0:
                reg=self._get_region()
                sfx={"Gizli Mağara":"step_cave","Terk Edilmiş Fabrika":"step_road"}.get(reg,"step_grass")
                play(sfx,0.1)

        cam.update(player["x"],player["y"])

        reg=self._get_region()
        if reg!=self.prev_region:
            self.prev_region=reg; self.region_msg=f"— {reg} —"; self.region_t=150
        if self.region_t>0: self.region_t-=1

        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN):
            npc=self._npc_near()
            if npc: self._show_npc(npc)
            else:
                fx=int(player["x"]+0.5+{"left":-1,"right":1,"up":0,"down":0}[player["facing"]])
                fy=int(player["y"]+0.5+{"up":-1,"down":1,"left":0,"right":0}[player["facing"]])
                t=tile_at(fx,fy)
                if t=='sv':
                    self.dialogue.show("KAYIT NOKTASI",["Bir sıcaklık hissediyorsun...","Kaydetmek ister misin?"],
                        cb=self._open_save,col=GREEN); play("save",0.3)
                elif t=='S':
                    self._handle_sign(fx,fy)
                elif t=='ch':
                    self._handle_chest(fx,fy)
                elif t=='d':
                    if 62<=fx<=76 and 16<=fy<=26: self.shop.open()
                    else: self.dialogue.show("KAPI",["İçerisi boş."],col=GRAY)
                elif t=='sd':
                    self.dialogue.show("MERDİVEN",["Aşağıya iniyorsun..."],
                        cb=lambda:play("stairs"),col=BROWN)
                elif t=='su':
                    self.dialogue.show("MERDİVEN",["Yukarı çıkıyorsun..."],
                        cb=lambda:play("stairs"),col=BROWN)
                elif t in ('w','W2'):
                    self.dialogue.show("GÖL",["Serin su...","Balıklar var."],col=BLUE)
                elif t=='T':
                    self.dialogue.show("AĞAÇ",["...","(Ağaç susuyor.)","(Ama dinliyor.)"],col=(50,150,50))
                elif t=='Bo':
                    self.dialogue.show("TEKNE",["Sallanan ahşap bir tekne.","Balıkçı kokuyor."],col=BROWN)
                elif t=='Po':
                    self.dialogue.show("PORTAL",["Güçlü bir çekim hissediyorsun.","THE ALGO bölgesi...","Hazır mısın?"],col=PURPLE)
                elif t=='An':
                    self.dialogue.show("ALGO NODU",["Veri akıyor.","İçinde bir şey fısıldıyor...","01010100 = T, 01010101 = U, 01010010 = R, 01001011 = K"],col=CYAN)
                elif t=='Fi':
                    self.dialogue.show("BALIK",["Bir balık gördün!","...","Gitti."],col=BLUE)

        if kj.get(pygame.K_s): self._open_save()
        if kj.get(pygame.K_j): self.quest_log.active=not self.quest_log.active; play("menu_open")
        if kj.get(pygame.K_q): self.pause_active=not self.pause_active; play("menu_open")

        ptx,pty=int(player["x"]+0.5),int(player["y"]+0.5)
        self.enc_cool=max(0,self.enc_cool-1)
        tod=get_time_of_day(player.get("global_frame",0))
        in_enc=any(f(ptx,pty) for f in ENCOUNTER_ZONES.values())
        night_enc=NIGHT_ENCOUNTER_ZONE(ptx,pty) and tod=="gece"

        if (in_enc or night_enc) and self.enc_cool==0:
            chance=0.012 if in_enc else 0.006
            if random.random()<chance:
                self.enc_cool=140
                if night_enc and not in_enc:
                    key="Gece Canavarı"
                else:
                    zone="cave" if ENCOUNTER_ZONES["cave"](ptx,pty) else \
                         "factory" if ENCOUNTER_ZONES["factory"](ptx,pty) else "forest"
                    pool={"cave":CAVE_POOL,"factory":FACTORY_POOL,"forest":NORMAL_POOL}[zone]
                    key=random.choice(pool)
                self.battle=Battle(key)

        if 68<=ptx<=72 and 33<=pty<=34 and not player.get("flags",{}).get("duman_met"):
            player.setdefault("flags",{})["duman_met"]=True
            n=player.get("name","???")
            lines=[l.format(n) if '{}'in l else l for l in DUMAN_DIALOGUES["ilk_karsilasma"]["lines"]]
            self.dialogue.show("DUMAN",lines,cb=self._duman_fight,portrait="npc_villain",col=RED)

        if 29<=ptx<=31 and 74<=pty<=76 and not player.get("flags",{}).get("orman_ruhu_met"):
            player.setdefault("flags",{})["orman_ruhu_met"]=True
            self.dialogue.show("???",["Ormanda bir güç hissediyorsun...","Orman seni sınıyor."],
                cb=self._orman_fight,col=(40,150,40))

        if 20<=ptx<=22 and 71<=pty<=73 and not player.get("flags",{}).get("puzzle_done"):
            if not self.puzzle.active:
                self.puzzle.open("Doğru sırayı bul: △ ○ □ ★")

        if 77<=ptx<=80 and 33<=pty<=34 and player.get("flags",{}).get("duman_met") and \
           not player.get("flags",{}).get("algo_met"):
            player.setdefault("flags",{})["algo_met"]=True
            self.cutscene=make_intro_cutscene(player.get("name","???"),
                cb=lambda: self.dialogue.show("???",
                    ["VERİ ALINIYOR...","Tanımsız değişken tespit edildi.","Sen...","...İlginçsin."],
                    cb=self._algo_fight,col=CYAN))

        self._check_ending()

    def _battle_end(self):
        key=self.battle.ekey
        if self.battle.dead():
            player["scene"]="gameover"
        elif key=="Duman":
            if self.battle.result=="spare":
                player.setdefault("flags",{})["duman_spared"]=True
                self.cutscene=make_duman_defeat_cutscene()
            else: player.setdefault("flags",{})["duman_killed"]=True
        elif key=="Duman 2.0":
            player.setdefault("flags",{})["duman2_done"]=True
        elif key=="Orman Ruhu":
            player.setdefault("flags",{})["orman_ruhu_done"]=True
            if self.battle.result=="spare": player.setdefault("items",[]).append({"name":"Orman Nefesi","heal":80})
        elif key=="THE ALGO":
            player.setdefault("flags",{})["algo_done"]=True
            player.setdefault("flags",{})["algo_spared"]=(self.battle.result=="spare")
            self.cutscene=make_algo_defeat_cutscene(player.get("name","???"))
        self.battle=None

    def _check_ending(self):
        flags=player.get("flags",{})
        if flags.get("algo_done"):
            k=player.get("kills",0); sp=player.get("spares",0)
            if flags.get("algo_spared") and k==0: player["scene"]="ending_good"
            elif k>=1: player["scene"]="ending_bad"

    def _duman_fight(self):
        self.battle=Battle("Duman")
        self.battle.talked=bool(player.get("talked",{}).get("ridvan")) and bool(player.get("talked",{}).get("ayse"))

    def _orman_fight(self): self.battle=Battle("Orman Ruhu"); play("battle_start",0.8)
    def _algo_fight(self): self.battle=Battle("THE ALGO"); play("battle_start",0.9)

    def _handle_sign(self,fx,fy):
        sig=SIGN_DIALOGUES.get("orman_uyarisi")
        if 38<=fy<=40 and 17<=fx<=21: sig=SIGN_DIALOGUES.get("koy_girisi")
        elif fy<=2 and fx>=70: sig=SIGN_DIALOGUES.get("algo_uyarisi")
        if sig: self.dialogue.show(sig["speaker"],sig["lines"],col=YELLOW)
        else: self.dialogue.show("TABELA",["Okunaksız yazı."],col=YELLOW)

    def _handle_chest(self,fx,fy):
        key=f"{fx}_{fy}"
        if key in self.chest_opened:
            self.dialogue.show("SANDIK",["Bu sandık boş."],col=BROWN); return
        self.chest_opened.add(key)
        player.setdefault("chest_opened",[]).append(key)
        rewards=[
            {"name":"Simit","heal":20},{"name":"Baklava","heal":40},
            {"name":"Çay","heal":15},{"name":"Börek","heal":30},
        ]
        if 50<=fx<80 and 40<=fy<80:
            rewards=[{"name":"Mağara Kristali","heal":70},{"name":"Fıstıklı Baklava","heal":60}]
        it=random.choice(rewards)
        player.setdefault("items",[]).append(it)
        self.dialogue.show("SANDIK",[f"İçinde {it['name']} buldun! +{it['heal']} HP"],col=YELLOW)
        play("chest_open"); player.setdefault("gold",0); player["gold"]+=random.randint(5,20)

    def _open_save(self):
        self.save_screen={"saved":False,"timer":0,"frame":0}

    def _upd_save(self,kj):
        ss=self.save_screen; ss["frame"]+=1
        if ss["saved"]:
            ss["timer"]-=1
            if ss["timer"]<=0: self.save_screen=None; return
        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN):
            save_game(); ss["saved"]=True; ss["timer"]=90
        if kj.get(pygame.K_x) or kj.get(pygame.K_ESCAPE):
            self.save_screen=None

    def _upd_pause(self,kj):
        n=3
        if kj.get(pygame.K_UP):   self.pause_sel=(self.pause_sel-1)%n; play("menu_select")
        if kj.get(pygame.K_DOWN): self.pause_sel=(self.pause_sel+1)%n; play("menu_select")
        if kj.get(pygame.K_q) or kj.get(pygame.K_x): self.pause_active=False
        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN):
            self.pause_active=False
            if self.pause_sel==0: self._open_save()
            elif self.pause_sel==1: player["scene"]="title"

    def draw(self,surf):
        if self.cutscene and self.cutscene.active:
            self.cutscene.draw(surf); return

        if self.battle: self.battle.draw(surf); return

        surf.fill((15,15,20))
        draw_map_view(surf,cam.tile_x(),cam.tile_y(),self.frame)

        t_ms=pygame.time.get_ticks()
        for npc in self.npcs:
            sx,sy=cam.world_to_screen(npc["tx"],npc["ty"])
            if -20<sx<VW+20 and -20<sy<VH+20:
                ns=spr(npc["spr"])
                surf.blit(ns,(sx,sy-ns.get_height()+TH))
                if not player.get("talked",{}).get(npc["id"]):
                    bx2,by2=sx+1,sy-ns.get_height()+TH-14
                    pygame.draw.rect(surf,WHITE,(bx2,by2,12,11))
                    pygame.draw.rect(surf,BLACK,(bx2,by2,12,11),1)
                    surf.blit(fmd.render("!",True,RED),(bx2+4,by2+1))

        wf=(self.frame//8)%2==0
        f=player["facing"]; sk=f"player_{f}_walk" if wf else f"player_{f}"
        ps=spr(sk if sk in sprites else f"player_{f}")
        px,py=cam.world_to_screen(player["x"],player["y"])
        surf.blit(ps,(int(px)-ps.get_width()//2+TW//2,int(py)-ps.get_height()+TH))

        gf=player.get("global_frame",0)
        dark=get_ambient_overlay(gf)
        if dark>10:
            night_surf=pygame.Surface((VW,VH),pygame.SRCALPHA)
            night_col=get_sky_color(gf) if dark<80 else NIGHT_BLUE
            night_surf.fill((*NIGHT_BLUE,dark))
            surf.blit(night_surf,(0,0))
            if dark>80:
                for sx2,sy2,_ in [(random.randint(0,VW),random.randint(0,VH//2),0) for _ in range(3)]:
                    if random.random()<0.3: pygame.draw.circle(surf,WHITE,(sx2,sy2),1)

        pygame.draw.rect(surf,BLACK,(0,0,VW,14))
        surf.blit(fsm.render(f"♥{player['hp']}/{player['max_hp']}",True,RED),(3,3))
        surf.blit(fmd.render(player["name"],True,YELLOW),(VW//2-fmd.size(player["name"])[0]//2,3))
        surf.blit(fsm.render(f"G:{player.get('gold',0)} LV:{player.get('lv',1)}",True,YELLOW),(VW-80,3))
        tod=get_time_of_day(gf); tcol=YELLOW if "gündüz"in tod else (150,150,255)
        ticon="☀" if "gündüz"in tod or "şafak"in tod else "★"
        surf.blit(fsm.render(f"{ticon}{tod}",True,tcol),(VW-80,3+9))

        if self.region_t>0:
            rm=fsm.render(self.region_msg,True,(180,180,255))
            surf.blit(rm,(VW//2-rm.get_width()//2,16))

        self.quest_log.draw_notif(surf)

        if self.hint_t>0:
            ht=fsm.render("Ok:Hareket Z:Konuş S:Kaydet J:Görev Q:Pause",True,(60,60,60))
            surf.blit(ht,(VW//2-ht.get_width()//2,VH-10))

        self.dialogue.draw(surf)

        if self.shop.active: self.shop.draw(surf)

        if self.quest_log.active:
            self.quest_log.draw(surf,WHITE,YELLOW,GRAY,DGRAY,GREEN,CYAN)

        if self.puzzle.active: self.puzzle.draw(surf)

        if self.save_screen: self._draw_save(surf)

        if self.pause_active: self._draw_pause(surf)

    def _draw_save(self,surf):
        ss=self.save_screen
        ov=pygame.Surface((VW,VH),pygame.SRCALPHA); ov.fill((0,0,0,160)); surf.blit(ov,(0,0))
        bx,by=VW//2-65,VH//2-35
        pygame.draw.rect(surf,BLACK,(bx-2,by-2,132,72)); pygame.draw.rect(surf,WHITE,(bx,by,130,70),2)
        pygame.draw.rect(surf,DGRAY,(bx+2,by+2,126,66))
        if ss["saved"]:
            surf.blit(fmd.render("KAYEDİLDİ!",True,GREEN),(bx+20,by+20))
            surf.blit(fsm.render(f"{player['name']} LV{player.get('lv',1)}",True,WHITE),(bx+20,by+36))
        else:
            surf.blit(fmd.render("KAYDET?",True,YELLOW),(bx+30,by+10))
            surf.blit(fsm.render("Z=Evet  X=İptal",True,GRAY),(bx+20,by+48))

    def _draw_pause(self,surf):
        ov=pygame.Surface((VW,VH),pygame.SRCALPHA); ov.fill((0,0,0,180)); surf.blit(ov,(0,0))
        bx,by=VW//2-60,VH//2-40
        pygame.draw.rect(surf,BLACK,(bx-2,by-2,124,84)); pygame.draw.rect(surf,WHITE,(bx,by,122,82),2)
        pygame.draw.rect(surf,DGRAY,(bx+2,by+2,118,78))
        surf.blit(fmd.render("PAUSE",True,YELLOW),(VW//2-fmd.size("PAUSE")[0]//2,by+6))
        for i,opt in enumerate(["KAYDET","ANA MENÜ","DEVAM"]):
            sel=i==self.pause_sel; y=by+28+i*15
            pygame.draw.rect(surf,(30,30,30) if not sel else (50,50,0),(bx+8,y,106,12))
            surf.blit(fsm.render(("▶ " if sel else "  ")+opt,True,YELLOW if sel else WHITE),(bx+10,y+2))

class GameOver:
    def __init__(self): self.f=0
    def update(self,kj):
        self.f+=1
        if self.f==30: play("bad_end",0.6)
        if self.f>90 and (kj.get(pygame.K_z) or kj.get(pygame.K_RETURN)):
            player["hp"]=player["max_hp"]; player["scene"]="overworld"
            player["x"]=5.0; player["y"]=10.0
    def draw(self,surf):
        surf.fill(BLACK)
        surf.blit(fttl.render("HAYATTA",True,RED),(VW//2-60,VH//2-45))
        surf.blit(fttl.render("KALAMADINIZ",True,RED),(VW//2-80,VH//2-25))
        surf.blit(fmd.render("Ama henüz bitmedi...",True,(120,50,50)),(VW//2-80,VH//2+5))
        if self.f>90 and (self.f//30)%2:
            surf.blit(fsm.render("Z: Devam Et",True,GRAY),(VW//2-30,VH//2+30))

class Ending:
    def __init__(self,kind):
        self.kind=kind; self.f=0; self.cur=0; self.ch=0; self.done=False; self.particles=[]
        n=player.get("name","???"); k=player.get("kills",0)
        raw=ENDING_SLIDES.get(kind,ENDING_SLIDES["notr_son"])
        self.slides=[{**s,"text":s["text"].format(n,k) if '{}'in s["text"] else s["text"]} for s in raw]
    def update(self,kj):
        self.f+=1
        sl=self.slides[self.cur] if self.cur<len(self.slides) else self.slides[-1]
        if self.f%2==0 and self.ch<len(sl["text"]): self.ch+=1
        if self.kind=="iyi_son" and self.f%5==0:
            self.particles.append({"x":random.randint(0,VW),"y":random.randint(0,VH),
                "vx":random.uniform(-0.5,0.5),"vy":random.uniform(-1,-0.2),
                "life":random.randint(60,120),"max":120,"col":random.choice([YELLOW,CYAN,GREEN,WHITE]),"sz":random.randint(1,3)})
        for p in self.particles: p["x"]+=p["vx"]; p["y"]+=p["vy"]; p["life"]-=1
        self.particles=[p for p in self.particles if p["life"]>0]
        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN):
            if self.ch<len(sl["text"]): self.ch=len(sl["text"])
            else:
                self.cur+=1; self.ch=0
                if self.cur>=len(self.slides):
                    if not self.done: self.done=True; play("good_end" if self.kind=="iyi_son" else "bad_end")
                else: play("menu_select",0.4)
        if self.done and (kj.get(pygame.K_z) or kj.get(pygame.K_RETURN)):
            player.update(dict(DEFAULT)); player["scene"]="title"
    def draw(self,surf):
        sl=self.slides[self.cur] if self.cur<len(self.slides) else self.slides[-1]
        surf.fill(sl["bg"])
        for p in self.particles:
            a=int(255*(p["life"]/p["max"]))
            ps2=pygame.Surface((p["sz"]*2,p["sz"]*2),pygame.SRCALPHA); ps2.fill((*p["col"],a))
            surf.blit(ps2,(int(p["x"]),int(p["y"])))
        y=20
        for i in range(self.cur):
            if i<len(self.slides):
                pt=fsm.render(self.slides[i]["text"],True,(50,50,50))
                surf.blit(pt,(VW//2-pt.get_width()//2,y)); y+=16
        shown=sl["text"][:self.ch]
        is_fin="SON" in shown or "DEVAM" in shown
        t=fxl.render(shown,True,YELLOW if is_fin else sl["col"])
        ty=max(y,VH//2-10)
        ts=fxl.render(shown,True,BLACK); surf.blit(ts,(VW//2-t.get_width()//2+2,ty+2))
        surf.blit(t,(VW//2-t.get_width()//2,ty))
        if self.cur>=len(self.slides) or self.ch>=len(sl["text"]):
            if (self.f//25)%2:
                surf.blit(fsm.render("Z: Devam",True,GRAY),(VW//2-20,VH-14))

cam=Camera()
name_entry=NameEntry()
title_scr=TitleScreen()
overworld=Overworld()
gameover=GameOver()
ending=None
kp={}; kj={}; running=True
FS=True

while running:
    kj={}
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT: running=False
        elif ev.type==pygame.KEYDOWN:
            kj[ev.key]=True
            if ev.key==pygame.K_ESCAPE: running=False
            if ev.key==pygame.K_F11: FS=not FS; set_screen(FS)
        elif ev.type==pygame.KEYUP: kp[ev.key]=False
    raw=pygame.key.get_pressed()
    for k in [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,
               pygame.K_z,pygame.K_RETURN,pygame.K_x,pygame.K_BACKSPACE,
               pygame.K_s,pygame.K_q,pygame.K_j]:
        kp[k]=raw[k]

    canvas.fill(BLACK)
    scene=player["scene"]

    if scene=="name_entry":
        if name_entry.update(kj):
            player["name"]=name_entry.name.strip() or "Dursun"
            player["scene"]="overworld"; overworld=Overworld(); save_game()
        name_entry.draw(canvas)

    elif scene=="title":
        res=title_scr.update(kj); title_scr.draw(canvas)
        if res=="YENİ OYUN":
            player.update(dict(DEFAULT)); player["scene"]="name_entry"; name_entry=NameEntry(); title_scr=TitleScreen()
        elif res=="DEVAM ET":
            if load_game(): player["scene"]="overworld"; overworld=Overworld()
        elif res=="ÇIKIŞ": running=False

    elif scene=="overworld":
        overworld.update(kp,kj); overworld.draw(canvas)

    elif scene=="gameover":
        if not isinstance(gameover,GameOver): gameover=GameOver()
        gameover.update(kj); gameover.draw(canvas)

    elif scene in ("ending_good","ending_bad","ending_notr"):
        kind={"ending_good":"iyi_son","ending_bad":"kotu_son","ending_notr":"notr_son"}[scene]
        if ending is None: ending=Ending(kind)
        ending.update(kj); ending.draw(canvas)
        if player["scene"]=="title": title_scr=TitleScreen(); ending=None

    scaled=pygame.transform.scale(canvas,(SW,SH))
    screen.blit(scaled,(0,0))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit(); sys.exit()
