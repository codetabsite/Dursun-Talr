import pygame, math, random

DAY_CYCLE_TICKS = 7200

def get_day_alpha(frame):
    t = (frame % DAY_CYCLE_TICKS) / DAY_CYCLE_TICKS
    return max(0.0, math.sin(t * math.pi))

def get_time_of_day(frame):
    t = (frame % DAY_CYCLE_TICKS) / DAY_CYCLE_TICKS
    if t < 0.15:   return "şafak"
    elif t < 0.45: return "gündüz"
    elif t < 0.55: return "akşam"
    elif t < 0.85: return "gece"
    else:          return "şafak"

def get_sky_color(frame):
    tod = get_time_of_day(frame)
    alpha = get_day_alpha(frame)
    colors = {
        "şafak":  (200, 120, 80),
        "gündüz": (80, 140, 220),
        "akşam":  (220, 80, 60),
        "gece":   (10, 10, 40),
    }
    return colors.get(tod, (20, 20, 35))

def get_ambient_overlay(frame):
    alpha = get_day_alpha(frame)
    darkness = int(alpha * 180)
    return darkness

def get_npc_night_bonus(npc_id, frame):
    tod = get_time_of_day(frame)
    if tod != "gece": return None
    night_lines = {
        "ridvan": ["Hâlâ uyumadın mı?", "Bu saatte gezmeyi severim.", "Yıldızlara bak. THE ALGO onları hesaplayamaz."],
        "ayse":   ["GECE!! En iyi vakit!!", "Fıstık bu saatte uyuyor mu? Bilmiyorum!!", "Yıldız sayıyordum. 47'de kaldım."],
        "meryem": ["Gece daha sakin...", "Yaşlılar gece iyi uyuyamaz.", "Senin için dua ettim bu gece, evladım."],
        "zeliha": ["Çay yapayım mı? Gece çayı başka olur.", "Bu saatte kim gezer böyle?"],
        "husrev": ["Dükkân kapalı ama konuşabiliriz.", "Gece çalışmak yasak dedi THE ALGO. Uymuyorum."],
        "fatih":  ["Sssst! Anne görmesin!", "Gece dışarıda olmak yasak ama... buradayım işte."],
    }
    return night_lines.get(npc_id)

QUESTS = {
    "cekic_bul": {
        "id": "cekic_bul",
        "title": "Hüsrev'in Çekici",
        "giver": "husrev",
        "desc": "Hüsrev'in kayıp çekicini bul. Ormanda bir yerlerde olabilir.",
        "steps": [
            "Hüsrev ile konuş",
            "Ormanda çekici ara (karşılaşmada düşür)",
            "Çekici Hüsrev'e geri ver",
        ],
        "reward_gold": 30,
        "reward_item": {"name": "Ustanın Simidi", "heal": 50},
        "reward_msg": "Hüsrev çekicini buldu! +30G ve Ustanın Simidi!",
        "state": "available",
        "cur_step": 0,
    },
    "fistik_izi": {
        "id": "fistik_izi",
        "title": "Fıstık'ın İzi",
        "giver": "ayse",
        "desc": "Ayşe'nin tilkisi Fıstık ormanda kayboldu. İzini bul.",
        "steps": [
            "Ayşe ile konuş",
            "Ormanda 'tilki izi' tabelasını bul",
            "Fıstık'ı Ayşe'ye geri götür",
        ],
        "reward_gold": 20,
        "reward_item": {"name": "Fıstıklı Baklava", "heal": 60},
        "reward_msg": "Fıstık bulundu! Ayşe ağladı (sevinçten). +20G ve Fıstıklı Baklava!",
        "state": "available",
        "cur_step": 0,
    },
    "ridvan_simit": {
        "id": "ridvan_simit",
        "title": "Rıdvan'ın Son Simidi",
        "giver": "ridvan",
        "desc": "Rıdvan Efendi'nin son simidini mağazadan al, geri getir.",
        "steps": [
            "Rıdvan ile konuş",
            "Mağazadan simit satın al",
            "Rıdvan'a ver",
        ],
        "reward_gold": 0,
        "reward_item": {"name": "Rıdvan'ın Duası", "heal": 999},
        "reward_msg": "Rıdvan Efendi dua etti. HP tamamen doldu!",
        "state": "available",
        "cur_step": 0,
    },
    "algo_sifre": {
        "id": "algo_sifre",
        "title": "THE ALGO'nun Şifresi",
        "giver": "meryem",
        "desc": "Meryem Nine THE ALGO'nun zayıf noktasını biliyor. Onu dinle.",
        "steps": [
            "Meryem ile konuş",
            "Gizli tabelayı oku (ormanda)",
            "THE ALGO ile savaşta empatiyi kullan",
        ],
        "reward_gold": 0,
        "reward_item": None,
        "reward_msg": "THE ALGO'nun zayıf noktasını öğrendin. Empati gücün +1!",
        "state": "available",
        "cur_step": 0,
    },
}

