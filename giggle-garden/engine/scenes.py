"""Giggle Garden scene library (doc 4.3): static background (cached) + animated layer per frame."""
import math, functools, random
import numpy as np, cv2
from engine import *
from engine import _p, SH

SKY = ((120,200,255),(205,238,255))

def hills(img, y, amp, col, phase=0, freq=1.0):
    pts = [(x, y + amp * math.sin(x / W * math.pi * 2 * freq + phase)) for x in range(0, W + 20, 20)]
    poly(img, pts + [(W, H), (0, H)], col)

def flower(img, x, y, s, col):
    line(img, (x, y), (x, y + 40 * s), (70,160,70), 5 * s)
    for k in range(5):
        a = k * 2 * math.pi / 5
        circ(img, (x + 13*s*math.cos(a), y + 13*s*math.sin(a)), 10*s, col)
    circ(img, (x, y), 9*s, (255,230,90))

def cloud(img, x, y, s, col=(255,255,255)):
    for dx, dy, r in ((-60,10,45),(0,-15,60),(60,10,45),(-25,20,45),(30,22,45)):
        circ(img, (x + dx*s, y + dy*s), r*s, col)

def rainbow(img, cx, cy, r0, w=26, a=1.0):
    cols = [(255,99,132),(255,170,51),(255,224,70),(140,220,90),(80,190,255),(190,120,255)]
    for i, c in enumerate(cols):
        arc(img, (cx, cy), (r0 - i*w, r0 - i*w), 180, 360, c, w + 1)

def tree(img, x, y, s, top=(90,190,90), fruit=None):
    rect(img, x - 18*s, y - 150*s, x + 18*s, y, (140,95,60))
    for dx, dy, r in ((0,-230,95),(-70,-180,70),(70,-180,70)):
        circ(img, (x + dx*s, y + dy*s), r*s, top)
    if fruit:
        for dx, dy in ((-40,-200),(30,-240),(50,-170),(-60,-150),(0,-160)):
            circ(img, (x+dx*s, y+dy*s), 13*s, fruit)

def pine(img, x, y, s, snow=False):
    rect(img, x-12*s, y-40*s, x+12*s, y, (120,85,55))
    for k in range(3):
        yy = y - 40*s - k*70*s; w = (110 - k*25)*s
        poly(img, [(x-w, yy), (x+w, yy), (x, yy-120*s)], (50,140,80))
        if snow: poly(img, [(x-w*0.45, yy-70*s), (x+w*0.45, yy-70*s), (x, yy-120*s)], (250,252,255))

def ground_detail(img, y0, col, n=40, seed=1):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(0, W); y = rnd.uniform(y0 + 40, H - 20)
        ell(img, (x, y), (rnd.uniform(8, 20), 4), col)

# ---------------------------------------------------------------- static backgrounds
@functools.lru_cache(maxsize=32)
def background(name):
    f = globals().get('bg_' + name, bg_meadow)
    img = f(); return img

def bg_meadow():
    img = gradient(*SKY); rainbow(img, 540, 1060, 470)
    hills(img, 1150, 40, (150,220,110), 0.5, 1.2); hills(img, 1250, 30, (120,205,95), 2, 0.9)
    rnd = random.Random(3)
    for _ in range(26): flower(img, rnd.uniform(20, 1060), rnd.uniform(1300, 1850), rnd.uniform(0.8, 1.3), rnd.choice(PALETTE))
    return img

def bg_sunset_meadow():
    img = gradient((255,150,90),(255,215,150))
    hills(img, 1150, 40, (200,170,90), 0.5, 1.2); hills(img, 1250, 30, (150,190,90), 2, 0.9)
    rnd = random.Random(4)
    for _ in range(18): flower(img, rnd.uniform(20,1060), rnd.uniform(1300,1850), 1, rnd.choice(PALETTE))
    return img

