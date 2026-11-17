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
def say(parts,gap=0.12):
    global CLIP
    aud=[]; words=[]; starts=[]; t=0.0
    for txt,k in parts:
        r,p=STY[k]; mp=f"e1_{CLIP}.mp3"; CLIP+=1
        subprocess.run(["python3","tts2.py",VOICE,txt,mp,r,p],check=True)
        a=dec(mp); wb=json.load(open(mp+".json"))
        s0=max(0,wb[0][1]-0.04); s1=min(len(a)/SR,wb[-1][1]+wb[-1][2]+0.08)
        seg=a[int(s0*SR):int(s1*SR)]
        starts.append(t)
        for w,o,du in wb: words.append((w,t+o-s0,t+o-s0+du,len(starts)))
        aud+=[seg,np.zeros(int(gap*SR),np.float32)]; t+=len(seg)/SR+gap
    return {"a":np.concatenate(aud),"w":words,"s":starts,"d":t}
random.seed(7)
BOSS_T=1e9
V={}
# --- standard Neuro intro (used at the start of every episode) ---
V["intro"]=say([("Oi! Eu sou o Neuro!","x"),("E hoje eu vou testar o seu cérebro!","x"),("Você tem três vidas.","n"),("Bora?","q")])
V["tema"]=say([("Tema de hoje:","n"),("teste de detetive!","x")])
V["i1"]=say([("Desafio um!","x")]); V["i2"]=say([("Desafio dois!","x")]); V["i3"]=say([("Desafio três!","x")]); V["ib"]=say([("Chefão final!","x")])
V["q1"]=say([("Qual é a sombra certa do Neuro?","q")])
V["r1"]=say([("É a B!","x"),("A A tem um bracinho a menos, e a C tem um calombo na cabeça!","n")])
V["q2"]=say([("Quantos Neuros tem nessa tela?","q"),("Conta direitinho!","x")])
V["r2"]=say([("Onze!","x"),("Achou o escondidinho?","q")])
V["q3"]=say([("Ache os três erros entre as duas imagens!","x")])
V["r3"]=say([("A janela,","n"),("a maçã,","n"),("e a florzinha!","x")])
V["q4"]=say([("O bolo da festa sumiu num domingo de manhã.","n"),("A Ana disse que estava lendo.","n"),("O Beto, fazendo café.","n"),("E a Carla, pegando as cartas no correio.","n"),("Quem mentiu?","q")])
V["r4"]=say([("A Carla!","x"),("Domingo não tem entrega de cartas!","x")])
V["out"]=say([("Quantas vidas sobraram?","q"),("Três? Detetive lendário!","q"),("Uma ou duas? Bom detetive!","q"),("Nenhuma? Você é o suspeito!","q"),("Comenta aí, e segue o Neuro pro próximo desafio!","x")])
# ---------- render engine ----------
ff=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-pix_fmt","yuv420p","-c:v","libx264","-preset","fast","-crf","20","e1v.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
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
def mouth_at(t):
    for key,st in plays:
        rel=t-st; a=V[key]["a"]
        if 0<=rel<len(a)/SR:
            i=int(rel*SR); seg=a[i:i+1470]
            return float(min(1,np.sqrt(np.mean(seg**2))*9)) if len(seg) else 0
    return 0
