import json, random, math

COLS, ROWS = 120, 80

T = {
    'grass':    'G',
    'road':     'R',
    'floor':    'F',
    'dirt':     'D',
    'sand':     'N',
    'snow':     'X',
    'cave':     'C',
    'factory':  'I',
    'water':    'w',
    'deep':     'W2',
    'wall':     'W',
    'tree':     'T',
    'rock':     'K',
    'fence':    'f',
    'crate':    'cr',
    'pillar':   'P',
    'door':     'd',
    'chest':    'ch',
    'sign':     'S',
    'save':     'sv',
    'npc':      'n',
    'boss':     'B',
    'stairs_d': 'sd',
    'stairs_u': 'su',
    'market':   'M',
    'bush':     'b',
    'flower':   'Fl',
    'lamp':     'L',
    'bridge':   'Br',
    'barrel':   'Ba',
    'pipe':     'Pi',
    'algo_node':'An',
    'portal':   'Po',
    'fish':     'Fi',
    'boat':     'Bo',
    'dock':     'Dk',
}

SOLID_TILES = {'W','T','K','f','W2','cr','P','Pi','Ba'}
FLOOR_TILES = {'G','R','F','D','N','X','C','I','w','Br','Dk'}
INTERACTIVE_TILES = {'d','ch','S','sv','n','B','sd','su','M','Bo','Po','Fish','An'}

def make_empty():
    return [['W' for _ in range(COLS)] for _ in range(ROWS)]

def fill_rect(m, x, y, w, h, tile):
    for ry in range(y, min(y+h, ROWS)):
        for rx in range(x, min(x+w, COLS)):
            m[ry][rx] = tile

def border_rect(m, x, y, w, h, wall, floor):
    fill_rect(m, x, y, w, h, floor)
    for rx in range(x, x+w):
        m[y][rx] = wall
        if y+h-1 < ROWS: m[y+h-1][rx] = wall
    for ry in range(y, y+h):
        m[ry][x] = wall
        if x+w-1 < COLS: m[ry][x+w-1] = wall

def scatter(m, x, y, w, h, tile, density=0.15):
    for ry in range(y, min(y+h, ROWS)):
        for rx in range(x, min(x+w, COLS)):
            if random.random() < density:
                m[ry][rx] = tile

def hline(m, x, y, length, tile):
    for rx in range(x, min(x+length, COLS)):
        if 0 <= y < ROWS: m[y][rx] = tile

def vline(m, x, y, length, tile):
    for ry in range(y, min(y+length, ROWS)):
        if 0 <= x < COLS: m[ry][x] = tile

def build_village(m):
    fill_rect(m, 0, 0, 40, 40, 'G')
    fill_rect(m, 0, 18, 40, 3, 'R')
    fill_rect(m, 18, 0, 3, 40, 'R')

    border_rect(m, 2, 2, 8, 7, 'W', 'F')
    m[2][5] = 'd'
    m[3][3] = 'n'

    border_rect(m, 12, 2, 8, 7, 'W', 'F')
    m[2][15] = 'd'
    m[3][13] = 'n'

    border_rect(m, 2, 24, 8, 7, 'W', 'F')
    m[24][5] = 'd'
    m[25][3] = 'n'

    border_rect(m, 12, 24, 8, 7, 'W', 'F')
    m[24][15] = 'd'
    m[25][13] = 'n'

    border_rect(m, 28, 24, 8, 7, 'W', 'F')
    m[24][31] = 'd'
    m[25][29] = 'n'

    fill_rect(m, 22, 8, 6, 6, 'F')
    m[11][24] = 'sv'
    m[9][24]  = 'S'
    m[10][22] = 'L'
    m[10][27] = 'L'

    for tx, ty in [(1,10),(1,12),(1,14),(35,10),(35,12),(35,14),
                   (6,16),(10,16),(25,16),(30,16),(35,16)]:
        if 0<=ty<ROWS and 0<=tx<COLS: m[ty][tx] = 'T'

    scatter(m, 2, 10, 8, 6, 'Fl', 0.2)
    scatter(m, 28, 10, 8, 6, 'b', 0.15)

    m[38][18] = 'S'
    m[38][19] = 'S'
    m[39][17] = 'f'
    m[39][21] = 'f'

    fill_rect(m, 30, 2, 8, 6, 'w')
    m[4][33] = 'Fi'
    m[5][35] = 'Fi'
    scatter(m, 30, 2, 8, 6, 'W2', 0.1)

    for lx in range(0, 40, 6):
        m[17][lx] = 'L'
        m[21][lx] = 'L'