def bg_garden():
    img = gradient(*SKY); hills(img, 1180, 20, (130,205,100), 1, 1)
    tree(img, 140, 1240, 1.1, fruit=(235,60,60)); tree(img, 950, 1230, 1.0, fruit=(235,60,60))
    for row, y in enumerate(range(1320, 1860, 110)):
        rect(img, 0, y, W, y + 40, (150,100,60))
        for x in range(60, W, 120):
            if row % 2 == 0:
                poly(img, [(x-12, y+5), (x+12, y+5), (x, y+50)], (255,140,40))
                for a in (-20, 0, 20): ell(img, (x + a*0.6, y - 14), (8, 22), (80,180,70), a)
            else:
                circ(img, (x, y - 8), 18, (110,200,80)); circ(img, (x+20, y-12), 12, (90,180,70))
    return img

def bg_garden_flowers():
    img = gradient(*SKY); hills(img, 1200, 25, (130,205,100), 1, 1)
    rnd = random.Random(5)
    for x in range(40, W, 90):
        h = rnd.uniform(250, 480); y = 1300
        line(img, (x, y), (x, y - h), (70,160,70), 9)
        if rnd.random() < 0.4:
            for k in range(14):
                a = k*2*math.pi/14; ell(img, (x+40*math.cos(a), y-h+40*math.sin(a)), (22, 10), (255,205,40), math.degrees(a))
            circ(img, (x, y-h), 30, (140,90,40))
        else: flower(img, x, y - h, 2.0, rnd.choice(PALETTE))
    return img

def bg_bathroom():
    img = np.zeros((H, W, 3), np.uint8); img[:] = (200,235,245)
    for y in range(0, 1300, 90):
        for x in range(0, W, 90): cv2.rectangle(img, (x, y), (x+88, y+88), (175,220,235), 3)
    img[1300:] = (240,235,225)
    oell(img, (300, 520), (150, 190), (220,245,255), (180,200,215), 12)
    rect(img, 760, 300, 790, 1300, (190,200,210)); circ(img, (775, 300), 50, (190,200,210))
    poly(img, [(560, 1180), (1060, 1180), (1030, 1380), (590, 1380)], WHITE)
    for k in range(12): circ(img, (590 + k*40, 1170 + 15*math.sin(k)), 34, (250,250,255))
    circ(img, (900, 1130), 32, (255,214,70)); circ(img, (930, 1100), 20, (255,214,70)); poly(img, [(945,1100),(970,1108),(945,1114)], (255,150,40))
    return img

def bg_bedroom():
    img = np.zeros((H, W, 3), np.uint8); img[:] = (190,170,235)
    rnd = random.Random(7)
    for _ in range(30): poly(img, star_pts(rnd.uniform(0,W), rnd.uniform(240,1200), 12), (230,215,255))
    rect(img, 330, 330, 750, 780, (40,50,110)); circ(img, (640, 450), 60, (255,240,170)); circ(img, (615, 435), 55, (40,50,110))
    for x in (330, 750): poly(img, [(x-80, 300), (x+80, 300), (x+40 if x>500 else x+20, 820), (x-40 if x>500 else x-20, 820)], (255,150,190))
    img[1300:] = (225,180,140)
    ell(img, (540, 1650), (420, 120), (255,200,120))
    rect(img, 760, 1080, 1060, 1320, (120,170,240)); rect(img, 760, 1040, 1060, 1110, WHITE)
    rect(img, 40, 900, 330, 920, (150,100,60))
    for k, c in enumerate(PALETTE[:4]): rect(img, 60 + k*40, 830, 90 + k*40, 900, c)
    circ(img, (270, 860), 38, (190,140,90)); circ(img, (245, 820), 16, (190,140,90)); circ(img, (295, 820), 16, (190,140,90))
    return img