MOOD=["happy"]
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
    for x,y,r in lobes: d.ellipse([cx+(x-r-0.06)*u,cy+(y-r-0.06)*u,cx+(x+r+0.06)*u,cy+(y+r+0.06)*u],fill=(200,60,110))
    for x,y,r in lobes: d.ellipse([cx+(x-r)*u,cy+(y-r)*u,cx+(x+r)*u,cy+(y+r)*u],fill=(255,135,175))
    d.line([cx,cy-1.65*u,cx,cy-0.7*u],fill=(220,80,130),width=max(2,int(7*s)))
    for x,y in [(-1.1,-0.5),(1.1,-0.5),(-0.6,-1.1),(0.6,-1.1)]:
        d.arc([cx+(x-0.3)*u,cy+(y-0.2)*u,cx+(x+0.3)*u,cy+(y+0.2)*u],200,340,fill=(220,80,130),width=max(2,int(6*s)))
    look=math.sin(fn/25)*0.06; lw=max(3,int(9*s))
    for ex in (-0.42,0.42):
        if mood=="laugh":
            d.arc([cx+(ex-0.22)*u,cy-0.12*u,cx+(ex+0.22)*u,cy+0.25*u],200,340,fill=(60,20,40),width=lw); continue
        h=0.04 if blink else (0.38 if mood=="surprised" else 0.3); wv=0.32 if mood=="surprised" else 0.27
        d.ellipse([cx+(ex-wv)*u,cy+(0.05-h)*u,cx+(ex+wv)*u,cy+(0.05+h)*u],fill=(255,255,255),outline=(60,20,40),width=max(2,int(5*s)))
        if not blink:
            pr=0.1 if mood=="surprised" else 0.13
            px=cx+(ex+look)*u; d.ellipse([px-pr*u,cy+(0.08-pr)*u,px+pr*u,cy+(0.08+pr)*u],fill=(30,20,40)); d.ellipse([px-0.04*u,cy-0.02*u,px+0.03*u,cy+0.05*u],fill=(255,255,255))
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
def hearts(d):
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
neuro_intro()
episode_card("tema","TESTE DE","DETETIVE",(255,180,0),magnifier)
# ================= 1 SHADOW =================
def sil(kind):
    global fn
    fsave=fn; fn=0
    im=Image.new("RGBA",(900,600),(0,0,0,0)); dd=ImageDraw.Draw(im)
    brain(dd,450,330,1.45,"happy",arms=(kind!="noarm"),talk=False)
    if kind=="noarm":
        u=145; sx,sy=450+1.55*u,330+0.25*u; ang=0.6+0.35*math.sin(1); ex,ey=sx+math.cos(ang)*0.9*u,sy-math.sin(ang)*0.9*u
        dd.line([sx,sy,ex,ey],fill=(0,0,0),width=20); dd.ellipse([ex-0.17*u,ey-0.17*u,ex+0.17*u,ey+0.17*u],fill=(0,0,0))
    if kind=="lump": dd.ellipse([260,70,400,190],fill=(0,0,0))
    fn=fsave
    a=im.split()[3]; out=Image.new("RGBA",im.size,(25,20,45,0)); out.putalpha(a); solid=Image.new("RGBA",im.size,(25,20,45,255)); solid.putalpha(a)
    return solid
SILS=[sil("noarm"),sil("ok"),sil("lump")]
SILS_S=[x.resize((300,200),Image.LANCZOS) for x in SILS]
C1=(120,90,255); intro_card("i1","DESAFIO 1",C1,TH(C1),sub="SOMBRA")
OPT1=["Sombra A","Sombra B","Sombra C"]
def shadows(im,d,reveal=None,k=0):
    for i,sp in enumerate(SILS_S):
        x=60+i*330; y=720
        c=(235,235,245) if reveal is None else ((150,255,170) if i==reveal else (120,90,100))
        d.rounded_rectangle([x,y,x+300,y+260],radius=26,fill=c,outline=(255,255,255),width=5)
        im.paste(sp,(x,y+40),sp)
        d.ellipse([x+10,y+10,x+70,y+70],fill=(255,215,0)); L="ABC"[i]; tw=d.textlength(L,font=F(40)); d.text((x+40-tw/2,y+16),L,font=F(40),fill=(30,20,40))
CUR=[None]
def d_q1(k,t,ph,d):
    ctext(d,330,"QUAL É A SOMBRA CERTA?",64,(255,215,0),6,pop(k,6,0.6))
    brain(d,W/2,540,0.75,"happy",talk=False); shadows(CUR[0],d); options(d,OPT1,k-10 if k>10 else -1)
def scene_im(key,bgc,step,title,col,draw,**kw):
    def wrap(k,t,ph,d): draw(k,t,ph,d)
    scene(key,bgc,step,title,col,wrap,**kw)
# give draw access to the image (needed to paste silhouettes)
_old_bg=bg
def bg(c1,c2):
    im,d=_old_bg(c1,c2); CUR[0]=im; return im,d