def build_market(m):
    fill_rect(m, 40, 0, 40, 30, 'G')
    fill_rect(m, 40, 12, 40, 3, 'R')
    fill_rect(m, 58, 0, 3, 30, 'R')

    stalls = [
        (42,2),(42,6),(42,10),
        (48,2),(48,6),(48,10),
        (54,2),(54,6),
        (62,2),(62,6),(62,10),
        (68,2),(68,6),(68,10),
        (74,2),(74,6),
    ]
    for sx, sy in stalls:
        fill_rect(m, sx, sy, 5, 3, 'F')
        m[sy][sx+2] = 'M'
        m[sy+1][sx] = 'n'
        items = ['ch','Ba','S']
        m[sy+1][sx+3] = random.choice(items)

    m[11][58] = 'S'
    m[11][59] = 'S'
    m[11][60] = 'S'

    border_rect(m, 64, 16, 12, 10, 'W', 'I')
    m[16][69] = 'd'
    m[17][65] = 'n'
    m[18][70] = 'sv'
    m[19][67] = 'Ba'
    m[20][68] = 'Ba'
    scatter(m, 65, 17, 10, 8, 'cr', 0.1)

    fill_rect(m, 70, 2, 8, 10, 'F')
    m[6][74] = 'S'
    m[7][73] = 'L'
    m[7][76] = 'L'

    hline(m, 40, 0, 40, 'f')
    for fx in range(40, 80, 3):
        if m[0][fx] == 'f': m[0][fx] = 'L'

    for tx in range(40, 60, 5):
        m[28][tx] = 'T'
        m[29][tx] = 'T'

def build_deep_forest(m):
    fill_rect(m, 0, 40, 50, 40, 'G')

    forest_clusters = [
        (2,42,8,10), (12,42,6,8), (20,45,10,12),
        (1,54,7,8),  (15,52,8,10),(28,44,8,8),
        (35,50,10,12),(38,60,8,10),(2,62,10,10),
        (15,64,8,8), (30,62,10,10),(40,68,8,8),
    ]
    for cx, cy, cw, ch in forest_clusters:
        for ty in range(cy, min(cy+ch, ROWS)):
            for tx in range(cx, min(cx+cw, COLS)):
                if random.random() < 0.55:
                    m[ty][tx] = 'T'
                elif random.random() < 0.1:
                    m[ty][tx] = 'K'

    path_x = 5
    for py in range(40, 80):
        path_x += random.randint(-1, 1)
        path_x = max(2, min(46, path_x))
        m[py][path_x] = 'D'
        if path_x+1 < COLS: m[py][path_x+1] = 'D'

    fill_rect(m, 22, 56, 8, 6, 'w')
    m[58][25] = 'Fi'
    m[59][26] = 'Fi'
    m[57][28] = 'Bo'

    m[72][8]  = 'sd'
    m[72][7]  = 'K'
    m[72][9]  = 'K'
    m[71][8]  = 'S'

    m[65][18] = 'S'
    m[66][19] = 'n'

    m[75][30] = 'B'
    m[74][30] = 'sv'
    m[76][28] = 'S'

    m[50][10] = 'sv'
    m[60][35] = 'sv'

    scatter(m, 0, 40, 50, 40, 'b', 0.05)
    scatter(m, 0, 40, 50, 40, 'Fl', 0.04)

    for lx, ly in [(10,48),(20,55),(35,62),(15,70)]:
        m[ly][lx] = 'L'

def build_cave(m):
    fill_rect(m, 50, 40, 30, 40, 'W')

    rooms = [
        (52, 42, 12, 8),
        (56, 50, 15, 10),
        (52, 60, 10, 8),
        (64, 58, 12, 10),
        (55, 68, 16, 8),
        (62, 42, 14, 8),
    ]
    for rx, ry, rw, rh in rooms:
        fill_rect(m, rx, ry, rw, rh, 'C')
        scatter(m, rx, ry, rw, rh, 'K', 0.08)

    corridors = [
        (57, 50, 5, 0),
        (60, 57, 0, 5),
        (64, 55, 0, 5),
        (60, 67, 0, 5),
    ]
    for cx, cy, cw, ch in corridors:
        if cw: fill_rect(m, cx, cy, max(cw,3), 3, 'C')
        if ch: fill_rect(m, cx, cy, 3, max(ch,3), 'C')

    fill_rect(m, 63, 42, 3, 8, 'C')

    m[42][55] = 'su'

    m[44][58]  = 'ch'
    m[44][64]  = 'ch'
    m[62][54]  = 'ch'
    m[65][65]  = 'n'
    m[70][62]  = 'B'
    m[69][62]  = 'sv'
    m[44][70]  = 'ch'

    fill_rect(m, 66, 62, 4, 3, 'w')

    m[52][57] = 'sv'
    m[58][63] = 'sv'

    for lx, ly in [(53,43),(60,51),(53,61),(65,59),(56,69),(63,43)]:
        if 0<=ly<ROWS and 0<=lx<COLS: m[ly][lx] = 'L'

    scatter(m, 50, 40, 30, 40, 'K', 0.04)

