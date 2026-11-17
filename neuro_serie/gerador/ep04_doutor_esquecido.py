import subprocess, random, math, json, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H,FPS,SR=1080,1920,30,44100
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FC={}
def F(s):
    s=max(8,int(s))
    if s not in FC: FC[s]=ImageFont.truetype(FB,s)
    return FC[s]
rng=np.random.default_rng(3); random.seed(11)
# ---------- voice with word timings ----------
VOICE="pt-BR-AntonioNeural"
STY={"q":("-4%","+12Hz"),"x":("+12%","+6Hz"),"n":("+8%","+0Hz"),"f":("+20%","+8Hz")}
def dec(p):
    raw=subprocess.check_output(["ffmpeg","-v","error","-i",p,"-f","s16le","-ac","1","-ar",str(SR),"-"])
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
CLIP=0
def say(parts,gap=0.12,spk="neuro",VO=None,echo=False):
    global CLIP
    aud=[]; words=[]; starts=[]; t=0.0
    for it in parts:
        txt,k=it[0],it[1]; vc=it[2] if len(it)>2 else (VO or VOICE)
        r,p=STY[k] if isinstance(k,str) else k; mp=f"ep04_{CLIP}.mp3"; CLIP+=1
        subprocess.run(["python3","tts2.py",vc,txt,mp,r,p],check=True)
        a=dec(mp); wb=json.load(open(mp+".json"))
        s0=max(0,wb[0][1]-0.04); s1=min(len(a)/SR,wb[-1][1]+wb[-1][2]+0.08)
        seg=a[int(s0*SR):int(s1*SR)]
        starts.append(t)
        for w,o,du in wb: words.append((w,t+o-s0,t+o-s0+du,len(starts)))
        aud+=[seg,np.zeros(int(gap*SR),np.float32)]; t+=len(seg)/SR+gap
    A=np.concatenate(aud)
    if echo:
        A=np.concatenate([A,np.zeros(int(0.5*SR),np.float32)]); E=A.copy()
        for dl,g in ((0.11,0.38),(0.23,0.22),(0.37,0.12)): n_=int(dl*SR); E[n_:]+=g*A[:-n_]
        A=E*0.8; t+=0.4
    return {"a":A,"w":words,"s":starts,"d":t,"spk":spk}
BOSS_T=1e9
V={}
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
V["intro"]=say([("Oi! Eu sou o Neuro!","x"),("E hoje eu vou testar o seu cérebro!","x"),("Você tem três vidas.","n"),("Bora?","q")])
V["tema"]=say([("Tema de hoje:","n"),("o Doutor Esquecido!","x")])
V["d1"]=say([("Eu sou o Doutor Esquecido!",DEEP,VA),("Com a minha máquina, vou apagar a memória de todo mundo!",DEEP,VA),("Começando por você, Neuro!",DEEP,VA)],spk="doc",echo=True)
V["n1"]=say([("Socorro! Tô esquecendo tudo!","x"),("Me ajuda!","x"),("Cada desafio que você acertar, devolve um pedaço da minha memória!","n")])
V["q1a"]=say([("Desafio um!","x"),("Memoriza a sequência de cores!","x")])
V["q1b"]=say([("Qual foi a ordem?","q")])
V["r1"]=say([("A C!","x"),("Vermelho, azul, verde, vermelho, amarelo!","n")])
V["m1"]=say([("Opa! Tô lembrando!","x")])
V["q2a"]=say([("Desafio dois!","x"),("Presta atenção nos números!","x")])
V["q2b"]=say([("Qual era o terceiro número?","q")])
V["r2"]=say([("Nove!","x"),("Sete, três, nove!","n")])
V["m2"]=say([("Mais memória voltando!","x")])
V["q3"]=say([("Desafio três!","x"),("O doutor criou clones!","x"),("Qual é o Neuro de verdade?","q")])
V["r3"]=say([("Sou eu, o E!","x"),("Os clones têm olhos roxos!","n")])
V["m3"]=say([("Quase lá!","x")])
V["ib"]=say([("Chefão final!","x")])
V["d2"]=say([("Ninguém resolve o meu enigma!",DEEP,VA),("O que é que, quanto mais você tira, maior fica?",DEEP,VA)],spk="doc",echo=True)
V["rb"]=say([("Um buraco!","x"),("Quanto mais terra você tira, maior ele fica!","n")])
V["d3"]=say([("Nãããão! A minha máquina!",DEEP,VA)],spk="doc",echo=True)
V["m4"]=say([("Memória cem por cento!","x"),("Valeu, pessoal!","x")])
V["d4"]=say([("Isso não acabou, Neuro!",DEEP,VA),("Eu vou voltar!",DEEP,VA)],spk="doc",echo=True)
V["out"]=say([("Quantas vidas sobraram?","q"),("Três? Memória de elefante!","q"),("Uma ou duas? Memória boa!","q"),("Nenhuma? O doutor te apagou!","q"),("Comenta se você vai me ajudar na batalha final!","x")])
# ---------- render engine ----------
ff=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-pix_fmt","yuv420p","-c:v","libx264","-preset","fast","-crf","20","ep04v.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
fn=0; plays=[]; sfx=[]; caps=[]; FX={"shake":0,"zoom":0,"flash":0}; CAPY=[1560]
def T(): return fn/FPS
def play(key,delay=0.1):
    st=T()+delay; plays.append((key,st)); w=V[key]["w"]
    chunk=[]; f=F(80); dm=ImageDraw.Draw(Image.new("RGB",(1,1)))
    def width(ch): return sum(dm.textlength(x[0].upper(),font=f) for x in ch)+dm.textlength(" ",font=f)*(len(ch)-1)
    for i,x in enumerate(w):
        if chunk and (x[3]!=chunk[-1][3] or len(chunk)==3 or width(chunk+[x])>900):
            caps.append([(q[0],st+q[1],st+q[2]) for q in chunk]); chunk=[]
        chunk.append(x)
    if chunk: caps.append([(q[0],st+q[1],st+q[2]) for q in chunk])
    return V[key]["d"]
def draw_caps(d):
    t=T()
    for i,ch in enumerate(caps):
        end=caps[i+1][0][1] if i+1<len(caps) and caps[i+1][0][1]-ch[-1][2]<0.6 else ch[-1][2]+0.35
        if ch[0][1]-0.05<=t<end:
            f=F(80); sp=d.textlength(" ",font=f)
            ws=[w.upper() for w,_,_ in ch]; tw=sum(d.textlength(w,font=f) for w in ws)+sp*(len(ws)-1)
            x=(W-tw)/2; y=CAPY[0]
            for (w,a,b),u in zip(ch,ws):
                act=a<=t<(b+0.12)
                if act: d.rounded_rectangle([x-12,y-8,x+d.textlength(u,font=f)+12,y+92],radius=18,fill=(255,40,90))
                d.text((x,y),u,font=f,fill=(255,255,255) if not act else (255,255,0),stroke_width=7,stroke_fill=(0,0,0))
                x+=d.textlength(u,font=f)+sp
            break