scene("q1",TH(C1),0,"SOMBRA",C1,d_q1,countdown=3)
sfx.append((T(),"crash")); FX["shake"]=6; MOOD[0]="laugh"
def d_r1(k,t,ph,d):
    ctext(d,330,"É A B!",110,(80,255,140),7,pop(k,6,0.5))
    brain(d,W/2,540,0.75,"happy",talk=False); shadows(CUR[0],d,reveal=1,k=k)
    if ph>=1:
        for x,y in ((60+42,720+40+80),(720+110,720+40+43)):
            R=50+6*math.sin(k/2); d.ellipse([x-R,y-R,x+R,y+R],outline=(255,40,60),width=8)
    options(d,OPT1,99,reveal=1,rk=k); lifepill(d,V["r1"]["s"][1]+0.4,t)
scene("r1",TH(C1),0,"SOMBRA",C1,d_r1,extra=0.4)
# ================= 2 COUNT NEUROS =================
C2=(255,90,150); MOOD[0]="surprised"; intro_card("i2","DESAFIO 2",C2,TH(C2),sub="CONTAGEM")
NEU=[(170,460,0.42,"happy"),(420,405,0.5,"laugh"),(720,435,0.38,"surprised"),(930,480,0.3,"happy"),(300,620,0.55,"angry"),(560,650,0.4,"happy"),
     (820,660,0.52,"laugh"),(150,830,0.36,"surprised"),(450,860,0.5,"happy"),(700,890,0.42,"angry"),(985,915,0.16,"happy")]
def neuros(d,k,num=0):
    for i,(x,y,s,m) in enumerate(NEU): brain(d,x,y+math.sin(k/5+i)*4,s*0.9,m,arms=False,talk=False)
    for i in range(min(num,len(NEU))):
        x,y,_,_=NEU[i]; d.ellipse([x-34,y-34,x+34,y+34],fill=(255,215,0),outline=(0,0,0),width=4)
        tw=d.textlength(str(i+1),font=F(40)); d.text((x-tw/2,y-24),str(i+1),font=F(40),fill=(0,0,0))
OPT2=["9","11","12"]
def d_q2(k,t,ph,d):
    ctext(d,290,"QUANTOS NEUROS?",76,(255,215,0),6,pop(k,6,0.6)); neuros(d,k); options(d,OPT2,k-10 if k>10 else -1)
MOOD[0]="happy"
scene("q2",TH(C2),1,"CONTAGEM",C2,d_q2,countdown=4)
sfx.append((T(),"crash")); MOOD[0]="laugh"
for i in range(11): sfx.append((T()+0.15+i*0.12,"tick"))
def d_r2(k,t,ph,d):
    n=int(k/(0.12*FPS))+1
    ctext(d,300,"ONZE!" if n>=11 else str(min(n,11)),110,(80,255,140) if n>=11 else (255,255,255),7,pop(k,6,0.5)); neuros(d,k,n)
    if ph>=1:
        x,y=NEU[-1][0],NEU[-1][1]; R=55+6*math.sin(k/2); d.ellipse([x-R,y-R,x+R,y+R],outline=(255,40,60),width=8)
    options(d,OPT2,99,reveal=1,rk=k); lifepill(d,V["r2"]["s"][1]+0.4,t)
