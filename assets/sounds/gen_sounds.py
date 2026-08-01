import wave, struct, math, random, os

SR = 22050

def write_wav(filename, samples, sr=SR):
    with wave.open(filename,'w') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr)
        data = b''
        for s in samples:
            v = max(-32768, min(32767, int(s)))
            data += struct.pack('<hh', v, v)
        f.writeframes(data)

def envelope(n, att=0.05, rel=0.2):
    out = []
    for i in range(n):
        a = min(1.0, i/(n*att))
        r = max(0.0, 1-(i/n-1+rel)/rel) if i/n > 1-rel else 1.0
        out.append(a*r)
    return out

def square(freq, dur, vol=0.4, sr=SR):
    n = int(sr*dur); env = envelope(n)
    return [int(32767*vol*env[i]*(1 if math.sin(2*math.pi*freq*i/sr)>0 else -1)) for i in range(n)]

def sine(freq, dur, vol=0.4, sr=SR):
    n = int(sr*dur); env = envelope(n)
    return [int(32767*vol*env[i]*math.sin(2*math.pi*freq*i/sr)) for i in range(n)]

def saw(freq, dur, vol=0.35, sr=SR):
    n = int(sr*dur); env = envelope(n)
    return [int(32767*vol*env[i]*(2*(freq*i/sr%1)-1)) for i in range(n)]

def noise(dur, vol=0.3, sr=SR):
    n = int(sr*dur); env = envelope(n)
    return [int(32767*vol*env[i]*random.uniform(-1,1)) for i in range(n)]

def sweep(f1, f2, dur, vol=0.4, sr=SR):
    n = int(sr*dur); env = envelope(n); out = []
    for i in range(n):
        f = f1 + (f2-f1)*(i/n)
        out.append(int(32767*vol*env[i]*math.sin(2*math.pi*f*i/sr)))
    return out

def concat(*segs):
    out = []
    for s in segs: out.extend(s)
    return out

sounds = {
    "sfx_menu_select":   square(440,0.06,0.3),
    "sfx_menu_open":     concat(square(330,0.05,0.3),square(440,0.05,0.3)),
    "sfx_dialogue":      square(600,0.025,0.2),
    "sfx_dialogue_end":  concat(square(660,0.05,0.3),square(880,0.08,0.3)),
    "sfx_step_grass":    [int(32767*0.1*random.uniform(-1,1)) for _ in range(int(SR*0.04))],
    "sfx_step_road":     [int(32767*0.12*random.uniform(-1,1)) for _ in range(int(SR*0.03))],
    "sfx_step_cave":     [int(32767*0.15*random.uniform(-1,1)) for _ in range(int(SR*0.05))],
    "sfx_save":          concat(sine(523,0.1,0.35),sine(659,0.1,0.35),sine(784,0.2,0.4)),
    "sfx_level_up":      concat(sine(440,0.08),sine(554,0.08),sine(659,0.08),sine(880,0.2,0.5)),
    "sfx_battle_start":  concat(square(150,0.08,0.6),square(200,0.1,0.5)),
    "sfx_attack":        concat(saw(150,0.06,0.5),saw(120,0.08,0.4)),
    "sfx_player_hurt":   concat([int(32767*0.5*random.uniform(-1,1)) for _ in range(int(SR*0.06))],square(180,0.08,0.4)),
    "sfx_enemy_defeat":  concat(sweep(400,200,0.15,0.4),sine(220,0.15,0.3)),
    "sfx_spare":         concat(sine(660,0.1,0.4),sine(880,0.1,0.4),sine(1100,0.2,0.5)),
    "sfx_flee":          concat(sweep(200,600,0.12,0.4),square(800,0.06,0.3)),
    "sfx_boss_hit":      concat(saw(80,0.15,0.7),[int(32767*0.4*random.uniform(-1,1)) for _ in range(int(SR*0.05))]),
    "sfx_algo_hit":      concat(saw(50,0.2,0.8),[int(32767*0.5*random.uniform(-1,1)) for _ in range(int(SR*0.06))]),
    "sfx_boss_phase":    concat(sweep(200,400,0.15,0.5),sweep(400,800,0.2,0.5)),
    "sfx_empathy":       concat(sine(440,0.1,0.3),sine(550,0.1,0.3),sine(660,0.1,0.3),sine(880,0.3,0.5)),
    "sfx_shop_open":     concat(square(380,0.06,0.3),square(480,0.06,0.3)),
    "sfx_shop_buy":      concat(sine(523,0.08,0.3),sine(659,0.1,0.4)),
    "sfx_chest_open":    concat(square(330,0.06,0.3),square(440,0.06,0.3),square(550,0.1,0.4)),
    "sfx_quest_start":   concat(sine(440,0.08,0.3),sine(660,0.1,0.4)),
    "sfx_quest_done":    concat(sine(440,0.08),sine(554,0.08),sine(659,0.08),sine(880,0.08),sine(1100,0.2,0.5)),
    "sfx_stairs":        concat([int(32767*0.2*random.uniform(-1,1)) for _ in range(int(SR*0.04))],square(200,0.06,0.3)),
    "sfx_portal":        concat(sweep(200,800,0.2,0.5),sine(400,0.2,0.3),sweep(800,200,0.2,0.4)),
    "sfx_night_start":   concat(sweep(400,200,0.3,0.3),sine(220,0.3,0.2)),
    "sfx_day_start":     concat(sweep(200,600,0.3,0.4),sine(660,0.2,0.3)),
    "sfx_good_end":      concat(sine(523,0.1,0.3),sine(659,0.1,0.3),sine(784,0.1,0.3),sine(1047,0.4,0.5)),
    "sfx_bad_end":       concat(sweep(400,100,0.4,0.5),saw(80,0.3,0.4)),
    "sfx_tilki":         concat(square(800,0.05,0.3),square(1000,0.05,0.3),square(800,0.08,0.3)),
    "sfx_cutscene":      sweep(300,600,0.3,0.3),
    "sfx_block":         concat(square(300,0.03,0.5),[int(32767*0.2*random.uniform(-1,1)) for _ in range(int(SR*0.03))]),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))
for name, data in sounds.items():
    write_wav(f"{name}.wav", data)
    print(f"  {name}.wav")
print(f"\nToplam {len(sounds)} ses dosyasi!")