def build_factory(m):
    fill_rect(m, 80, 40, 40, 40, 'D')

    border_rect(m, 82, 42, 34, 30, 'W', 'I')
    vline(m, 100, 42, 30, 'W')
    hline(m, 82, 56, 34, 'W')
    m[42][90]  = 'd'
    m[42][108] = 'd'
    m[56][91]  = 'd'
    m[56][109] = 'd'
    m[72][90]  = 'd'

    for fx, fy in [(84,44),(88,44),(92,44),(84,48),(88,48),
                    (102,44),(106,44),(110,44),(102,48)]:
        if 0<=fy<ROWS and 0<=fx<COLS:
            m[fy][fx] = 'cr'
    for fx, fy in [(85,58),(89,58),(93,58),(85,62),(103,58),(107,58)]:
        if 0<=fy<ROWS and 0<=fx<COLS:
            m[fy][fx] = 'Ba'

    hline(m, 82, 50, 18, 'Pi')
    hline(m, 100, 50, 16, 'Pi')
    vline(m, 98, 42, 14, 'Pi')

    m[46][95]  = 'n'
    m[60][104] = 'n'
    m[65][88]  = 'B'
    m[64][88]  = 'sv'

    m[44][84]  = 'sv'
    m[58][102] = 'sv'

    m[50][112] = 'n'

    scatter(m, 80, 72, 40, 8, 'Ba', 0.1)
    scatter(m, 80, 72, 40, 8, 'cr', 0.08)
    for tx in range(80, 120, 8):
        m[79][tx] = 'T'

    for lx, ly in [(83,43),(101,43),(83,57),(101,57),(83,71)]:
        if 0<=ly<ROWS and 0<=lx<COLS: m[ly][lx] = 'L'

    fill_rect(m, 80, 40, 40, 2, 'R')
    fill_rect(m, 116, 40, 4, 40, 'R')

def build_lake(m):
    fill_rect(m, 80, 0, 40, 40, 'G')

    fill_rect(m, 90, 2, 28, 20, 'w')
    scatter(m, 90, 2, 28, 20, 'W2', 0.12)

    fill_rect(m, 89, 2, 1, 20, 'N')
    fill_rect(m, 118, 2, 2, 20, 'N')
    fill_rect(m, 89, 2, 30, 1, 'N')
    fill_rect(m, 89, 21, 30, 1, 'N')

    for fx, fy in [(93,5),(100,8),(108,5),(115,10),(95,15),(110,15)]:
        m[fy][fx] = 'Fi'

    m[3][93]  = 'Bo'
    m[4][105] = 'Bo'
    m[15][96] = 'Bo'

    fill_rect(m, 83, 10, 8, 2, 'Dk')
    m[10][84] = 'Dk'
    m[11][84] = 'Dk'

    border_rect(m, 81, 2, 7, 6, 'W', 'F')
    m[2][84] = 'd'
    m[3][82] = 'n'

    border_rect(m, 81, 10, 7, 6, 'W', 'F')
    m[10][84] = 'd'
    m[11][82] = 'n'

    border_rect(m, 81, 22, 7, 6, 'W', 'F')
    m[22][84] = 'd'
    m[23][82] = 'n'

    fill_rect(m, 81, 30, 10, 8, 'F')
    m[33][85] = 'M'
    m[33][87] = 'M'
    m[34][85] = 'sv'
    m[32][85] = 'S'

    for tx in range(80, 90, 2):
        m[0][tx] = 'T'
    for ty in range(25, 40, 3):
        m[ty][118] = 'T'
        m[ty][119] = 'T'

    scatter(m, 80, 0, 10, 40, 'Fl', 0.1)
    scatter(m, 80, 0, 10, 40, 'b', 0.08)

    fill_rect(m, 80, 14, 3, 3, 'Br')

    for lx, ly in [(82,8),(82,20),(82,29),(88,0)]:
        m[ly][lx] = 'L'

def build_algo_approach(m):
    fill_rect(m, 40, 30, 40, 10, 'D')

    fill_rect(m, 40, 33, 40, 4, 'R')

    for px in range(44, 80, 6):
        m[32][px] = 'P'
        m[37][px] = 'P'
        m[32][px+1] = 'L'
        m[37][px+1] = 'L'

    for ax in range(42, 78, 4):
        m[31][ax] = 'An'

    m[33][78] = 'Po'
    m[33][79] = 'Po'
    m[34][78] = 'Po'
    m[34][79] = 'Po'

    m[33][70] = 'B'
    m[32][70] = 'sv'

    m[31][60] = 'S'
    m[31][65] = 'S'
    m[30][72] = 'S'

