import pygame, math

class TouchControls:
    def __init__(self, screen_w, screen_h):
        self.sw = screen_w
        self.sh = screen_h

        # Joystick (sol alt)
        self.joy_cx = int(screen_w * 0.18)
        self.joy_cy = int(screen_h * 0.75)
        self.joy_r  = int(screen_w * 0.12)
        self.joy_knob_r = int(screen_w * 0.05)
        self.joy_dx = 0.0
        self.joy_dy = 0.0
        self.joy_touch_id = None
        self.joy_kx = self.joy_cx
        self.joy_ky = self.joy_cy

        # Butonlar (sağ alt)
        bsize = int(screen_w * 0.09)
        bx = int(screen_w * 0.82)
        by = int(screen_h * 0.72)
        gap = int(bsize * 1.3)
        self.buttons = {
            "Z":      {"cx": bx+gap,  "cy": by,       "r": bsize, "col": (60,180,80),  "pressed": False, "touch_id": None},
            "X":      {"cx": bx,      "cy": by,       "r": bsize, "col": (180,60,60),  "pressed": False, "touch_id": None},
            "ENTER":  {"cx": bx+gap,  "cy": by-gap,   "r": bsize, "col": (60,100,200), "pressed": False, "touch_id": None},
            "S":      {"cx": bx,      "cy": by-gap,   "r": bsize, "col": (180,140,40), "pressed": False, "touch_id": None},
            "J":      {"cx": bx-gap,  "cy": by,       "r": bsize, "col": (120,60,180), "pressed": False, "touch_id": None},
        }

        # Key mapping
        self.key_map = {
            "Z":     pygame.K_z,
            "X":     pygame.K_x,
            "ENTER": pygame.K_RETURN,
            "S":     pygame.K_s,
            "J":     pygame.K_j,
        }

        self.active_touches = {}

    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            self._on_down(event.finger_id, event.x * self.sw, event.y * self.sh)
        elif event.type == pygame.FINGERMOTION:
            self._on_move(event.finger_id, event.x * self.sw, event.y * self.sh)
        elif event.type == pygame.FINGERUP:
            self._on_up(event.finger_id)

    def _on_down(self, fid, fx, fy):
        # Joystick kontrolü
        dx = fx - self.joy_cx
        dy = fy - self.joy_cy
        if math.hypot(dx, dy) < self.joy_r * 1.4:
            self.joy_touch_id = fid
            self._update_joy(fx, fy)
            return
        # Buton kontrolü
        for name, btn in self.buttons.items():
            if math.hypot(fx - btn["cx"], fy - btn["cy"]) < btn["r"] * 1.2:
                btn["pressed"] = True
                btn["touch_id"] = fid
                return

    def _on_move(self, fid, fx, fy):
        if fid == self.joy_touch_id:
            self._update_joy(fx, fy)

    def _on_up(self, fid):
        if fid == self.joy_touch_id:
            self.joy_touch_id = None
            self.joy_dx = 0.0
            self.joy_dy = 0.0
            self.joy_kx = self.joy_cx
            self.joy_ky = self.joy_cy
        for name, btn in self.buttons.items():
            if btn["touch_id"] == fid:
                btn["pressed"] = False
                btn["touch_id"] = None

    def _update_joy(self, fx, fy):
        dx = fx - self.joy_cx
        dy = fy - self.joy_cy
        dist = math.hypot(dx, dy)
        if dist > self.joy_r:
            dx = dx / dist * self.joy_r
            dy = dy / dist * self.joy_r
        self.joy_dx = dx / self.joy_r
        self.joy_dy = dy / self.joy_r
        self.joy_kx = self.joy_cx + dx
        self.joy_ky = self.joy_cy + dy

    def get_keys_pressed(self):
        keys = {}
        DEAD = 0.25
        keys[pygame.K_LEFT]  = self.joy_dx < -DEAD
        keys[pygame.K_RIGHT] = self.joy_dx >  DEAD
        keys[pygame.K_UP]    = self.joy_dy < -DEAD
        keys[pygame.K_DOWN]  = self.joy_dy >  DEAD
        for name, btn in self.buttons.items():
            k = self.key_map.get(name)
            if k: keys[k] = btn["pressed"]
        return keys

    def get_keys_just_pressed(self):
        kj = {}
        for name, btn in self.buttons.items():
            k = self.key_map.get(name)
            if k and btn["pressed"] and btn.get("was_pressed") != True:
                kj[k] = True
            btn["was_pressed"] = btn["pressed"]
        return kj

    def draw(self, surface):
        # Joystick dış halka
        pygame.draw.circle(surface, (60,60,60,150),
            (self.joy_cx, self.joy_cy), self.joy_r, 3)
        pygame.draw.circle(surface, (40,40,40,100),
            (self.joy_cx, self.joy_cy), self.joy_r)

        # Yön okları (ipucu)
        arrow_col = (80,80,80)
        ar = self.joy_r - 8
        pygame.draw.polygon(surface, arrow_col, [
            (self.joy_cx, self.joy_cy - ar),
            (self.joy_cx - 6, self.joy_cy - ar + 10),
            (self.joy_cx + 6, self.joy_cy - ar + 10)])
        pygame.draw.polygon(surface, arrow_col, [
            (self.joy_cx, self.joy_cy + ar),
            (self.joy_cx - 6, self.joy_cy + ar - 10),
            (self.joy_cx + 6, self.joy_cy + ar - 10)])
        pygame.draw.polygon(surface, arrow_col, [
            (self.joy_cx - ar, self.joy_cy),
            (self.joy_cx - ar + 10, self.joy_cy - 6),
            (self.joy_cx - ar + 10, self.joy_cy + 6)])
        pygame.draw.polygon(surface, arrow_col, [
            (self.joy_cx + ar, self.joy_cy),
            (self.joy_cx + ar - 10, self.joy_cy - 6),
            (self.joy_cx + ar - 10, self.joy_cy + 6)])

        # Joystick knob
        knob_col = (120,120,180) if self.joy_touch_id else (100,100,150)
        pygame.draw.circle(surface, knob_col,
            (int(self.joy_kx), int(self.joy_ky)), self.joy_knob_r)
        pygame.draw.circle(surface, (160,160,220),
            (int(self.joy_kx), int(self.joy_ky)), self.joy_knob_r, 2)

        # Butonlar
        labels = {"Z":"Z","X":"X","ENTER":"OK","S":"KYT","J":"GRV"}
        try:
            f = pygame.font.SysFont("Courier New", max(10, self.joy_knob_r), bold=True)
        except:
            f = pygame.font.Font(None, max(14, self.joy_knob_r+4))

        for name, btn in self.buttons.items():
            col = tuple(min(255, c + 60) for c in btn["col"]) if btn["pressed"] else btn["col"]
            alpha_surf = pygame.Surface((btn["r"]*2+4, btn["r"]*2+4), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surf, (*col, 180),
                (btn["r"]+2, btn["r"]+2), btn["r"])
            pygame.draw.circle(alpha_surf, (255,255,255,100),
                (btn["r"]+2, btn["r"]+2), btn["r"], 2)
            surface.blit(alpha_surf, (btn["cx"]-btn["r"]-2, btn["cy"]-btn["r"]-2))
            lbl = labels.get(name, name)
            t = f.render(lbl, True, (255,255,255))
            surface.blit(t, (btn["cx"]-t.get_width()//2, btn["cy"]-t.get_height()//2))