QUEST_LOG_LABELS = {
    "available": "[ ]",
    "active":    "[~]",
    "done":      "[✓]",
}

class QuestLog:
    def __init__(self):
        self.quests = {k: dict(v) for k, v in QUESTS.items()}
        self.active = False
        self.sel = 0
        self.new_quest_notif = None
        self.notif_timer = 0

    def start_quest(self, qid):
        q = self.quests.get(qid)
        if q and q["state"] == "available":
            q["state"] = "active"
            self.new_quest_notif = q["title"]
            self.notif_timer = 180

    def advance_quest(self, qid):
        q = self.quests.get(qid)
        if not q or q["state"] != "active": return False
        q["cur_step"] += 1
        if q["cur_step"] >= len(q["steps"]):
            q["state"] = "done"
            return True
        return False

    def is_active(self, qid):
        return self.quests.get(qid, {}).get("state") == "active"

    def is_done(self, qid):
        return self.quests.get(qid, {}).get("state") == "done"

    def get_step(self, qid):
        return self.quests.get(qid, {}).get("cur_step", 0)

    def update(self, kj):
        if self.notif_timer > 0: self.notif_timer -= 1
        if not self.active: return
        n = len(self.quests)
        if kj.get(pygame.K_UP):   self.sel = (self.sel - 1) % n
        if kj.get(pygame.K_DOWN): self.sel = (self.sel + 1) % n
        if kj.get(pygame.K_x) or kj.get(pygame.K_q): self.active = False

    def draw(self, surface, WHITE=(255,255,255), YELLOW=(255,220,60),
             GRAY=(100,100,100), DGRAY=(40,40,40), GREEN=(50,200,80),
             CYAN=(60,220,220)):
        W, H = surface.get_size()
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        bx, by, bw, bh = 15, 15, W-30, H-30
        pygame.draw.rect(surface, DGRAY, (bx, by, bw, bh))
        pygame.draw.rect(surface, YELLOW, (bx, by, bw, bh), 2)

        try:
            font_lg = pygame.font.SysFont("Courier New", 16, bold=True)
            font_md = pygame.font.SysFont("Courier New", 11, bold=True)
            font_sm = pygame.font.SysFont("Courier New", 8, bold=True)
        except:
            font_lg = pygame.font.Font(None, 20)
            font_md = pygame.font.Font(None, 14)
            font_sm = pygame.font.Font(None, 11)

        t = font_lg.render("★ GÖREV GÜNLÜĞÜ ★", True, YELLOW)
        surface.blit(t, (bx + bw//2 - t.get_width()//2, by + 6))

        qlist = list(self.quests.values())
        for i, q in enumerate(qlist):
            y = by + 30 + i * 38
            sel = i == self.sel
            col = {"available": WHITE, "active": CYAN, "done": GREEN}.get(q["state"], WHITE)
            if sel:
                pygame.draw.rect(surface, (30, 30, 20), (bx+4, y, bw-8, 36))
                pygame.draw.rect(surface, YELLOW, (bx+4, y, bw-8, 36), 1)
            lbl = QUEST_LOG_LABELS.get(q["state"], "[ ]")
            t2 = font_md.render(f"{lbl} {q['title']}", True, col)
            surface.blit(t2, (bx+10, y+2))
            if sel:
                t3 = font_sm.render(q["desc"], True, (180,180,180))
                surface.blit(t3, (bx+14, y+14))
                step_txt = q["steps"][min(q["cur_step"], len(q["steps"])-1)]
                sc = GREEN if q["state"]=="done" else YELLOW
                t4 = font_sm.render(f"► {step_txt}", True, sc)
                surface.blit(t4, (bx+14, y+24))

        ht = font_sm.render("↑↓: Seç   X: Kapat", True, GRAY)
        surface.blit(ht, (bx + bw//2 - ht.get_width()//2, by + bh - 12))

        if self.notif_timer > 0 and self.new_quest_notif:
            nt = font_md.render(f"★ YENİ GÖREV: {self.new_quest_notif}", True, YELLOW)
            surface.blit(nt, (W//2 - nt.get_width()//2, H - 22))

    def draw_notif(self, surface):
        if self.notif_timer <= 0: return
        try:
            font_md = pygame.font.SysFont("Courier New", 11, bold=True)
        except:
            font_md = pygame.font.Font(None, 14)
        a = min(255, self.notif_timer * 3)
        ns = pygame.Surface((200, 14), pygame.SRCALPHA)
        ns.fill((0, 0, 0, 180))
        W = surface.get_width()
        surface.blit(ns, (W//2-100, 16))
        nt = font_md.render(f"★ GÖREV: {self.new_quest_notif}", True, (255, 220, 60))
        surface.blit(nt, (W//2 - nt.get_width()//2, 17))

class CutsceneFrame:
    def __init__(self, bg_color, text, speaker="", char_sprite=None,
                 char_pos="left", effect=None, duration=None, color=(255,255,255)):
        self.bg_color  = bg_color
        self.text      = text
        self.speaker   = speaker
        self.char_sprite = char_sprite
        self.char_pos  = char_pos
        self.effect    = effect
        self.duration  = duration
        self.color     = color

class Cutscene:
    def __init__(self, frames, callback=None):
        self.frames   = frames
        self.cur      = 0
        self.char_pos = 0
        self.active   = True
        self.callback = callback
        self.frame_t  = 0
        self.text_idx = 0
        self.done     = False
        self.shake_t  = 0
        self.flash_t  = 0
        self.fade_alpha = 0

    def update(self, kj):
        if not self.active: return
        self.frame_t += 1
        f = self.frames[self.cur]

        if f.effect == "shake": self.shake_t = 20
        if f.effect == "flash": self.flash_t = 15
        if f.effect == "fade_in": self.fade_alpha = max(0, 255 - self.frame_t * 8)
        if f.effect == "fade_out": self.fade_alpha = min(255, self.frame_t * 8)
        if self.shake_t > 0: self.shake_t -= 1
        if self.flash_t > 0: self.flash_t -= 1

        if self.text_idx < len(f.text):
            if self.frame_t % 2 == 0:
                self.text_idx += 1

        auto_done = f.duration and self.frame_t >= f.duration
        manual = kj.get(pygame.K_z) or kj.get(pygame.K_RETURN)

        if auto_done or (manual and self.text_idx >= len(f.text)):
            self._next()
        elif manual:
            self.text_idx = len(f.text)

    def _next(self):
        self.cur += 1
        self.frame_t = 0
        self.text_idx = 0
        self.shake_t = 0
        self.flash_t = 0
        self.fade_alpha = 0
        if self.cur >= len(self.frames):
            self.active = False
            self.done = True
            if self.callback: self.callback()

    def draw(self, surface):
        if not self.active: return
        f = self.frames[self.cur]
        W, H = surface.get_size()

        ox = random.randint(-3,3) if self.shake_t > 0 else 0
        oy = random.randint(-2,2) if self.shake_t > 0 else 0

        bg = pygame.Surface((W, H))
        bg.fill(f.bg_color)

        if f.char_sprite:
            try:
                cs = pygame.image.load(f.char_sprite).convert_alpha()
            except:
                cs = pygame.Surface((32, 48), pygame.SRCALPHA)
                cs.fill((200, 100, 200, 200))
            scaled = pygame.transform.scale(cs, (64, 96))
            if f.char_pos == "left":    cx = 20
            elif f.char_pos == "right": cx = W - 84
            else:                       cx = W//2 - 32
            cy = H//2 - 48
            bg.blit(scaled, (cx + ox, cy + oy))

        surface.blit(bg, (0, 0))

        if self.flash_t > 0:
            fl = pygame.Surface((W, H), pygame.SRCALPHA)
            fl.fill((255, 255, 255, int(self.flash_t * 17)))
            surface.blit(fl, (0, 0))

        if self.fade_alpha > 0:
            fd = pygame.Surface((W, H), pygame.SRCALPHA)
            fd.fill((0, 0, 0, self.fade_alpha))
            surface.blit(fd, (0, 0))

        try:
            font_md = pygame.font.SysFont("Courier New", 11, bold=True)
            font_sm = pygame.font.SysFont("Courier New", 8, bold=True)
        except:
            font_md = pygame.font.Font(None, 14)
            font_sm = pygame.font.Font(None, 11)

        bx, by, bw, bh = 8, H-68, W-16, 60
        pygame.draw.rect(surface, (0,0,0), (bx,by,bw,bh))
        pygame.draw.rect(surface, f.color, (bx,by,bw,bh), 2)
        pygame.draw.rect(surface, (20,20,20), (bx+2,by+2,bw-4,bh-4))

        if f.speaker:
            sw = font_md.size(f.speaker)[0] + 10
            pygame.draw.rect(surface, (0,0,0), (bx, by-14, sw+4, 14))
            pygame.draw.rect(surface, f.color, (bx, by-14, sw+4, 14), 1)
            st = font_md.render(f.speaker, True, f.color)
            surface.blit(st, (bx+5, by-13))

        shown = f.text[:self.text_idx]
        words = shown.split(' ')
        lines_out, cur_l = [], ""
        for w in words:
            test = (cur_l + " " + w).strip()
            if font_md.size(test)[0] > bw - 16:
                if cur_l: lines_out.append(cur_l)
                cur_l = w
            else: cur_l = test
        if cur_l: lines_out.append(cur_l)
        for i, ln in enumerate(lines_out[:3]):
            t = font_md.render(ln, True, (255,255,255))
            surface.blit(t, (bx+8, by+8+i*16))

        if self.text_idx >= len(f.text) and f.duration is None:
            if (pygame.time.get_ticks()//400)%2:
                pygame.draw.polygon(surface, f.color,
                    [(bx+bw-12,by+bh-10),(bx+bw-6,by+bh-10),(bx+bw-9,by+bh-5)])

def make_intro_cutscene(player_name, callback=None):
    return Cutscene([
        CutsceneFrame((5,5,15), "Çok uzun zaman önce...", duration=120,
                      effect="fade_in", color=(100,100,200)),
        CutsceneFrame((5,5,20), "Bu köyde herkes birbirini tanırdı.",
                      duration=140, color=(100,100,200)),
        CutsceneFrame((10,5,5), "Sonra Duman geldi.", "ANLATICI",
                      effect="flash", color=(220,80,80)),
        CutsceneFrame((5,5,20), "Sonra THE ALGO geldi.", "ANLATICI",
                      effect="shake", color=(60,200,255)),
        CutsceneFrame((0,0,0), "Ve hiçbir şey eskisi gibi olmadı.", "ANLATICI",
                      color=(180,180,180)),
        CutsceneFrame((0,0,5), f"Ama {player_name}...", "ANLATICI",
                      color=(255,220,60)),
        CutsceneFrame((0,5,0), f"{player_name} hâlâ umursuyor.", "ANLATICI",
                      effect="fade_out", color=(60,220,100)),
    ], callback=callback)

def make_duman_defeat_cutscene(callback=None):
    return Cutscene([
        CutsceneFrame((15,5,5), "Duman senin gözlerine baktı.", "ANLATICI",
                      effect="fade_in", color=(220,80,80)),
        CutsceneFrame((10,3,3), "Uzun zaman olmuştu... biri ona merhamet göstermeyeli.",
                      "ANLATICI", color=(200,100,100)),
        CutsceneFrame((5,2,2), "...", "DUMAN", color=(200,80,80)),
        CutsceneFrame((5,2,2), "Ben... neden böyle yaptım?", "DUMAN",
                      color=(200,80,80)),
        CutsceneFrame((3,3,10), "THE ALGO ona demiş ki... güç tek gerçektir.",
                      "ANLATICI", color=(100,100,200)),
        CutsceneFrame((0,5,0), "Ama sen farklı bir gerçek gösterdin.",
                      "ANLATICI", effect="flash", color=(60,220,100)),
    ], callback=callback)

def make_algo_defeat_cutscene(player_name, callback=None):
    return Cutscene([
        CutsceneFrame((0,20,40), "THE ALGO durdu.", "ANLATICI",
                      effect="fade_in", color=(60,200,255)),
        CutsceneFrame((0,15,30), "İlk kez... hesap yapamadı.", "ANLATICI",
                      color=(60,200,255)),
        CutsceneFrame((0,10,20), "Çünkü empati... hesaplanamaz.", "THE ALGO",
                      effect="shake", color=(60,200,255)),
        CutsceneFrame((0,5,10), f"Teşekkür ederim, {player_name}.", "THE ALGO",
                      color=(100,220,255)),
        CutsceneFrame((0,5,10), "Sistemi... yeniden başlatıyorum.", "THE ALGO",
                      effect="fade_out", color=(100,220,255)),
        CutsceneFrame((0,0,0), "Bu sefer daha iyi.", "THE ALGO",
                      color=(60,160,200)),
    ], callback=callback)

def make_chapter2_cutscene(callback=None):
    return Cutscene([
        CutsceneFrame((20,5,5), "Ama hikaye bitmemişti.", "ANLATICI",
                      effect="fade_in", color=(220,80,80)),
        CutsceneFrame((15,5,5), "Duman 2.0 aktive edildi.", "SİSTEM",
                      effect="flash", color=(255,120,50)),
        CutsceneFrame((10,3,3), "THE ALGO onu yeniden programlamıştı.", "ANLATICI",
                      color=(200,100,50)),
        CutsceneFrame((10,3,3), "Bu sefer... daha güçlü.", "SİSTEM",
                      effect="shake", color=(255,100,30)),
        CutsceneFrame((5,2,2), "Ama içinde hâlâ o... o insan kıvılcımı var mı?",
                      "ANLATICI", color=(180,80,80)),
    ], callback=callback)

class PuzzleRoom:
    SYMBOLS = ["△", "○", "□", "★", "◇", "♦"]

    def __init__(self, solution=None, reward=None, title="PUZZLE ODASI"):
        self.solution = solution or [0, 2, 1, 3]
        self.player   = [0, 0, 0, 0]
        self.sel_slot = 0
        self.active   = False
        self.solved   = False
        self.failed   = False
        self.fail_timer = 0
        self.reward   = reward
        self.title    = title
        self.hint     = "Sembolleri doğru sıraya diz!"
        self.frame    = 0

    def open(self, hint=""):
        self.active  = True
        self.solved  = False
        self.failed  = False
        self.player  = [0, 0, 0, 0]
        self.sel_slot= 0
        self.frame   = 0
        if hint: self.hint = hint

    def update(self, kj):
        if not self.active or self.solved: return
        self.frame += 1
        if self.fail_timer > 0:
            self.fail_timer -= 1
            if self.fail_timer == 0: self.failed = False; return

        n = len(self.SYMBOLS)
        if kj.get(pygame.K_LEFT):
            self.sel_slot = (self.sel_slot - 1) % 4
        if kj.get(pygame.K_RIGHT):
            self.sel_slot = (self.sel_slot + 1) % 4
        if kj.get(pygame.K_UP):
            self.player[self.sel_slot] = (self.player[self.sel_slot] - 1) % n
        if kj.get(pygame.K_DOWN):
            self.player[self.sel_slot] = (self.player[self.sel_slot] + 1) % n
        if kj.get(pygame.K_z) or kj.get(pygame.K_RETURN):
            self._check()
        if kj.get(pygame.K_x) or kj.get(pygame.K_ESCAPE):
            self.active = False

    def _check(self):
        if self.player == self.solution:
            self.solved = True
        else:
            self.failed = True
            self.fail_timer = 90
            import random
            for i in range(4):
                if random.random() < 0.3:
                    self.player[i] = random.randint(0, len(self.SYMBOLS)-1)

    def draw(self, surface):
        if not self.active: return
        W, H = surface.get_size()
        try:
            font_xl = pygame.font.SysFont("Courier New", 20, bold=True)
            font_lg = pygame.font.SysFont("Courier New", 16, bold=True)
            font_md = pygame.font.SysFont("Courier New", 11, bold=True)
            font_sm = pygame.font.SysFont("Courier New", 8, bold=True)
        except:
            font_xl = pygame.font.Font(None, 24)
            font_lg = pygame.font.Font(None, 20)
            font_md = pygame.font.Font(None, 14)
            font_sm = pygame.font.Font(None, 11)

        DGRAY=(40,40,40); YELLOW=(255,220,60); WHITE=(255,255,255)
        CYAN=(60,220,220); RED=(220,50,50); GREEN=(50,200,80); GRAY=(100,100,100)

        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        surface.blit(overlay, (0, 0))

        bx, by, bw, bh = W//2-90, H//2-70, 180, 140
        pygame.draw.rect(surface, DGRAY, (bx, by, bw, bh))
        col = RED if self.failed else (GREEN if self.solved else CYAN)
        pygame.draw.rect(surface, col, (bx, by, bw, bh), 2)

        t = font_lg.render(self.title, True, YELLOW)
        surface.blit(t, (W//2 - t.get_width()//2, by+6))

        ht = font_sm.render(self.hint, True, GRAY)
        surface.blit(ht, (W//2 - ht.get_width()//2, by+22))

        for i in range(4):
            sx = bx + 14 + i * 38
            sy = by + 42
            sel = i == self.sel_slot
            bg = (50, 50, 10) if sel else (30, 30, 30)
            pygame.draw.rect(surface, bg, (sx, sy, 30, 34))
            bc = YELLOW if sel else WHITE
            pygame.draw.rect(surface, bc, (sx, sy, 30, 34), 2 if sel else 1)
            sym = self.SYMBOLS[self.player[i]]
            st = font_xl.render(sym, True, bc)
            surface.blit(st, (sx + 15 - st.get_width()//2, sy + 5))

        sx_sel = bx + 14 + self.sel_slot * 38
        pygame.draw.polygon(surface, YELLOW,
            [(sx_sel+15, by+40),(sx_sel+10, by+35),(sx_sel+20, by+35)])
        pygame.draw.polygon(surface, YELLOW,
            [(sx_sel+15, by+79),(sx_sel+10, by+84),(sx_sel+20, by+84)])

        if self.solved:
            gt = font_md.render("✓ ÇÖZÜLDÜ!", True, GREEN)
            surface.blit(gt, (W//2 - gt.get_width()//2, by+85))
        elif self.failed:
            shake = import_int(self.fail_timer)
            ft = font_md.render("✗ YANLIŞ!", True, RED)
            surface.blit(ft, (W//2 - ft.get_width()//2 + (shake%2)*4, by+85))
        else:
            ct = font_sm.render("Z=Onayla  ←→=Slot  ↑↓=Sembol  X=Çık", True, GRAY)
            surface.blit(ct, (W//2 - ct.get_width()//2, by+bh-12))

def import_int(x):
    try: return int(x)
    except: return 0

EXTRA_BOSSES = {
    "Orman Ruhu": {
        "spr": "enemy_ghost",
        "hp": 180, "atk": 18, "gold": 0, "xp": 80,
        "desc": "Ormanın koruyucusu. Seni sınamak istiyor.",
        "spare_lines": [
            "Cesaretini görüyorum...",
            "Ama orman senin niyetini sormak istiyor.",
            "Neden buradasın, insan?",
            "Güç için mi? Yoksa başkası için mi?",
            "Cevabın... tatmin edici.",
            "Geç. Orman seni tanıdı.",
            "Ama bir daha gel — hazır ol.",
            "Tamam. Dur.",
        ],
        "defeat_line": "Orman Ruhu dağıldı. Ama orman hâlâ burada.",
        "spare_cond": "talk",
        "bullets": ["circle", "rain", "diagonal", "laser"],
        "spare_sound": "emp_charge",
        "is_boss": True,
        "phases": [
            {"hp_pct": 100, "label": "ORMAN RUHU - UYANIK",  "color": (40,140,60),  "atk": 18, "speed": 1.0},
            {"hp_pct": 50,  "label": "ORMAN RUHU - ÖFKELI",  "color": (140,60,20),  "atk": 26, "speed": 1.5},
            {"hp_pct": 20,  "label": "ORMAN RUHU - SON NEFES","color": (200,200,80), "atk": 32, "speed": 1.9},
        ],
    },
    "Veri Kalesi": {
        "spr": "npc_villain",
        "hp": 250, "atk": 25, "gold": 0, "xp": 150,
        "desc": "THE ALGO'nun son savunma katmanı. Saf veri.",
        "spare_lines": [
            "ERIŞIM REDDEDİLDİ.",
            "YETKI YOK.",
            "SEN KİMSİN?",
            "VERİ TABANINDA KAYIT YOK.",
            "AMA... SEN VARSИН.",
            "TANIMSIZ VERİ = TEHDİT.",
            "VEYA...",
            "TANIMSIZ VERİ = YENİ BİLGİ.",
            "Geçiş izni verildi.",
        ],
        "defeat_line": "Veri Kalesi çöktü. THE ALGO'nun son zırhı kırıldı.",
        "spare_cond": "empathy",
        "bullets": ["grid", "laser", "circle", "rain", "diagonal"],
        "spare_sound": "emp_charge",
        "is_boss": True,
        "phases": [
            {"hp_pct": 100, "label": "VERİ KALESİ - AKTİF",  "color": (60,60,200), "atk": 25, "speed": 1.1},
            {"hp_pct": 60,  "label": "VERİ KALESİ - SALDIRI", "color": (200,60,200),"atk": 33, "speed": 1.4},
            {"hp_pct": 25,  "label": "VERİ KALESİ - ÇÖKÜŞ",  "color": (200,200,60),"atk": 40, "speed": 1.8},
        ],
    },
    "Gece Canavarı": {
        "spr": "enemy",
        "hp": 90, "atk": 14, "gold": 15, "xp": 45,
        "desc": "Sadece gece çıkar. Gündüz görmez.",
        "spare_lines": [
            "Gece... seviyorum.",
            "Gündüzden korkuyorum.",
            "Sen gündüz gibisin. Parlak.",
            "Beni yakıyorsun.",
            "Ama... ısınmak istiyorum aslında.",
            "Dur. Gitmeni istemiyorum.",
            "Seninle biraz daha konuşabilir miyim?",
            "Tamam. Affet.",
        ],
        "defeat_line": "Gece Canavarı sabahı beklemeye başladı.",
        "spare_cond": "talk",
        "bullets": ["rain", "diagonal", "circle"],
        "spare_sound": "spare",
        "is_boss": False,
        "night_only": True,
    },
}