def bg_night():
    img = gradient((20,25,70),(60,60,130)); rnd = random.Random(8)
    for _ in range(80): circ(img, (rnd.uniform(0,W), rnd.uniform(240,1150)), rnd.uniform(2,5), (255,250,220))
    hills(img, 1180, 45, (40,70,70), 0.3, 1.1); hills(img, 1280, 30, (50,90,70), 2.1, 0.8)
    return img

def bg_space():
    img = gradient((15,10,45),(50,30,100)); rnd = random.Random(9)
    for _ in range(120): circ(img, (rnd.uniform(0,W), rnd.uniform(0,H)), rnd.uniform(1.5,4.5), (255,255,240))
    circ(img, (850, 520), 110, (255,140,100)); circ(img, (820, 490), 30, (255,170,130))
    circ(img, (200, 900), 80, (110,200,255)); circ(img, (230, 870), 22, (150,220,255))
    ell(img, (720, 1150), (160, 40), (255,214,120), -12, 14); circ(img, (720, 1150), 70, (210,150,255))
    return img

def bg_moon():
    img = gradient((10,10,40),(30,30,80)); rnd = random.Random(10)
    for _ in range(90): circ(img, (rnd.uniform(0,W), rnd.uniform(0,1250)), rnd.uniform(1.5,4), (255,255,240))
    circ(img, (840, 450), 120, (80,160,255)); ell(img, (810, 420), (50, 35), (110,200,110)); ell(img, (880, 500), (35, 25), (110,200,110))
    hills(img, 1260, 25, (175,175,185), 0.4, 1.3)
    for x, y, r in ((150,1450,60),(800,1380,45),(500,1750,80),(950,1700,50),(260,1800,40)):
        ell(img, (x, y), (r, r*0.35), (140,140,150)); ell(img, (x, y - 4), (r*0.8, r*0.25), (120,120,130))
    line(img, (960, 1380), (960, 1180), (220,220,220), 6); poly(img, [(960,1180),(1050,1205),(960,1230)], (255,99,132))
    return img

def bg_rain():
    img = gradient((140,150,170),(195,200,210))
    hills(img, 1220, 30, (110,170,100), 1, 1)
    for x, y, s in ((200, 330, 1.6), (600, 280, 1.9), (930, 380, 1.5)): cloud(img, x, y, s, (150,155,170))
    for x, y, r in ((200,1600,120),(800,1450,90),(540,1820,140)): ell(img, (x, y), (r, r*0.25), (120,150,190))
    return img

def bg_mud():
    img = gradient(*SKY); hills(img, 1220, 30, (130,190,95), 1, 1)
    for x, y, r in ((200,1580,150),(820,1500,120),(560,1800,160)): ell(img, (x, y), (r, r*0.28), (120,80,50)); ell(img, (x-10, y-5), (r*0.7, r*0.15), (140,95,60))
    for x, y, s in ((250, 380, 1.2), (800, 320, 1.4)): cloud(img, x, y, s)
    return img

def bg_clouds():
    img = gradient((190,210,255),(255,220,240)); rainbow(img, 540, 1000, 430)
    for x, y, s in ((180,700,1.4),(880,820,1.2),(500,500,1.0)): cloud(img, x, y, s)
    for x in range(-60, W + 120, 150): cloud(img, x, 1450, 1.8); cloud(img, x + 70, 1650, 2.2)
    img[1700:] = (255,255,255)
    return img

def bg_beach():
    img = gradient((100,200,255),(190,235,255))
    rect(img, 0, 1100, W, 1260, (60,170,230))
    poly(img, [(x, 1240 + 18*math.sin(x/60)) for x in range(0, W+20, 20)] + [(W, H), (0, H)], (250,225,160))
    rect(img, 150, 1000, 175, 1300, (150,105,65))
    for a in (-60, -20, 20, 60): ell(img, (162 + 80*math.sin(math.radians(a)), 990 + 20*abs(a)/60), (95, 22), (70,180,80), a)
    line(img, (880, 1500), (880, 1200), WHITE, 8)
    cv2.ellipse(img, (_p(880), _p(1200)), (_p(170), _p(100)), 0, 180, 360, (255,99,132), -1, cv2.LINE_AA, SH)
    return img

