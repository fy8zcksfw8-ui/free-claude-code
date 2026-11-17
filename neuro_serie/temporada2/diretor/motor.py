"""Motor comum dos episodios da Temporada 2: vozes, legendas, boca, trilha, efeitos e linha do tempo (JSON) para o Remotion."""
import hashlib, json, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.join(HERE, "..", "estudio")
CACHE = os.path.join(HERE, "cache"); os.makedirs(CACHE, exist_ok=True)
SR, FPS = 44100, 30
NEURO, RIVAL = "neuro", "robo"   # a boca do rival usa a chave "robo"
ESTILO = {"x": ("+12%", "+6Hz"), "n": ("+8%", "+0Hz"), "q": ("-4%", "+12Hz"), "r": ("+6%", "+18Hz"),
          "rapido": ("+28%", "+14Hz"), "grave": ("-14%", "-30Hz"), "mistica": ("-6%", "-4Hz"), "mq": ("-8%", "+6Hz")}
rng = np.random.default_rng(7)

def fala(q, t, e="n"): return (q, t, e)

def dec(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def fx_robo(a):
    t = np.arange(len(a)) / SR; y = a * (0.62 + 0.38 * np.sin(2 * np.pi * 55 * t))
    d = int(0.0065 * SR); z = y.copy(); z[d:] += 0.55 * y[:-d]; q = np.round(z * 24) / 24
    return (0.7 * z + 0.3 * q) * 0.85

def fx_eco(a):
    a = np.concatenate([a, np.zeros(int(0.35 * SR), np.float32)]); e = a.copy()
    for dl, g in ((0.09, 0.3), (0.19, 0.16)): n = int(dl * SR); e[n:] += g * a[:-n]
    return e * 0.85

FX = {None: lambda a: a, "robo": fx_robo, "eco": fx_eco}

def tts(texto, voz, estilo, fx=None):
    r, p = ESTILO[estilo]
    key = hashlib.md5(f"{voz}|{texto}|{r}|{p}".encode()).hexdigest()[:16]
    mp = os.path.join(CACHE, key + ".mp3")
    if not os.path.exists(mp + ".json"):
        subprocess.run([sys.executable, os.path.join(HERE, "tts2.py"), voz, texto, mp, r, p], check=True)
    a = dec(mp); wb = json.load(open(mp + ".json"))
    s0 = max(0, wb[0][1] - 0.04); s1 = min(len(a) / SR, wb[-1][1] + wb[-1][2] + 0.1)
    seg = FX[fx](a[int(s0 * SR):int(s1 * SR)])
    return seg, [(w, o - s0, o - s0 + du) for w, o, du in wb]

def montar(nome, CENAS, VOZ, contagem=2.5, transicao=14, bpm=118, tom=0, gap=0.14):
    """VOZ: {quem: (voz_edge, efeito)}. Gera public/<nome>/mix.wav e src/data/<nome>.json"""
    clips, sfx = [], []
    timeline = {"fps": FPS, "transicao": transicao, "cenas": []}
    inicio = 0

    ev = {}
    def bloco(falas, t_local, acc):
        for q, txt, e in falas:
            if q == "pausa": t_local += float(txt); continue
            if q == "marca": ev[txt] = t_local; continue
            voz, fx = VOZ[q]; a, w = tts(txt, voz, e, fx)
            acc.append(dict(quem=q, texto=txt, ini=t_local, dur=len(a) / SR, palavras=[[x, round(s, 3), round(f, 3)] for x, s, f in w], _a=a))
            t_local += len(a) / SR + gap
        return t_local

    for i, c in enumerate(CENAS):
        pad = transicao / FPS + 0.06; cl = []; ev.clear()
        if c["tipo"] == "rodada":
            cont = c.get("contagem", contagem)
            t = bloco(c["pergunta"], pad, cl)
            ev["roboEm"] = t + 0.05
            t = bloco(c["roboFala"], t + 0.05, cl)
            ev["contaIni"] = t + 0.05; ev["contaFim"] = ev["contaIni"] + cont; ev["revelaEm"] = ev["contaFim"]
            t = bloco(c["revela"], ev["revelaEm"] + 0.3, cl)
            ev["pontoEm"] = ev["revelaEm"] + 0.8
            if c.get("depois"):
                ev["bugEm"] = t + 0.05; t = bloco(c["depois"], t + 0.1, cl)
            dur = max(t + c.get("cauda", 0.35), ev["pontoEm"] + 1.0)
        else:
            t = bloco(c["falas"], pad + c.get("atraso", 0), cl)
            ev["falas"] = [round(x["ini"], 3) for x in cl]
            dur = t + c.get("cauda", 0.3)
        dfr = int(round(dur * FPS))
        cena = {k: v for k, v in c.items() if k not in ("falas", "pergunta", "roboFala", "revela", "depois")}
        cena.update(inicio=inicio, duracao=dfr, eventos={k: (round(v, 3) if isinstance(v, float) else v) for k, v in ev.items()})
        cena["clipes"] = [{k: v for k, v in x.items() if k != "_a"} for x in cl]
        timeline["cenas"].append(cena)
        g = inicio / FPS
        for x in cl: clips.append((g + x["ini"], x["quem"], x["_a"]))
        if i > 0: sfx.append((g, "whoosh"))
        if c["tipo"] == "rodada":
            sfx.append((g + ev["roboEm"], "bip"))
            sfx.append((g + ev["contaIni"], "rufar", ev["contaFim"] - ev["contaIni"]))
            k = 0.0
            while k < ev["contaFim"] - ev["contaIni"] - 0.01: sfx.append((g + ev["contaIni"] + k, "tick")); k += 1.0
            sfx.append((g + ev["revelaEm"], "prato")); sfx.append((g + ev["revelaEm"] + 0.05, "ding"))
            if c["certa"] != c["robo"]: sfx.append((g + ev["revelaEm"] + 0.4, "erro"))
            sfx.append((g + ev["pontoEm"], "moeda"))
            if ev.get("bugEm"): sfx += [(g + ev["bugEm"], "glitch"), (g + ev["bugEm"] + 0.6, "glitch")]
        for s_ in c.get("sfx", []): sfx.append((g + s_[0], *s_[1:]))
        if c.get("boom"): sfx.append((g + 0.05, "boom"))
        inicio += dfr - (transicao if i < len(CENAS) - 1 else 0)

    TOTAL = inicio; timeline["total"] = TOTAL
    N = int(TOTAL / FPS * SR) + SR

    def put(arr, s, sig):
        s = int(s); e = min(len(arr), s + len(sig))
        if 0 <= s < len(arr): arr[s:e] += sig[:e - s]
    voz = np.zeros(N, np.float32); porq = {}
    for st, q, a in clips:
        put(voz, st * SR, a); porq.setdefault(q, np.zeros(N, np.float32)); put(porq[q], st * SR, a)
    hop = SR // FPS; timeline["boca"] = {}
    for q in sorted(set([NEURO, RIVAL]) | set(porq)):
        arr = porq.get(q, np.zeros(N, np.float32))
        v = np.array([np.sqrt(np.mean(arr[i * hop:(i + 1) * hop] ** 2)) for i in range(TOTAL)])
        v = np.convolve(np.clip(v * 7.5, 0, 1), [0.25, 0.5, 0.25], "same")
        timeline["boca"][q] = [round(float(x), 2) for x in v]

    beat = 60 / bpm; mus = np.zeros(N, np.float32)
    nota = lambda m: 440 * 2 ** ((m + tom - 69) / 12)
    acordes = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
    kick = lambda L: np.sin(2 * np.pi * np.cumsum(np.linspace(130, 45, L)) / SR) * np.exp(-np.arange(L) / SR * 14)
    snare = lambda L: (rng.standard_normal(L) * 0.8 + 0.4 * np.sin(2 * np.pi * 190 * np.arange(L) / SR)) * np.exp(-np.arange(L) / SR * 20)
    hat = lambda L: np.diff(np.concatenate([[0], rng.standard_normal(L)])) * np.exp(-np.arange(L) / SR * 80)
    b = 0
    while b * beat < TOTAL / FPS:
        s = int(b * beat * SR); ac = acordes[(b // 4) % 4]
        put(mus, s, 0.85 * kick(int(.3 * SR)))
        if b % 2 == 1: put(mus, s, 0.3 * snare(int(.22 * SR)))
        put(mus, s + int(0.5 * beat * SR), 0.12 * hat(int(.05 * SR))); put(mus, s + int(0.75 * beat * SR), 0.06 * hat(int(.03 * SR)))
        Lb = int(beat * 0.9 * SR); tt = np.arange(Lb) / SR
        put(mus, s, 0.22 * np.tanh(2 * np.sin(2 * np.pi * nota(ac[0] - 24) * tt)) * np.exp(-tt * 4))
        for k_ in range(2):
            m = ac[(b * 2 + k_) % 3] + 12; La = int(beat / 2 * SR); ta = np.arange(La) / SR
            put(mus, s + k_ * La, 0.07 * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * nota(m) * ta)) * np.exp(-ta * 9))
        if b % 4 == 0:
            Lp = int(beat * 4 * SR); tp = np.arange(Lp) / SR; env = np.minimum(1, tp / 0.4) * np.minimum(1, tp[::-1] / 0.5)
            put(mus, s, 0.035 * sum(np.sin(2 * np.pi * nota(m) * tp) + 0.3 * np.sin(2 * np.pi * nota(m) * 2.003 * tp) for m in ac) * env)
        b += 1
    env = np.convolve((np.abs(voz) > 0.015).astype(np.float32), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    duck = 1 - 0.62 * np.clip(env * 3, 0, 1)
    fx = np.zeros(N, np.float32)
    for e in sfx:
        st, k = e[0], e[1]; s = st * SR
        if k == "tick": L = int(.06 * SR); tt = np.arange(L) / SR; put(fx, s, 0.3 * np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt * 70))
        elif k == "bip": L = int(.25 * SR); tt = np.arange(L) / SR; put(fx, s, 0.16 * np.sign(np.sin(2 * np.pi * np.where(tt < .12, 880, 1320) * tt)) * np.exp(-tt * 6))
        elif k == "ding": L = int(.9 * SR); tt = np.arange(L) / SR; put(fx, s, 0.28 * (np.sin(2 * np.pi * 1318 * tt) + .5 * np.sin(2 * np.pi * 1976 * tt)) * np.exp(-tt * 4.5))
        elif k == "erro": L = int(.5 * SR); tt = np.arange(L) / SR; put(fx, s, 0.22 * np.sign(np.sin(2 * np.pi * 120 * tt)) * np.exp(-tt * 3.5))
        elif k == "moeda": L = int(.4 * SR); tt = np.arange(L) / SR; put(fx, s, 0.22 * np.sin(2 * np.pi * np.where(tt < .08, 988, 1319) * tt) * np.exp(-tt * 6))
        elif k == "whoosh": L = int(.4 * SR); n_ = np.convolve(rng.standard_normal(L), np.ones(9) / 9, "same"); put(fx, s, 0.4 * n_ * np.sin(np.pi * np.arange(L) / L) ** 2)
        elif k == "boom": L = int(.8 * SR); tt = np.arange(L) / SR; put(fx, s, 0.6 * np.sin(2 * np.pi * np.cumsum(np.linspace(95, 32, L)) / SR) * np.exp(-tt * 4.5))
        elif k == "prato": L = int(1.4 * SR); tt = np.arange(L) / SR; n_ = rng.standard_normal(L); n_ = n_ - np.convolve(n_, np.ones(5) / 5, "same"); put(fx, s, 0.3 * n_ * np.exp(-tt * 2.6))
        elif k == "glitch": L = int(.4 * SR); put(fx, s, 0.25 * rng.standard_normal(L) * (np.sign(np.sin(2 * np.pi * 21 * np.arange(L) / SR)) > 0) * np.exp(-np.arange(L) / SR * 4))
        elif k == "magia":
            L = int(1.0 * SR); tt = np.arange(L) / SR; put(fx, s, 0.12 * sum(np.sin(2 * np.pi * f0 * tt) * np.exp(-((tt - d0) * 9) ** 2) for f0, d0 in ((1568, .1), (2093, .25), (2637, .4), (3136, .55))))
        elif k == "riser": D = e[2]; L = int(D * SR); tt = np.arange(L) / SR; put(fx, s, 0.12 * np.sin(2 * np.pi * np.cumsum(np.linspace(200, 1400, L)) / SR) * (tt / D))
        elif k == "rufar":
            D = e[2]; tt = 0.0
            while tt < D: put(fx, s + tt * SR, (0.06 + 0.2 * tt / D) * snare(int(.07 * SR))); tt += 0.11 - 0.07 * tt / D
    mix = np.tanh((0.16 * mus * duck + 1.05 * voz + fx) * 1.05) * 0.9
    mix = mix[:int(TOTAL / FPS * SR)]
    os.makedirs(os.path.join(STUDIO, "public", nome), exist_ok=True)
    bruto = os.path.join(CACHE, f"{nome}_bruto.wav")
    with wave.open(bruto, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", bruto, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2",
                    os.path.join(STUDIO, "public", nome, "mix.wav")], check=True)
    json.dump(timeline, open(os.path.join(STUDIO, "src", "data", f"{nome}.json"), "w"), ensure_ascii=False)
    print(nome, "total", round(TOTAL / FPS, 1), "s")
    for c in timeline["cenas"]: print(f'  {c["id"]:8s} ini {c["inicio"]/FPS:6.1f}s dur {c["duracao"]/FPS:5.1f}s')