def build_connections(m):
    fill_rect(m, 38, 17, 4, 3, 'R')

    fill_rect(m, 17, 38, 3, 4, 'R')

    fill_rect(m, 78, 12, 4, 3, 'R')

    fill_rect(m, 48, 38, 4, 4, 'Br')
    fill_rect(m, 48, 40, 4, 2, 'R')

    fill_rect(m, 98, 38, 3, 4, 'R')

    fill_rect(m, 58, 28, 3, 4, 'R')

    fill_rect(m, 115, 0, 3, 40, 'R')

def build_full_map():
    m = make_empty()
    random.seed(42)

    print("Köy merkezi...")
    build_village(m)
    print("Pazar yeri...")
    build_market(m)
    print("Gizemli orman...")
    build_deep_forest(m)
    print("Gizli mağara...")
    build_cave(m)
    print("Terk edilmiş fabrika...")
    build_factory(m)
    print("Göl kenarı / balıkçı...")
    build_lake(m)
    print("Algo geçiş bölgesi...")
    build_algo_approach(m)
    print("Yollar...")
    build_connections(m)

    return m

def map_to_json(m):
    tile_ids = {}
    tile_counter = [0]
    def get_id(tile):
        if tile not in tile_ids:
            tile_ids[tile] = tile_counter[0]
            tile_counter[0] += 1
        return tile_ids[tile]

    grid = []
    for row in m:
        grid.append([get_id(t) for t in row])

    tile_props = {}
    for tile, tid in tile_ids.items():
        tile_props[str(tid)] = {
            "char": tile,
            "solid": tile in SOLID_TILES,
            "interactive": tile in INTERACTIVE_TILES,
            "floor": tile in FLOOR_TILES,
        }

    npcs = []
    bosses = []
    chests = []
    saves = []
    signs = []
    portals = []

    for ry, row in enumerate(m):
        for rx, tile in enumerate(row):
            if tile == 'n':   npcs.append({"x": rx, "y": ry})
            elif tile == 'B': bosses.append({"x": rx, "y": ry})
            elif tile == 'ch':chests.append({"x": rx, "y": ry})
            elif tile == 'sv':saves.append({"x": rx, "y": ry})
            elif tile == 'S': signs.append({"x": rx, "y": ry})
            elif tile == 'Po':portals.append({"x": rx, "y": ry})

    return {
        "width": COLS,
        "height": ROWS,
        "tile_size": 16,
        "grid": grid,
        "tile_ids": {v: k for k, v in tile_ids.items()},
        "tile_props": tile_props,
        "objects": {
            "npcs": npcs,
            "bosses": bosses,
            "chests": chests,
            "saves": saves,
            "signs": signs,
            "portals": portals,
        },
        "regions": {
            "village":      {"x": 0,  "y": 0,  "w": 40, "h": 40, "name": "Dursunköy"},
            "market":       {"x": 40, "y": 0,  "w": 40, "h": 30, "name": "Pazar Yeri"},
            "deep_forest":  {"x": 0,  "y": 40, "w": 50, "h": 40, "name": "Gizemli Orman"},
            "cave":         {"x": 50, "y": 40, "w": 30, "h": 40, "name": "Gizli Mağara"},
            "factory":      {"x": 80, "y": 40, "w": 40, "h": 40, "name": "Terk Edilmiş Fabrika"},
            "lake":         {"x": 80, "y": 0,  "w": 40, "h": 40, "name": "Göl Kenarı"},
            "algo_approach":{"x": 40, "y": 30, "w": 40, "h": 10, "name": "THE ALGO Geçişi"},
        }
    }

if __name__ == "__main__":
    print("120x80 dev harita üretiliyor...")
    m = build_full_map()
    data = map_to_json(m)
    with open("map_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"map_data.json yazıldı!")
    print(f"  Boyut: {data['width']}x{data['height']}")
    print(f"  NPC sayısı: {len(data['objects']['npcs'])}")
    print(f"  Boss sayısı: {len(data['objects']['bosses'])}")
    print(f"  Sandık sayısı: {len(data['objects']['chests'])}")
    print(f"  Kayıt noktası: {len(data['objects']['saves'])}")
    print(f"  Bölge sayısı: {len(data['regions'])}")

    print("\nHarita önizleme (her 3. tile):")
    for ry in range(0, ROWS, 3):
        row_str = ""
        for rx in range(0, COLS, 3):
            t = m[ry][rx]
            c = {'G':'.','R':'=','W':'#','T':'^','w':'~',
                 'C':'c','I':'i','F':',','D':'-','W2':'~',
                 'N':'n','B':'!','sv':'*','n':'@','ch':'$'}.get(t,'?')
            row_str += c
        print(row_str)