def bg_sunset_beach():
    img = gradient((255,130,170),(255,200,140)); circ(img, (540, 1100), 130, (255,230,120))
    rect(img, 0, 1100, W, 1260, (200,110,170))
    for k in range(6): rect(img, 470 - k*12, 1120 + k*22, 610 + k*12, 1128 + k*22, (255,210,140))
    poly(img, [(x, 1240 + 18*math.sin(x/60)) for x in range(0, W+20, 20)] + [(W, H), (0, H)], (245,205,150))
    return img

def bg_underwater():
    img = gradient((40,160,220),(10,70,140))
    for k in range(5): poly(img, [(100+k*220, 0), (180+k*220, 0), (60+k*220+120, 1600), (k*220-20, 1600)], (70,180,230))
    img[:] = cv2.addWeighted(img, 0.85, gradient((40,160,220),(10,70,140)), 0.15, 0)
    poly(img, [(x, 1500 + 20*math.sin(x/90)) for x in range(0, W+20, 20)] + [(W, H), (0, H)], (240,215,150))
    for x, c in ((120,(255,120,150)),(950,(255,170,80)),(780,(190,120,255))):
        for a in (-30, 0, 30): ell(img, (x + a, 1450), (16, 70), c, a)
    return img

def bg_farm():
    img = gradient(*SKY); hills(img, 1200, 30, (130,205,100), 1, 0.8)
    rect(img, 620, 860, 980, 1260, (220,60,60)); poly(img, [(600, 870), (1000, 870), (800, 700)], (170,40,40))
    rect(img, 740, 1060, 860, 1260, WHITE); rect(img, 755, 1075, 845, 1260, (180,50,50))
    rect(img, 1000, 760, 1070, 1260, (190,200,210)); circ(img, (1035, 760), 35, (150,160,175))
    for x in range(0, W, 70): rect(img, x, 1270, x+14, 1360, (240,230,210))
    rect(img, 0, 1290, W, 1302, (240,230,210)); rect(img, 0, 1330, W, 1342, (240,230,210))
    for x in (120, 330): ell(img, (x, 1650), (90, 60), (240,200,90)); arc(img, (x, 1650), (70, 40), 0, 360, (210,170,60), 4)
    return img

def bg_pond():
    img = gradient(*SKY); hills(img, 1180, 30, (130,205,100), 1, 1)
    ell(img, (540, 1400), (520, 170), (80,170,220))
    for x, y in ((250,1400),(780,1440),(560,1330)): ell(img, (x, y), (55, 22), (90,180,80))
    for x in (60, 100, 990, 1030):
        line(img, (x, 1450), (x, 1150), (80,150,70), 8); ell(img, (x, 1170), (12, 45), (140,90,50))
    return img

def bg_snow():
    img = gradient((170,210,240),(230,240,250))
    hills(img, 1150, 50, (240,245,255), 0.5, 1.2); hills(img, 1260, 30, (250,252,255), 2, 0.9)
    for x, s in ((120, 1.0), (980, 1.1), (850, 0.7)): pine(img, x, 1250, s, True)
    return img

def bg_snowman():
    img = bg_snow()
    circ(img, (880, 1250), 90, WHITE); circ(img, (880, 1110), 65, WHITE); circ(img, (880, 1000), 48, WHITE)
    rect(img, 840, 920, 920, 960, (40,40,50)); rect(img, 825, 955, 935, 965, (40,40,50))
    poly(img, [(880,1005),(925,1012),(880,1020)], (255,140,40)); rect(img, 832, 1040, 928, 1062, (255,99,132))
    return img

