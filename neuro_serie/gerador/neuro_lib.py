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
        r,p=STY[k] if isinstance(k,str) else k; mp=f"@@NAME@@_{CLIP}.mp3"; CLIP+=1
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
#@@VOICES
# ---------- render engine ----------
ff=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-pix_fmt","yuv420p","-c:v","libx264","-preset","fast","-crf","20","@@NAME@@v.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
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
def mouth_at(t,spk="neuro"):
    for key,st in plays:
        if V[key].get("spk","neuro")!=spk: continue
        rel=t-st; a=V[key]["a"]
        if 0<=rel<len(a)/SR:
            i=int(rel*SR); seg=a[i:i+1470]
            return float(min(1,np.sqrt(np.mean(seg**2))*9)) if len(seg) else 0
    return 0
MOOD=["happy"]
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
#@@SCENES
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
with wave.open("@@NAME@@a.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix[:int(TOT*SR)]*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-i","@@NAME@@v.mp4","-i","@@NAME@@a.wav","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","@@NAME@@.mp4"],check=True,stderr=subprocess.DEVNULL)
print("total",round(TOT,1))