scene("r2",TH(C2),1,"CONTAGEM",C2,d_r2,extra=0.5,minlen=2.4)
# ================= 3 SPOT THE DIFFERENCE =================
C3=(40,180,120); MOOD[0]="happy"; intro_card("i3","DESAFIO 3",C3,TH(C3),sub="3 ERROS")
def landscape(d,ox,oy,alt=False):
    w,h=900,400
    d.rounded_rectangle([ox,oy,ox+w,oy+h],radius=24,fill=(150,210,255),outline=(255,255,255),width=5)
    d.rectangle([ox+5,oy+300,ox+w-5,oy+h-5],fill=(90,190,90))
    sx,sy=ox+110,oy+90; d.ellipse([sx-45,sy-45,sx+45,sy+45],fill=(255,215,0))
    for i in range(8): a=i*math.pi/4; d.line([sx+60*math.cos(a),sy+60*math.sin(a),sx+85*math.cos(a),sy+85*math.sin(a)],fill=(255,215,0),width=7)
    for cx in (ox+330,ox+380,ox+430): d.ellipse([cx-45,oy+50,cx+45,oy+120],fill=(255,255,255))
    hx,hy=ox+470,oy+170; d.rectangle([hx,hy,hx+230,hy+170],fill=(240,200,150),outline=(120,70,40),width=4)
    d.polygon([(hx-25,hy),(hx+115,hy-90),(hx+255,hy)],fill=(200,60,50)); d.rectangle([hx+90,hy+80,hx+140,hy+170],fill=(130,80,40))
    d.rectangle([hx+20,hy+30,hx+70,hy+80],fill=(170,220,255),outline=(255,255,255),width=4)
    if not alt: d.rectangle([hx+160,hy+30,hx+210,hy+80],fill=(170,220,255),outline=(255,255,255),width=4)
    tx,ty=ox+800,oy+200; d.rectangle([tx-14,ty,tx+14,ty+130],fill=(120,70,30)); d.ellipse([tx-75,ty-110,tx+75,ty+30],fill=(40,140,60))
    for j,(ax,ay) in enumerate([(-35,-50),(25,-70),(10,-10)]):
        if alt and j==1: continue
        d.ellipse([tx+ax-14,ty+ay-14,tx+ax+14,ty+ay+14],fill=(230,40,50))
    for j,fx_ in enumerate([ox+90,ox+170,ox+250]):
        if alt and j==2: continue
        fy=oy+350; d.line([fx_,fy,fx_,fy+30],fill=(30,110,40),width=5)
        for a in range(5): ang=a*2*math.pi/5; d.ellipse([fx_+16*math.cos(ang)-10,fy+16*math.sin(ang)-10,fx_+16*math.cos(ang)+10,fy+16*math.sin(ang)+10],fill=(255,120,200))
        d.ellipse([fx_-8,fy-8,fx_+8,fy+8],fill=(255,230,0))
DIFFS=[(90+470+185,760+170+55),(90+800+25,760+200-70),(90+250,760+350)]
def d_q3(k,t,ph,d):
    landscape(d,90,330); landscape(d,90,760,alt=True)
    ctext(d,1220,"ACHE OS 3 ERROS",72,(255,215,0),6,pop(k,6,0.6))
scene("q3",TH(C3),2,"3 ERROS",C3,d_q3,countdown=5,capy=1330)
sfx.append((T(),"crash")); MOOD[0]="laugh"
R3=V["r3"]["s"]
for j in range(3): sfx.append((T()+0.1+R3[j],"ding"))
def d_r3(k,t,ph,d):
    landscape(d,90,330); landscape(d,90,760,alt=True)
    for j in range(3):
        if ph>=j:
            x,y=DIFFS[j]; s=pop(int((t-R3[j])*FPS),5,0.3); R=60*s+5*math.sin(k/2)
            d.ellipse([x-R,y-R,x+R,y+R],outline=(255,40,60),width=10)
            d.ellipse([x+R*0.6,y-R-20,x+R*0.6+50,y-R+30],fill=(255,40,60)); d.text((x+R*0.6+16,y-R-16),str(j+1),font=F(38),fill=(255,255,255))
    ctext(d,1220,f"{max(0,ph+1)}/3",90,(80,255,140),6)
    lifepill(d,R3[2]+0.5,t)
scene("r3",TH(C3),2,"3 ERROS",C3,d_r3,extra=0.6,capy=1330)
# ================= BOSS: WHO LIED =================
BOSS_T=T(); CB=(230,30,50); MOOD[0]="angry"
FX["shake"]=10; sfx.append((T()+0.05,"boom"))
intro_card("ib","CHEFÃO",CB,((90,0,10),(10,0,0)),sub="FINAL")
def cake(d,x,y,s=1):
    d.rectangle([x-70*s,y-20*s,x+70*s,y+50*s],fill=(240,180,200),outline=(255,255,255),width=4); d.rectangle([x-70*s,y-35*s,x+70*s,y-15*s],fill=(255,255,255))
    d.rectangle([x-5*s,y-75*s,x+5*s,y-35*s],fill=(120,180,255)); d.ellipse([x-9*s,y-95*s,x+9*s,y-72*s],fill=(255,180,0))
def ico(d,kind,x,y):
    if kind=="book": d.rectangle([x-40,y-30,x+40,y+30],fill=(60,120,230),outline=(255,255,255),width=4); d.line([x,y-30,x,y+30],fill=(255,255,255),width=4)
    if kind=="cup": d.rounded_rectangle([x-32,y-25,x+28,y+35],radius=10,fill=(255,255,255)); d.arc([x+15,y-12,x+45,y+18],270,90,fill=(255,255,255),width=8); d.ellipse([x-26,y-30,x+22,y-18],fill=(110,60,20))
    if kind=="mail": d.rectangle([x-42,y-28,x+42,y+28],fill=(255,240,200),outline=(255,255,255),width=4); d.line([x-42,y-28,x,y+5,x+42,y-28],fill=(200,120,60),width=5)