def bg_snow_night():
    img = gradient((30,40,90),(80,90,150))
    hills(img, 1180, 40, (215,225,245), 0.5, 1.1); hills(img, 1270, 30, (230,235,250), 2, 0.9)
    rect(img, 700, 950, 1000, 1240, (140,90,60)); poly(img, [(680, 960), (1020, 960), (850, 820)], (240,245,255))
    rect(img, 740, 1020, 820, 1090, (255,215,110)); rect(img, 880, 1020, 960, 1090, (255,215,110)); rect(img, 930, 830, 965, 920, (120,80,60))
    pine(img, 150, 1250, 1.0, True)
    return img

def bg_launch():
    img = gradient(*SKY); hills(img, 1230, 20, (130,200,100), 1, 1)
    rect(img, 760, 1180, 1020, 1240, (150,150,160)); rect(img, 990, 700, 1010, 1180, (200,80,80))
    return img

def bg_autumn():
    img = gradient((255,200,140),(255,230,190)); hills(img, 1200, 35, (220,170,80), 1, 1)
    for x, c in ((130, (240,130,40)), (950, (220,80,40)), (800, (250,180,50))): tree(img, x, 1250, 1.0, top=c)
    for x in (300, 700, 520): circ(img, (x, 1640), 55, (255,140,30)); rect(img, x-6, 1575, x+6, 1595, (100,140,60))
    return img

def bg_disco():
    img = gradient((70,30,120),(120,50,170))
    rect(img, 0, 1280, W, H, (60,30,90))
    for x, y in ((90, 1050), (990, 1050)):
        rect(img, x-70, y, x+70, y+230, (30,20,40)); circ(img, (x, y+70), 40, (90,80,110)); circ(img, (x, y+170), 30, (90,80,110))
    return img

# ---------------------------------------------------------------- animated layers
def sun(img, x, y, r, t):
    for k in range(12):
        a = t * 0.6 + k * math.pi / 6
        line(img, (x + (r+15)*math.cos(a), y + (r+15)*math.sin(a)), (x + (r+50)*math.cos(a), y + (r+50)*math.sin(a)), (255,200,40), 12)
    circ(img, (x, y), r, (255,220,60))
    circ(img, (x-25, y-10), 8, (90,60,30)); circ(img, (x+25, y-10), 8, (90,60,30))
    arc(img, (x, y+8), (28, 18), 20, 160, (90,60,30), 6)

def butterfly(img, x, y, t, col):
    f = abs(math.sin(t * 12))
    for s in (-1, 1): ell(img, (x + s*18*f, y), (18*f + 3, 22), col)
    line(img, (x, y-14), (x, y+14), (60,40,40), 5)

def bee(img, x, y, t):
    ell(img, (x, y), (24, 17), (255,214,70)); line(img, (x-6, y-16), (x-6, y+16), (50,40,40), 6); line(img, (x+8, y-15), (x+8, y+15), (50,40,40), 6)
    f = abs(math.sin(t*20)); ell(img, (x-4, y-22), (10, 14*f+3), (230,240,255))

def fish(img, x, y, s, col, d=1):
    ell(img, (x, y), (40*s, 24*s), col); poly(img, [(x - d*35*s, y), (x - d*65*s, y-22*s), (x - d*65*s, y+22*s)], col)
    circ(img, (x + d*20*s, y-6*s), 5*s, (30,30,50))