def emit(im):
    global fn
    d=ImageDraw.Draw(im); draw_caps(d)
    if FX["zoom"]>0:
        z=1+0.08*(FX["zoom"]/6); cw,ch=int(W/z),int(H/z)
        im=im.crop(((W-cw)//2,(H-ch)//2,(W-cw)//2+cw,(H-ch)//2+ch)).resize((W,H)); FX["zoom"]-=1
    if FX["shake"]>0:
        a=FX["shake"]*3; im=Image.fromarray(np.roll(np.roll(np.asarray(im),random.randint(-a,a),0),random.randint(-a,a),1)); FX["shake"]-=1
    if FX.get("glitch",0)>0:
        arr=np.asarray(im).copy(); o=random.randint(10,34); arr[...,0]=np.roll(arr[...,0],o,1); arr[...,2]=np.roll(arr[...,2],-o,1)
        for _ in range(7):
            y_=random.randint(0,H-80); h_=random.randint(12,80); arr[y_:y_+h_]=np.roll(arr[y_:y_+h_],random.randint(-120,120),1)
        im=Image.fromarray(arr); FX["glitch"]-=1
    if FX.get("wipe",0)>0:
        p=FX["wipe"]/9; dd=ImageDraw.Draw(im); x=W*1.6*p-300
        dd.polygon([(x-W,0),(x+300,0),(x,H),(x-W-300,H)],fill=WIPEC[0]); dd.polygon([(x+300,0),(x+360,0),(x+60,H),(x,H)],fill=(255,255,255)); FX["wipe"]-=1
    if FX["flash"]>0:
        im=Image.blend(im,Image.new("RGB",(W,H),(255,255,255)),FX["flash"]/5); FX["flash"]-=1
    ff.stdin.write(im.tobytes()); fn+=1
WIPEC=[(255,200,0)]
def cut(c=(255,200,0)): FX["zoom"]=5; FX["wipe"]=9; WIPEC[0]=c; sfx.append((T(),"whoosh"))
yy=np.linspace(0,1,H,dtype=np.float32)[:,None,None]
PART=[(rng.uniform(0,W),rng.uniform(0,H),rng.uniform(3,9),rng.uniform(20,60)) for _ in range(30)]
def bg(c1,c2):
    t=np.clip(yy+0.07*math.sin(fn/18),0,1)
    im=Image.fromarray((np.array(c1,np.float32)*(1-t)+np.array(c2,np.float32)*t).astype(np.uint8).repeat(1,0).__array__() if False else np.broadcast_to(np.array(c1,np.float32)*(1-t)+np.array(c2,np.float32)*t,(H,W,3)).astype(np.uint8))
    d=ImageDraw.Draw(im)
    for x,y,r,v in PART:
        py=(y-fn*v/FPS*3)%H; d.ellipse([x-r,py-r,x+r,py+r],fill=tuple(min(255,int(c*1.6)+30) for c in c1))
    return im,d
def ctext(d,y,t,size,fill=(255,255,255),stroke=6,s=1.0):
    f=F(size*s); w=d.textlength(t,font=f); d.text(((W-w)/2,y-size*s/2),t,font=f,fill=fill,stroke_width=stroke,stroke_fill=(0,0,0))
def pop(k,n=7,lo=0.3):
    if k<0: return 0
    if k>=n: return 1
    x=k/n; return lo+(1-lo)*x+0.35*math.sin(x*math.pi)
def header(d,step,title,col):
    if step<0: return
    for i in range(4):
        cx=W/2+(i-1.5)*110; on=i<=step
        d.ellipse([cx-38,60,cx+38,136],fill=col if on else (60,60,80),outline=(255,255,255),width=4)
        tw=d.textlength(str(i+1),font=F(44)); d.text((cx-tw/2,72),str(i+1),font=F(44),fill=(255,255,255))
    f=F(52); w=d.textlength(title,font=f)
    d.rounded_rectangle([(W-w)/2-30,170,(W+w)/2+30,250],radius=40,fill=col); d.text(((W-w)/2,182),title,font=f,fill=(255,255,255))
def timer(d,frac,col=(255,215,0)):
    d.rounded_rectangle([80,1780,W-80,1820],radius=20,outline=(255,255,255),width=3)
    d.rounded_rectangle([80,1780,80+(W-160)*max(frac,0.002),1820],radius=20,fill=col)
def frames(sec): return int(round(sec*FPS))
# ---------- mascot (lip-synced to the voice) ----------
def mouth_at(t,spk="neuro"):
    for key,st in plays:
        if V[key].get("spk","neuro")!=spk: continue
        rel=t-st; a=V[key]["a"]
        if 0<=rel<len(a)/SR:
            i=int(rel*SR); seg=a[i:i+1470]
            return float(min(1,np.sqrt(np.mean(seg**2))*9)) if len(seg) else 0
    return 0
MOOD=["happy"]
CLONE=[False]
HAT=[True]
def brain(d,cx,cy,s,mood=None,arms=True,talk=True):
    mood=mood or MOOD[0]; t=T(); m=mouth_at(t) if talk else 0; u=100*s
    blink=(fn%96)<4 and mood not in("laugh",)
    lobes=[(-1.0,-0.25,0.85),(0,-0.75,0.95),(1.0,-0.25,0.85),(-0.65,0.45,0.85),(0.65,0.45,0.85),(0,0.15,1.0),(-0.5,-0.6,0.8),(0.5,-0.6,0.8)]
    cy=cy+math.sin(fn/6)*6*s+(math.sin(fn*1.3)*4*s if mood=="laugh" else 0)
    if arms:
        for sg in (-1,1):
            ang=(0.6+0.35*math.sin(fn/5+sg)) if mood!="surprised" else 1.3
            sx,sy=cx+sg*1.55*u,cy+0.25*u; ex,ey=sx+sg*math.cos(ang)*0.9*u,sy-math.sin(ang)*0.9*u
            d.line([sx,sy,ex,ey],fill=(200,60,110),width=max(3,int(14*s))); d.ellipse([ex-0.17*u,ey-0.17*u,ex+0.17*u,ey+0.17*u],fill=(255,255,255),outline=(200,60,110),width=max(2,int(5*s)))
            if HAT[0] and sg==1:
                d.line([ex,ey,ex+0.35*u,ey-0.45*u],fill=(90,55,25),width=max(3,int(12*s)))
                lx,ly=ex+0.55*u,ey-0.75*u; d.ellipse([lx-0.32*u,ly-0.32*u,lx+0.32*u,ly+0.32*u],fill=(190,230,255),outline=(70,70,80),width=max(2,int(8*s)))
    for x,y,r in lobes: d.ellipse([cx+(x-r-0.06)*u,cy+(y-r-0.06)*u,cx+(x+r+0.06)*u,cy+(y+r+0.06)*u],fill=(200,60,110))
    for x,y,r in lobes: d.ellipse([cx+(x-r)*u,cy+(y-r)*u,cx+(x+r)*u,cy+(y+r)*u],fill=(255,135,175))
    d.line([cx,cy-1.65*u,cx,cy-0.7*u],fill=(220,80,130),width=max(2,int(7*s)))
    for x,y in [(-1.1,-0.5),(1.1,-0.5),(-0.6,-1.1),(0.6,-1.1)]:
        d.arc([cx+(x-0.3)*u,cy+(y-0.2)*u,cx+(x+0.3)*u,cy+(y+0.2)*u],200,340,fill=(220,80,130),width=max(2,int(6*s)))
    if HAT[0]:
        d.ellipse([cx-1.25*u,cy-1.2*u,cx+1.25*u,cy-0.85*u],fill=(110,70,40),outline=(60,35,20),width=max(2,int(5*s)))
        d.chord([cx-0.95*u,cy-2.05*u,cx+0.95*u,cy-0.75*u],180,360,fill=(150,100,60),outline=(60,35,20),width=max(2,int(5*s)))
        for q in (-0.5,0,0.5): d.line([cx+q*u,cy-1.98*u,cx+q*u,cy-1.4*u],fill=(110,70,40),width=max(2,int(4*s)))
        d.line([cx-0.92*u,cy-1.65*u,cx+0.92*u,cy-1.65*u],fill=(110,70,40),width=max(2,int(4*s)))
        d.rectangle([cx-0.95*u,cy-1.48*u,cx+0.95*u,cy-1.36*u],fill=(60,35,20))
        d.ellipse([cx-0.12*u,cy-2.17*u,cx+0.12*u,cy-1.93*u],fill=(110,70,40))
    look=math.sin(fn/25)*0.06; lw=max(3,int(9*s))
    for ex in (-0.42,0.42):
        if mood=="laugh":
            d.arc([cx+(ex-0.22)*u,cy-0.12*u,cx+(ex+0.22)*u,cy+0.25*u],200,340,fill=(60,20,40),width=lw); continue
        h=0.04 if blink else (0.38 if mood=="surprised" else 0.3); wv=0.32 if mood=="surprised" else 0.27
        d.ellipse([cx+(ex-wv)*u,cy+(0.05-h)*u,cx+(ex+wv)*u,cy+(0.05+h)*u],fill=(255,255,255),outline=(60,20,40),width=max(2,int(5*s)))
        if not blink:
            pr=0.1 if mood=="surprised" else 0.13
            px=cx+(ex+look)*u; d.ellipse([px-pr*u,cy+(0.08-pr)*u,px+pr*u,cy+(0.08+pr)*u],fill=(170,60,255) if CLONE[0] else (30,20,40)); d.ellipse([px-0.04*u,cy-0.02*u,px+0.03*u,cy+0.05*u],fill=(255,255,255))
        if mood=="angry": d.line([cx+(ex-0.3*np.sign(ex))*u,cy-0.42*u,cx+(ex+0.25*np.sign(ex))*u,cy-0.22*u],fill=(60,20,40),width=max(3,int(10*s)))
        if mood=="surprised": d.arc([cx+(ex-0.25)*u,cy-0.65*u,cx+(ex+0.25)*u,cy-0.35*u],200,340,fill=(60,20,40),width=lw)
    if mood=="laugh":
        mh=0.3+0.15*m; d.chord([cx-0.38*u,cy+(0.45-mh/2)*u,cx+0.38*u,cy+(0.45+mh)*u],0,180,fill=(120,20,50),outline=(60,20,40),width=max(2,int(4*s)))
        d.ellipse([cx-0.17*u,cy+(0.45+mh*0.45)*u,cx+0.17*u,cy+(0.45+mh*0.95)*u],fill=(255,90,110))
    else:
        mh=(0.28 if mood=="surprised" else 0.06)+0.32*m; mw=0.18 if mood=="surprised" else 0.26
        d.ellipse([cx-mw*u,cy+(0.62-mh/2)*u,cx+mw*u,cy+(0.62+mh/2)*u],fill=(120,20,50),outline=(60,20,40),width=max(2,int(4*s)))
        if mh>0.2 and mood!="surprised": d.ellipse([cx-0.14*u,cy+(0.62+mh/2-0.12)*u,cx+0.14*u,cy+(0.62+mh/2-0.01)*u],fill=(255,90,110))
    for ex in (-0.78,0.78): d.ellipse([cx+(ex-0.13)*u,cy+0.35*u,cx+(ex+0.13)*u,cy+0.5*u],fill=(255,170,200))
# ---------- scene runner ----------
def scene(key,bgc,step,title,col,draw,extra=0.3,countdown=0,delay=0.1,capy=1560,minlen=0,host=True,mood=None):
    CAPY[0]=capy
    L=play(key,delay) if key else 0; st=V[key]["s"] if key else [0]
    base=fn; total=frames(max(minlen,L+delay+extra+countdown))
    for k in range(total):
        t=(fn-base)/FPS-delay
        ph=max([i for i,s_ in enumerate(st) if s_<=t],default=-1) if key else -1
        im,d=bg(*bgc); header(d,step,title,col); draw(k,t,ph,d)
        if host: brain(d,970,175,0.42,mood,arms=False); hearts(d)
        if countdown:
            tl=(total-k)/FPS
            if total-k==frames(countdown): sfx.append((T(),"roll",countdown))
            if tl<=countdown:
                timer(d,tl/countdown); ctext(d,1712,str(math.ceil(tl)),70,(255,255,255),5)
        emit(im)
def at(key,ph,delay=0.1): return T()+delay+V[key]["s"][ph]
def pill(d,y,txt,col,s=1.0,size=56):
    f=F(size*s); w=d.textlength(txt,font=f)
    d.rounded_rectangle([(W-w)/2-35*s,y-size*s*0.85,(W+w)/2+35*s,y+size*s*0.85],radius=int(size*s*0.85),fill=col)
    d.text(((W-w)/2,y-size*s*0.6),txt,font=f,fill=(255,255,255))
def check(d,x,y,s,c=(255,255,255)): d.line([(x-0.5*s,y),(x-0.15*s,y+0.35*s),(x+0.55*s,y-0.4*s)],fill=c,width=int(s*0.18),joint="curve")
def options(d,items,k,reveal=None,rk=0):
    for i,txt in enumerate(items):
        y=1060+i*150; s=pop(k-i*3,6,0.2)
        if s<=0: continue
        x0,x1=100+(1-s)*200,W-100-(1-s)*200
        if reveal is None: c=(40,40,70); oc=(255,255,255) if (k//8)%3!=i else (255,215,0)
        elif i==reveal: c=(40,190,90); oc=(255,255,255)
        else: c=(70,25,35); oc=(110,60,70)
        if reveal==i:
            g=10+6*math.sin(rk/2); d.rounded_rectangle([x0-g,y-60-g,x1+g,y+60+g],radius=70,outline=(150,255,170),width=6)
        d.rounded_rectangle([x0,y-60,x1,y+60],radius=60,fill=c,outline=oc,width=5)
        d.ellipse([x0+15,y-45,x0+105,y+45],fill=(255,215,0) if reveal is None or reveal==i else (110,60,70))
        L="ABC"[i]; tw=d.textlength(L,font=F(56)); d.text((x0+60-tw/2,y-34),L,font=F(56),fill=(30,20,40))
        d.text((x0+135,y-34),txt,font=F(58),fill=(255,255,255) if reveal is None or reveal==i else (150,110,120))
        if reveal==i: check(d,x1-70,y,70)
def intro_card(key,num,col,bgc,mood=None,sub=""):
    cut(col)
    def dr(k,t,ph,d):
        s=pop(k,6,0.4); ctext(d,560,num,230 if len(num)<3 else 150,(255,255,255),12,s*(1+0.03*math.sin(k/2)))
        if sub: ctext(d,760,sub,80,col,6,pop(k-4,6,0.4))
        brain(d,W/2,1180,1.5,mood)
    scene(key,bgc,-1,"",None,dr,extra=0.45,delay=0.05,capy=1560,host=False)
TH=lambda c:((int(c[0]*0.45),int(c[1]*0.45),int(c[2]*0.45)),(5,5,20))
def heart(d,cx,cy,r,c,outline=(255,255,255)):
    rr=r*.55
    d.ellipse([cx-r-3,cy-r*.75-3,cx-r+2*rr+3,cy-r*.75+2*rr+3],fill=outline); d.ellipse([cx+r-2*rr-3,cy-r*.75-3,cx+r+3,cy-r*.75+2*rr+3],fill=outline)
    d.polygon([(cx-r*1.0,cy-r*.05),(cx+r*1.0,cy-r*.05),(cx,cy+r*1.05)],fill=outline)
    d.ellipse([cx-r,cy-r*.75,cx-r+2*rr,cy-r*.75+2*rr],fill=c); d.ellipse([cx+r-2*rr,cy-r*.75,cx+r,cy-r*.75+2*rr],fill=c)
    d.polygon([(cx-r*.97,cy-r*.05),(cx+r*.97,cy-r*.05),(cx,cy+r)],fill=c)
SHOW_HEARTS=[True]
def hearts(d):
    if not SHOW_HEARTS[0]: return
    for i in range(3): heart(d,70+i*62,100,24*(1+0.08*math.sin(fn/5+i)),(235,40,70))
def lifepill(d,t0,t):
    s=pop(int((t-t0)*FPS),6,0.4)
    if s<=0: return
    txt="ERROU? PERDE 1 VIDA"; f=F(44*s); w=d.textlength(txt,font=f)+70*s
    x0=(W-w)/2; d.rounded_rectangle([x0-20,1730-40*s,x0+w+20,1730+40*s],radius=int(40*s),fill=(200,30,60))
    heart(d,x0+30*s,1728,20*s,(255,255,255),(200,30,60)); d.text((x0+65*s,1730-26*s),txt,font=f,fill=(255,255,255))
# ================= STANDARD NEURO INTRO =================
def neuro_intro():
    sfx.append((T(),"boom")); MOOD[0]="laugh"
    I=V["intro"]["s"]
    for i_ in range(3): sfx.append((T()+0.05+I[2]+0.25+i_*0.18,"coin"))
    def d_intro(k,t,ph,d):
        # logo
        s=pop(k,6,0.7)
        d.rounded_rectangle([W/2-420*s,190-70*s,W/2+420*s,190+70*s],radius=int(70*s),fill=(255,60,130),outline=(255,255,255),width=6)
        ctext(d,190,"DESAFIOS DO NEURO",64,(255,255,255),4,s)
        MOOD[0]="laugh" if ph<=0 else "happy"
        brain(d,W/2,720,2.0)
        if ph>=0: ctext(d,1060,"OI! EU SOU O NEURO",76,(255,215,0),6,pop(k-3,6,0.5))
        if ph>=1: ctext(d,1170,"VOU TESTAR SEU CÉREBRO",60,(255,255,255),5,pop(int((t-I[1])*FPS),6,0.5))
        if ph>=2:
            t2=t-I[2]
            for i in range(3):
                s2=pop(int((t2-0.25-i*0.18)*FPS),6,0.3)
                if s2>0: heart(d,W/2+(i-1)*150,1320,52*s2,(235,40,70))
        if ph>=3: pill(d,1450,"BORA?",(120,60,230),pop(int((t-I[3])*FPS),6,0.4)*(1+0.05*math.sin(k/3)),64)
    scene("intro",((70,20,130),(10,5,30)),-1,"",None,d_intro,extra=0.25,delay=0.05,capy=1580,host=False)
def episode_card(key,title,sub,col,icon):
    cut(col); MOOD[0]="happy"
    def dr(k,t,ph,d):
        ctext(d,420,"TEMA DE HOJE",70,(255,255,255),5,pop(k,6,0.6))
        icon(d,W/2,760,pop(k-3,6,0.3))
        if ph>=1:
            kk=int((t-V[key]["s"][1])*FPS)
            ctext(d,1060,title,120,col,8,pop(kk,6,0.4)*(1+0.03*math.sin(k/2))); ctext(d,1190,sub,110,(255,255,255),7,pop(kk-3,6,0.4))
    scene(key,((int(col[0]*.3),int(col[1]*.3),int(col[2]*.3)),(5,5,15)),-1,"",None,dr,extra=0.35,capy=1560,host=True)
def magnifier(d,cx,cy,s):
    if s<=0: return
    r=150*s; d.line([cx+r*0.6,cy+r*0.6,cx+r*1.5,cy+r*1.5],fill=(120,70,30),width=int(50*s)); d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(170,220,255),outline=(60,60,70),width=int(26*s))
    d.arc([cx-r*0.7,cy-r*0.7,cx+r*0.3,cy+r*0.3],190,260,fill=(255,255,255),width=int(14*s))
# ---------- episode 2 art ----------
def crown(d,x,y,s=1.0,c=(255,200,0)):
    d.polygon([(x-90*s,y+40*s),(x-90*s,y-40*s),(x-45*s,y),(x,y-60*s),(x+45*s,y),(x+90*s,y-40*s),(x+90*s,y+40*s)],fill=c,outline=(255,255,255),width=max(2,int(5*s)))
    for gx,gc in ((-45,(230,40,60)),(0,(60,140,255)),(45,(40,200,90))): d.ellipse([x+(gx-10)*s,y+(12)*s,x+(gx+10)*s,y+32*s],fill=gc)
def hat_icon(d,x,y,s=1.0): d.ellipse([x-70*s,y+10*s,x+70*s,y+40*s],fill=(90,60,40)); d.rounded_rectangle([x-40*s,y-45*s,x+40*s,y+25*s],radius=int(14*s),fill=(120,80,50))
def boot_icon(d,x,y,s=1.0,mud=False):
    d.polygon([(x-30*s,y-55*s),(x+10*s,y-55*s),(x+10*s,y+15*s),(x+55*s,y+25*s),(x+55*s,y+50*s),(x-30*s,y+50*s)],fill=(110,60,30),outline=(255,255,255))
    if mud: d.ellipse([x-30*s,y+30*s,x+20*s,y+55*s],fill=(70,120,40))
def shoe_icon(d,x,y,s=1.0): d.polygon([(x-40*s,y+5*s),(x+20*s,y+5*s),(x+50*s,y+25*s),(x+50*s,y+40*s),(x-40*s,y+40*s)],fill=(30,30,40),outline=(255,255,255))
def window_icon(d,x,y,s=1.0):
    d.rectangle([x-50*s,y-50*s,x+50*s,y+50*s],fill=(120,200,110),outline=(255,255,255),width=max(2,int(5*s))); d.ellipse([x-30*s,y-10*s,x+10*s,y+30*s],fill=(40,140,60))
CLUES=[("CHAPÉU",hat_icon),("BOTAS",boot_icon),("JARDIM",window_icon)]
def clueboard(d,n,y=310,newi=-1,kk=0):
    for i,(txt,ic) in enumerate(CLUES):
        x=W/2+(i-1)*325; on=i<n; s=pop(kk,6,0.3) if i==newi else 1
        d.rounded_rectangle([x-150*s,y-50*s,x+150*s,y+50*s],radius=int(40*s),fill=(40,150,90) if on else (55,50,75),outline=(255,255,255),width=4)
        if on:
            ic(d,x-90*s,y,0.45*s); d.text((x-50*s,y-24*s),txt,font=F(40*s),fill=(255,255,255))
        else:
            d.text((x-105,y-24),f"PISTA {i+1} ?",font=F(40),fill=(170,160,190))
SUS=[("DUQUE","salão"),("COZINHEIRA","cozinha"),("JARDINEIRO","jardim"),("GUARDA","salão")]
def face(d,x,y,kind,s=1.0):
    skin=[(240,200,170),(200,150,110),(170,120,85),(230,185,150)][kind]
    d.ellipse([x-70*s,y-70*s,x+70*s,y+70*s],fill=skin,outline=(60,40,30),width=max(2,int(4*s)))
    for ex in (-25,25): d.ellipse([x+(ex-9)*s,y-15*s,x+(ex+9)*s,y+5*s],fill=(30,20,20))
    d.arc([x-28*s,y+5*s,x+28*s,y+40*s],20,160,fill=(120,40,40),width=max(2,int(5*s)))
    if kind==0:  # duke: mustache + monocle, no hat, curly hair
        d.polygon([(x-40*s,y+18*s),(x,y+10*s),(x+40*s,y+18*s),(x,y+24*s)],fill=(80,50,30)); d.ellipse([x+12*s,y-28*s,x+40*s,y],outline=(255,215,0),width=max(2,int(4*s)))
        for hx in (-50,-20,10,40): d.ellipse([x+(hx-16)*s,y-82*s,x+(hx+16)*s,y-52*s],fill=(220,220,230))
    if kind==1:  # chef hat
        d.rectangle([x-50*s,y-90*s,x+50*s,y-55*s],fill=(255,255,255)); 
        for hx in (-35,0,35): d.ellipse([x+(hx-32)*s,y-150*s,x+(hx+32)*s,y-80*s],fill=(255,255,255))
    if kind==2:  # straw hat
        d.ellipse([x-110*s,y-75*s,x+110*s,y-45*s],fill=(230,190,80),outline=(150,110,40),width=max(2,int(4*s))); d.chord([x-55*s,y-125*s,x+55*s,y-40*s],180,360,fill=(240,200,90),outline=(150,110,40)); d.rectangle([x-55*s,y-70*s,x+55*s,y-58*s],fill=(200,50,50))
    if kind==3:  # guard helmet
        d.chord([x-75*s,y-115*s,x+75*s,y-5*s],180,360,fill=(60,80,160),outline=(255,255,255),width=max(2,int(4*s))); d.rectangle([x-85*s,y-62*s,x+85*s,y-50*s],fill=(40,50,110)); d.ellipse([x-12*s,y-110*s,x+12*s,y-86*s],fill=(255,215,0))
FEET=[True,False,True,True]  # boots?
def suspects(d,elim=(),guilty=None,k=0,y0=470):
    for i,(nm,loc) in enumerate(SUS):
        c_,r_=i%2,i//2; x=80+c_*480; y=y0+r_*360; w,h=440,330
        col=(50,45,75)
        if guilty==i: col=(40,160,80)
        d.rounded_rectangle([x,y,x+w,y+h],radius=30,fill=col,outline=(255,255,255),width=5)
        d.ellipse([x+12,y+12,x+72,y+72],fill=(255,215,0)); L="ABCD"[i]; tw=d.textlength(L,font=F(42)); d.text((x+42-tw/2,y+17),L,font=F(42),fill=(30,20,40))
        sz=40
        while d.textlength(nm,font=F(sz))>w-110: sz-=2
        tw=d.textlength(nm,font=F(sz)); d.text((x+85+(w-100)/2-tw/2,y+22),nm,font=F(sz),fill=(255,255,255))
        face(d,x+w/2,y+200,i,0.75)
        if FEET[i]: boot_icon(d,x+70,y+270,0.45)
        else: shoe_icon(d,x+70,y+270,0.7)
        tw=d.textlength(loc.upper(),font=F(32)); d.rounded_rectangle([x+w-tw-50,y+h-60,x+w-15,y+h-15],radius=20,fill=(255,255,255)); d.text((x+w-tw-32,y+h-54),loc.upper(),font=F(32),fill=(40,30,60))
        if i in elim:
            d.rounded_rectangle([x,y,x+w,y+h],radius=30,outline=(255,40,60),width=10)
            d.line([x+40,y+40,x+w-40,y+h-40],fill=(255,40,60),width=22); d.line([x+w-40,y+40,x+40,y+h-40],fill=(255,40,60),width=22)
        if guilty==i:
            g=10+6*math.sin(k/2); d.rounded_rectangle([x-g,y-g,x+w+g,y+h+g],radius=36,outline=(150,255,170),width=8)
def clue_scene(key,n):
    cut((40,170,90)); sfx.append((T()+0.1,"coin")); sfx.append((T()+0.1+V[key]["s"][1],"ding")); MOOD[0]="laugh"
    def dr(k,t,ph,d):
        ctext(d,470,"PISTA DESBLOQUEADA!",76,(255,215,0),6,pop(k,6,0.5))
        txt,ic=CLUES[n-1]; s=pop(k-4,6,0.3)
        r=170*s; d.ellipse([W/2-r,820-r,W/2+r,820+r],fill=(40,150,90),outline=(255,255,255),width=8); 
        if s>0: ic(d,W/2,820,1.4*s)
        if ph>=1: ctext(d,1070,txt,140,(255,255,255),8,pop(int((t-V[key]["s"][1])*FPS),6,0.4))
        clueboard(d,n,y=1290,newi=n-1,kk=int((t-V[key]["s"][1])*FPS) if ph>=1 else 0) if ph>=1 else clueboard(d,n-1,y=1290)
    scene(key,((15,70,40),(3,15,8)),-1,"",None,dr,extra=0.3,capy=1470,host=True)
# ================= EP4: O DOUTOR ESQUECIDO =================
HAT[0]=True
MEM=[0.0]
def membar(d,val,y=320,label="MEMÓRIA DO NEURO"):
    tw=d.textlength(label,font=F(40)); d.text(((W-tw)/2,y-75),label,font=F(40),fill=(255,255,255),stroke_width=3,stroke_fill=(0,0,0))
    d.rounded_rectangle([110,y-25,W-110,y+25],radius=25,fill=(40,30,60),outline=(255,255,255),width=4)
    if val>0.01: d.rounded_rectangle([110,y-25,110+(W-220)*val,y+25],radius=25,fill=(200,60,255) if val<0.99 else (60,220,120))
    tx=f"{int(round(val*100))}%"; tw=d.textlength(tx,font=F(36)); d.text(((W-tw)/2,y-20),tx,font=F(36),fill=(255,255,255),stroke_width=3,stroke_fill=(0,0,0))
def machine(d,x,y,s=1.0,broken=False,k=0):
    d.rounded_rectangle([x-150*s,y-90*s,x+150*s,y+90*s],radius=int(20*s),fill=(70,70,90),outline=(255,255,255),width=4)
    for i in range(3): c=(255,60,60) if (k//6+i)%3==0 else (80,80,100); d.ellipse([x+(-90+i*90-18)*s,y-55*s,x+(-90+i*90+18)*s,y-19*s],fill=c)
    d.polygon([(x+150*s,y-30*s),(x+230*s,y-50*s),(x+230*s,y+50*s),(x+150*s,y+30*s)],fill=(110,110,130),outline=(255,255,255))
    if broken:
        for i in range(8):
            a=random.random()*6.28; r=random.randint(40,160); d.line([x,y,x+r*math.cos(a),y+r*math.sin(a)],fill=(255,200,40),width=6)
        d.ellipse([x-60*s,y-120*s,x+60*s,y-40*s],fill=(90,90,100))
def zap(d,x0,y0,x1,y1,k):
    pts=[(x0,y0)]
    for i in range(1,8):
        t=i/8; pts.append((x0+(x1-x0)*t+random.randint(-25,25),y0+(y1-y0)*t+random.randint(-25,25)))
    pts.append((x1,y1)); d.line(pts,fill=(200,60,255),width=26); d.line(pts,fill=(255,255,255),width=8)
def mem_scene(key,v0,v1):
    cut((60,220,120)); MOOD[0]="laugh"; sfx.append((T()+0.1,"coin")); sfx.append((T()+0.5,"ding"))
    def dr(k,t,ph,d):
        v=v0+(v1-v0)*min(1,k/18); membar(d,v,y=420)
        brain(d,W/2,900,1.6)
        ctext(d,1250,f"+{int(round((v1-v0)*100))}%",150,(80,255,140),8,pop(k-6,6,0.4))
    scene(key,((15,70,40),(3,15,8)),-1,"",None,dr,extra=0.3,capy=1470,host=False)
CLONE=[False]
neuro_intro()
episode_card("tema","O DOUTOR","ESQUECIDO",(200,60,255),lambda d,x,y,s: doctor(d,x,y-60,0.9*s) if s>0.05 else None)
# --- villain reveal + zap ---
cut((200,60,255)); SHOW_HEARTS[0]=False; FX["glitch"]=8; sfx.append((T(),"glitch")); sfx.append((T()+0.05,"boom"))
D1=V["d1"]["s"]
def d_d1(k,t,ph,d):
    if (k//5)%7==0: d.rectangle([0,0,W,H],fill=(30,0,45))
    doctor(d,W/2,620,1.6)
    machine(d,W/2-120,1180,1.0,k=k)
    pill(d,250,"DOUTOR ESQUECIDO",(150,40,200),pop(k,6,0.4),56)
    if ph>=2:
        brain(d,880,1500,0.6,"surprised")
        if (k//2)%2==0: zap(d,W/2-120+230,1180,880,1450,k)
scene("d1",((25,0,40),(0,0,0)),-1,"",None,d_d1,extra=0.2,capy=1640,host=False)
FX["glitch"]=10; sfx.append((T(),"glitch"))
N1=V["n1"]["s"]
def d_n1(k,t,ph,d):
    v=max(0.1,1-k/20) if ph<1 else 0.1
    membar(d,v,y=330); MOOD[0]="surprised"
    brain(d,W/2+random.randint(-6,6)*(ph<1),850,1.7)
    if ph>=0 and ph<1: ctext(d,1220,"SOCORRO!",130,(255,60,80),8,pop(k,6,0.5))
    if ph>=2: pill(d,1240,"ACERTE = MEMÓRIA VOLTA",(40,170,90),pop(int((t-N1[2])*FPS),6,0.4),52)
scene("n1",((40,10,60),(5,2,10)),-1,"",None,d_n1,extra=0.3,capy=1450,host=False)
SHOW_HEARTS[0]=True; MEM[0]=0.1
# --- 1: Simon colors ---
cut((255,80,80)); MOOD[0]="happy"; C1=(255,80,80)
PADC=[(230,50,60),(50,110,240),(40,190,90),(250,200,30)]; PADF=[392,330,262,523]
SEQ1=[0,1,2,0,3]
def pads(d,lit=-1,y0=650):
    for i,c in enumerate(PADC):
        x=W/2+(-1 if i%2==0 else 1)*135; y=y0+(-1 if i<2 else 1)*135; on=i==lit
        cc=tuple(min(255,int(v*1.0+120)) for v in c) if on else tuple(int(v*0.45) for v in c)
        r=120 if not on else 128
        d.rounded_rectangle([x-r,y-r,x+r,y+r],radius=40,fill=cc,outline=(255,255,255) if on else (90,90,110),width=10 if on else 4)
def d_q1a(k,t,ph,d): ctext(d,330,"MEMORIZE AS CORES!",76,(255,215,0),6,pop(k,6,0.6)); pads(d)
scene("q1a",TH(C1),0,"SEQUÊNCIA",C1,d_q1a,extra=0.3,capy=1560)
STEP=0.55
for j,p in enumerate(SEQ1): sfx.append((T()+j*STEP+0.1,"tone",PADF[p]))
for k in range(int((len(SEQ1)*STEP+0.4)*FPS)):
    im,d=bg(*TH(C1)); header(d,0,"SEQUÊNCIA",C1); brain(d,970,175,0.42,arms=False); hearts(d)
    j=int((k/FPS-0.1)/STEP); lit=SEQ1[j] if 0<=j<len(SEQ1) and ((k/FPS-0.1)%STEP)<STEP*0.75 else -1
    ctext(d,330,f"{min(len(SEQ1),max(0,j+1))}/5",90,(255,255,255),6); pads(d,lit); emit(im)
def dots(d,x,y,seq,s=1.0):
    for i,c in enumerate(seq): d.ellipse([x+i*62*s-24*s,y-24*s,x+i*62*s+24*s,y+24*s],fill=PADC[c],outline=(255,255,255),width=3)
OPT1=[[0,2,1,0,3],[0,1,2,3,0],[0,1,2,0,3]]
def coptions(d,items,k,reveal=None,rk=0):
    options(d,["","",""],k,reveal,rk)
    for i,sq in enumerate(items):
        if pop(k-i*3,6,0.2)>=0.95 or reveal is not None: dots(d,330,1060+i*150,sq)
def d_q1b(k,t,ph,d): ctext(d,330,"QUAL FOI A ORDEM?",80,(255,215,0),6,pop(k,6,0.6)); pads(d); coptions(d,OPT1,k)
scene("q1b",TH(C1),0,"SEQUÊNCIA",C1,d_q1b,countdown=3.5)
sfx.append((T(),"crash")); FX["shake"]=6; MOOD[0]="laugh"
def d_r1(k,t,ph,d):
    ctext(d,330,"É A C!",110,(80,255,140),7,pop(k,6,0.5))
    j=int(k/(0.35*FPS)); pads(d,SEQ1[j] if j<5 else -1); coptions(d,OPT1,99,reveal=2,rk=k); lifepill(d,V["r1"]["s"][1]+0.4,t)
scene("r1",TH(C1),0,"SEQUÊNCIA",C1,d_r1,extra=0.4)
mem_scene("m1",0.1,0.4)
# --- 2: digits ---
cut((40,160,255)); MOOD[0]="happy"; C2=(40,160,255); DIG=["7","3","9","1","5"]
def d_q2a(k,t,ph,d): ctext(d,330,"PRESTA ATENÇÃO!",86,(255,215,0),6,pop(k,6,0.6)); brain(d,W/2,850,1.3,"surprised")
scene("q2a",TH(C2),1,"NÚMEROS",C2,d_q2a,extra=0.2)
for j in range(5): sfx.append((T()+j*0.7+0.05,"tick"))
FX["glitch"]=0
for k in range(int(5*0.7*FPS)):
    im,d=bg(*TH(C2)); header(d,1,"NÚMEROS",C2); brain(d,970,175,0.42,arms=False); hearts(d)
    j=int(k/(0.7*FPS)); kk=k-int(j*0.7*FPS)
    if kk==int(0.35*FPS) and j==3: FX["glitch"]=5; sfx.append((T(),"glitch"))
    ctext(d,850,DIG[j],520,(255,255,255),16,pop(kk,4,0.5))
    for i in range(5): d.ellipse([W/2-140+i*70-14,1250-14,W/2-140+i*70+14,1250+14],fill=(255,215,0) if i<=j else (70,70,90))
    emit(im)
OPT2=["3","9","1"]
def d_q2b(k,t,ph,d): ctext(d,380,"QUAL ERA O",80,(255,255,255),6,pop(k,6,0.6)); ctext(d,520,"3º NÚMERO?",120,(255,215,0),8,pop(k-3,6,0.6)); options(d,OPT2,k-6 if k>6 else -1)
scene("q2b",TH(C2),1,"NÚMEROS",C2,d_q2b,countdown=3)
sfx.append((T(),"crash")); FX["shake"]=6; MOOD[0]="laugh"
def d_r2(k,t,ph,d):
    ctext(d,380,"NOVE!",140,(80,255,140),8,pop(k,6,0.5))
    for i,dg in enumerate(DIG):
        x=W/2-280+i*140; c=(40,190,90) if i==2 else (50,60,110)
        d.rounded_rectangle([x-55,640,x+55,780],radius=20,fill=c,outline=(255,255,255),width=4); tw=d.textlength(dg,font=F(90)); d.text((x-tw/2,660),dg,font=F(90),fill=(255,255,255))
    options(d,OPT2,99,reveal=1,rk=k); lifepill(d,V["r2"]["s"][1]+0.4,t)
scene("r2",TH(C2),1,"NÚMEROS",C2,d_r2,extra=0.4)
mem_scene("m2",0.4,0.7)
# --- 3: real Neuro among clones ---
cut((255,140,0)); MOOD[0]="happy"; C3=(255,140,0); REAL=4
def clones(d,k,reveal=False):
    for i in range(6):
        x=230+(i%3)*310; y=600+(i//3)*370
        if reveal and i!=REAL and k>8: continue
        CLONE[0]=(i!=REAL); brain(d,x,y,0.72,"happy",arms=False,talk=False); CLONE[0]=False
        d.ellipse([x-150,y-180,x-90,y-120],fill=(255,215,0),outline=(0,0,0),width=3); L="ABCDEF"[i]; tw=d.textlength(L,font=F(40)); d.text((x-120-tw/2,y-174),L,font=F(40),fill=(0,0,0))
        if reveal and i==REAL: R=200+8*math.sin(k/2); d.ellipse([x-R,y-R,x+R,y+R],outline=(80,255,140),width=12)
def d_q3(k,t,ph,d):
    ctext(d,330,"QUAL É O VERDADEIRO?",72,(255,215,0),6,pop(k,6,0.6)); clones(d,k)
scene("q3",TH(C3),2,"CLONES",C3,d_q3,countdown=4,capy=1440)
sfx.append((T(),"crash")); FX["glitch"]=6; sfx.append((T(),"glitch")); MOOD[0]="laugh"
def d_r3(k,t,ph,d):
    ctext(d,330,"O VERDADEIRO É O E!",72,(80,255,140),6,pop(k,6,0.5)); clones(d,k,True)
    if ph>=1: pill(d,1300,"CLONES TÊM OLHOS ROXOS",(150,40,200),pop(int((t-V["r3"]["s"][1])*FPS),6,0.4),46)
    lifepill(d,V["r3"]["s"][1]+0.5,t)
scene("r3",TH(C3),2,"CLONES",C3,d_r3,extra=0.4,capy=1440)
mem_scene("m3",0.7,0.9)
# --- boss: doctor's riddle ---
BOSS_T=T(); CB=(200,60,255); MOOD[0]="angry"; FX["shake"]=10; sfx.append((T()+0.05,"boom"))
intro_card("ib","CHEFÃO",CB,((50,0,70),(5,0,10)),sub="FINAL")
OPT4=["Um buraco","Uma sombra","A idade"]
def d_d2(k,t,ph,d):
    doctor(d,W/2,560,1.05); machine(d,820,880,0.6,k=k)
    if ph>=1: options(d,OPT4,int((t-V["d2"]["s"][1])*FPS)-6)
scene("d2",((50,0,70),(5,0,10)),3,"ENIGMA DO DOUTOR",CB,d_d2,countdown=3.5,capy=1560)
sfx.append((T(),"crash")); FX["shake"]=8; MOOD[0]="laugh"
def d_rb(k,t,ph,d):
    doctor(d,W/2,560,1.05); machine(d,820,880,0.6,k=k)
    options(d,OPT4,99,reveal=0,rk=k); ctext(d,300,"UM BURACO!",100,(80,255,140),7,pop(k,6,0.5)); lifepill(d,V["rb"]["s"][1]+0.4,t)
scene("rb",((50,0,70),(5,0,10)),3,"ENIGMA DO DOUTOR",CB,d_rb,extra=0.3)
FX["flash"]=5; sfx.append((T(),"boom")); sfx.append((T()+0.3,"glitch"))
def d_d3(k,t,ph,d):
    doctor(d,W/2+random.randint(-10,10),600,1.2); machine(d,W/2,1180,1.2,broken=True,k=k)
    if (k//3)%2==0: d.ellipse([W/2-200,1000,W/2+200,1350],outline=(255,200,40),width=10)
    ctext(d,1450,"BOOOM!",140,(255,200,40),9,pop(k,5,0.4))
scene("d3",((60,10,0),(10,0,0)),-1,"",None,d_d3,extra=0.4,capy=1640,host=False)
mem_scene("m4",0.9,1.0)
sfx.append((T()+0.2,"riser",2.2)); SHOW_HEARTS[0]=False
D4=V["d4"]["s"]
def d_d4(k,t,ph,d):
    sc=max(0.05,1-max(0,t-D4[1])/1.2) if ph>=1 else 1
    for i in range(6):
        r=(k*12+i*80)%500; d.ellipse([W/2-r,760-r*0.6,W/2+r,760+r*0.6],outline=(150,40,200),width=6)
    doctor(d,W/2,680,1.3*sc)
    if ph>=1: ctext(d,1350,"PRÓXIMO EPISÓDIO",64,(255,255,255),5,pop(int((t-D4[1])*FPS),6,0.5)); ctext(d,1460,"A BATALHA FINAL",96,(255,60,80),7,pop(int((t-D4[1])*FPS)-4,6,0.5))
scene("d4",((30,0,45),(0,0,0)),-1,"",None,d_d4,extra=0.9,capy=1640,host=False)
SHOW_HEARTS[0]=True
cut((120,60,230)); MOOD[0]="happy"
O=V["out"]["s"]
TIERS=[(1,"3","MEMÓRIA DE ELEFANTE",(255,170,0)),(2,"1-2","MEMÓRIA BOA",(40,170,90)),(3,"0","APAGADO PELO DOUTOR",(110,110,140))]
for p_,*_ in TIERS: sfx.append((at("out",p_)+0.7,"coin"))
def d_o(k,t,ph,d):
    ctext(d,300,"QUANTAS VIDAS",96,(255,215,0),7,pop(k,6,0.6)); ctext(d,410,"SOBRARAM?",96,(255,255,255),7,pop(k-3,6,0.6))
    for i,(p0,a,b,c) in enumerate(TIERS):
        if ph>=p0:
            s=pop(int((t-O[p0])*FPS),6,0.3); y=600+i*175
            d.rounded_rectangle([90,y-75*s,W-90,y+75*s],radius=40,fill=c)
            if s>0.6:
                for j in range(3): heart(d,165+j*62,y,22,(235,40,70) if j<(3 if a=="3" else (2 if a=="1-2" else 0)) else (70,70,90))
                sz=60
                while d.textlength(b,font=F(sz))>W-90-370-30: sz-=2
                d.text((370,y-sz*0.55),b,font=F(sz),fill=(255,255,255),stroke_width=3,stroke_fill=(0,0,0))
    MOOD[0]="laugh" if ph in (1,3) else "happy"
    brain(d,W/2,1290,0.95)
    if ph>=4: pill(d,1640,"SEGUE O NEURO",(255,40,90),1+0.05*math.sin(k/3),56)
scene("out",((60,10,90),(5,5,25)),-1,"",None,d_o,extra=0.8,capy=1470,host=False)
ff.stdin.close(); ff.wait()
TOT=fn/FPS; N=int(TOT*SR)+SR
# ---------- audio ----------
mus=np.zeros(N,np.float32); beat=60/128
kick=lambda L: np.sin(2*np.pi*np.cumsum(np.linspace(120,45,L))/SR)*np.exp(-np.arange(L)/SR*16)
hat=lambda L: rng.standard_normal(L)*np.exp(-np.arange(L)/SR*70)
snare=lambda L: (rng.standard_normal(L)*0.7+np.sin(2*np.pi*190*np.arange(L)/SR))*np.exp(-np.arange(L)/SR*22)
bassn=[55,55,65.4,49]; b=0
def put(arr,s,sig):
    e=min(len(arr),s+len(sig)); 
    if s<len(arr): arr[s:e]+=sig[:e-s]
while b*beat<TOT:
    s=int(b*beat*SR)
    put(mus,s,0.9*kick(int(.3*SR)))
    if b%2==1: put(mus,s,0.35*snare(int(.2*SR)))
    for h in ((0.25,0.5,0.75) if b*beat>BOSS_T else (0.5,0.75)): put(mus,int((b+h)*beat*SR),0.18*hat(int(.04*SR)))
    f=bassn[(b//4)%4]; Lb=int(beat*0.45*SR); tt=np.arange(Lb)/SR
    put(mus,s,0.35*np.tanh(2.5*np.sin(2*np.pi*f*tt))*np.exp(-tt*5)); put(mus,int((b+0.5)*beat*SR),0.3*np.tanh(2.5*np.sin(2*np.pi*f*2*tt))*np.exp(-tt*6))
    b+=1
vo=np.zeros(N,np.float32)
for k,st in plays: put(vo,int(st*SR),V[k]["a"])
env=np.convolve((np.abs(vo)>0.02).astype(np.float32),np.ones(int(0.25*SR))/int(0.25*SR),"same")
duck=1-0.65*np.clip(env*3,0,1)
fx=np.zeros(N,np.float32)
for e in sfx:
    st,kind=e[0],e[1]; s=int(st*SR)
    if kind=="tick": L=int(.06*SR); tt=np.arange(L)/SR; put(fx,s,0.35*np.sin(2*np.pi*1800*tt)*np.exp(-tt*80))
    elif kind=="ding": L=int(.8*SR); tt=np.arange(L)/SR; put(fx,s,0.3*(np.sin(2*np.pi*1320*tt)+0.5*np.sin(2*np.pi*1980*tt))*np.exp(-tt*5))
    elif kind=="buzz": L=int(.5*SR); tt=np.arange(L)/SR; put(fx,s,0.25*np.sign(np.sin(2*np.pi*110*tt))*np.exp(-tt*3))
    elif kind in("whoosh","swish"):
        L=int((.4 if kind=="whoosh" else .2)*SR); n_=np.convolve(rng.standard_normal(L),np.ones(10)/10,"same"); tt=np.arange(L)/L
        put(fx,s,(0.5 if kind=="whoosh" else 0.3)*n_*np.sin(np.pi*tt)**2)
    elif kind=="boom": L=int(.7*SR); tt=np.arange(L)/SR; put(fx,s,0.6*np.sin(2*np.pi*np.cumsum(np.linspace(90,30,L))/SR)*np.exp(-tt*5))
    elif kind=="coin":
        L=int(.35*SR); tt=np.arange(L)/SR; put(fx,s,0.22*np.sin(2*np.pi*np.where(tt<0.08,988,1319)*tt)*np.exp(-tt*6))
    elif kind=="roll":
        Lr=e[2]; tt=0.0
        while tt<Lr:
            put(fx,s+int(tt*SR),(0.10+0.25*tt/Lr)*snare(int(.08*SR))); tt+=0.11-0.07*tt/Lr
    elif kind=="crash":
        L=int(1.6*SR); tt=np.arange(L)/SR; n_=rng.standard_normal(L); n_=n_-np.convolve(n_,np.ones(6)/6,"same"); put(fx,s,0.45*n_*np.exp(-tt*2.2))
    elif kind=="tone":
        L=int(.42*SR); tt=np.arange(L)/SR; put(fx,s,0.3*np.sin(2*np.pi*e[2]*tt)*np.minimum(1,tt*60)*np.exp(-tt*3))
    elif kind=="glitch":
        L=int(.35*SR); n_=rng.standard_normal(L)*(np.sign(np.sin(2*np.pi*23*np.arange(L)/SR))>0); put(fx,s,0.25*n_*np.exp(-np.arange(L)/SR*4))
    elif kind=="riser":
        L=int(e[2]*SR); tt=np.arange(L)/SR; put(fx,s,0.12*np.sin(2*np.pi*np.cumsum(np.linspace(200,1200,L))/SR)*(tt/e[2]))
mix=np.tanh((0.14*mus*duck+1.1*vo+fx)*1.1)*0.92
with wave.open("ep04a.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix[:int(TOT*SR)]*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-i","ep04v.mp4","-i","ep04a.wav","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","neuro_ep04_doutor.mp4"],check=True,stderr=subprocess.DEVNULL)
print("total",round(TOT,1))
