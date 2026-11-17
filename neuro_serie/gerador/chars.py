# ---------- shared characters (talking people + villain) ----------
VF="pt-BR-FranciscaNeural"; VT="pt-BR-ThalitaMultilingualNeural"; VA="pt-BR-AntonioNeural"
DEEP=("-14%","-30Hz"); RAULV=("-4%","-16Hz"); BIAV=("+6%","+8Hz"); LIAV=("+2%","+0Hz")
PEOPLE_STYLE={"lia":((235,190,160),(120,70,160)),"raul":((180,130,95),(30,50,110)),"bia":((245,210,180),(250,200,40))}
def person(d,x,y,kind,s=1.0,dim=False):
    skin,shirt=PEOPLE_STYLE[kind]
    if dim: skin=tuple(int(v*0.45) for v in skin); shirt=tuple(int(v*0.45) for v in shirt)
    m=mouth_at(T(),kind); u=s
    d.rounded_rectangle([x-120*u,y+60*u,x+120*u,y+260*u],radius=int(70*u),fill=shirt)
    if kind=="raul": d.polygon([(x-25*u,y+60*u),(x,y+110*u),(x+25*u,y+60*u)],fill=(230,230,240)); d.ellipse([x+50*u,y+110*u,x+80*u,y+140*u],fill=(255,215,0))
    if kind=="bia": d.line([x-80*u,y+70*u,x+30*u,y+170*u],fill=(40,40,40),width=max(2,int(8*u))); d.rounded_rectangle([x+10*u,y+150*u,x+80*u,y+200*u],radius=int(10*u),fill=(40,40,50)); d.ellipse([x+30*u,y+160*u,x+60*u,y+190*u],fill=(120,170,230))
    if kind=="lia": d.rounded_rectangle([x-150*u,y-100*u,x-60*u,y+40*u],radius=int(40*u),fill=(110,60,30)) if False else None; d.ellipse([x-45*u,y-125*u,x+45*u,y-55*u],fill=(110,60,30))
    if kind=="bia":
        d.ellipse([x-85*u,y-60*u,x-40*u,y+50*u],fill=(240,200,90)); d.ellipse([x+40*u,y-60*u,x+85*u,y+50*u],fill=(240,200,90))
    d.ellipse([x-72*u,y-80*u,x+72*u,y+72*u],fill=skin,outline=(60,40,30),width=max(2,int(4*u)))
    if kind=="lia": d.chord([x-75*u,y-85*u,x+75*u,y+10*u],180,360,fill=(110,60,30))
    if kind=="raul":
        d.chord([x-78*u,y-115*u,x+78*u,y-20*u],180,360,fill=(30,50,110)); d.rectangle([x-80*u,y-70*u,x+95*u,y-55*u],fill=(20,30,70)); d.ellipse([x-12*u,y-108*u,x+12*u,y-84*u],fill=(255,215,0))
        d.polygon([(x-38*u,y+18*u),(x,y+8*u),(x+38*u,y+18*u),(x,y+26*u)],fill=(60,35,20))
    if kind=="bia":
        d.ellipse([x-125*u,y-75*u,x+125*u,y-40*u],fill=(255,120,170)); d.chord([x-70*u,y-130*u,x+70*u,y-40*u],180,360,fill=(255,140,185)); d.rectangle([x-70*u,y-62*u,x+70*u,y-52*u],fill=(255,255,255))
    blink=(fn+hash(kind)%40)%90<4
    for ex in (-26,26):
        if blink: d.line([x+(ex-10)*u,y-10*u,x+(ex+10)*u,y-10*u],fill=(30,20,20),width=max(2,int(4*u)))
        else: d.ellipse([x+(ex-9)*u,y-20*u,x+(ex+9)*u,y],fill=(30,20,20))
        if kind=="lia": d.ellipse([x+(ex-22)*u,y-32*u,x+(ex+22)*u,y+12*u],outline=(40,40,40),width=max(2,int(5*u)))
    if m>0.06: mh=6+34*m; d.ellipse([x-20*u,y+(38-mh/2)*u,x+20*u,y+(38+mh/2)*u],fill=(120,30,40))
    else: d.arc([x-26*u,y+15*u,x+26*u,y+48*u],20,160,fill=(120,40,40),width=max(2,int(5*u)))
def doctor(d,x,y,s=1.0,sil=False):
    m=mouth_at(T(),"doc"); u=s
    coat=(25,25,30) if sil else (245,245,250); skin=(25,25,30) if sil else (185,220,185); hair=(30,30,36) if sil else (235,235,245)
    d.polygon([(x-150*u,y+300*u),(x-110*u,y+70*u),(x+110*u,y+70*u),(x+150*u,y+300*u)],fill=coat,outline=(80,80,90) if not sil else coat)
    if not sil: d.polygon([(x-40*u,y+70*u),(x,y+160*u),(x+40*u,y+70*u)],fill=(110,30,150)); d.line([x,y+160*u,x,y+300*u],fill=(180,180,190),width=max(2,int(4*u)))
    for i in range(9):
        a=math.pi*(0.9+i*0.15); r1=95*u; r2=150*u+(18*u if i%2 else 0)
        d.polygon([(x+r1*math.cos(a-0.2),y-20*u+r1*math.sin(a-0.2)),(x+r2*math.cos(a),y-20*u+r2*math.sin(a)),(x+r1*math.cos(a+0.2),y-20*u+r1*math.sin(a+0.2))],fill=hair)
    d.ellipse([x-90*u,y-110*u,x+90*u,y+85*u],fill=skin,outline=(40,60,40) if not sil else skin,width=max(2,int(4*u)))
    for ex in (-38,38):
        cx_,cy_=x+ex*u,y-25*u; r=32*u
        d.ellipse([cx_-r,cy_-r,cx_+r,cy_+r],fill=(255,255,255) if not sil else (60,0,80),outline=(40,40,40),width=max(2,int(6*u)))
        rot=fn*0.35
        for j in range(3):
            rr=r*(0.85-j*0.25); d.arc([cx_-rr,cy_-rr,cx_+rr,cy_+rr],int(math.degrees(rot)+j*120)%360,int(math.degrees(rot)+j*120+200)%360,fill=(200,60,255),width=max(2,int(5*u)))
        d.line([cx_-34*u*np.sign(ex)*-1-0*u,y-72*u,cx_+30*u*np.sign(ex),y-62*u+(-12*u if ex<0 else -12*u)],fill=(40,40,40) if not sil else (90,0,120),width=max(3,int(9*u)))
    mh=14+40*m
    d.chord([x-48*u,y+(28-mh/2)*u,x+48*u,y+(28+mh)*u],0,180,fill=(60,0,30) if not sil else (90,0,120))
    if not sil: d.line([x-44*u,y+28*u,x+44*u,y+28*u],fill=(255,255,255),width=max(2,int(7*u)))