def anim(name, img, t, ctx):
    rnd = random.Random(42)
    if name in ('meadow','garden','garden_flowers','farm','pond','mud','beach','launch','autumn','snow','snowman','clouds','sunset_meadow'):
        if name not in ('clouds','autumn','sunset_meadow'): sun(img, 900, 340, 75, t)
        if name not in ('clouds',):
            for k in range(3): cloud(img, ((k * 420 + t * 25) % (W + 400)) - 200, 300 + k * 90, 0.9 + 0.2 * k)
    if name in ('meadow','sunset_meadow','garden_flowers'):
        for k in range(3): butterfly(img, 200 + k*330 + 60*math.sin(t*0.9+k), 850 + 80*math.sin(t*1.3 + k*2), t + k, PALETTE[k*2])
    if name in ('garden','garden_flowers'):
        for k in range(2): bee(img, 300 + 400*k + 120*math.sin(t*1.1+k), 1000 + 60*math.sin(t*2.1+k), t)
    if name == 'clouds':
        for k in range(4): cloud(img, ((k * 350 + t * 30) % (W + 400)) - 200, 350 + k*120, 0.7)
    if name in ('night','snow_night','bedroom'):
        if name == 'night':
            circ(img, (850, 400), 95, (255,240,170)); circ(img, (815, 385), 10, (120,100,60)); circ(img, (870, 385), 10, (120,100,60))
            arc(img, (845, 420), (28, 16), 20, 160, (120,100,60), 6)
            p = (t % 6) / 6
            if p < 0.25:
                x = 100 + p * 4 * 700; line(img, (x, 300 + p*4*200), (x-120, 300 + p*4*200 - 35), (255,250,210), 6)
            for k in range(14):
                x = rnd.uniform(0, W); y = rnd.uniform(1200, 1800); a = 0.5 + 0.5*math.sin(t*3 + k)
                circ(img, (x + 20*math.sin(t + k), y), 5 + 4*a, (230,255,120))
        tw = ctx.get('twinkle', True)
        for k in range(20):
            x = rnd.uniform(0, W); y = rnd.uniform(240, 1150) if name != 'bedroom' else rnd.uniform(350, 760)
            if name == 'bedroom' and not (340 < x < 740): continue
            a = 0.5 + 0.5*math.sin(t*4 + k*1.7)
            poly(img, star_pts(x, y, 6 + 6*a), (255,250,200))
    if name == 'space':
        x = (t * 160) % (W + 400) - 200
        ell(img, (x, 650), (60, 22), (240,240,250)); poly(img, [(x+60, 650), (x+30, 630), (x+30, 670)], (255,99,132))
        poly(img, [(x-60, 650), (x-95, 635 + 6*math.sin(t*30)), (x-95, 665)], (255,170,51))
    if name in ('snow','snowman','snow_night'):
        for k in range(60):
            x = (rnd.uniform(0, W) + 30*math.sin(t + k)) % W; y = (rnd.uniform(0, H) + t * (60 + k % 5 * 20)) % H
            circ(img, (x, y), 4 + k % 3, WHITE)
    if name == 'snow_night':
        for k in range(4): circ(img, (948 + 10*math.sin(t+k), 800 - ((t*40 + k*45) % 180)), 18 + k*3, (200,200,210))
    if name == 'autumn':
        for k in range(22):
            x = (rnd.uniform(0, W) + 60*math.sin(t*1.5 + k)) % W; y = (rnd.uniform(0, H) + t * (80 + k % 4*20)) % H
            ell(img, (x, y), (16, 9), PALETTE[k % 2], (t*120 + k*30) % 360)
    if name == 'rain':
        for k in range(70):
            x = rnd.uniform(0, W); y = (rnd.uniform(0, H) + t * 900) % H
            line(img, (x, y), (x - 8, y + 34), (210,225,250), 3)
        for k, (x, y) in enumerate(((200,1600),(800,1450),(540,1820))):
            p = ((t + k*0.4) % 1.2) / 1.2; arc(img, (x, y), (40 + 90*p, (40+90*p)*0.25), 0, 360, (230,240,255), max(1, 4*(1-p)))
    if name == 'mud':
        for b in ctx.get('beats', []):
            dt = t - b
            if 0 <= dt < 0.5:
                for k in range(6):
                    a = math.pi * (0.15 + 0.7*k/5); r = 40 + 260*dt
                    circ(img, (540 + r*math.cos(a)*1.4, 1520 - r*math.sin(a) + 400*dt*dt), 12, (130,85,55))
    if name in ('pond',):
        for k in range(2):
            x = 300 + k*420 + 80*math.sin(t*0.6 + k*2); y = 1380 + 25*k
            ell(img, (x, y), (42, 26), (255,255,250)); circ(img, (x+38, y-26), 20, (255,255,250)); poly(img, [(x+55,y-28),(x+78,y-22),(x+55,y-18)], (255,150,40))
            arc(img, (x, y+20), (70, 14), 0, 180, (200,230,250), 3)
    if name == 'beach':
        for k in range(3):
            y = 1150 + k*40; poly(img, [(x, y + 8*math.sin(x/50 + t*2 + k)) for x in range(0, W+20, 30)] + [(W, y+20), (0, y+20)], (110,200,245))
        bx = 760; by = 1350 - abs(math.sin(t * 2.5)) * 160
        circ(img, (bx, by), 45, WHITE)
        for k, c in enumerate(((255,99,132),(80,190,255),(255,214,70))): cv2.ellipse(img, (_p(bx), _p(by)), (_p(45), _p(45)), t*80, k*120, k*120+60, c, -1, cv2.LINE_AA, SH)
        for k in range(2):
            x = (t*70 + k*500) % (W + 200) - 100; y = 600 + 60*k
            arc(img, (x-18, y), (18, 12), 200, 340, (60,60,80), 5); arc(img, (x+18, y), (18, 12), 200, 340, (60,60,80), 5)
    if name == 'underwater':
        for k in range(4):
            d = 1 if k % 2 == 0 else -1; x = (t * 90 * d + k * 300) % (W + 200) - 100
            fish(img, x, 700 + k*180, 1.0, PALETTE[k], d)
        for k in range(16):
            x = rnd.uniform(0, W) + 10*math.sin(t*2 + k); y = H - ((t * 120 + k * 137) % H)
            circ(img, (x, y), 8 + k % 3 * 3, (220,245,255), 3)
    if name == 'disco':
        cx, cy = 540, 330
        for k in range(6):
            a = math.pi/2 + 0.9*math.sin(t*1.2 + k)
            poly(img, [(cx, cy), (cx + 1500*math.cos(a-0.05), cy + 1500*math.sin(a-0.05)), (cx + 1500*math.cos(a+0.05), cy + 1500*math.sin(a+0.05))], PALETTE[k])
        line(img, (cx, 0), (cx, cy - 70), (200,200,210), 5); circ(img, (cx, cy), 75, (210,215,230))
        for k in range(16):
            a = k * math.pi / 8 + t; circ(img, (cx + 45*math.cos(a), cy + 45*math.sin(a)*0.9), 9, WHITE)
        bi = ctx.get('beat_i', 0)
        for i in range(6):
            for j in range(3):
                c = PALETTE[(i + j + bi) % 6]; x0 = i * 180; y0 = 1300 + j * 210
                blend(img, x0 + 6, y0 + 6, x0 + 174, y0 + 204, c, 0.55)
    if name == 'launch':
        cnt = ctx.get('count_t'); lift = ctx.get('lift_t')
        y = 1180; shake = 0
        if lift is not None and t > lift: y -= (t - lift) ** 2 * 500
        elif cnt is not None and t - cnt < 0.6: shake = 6 * math.sin(t * 60)
        x = 880 + shake
        ell(img, (x, y - 220), (70, 200), (240,240,250)); poly(img, [(x-60, y-380), (x+60, y-380), (x, y-470)], (255,99,132))
        circ(img, (x, y - 260), 30, (80,190,255)); poly(img, [(x-70, y-80), (x-120, y), (x-60, y-20)], (255,99,132)); poly(img, [(x+70, y-80), (x+120, y), (x+60, y-20)], (255,99,132))
        if (lift is not None and t > lift) or (cnt is not None and t - cnt < 0.6):
            poly(img, [(x-35, y-25), (x+35, y-25), (x, y + 90 + 30*math.sin(t*40))], (255,170,51))