PEOPLE=[("ANA","LENDO UM LIVRO","book"),("BETO","FAZENDO CAFÉ","cup"),("CARLA","PEGANDO CARTAS","mail")]
def cards(d,t,ph,reveal=False,k=0):
    for i,(nm,act,ic) in enumerate(PEOPLE):
        if ph>=i+1 or reveal:
            s=1.0 if reveal else pop(int((t-V["q4"]["s"][i+1])*FPS),6,0.3); y=640+i*140
            c=(60,40,80) if not reveal else ((200,40,60) if i==2 else (60,40,80))
            d.rounded_rectangle([90+(1-s)*300,y-62,W-90-(1-s)*300,y+62],radius=30,fill=c,outline=(255,255,255),width=4)
            if s>0.6:
                ico(d,ic,170,y); d.text((240,y-48),nm,font=F(48),fill=(255,215,0)); d.text((240,y+4),act,font=F(40),fill=(255,255,255))
OPT4=["Ana","Beto","Carla"]
def d_q4(k,t,ph,d):
    cake(d,W/2,470,0.8); ctext(d,300,"O BOLO SUMIU!" if ph<4 else "QUEM MENTIU?",70,(255,215,0),6,pop(k,6,0.6))
    if ph<0 or ph==0: pass
    cards(d,t,ph)
    if ph>=4: options(d,OPT4,int((t-V["q4"]["s"][4])*FPS))
    ctext(d,375,"(DOMINGO DE MANHÃ)",40,(255,255,255),3)
scene("q4",((90,0,10),(10,0,0)),3,"QUEM MENTIU?",CB,d_q4,countdown=4,capy=1580)
sfx.append((T(),"crash")); FX["shake"]=10; MOOD[0]="laugh"
def d_r4(k,t,ph,d):
    cake(d,W/2,470,0.8); ctext(d,330,"FOI A CARLA!",100,(80,255,140),7,pop(k,6,0.5)); cards(d,t,9,reveal=True,k=k)
    options(d,OPT4,99,reveal=2,rk=k)
    if ph>=1:
        s=pop(int((t-V["r4"]["s"][1])*FPS),5,0.3)
        d.rounded_rectangle([W/2-440*s,900-70*s,W/2+440*s,900+70*s],radius=30,fill=(255,215,0),outline=(255,255,255),width=6)
        ctext(d,900,"DOMINGO NÃO TEM CORREIO!",50,(150,0,20),0,s); lifepill(d,V["r4"]["s"][1]+0.5,t)
scene("r4",((90,0,10),(10,0,0)),3,"QUEM MENTIU?",CB,d_r4,extra=0.6,capy=1580)
# ================= OUTRO =================
cut((120,60,230)); MOOD[0]="happy"
O=V["out"]["s"]
TIERS=[(1,"3","DETETIVE LENDÁRIO",(255,170,0)),(2,"1-2","BOM DETETIVE",(40,170,90)),(3,"0","VOCÊ É O SUSPEITO",(110,110,140))]
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
    brain(d,W/2,1250,1.0)
    if ph>=4: pill(d,1620,"SEGUE O NEURO",(255,40,90),1+0.05*math.sin(k/3),56)
scene("out",((60,10,90),(5,5,25)),-1,"",None,d_o,extra=0.8,capy=1450,host=False)
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
    elif kind=="riser":
        L=int(e[2]*SR); tt=np.arange(L)/SR; put(fx,s,0.12*np.sin(2*np.pi*np.cumsum(np.linspace(200,1200,L))/SR)*(tt/e[2]))
mix=np.tanh((0.14*mus*duck+1.1*vo+fx)*1.1)*0.92
with wave.open("e1a.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix[:int(TOT*SR)]*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-i","e1v.mp4","-i","e1a.wav","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","neuro_ep_detetive.mp4"],check=True,stderr=subprocess.DEVNULL)
print("total",round(TOT,1))
