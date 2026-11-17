"""Diretor do episodio S2E1: gera vozes, legendas, boca, trilha e a linha do tempo (JSON) para o Remotion."""
import hashlib, json, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.join(HERE, "..", "estudio")
CACHE = os.path.join(HERE, "cache"); os.makedirs(CACHE, exist_ok=True)
SR, FPS, T_TRANS = 44100, 30, 14          # transicao entre cenas (frames)
NEURO, ROBO = "neuro", "robo"
VOZ = {NEURO: ("pt-BR-AntonioNeural", None), ROBO: ("pt-BR-AntonioNeural", "robo")}
ESTILO = {"x": ("+12%", "+6Hz"), "n": ("+8%", "+0Hz"), "q": ("-4%", "+12Hz"), "r": ("+6%", "+18Hz")}
rng = np.random.default_rng(7)

def dec(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def robotiza(a):
    t = np.arange(len(a)) / SR
    y = a * (0.62 + 0.38 * np.sin(2 * np.pi * 55 * t))
    d = int(0.0065 * SR); z = y.copy(); z[d:] += 0.55 * y[:-d]
    q = np.round(z * 24) / 24
    return (0.7 * z + 0.3 * q) * 0.85

def tts(texto, quem, estilo):
    voz, fx = VOZ[quem]; r, p = ESTILO[estilo]
    key = hashlib.md5(f"{voz}|{texto}|{r}|{p}".encode()).hexdigest()[:16]
    mp = os.path.join(CACHE, key + ".mp3")
    if not os.path.exists(mp + ".json"):
        subprocess.run([sys.executable, os.path.join(HERE, "tts2.py"), voz, texto, mp, r, p], check=True)
    a = dec(mp); wb = json.load(open(mp + ".json"))
    s0 = max(0, wb[0][1] - 0.04); s1 = min(len(a) / SR, wb[-1][1] + wb[-1][2] + 0.1)
    seg = a[int(s0 * SR):int(s1 * SR)]
    if fx == "robo": seg = robotiza(seg)
    words = [(w, o - s0, o - s0 + du) for w, o, du in wb]
    return seg, words

# ---------------- ROTEIRO ----------------
# cada cena: tipo, falas [(quem, texto, estilo)], extras
def fala(q, t, e="n"): return (q, t, e)
CENAS = [
 dict(id="hook", tipo="hook", falas=[fala(ROBO, "Nenhum humano consegue me vencer.", "r"), fala(NEURO, "Isso é o que a gente vai ver!", "x")], cauda=0.3),
 dict(id="intro", tipo="intro", falas=[fala(NEURO, "Oi! Eu sou o Neuro!", "x"), fala(NEURO, "Começou a temporada dois!", "x"), fala(NEURO, "Você tem três vidas.", "n"), fala(NEURO, "Bora?", "q")], cauda=0.25),
 dict(id="tema", tipo="tema", falas=[fala(NEURO, "Tema de hoje: o torneio dos gênios!", "x"), fala(NEURO, "E o meu primeiro rival é...", "n")], cauda=0.15),
 dict(id="robo", tipo="robo", falas=[fala(ROBO, "Calculino. Eu faço um milhão de contas por segundo.", "r"), fala(ROBO, "Humanos são lentos.", "r")], cauda=0.3),
 dict(id="regras", tipo="regras", falas=[fala(NEURO, "O Calculino responde primeiro.", "n"), fala(NEURO, "Se ele errar, e você acertar, ponto pro nosso time!", "x")], cauda=0.3),
 dict(id="r1", tipo="rodada", n=1, titulo="QUANTAS SOBRARAM?", texto=["17 OVELHAS", "TODAS MORREM, MENOS 9"],
      opcoes=["8", "9", "17"], certa=1, robo=0, visual="ovelhas",
      pergunta=[fala(NEURO, "Um fazendeiro tem dezessete ovelhas.", "n"), fala(NEURO, "Todas morrem, menos nove. Quantas sobraram?", "q")],
      roboFala=[fala(ROBO, "Fácil. Dezessete menos nove. Oito.", "r")],
      revela=[fala(NEURO, "Nove!", "x"), fala(NEURO, "Todas morreram, menos nove!", "n")], ponto=NEURO),
 dict(id="r2", tipo="rodada", n=2, titulo="EM QUE LUGAR VOCÊ FICA?", texto=["VOCÊ ULTRAPASSA", "O 2º COLOCADO"],
      opcoes=["Segundo", "Primeiro", "Terceiro"], certa=0, robo=1, visual="corrida",
      pergunta=[fala(NEURO, "Numa corrida, você ultrapassa o segundo colocado.", "n"), fala(NEURO, "Em que lugar você fica?", "q")],
      roboFala=[fala(ROBO, "Primeiro lugar.", "r")],
      revela=[fala(NEURO, "Segundo!", "x"), fala(NEURO, "Você só tomou o lugar dele!", "n")], ponto=NEURO),
 dict(id="r3", tipo="rodada", n=3, titulo="QUAL GIRA IGUAL À A?", texto=["A GIRA PRA DIREITA"],
      opcoes=["Engrenagem B", "Engrenagem C", "Engrenagem D"], certa=1, robo=1, visual="engrenagens",
      pergunta=[fala(NEURO, "A engrenagem A gira pra direita.", "n"), fala(NEURO, "Qual gira pro mesmo lado?", "q")],
      roboFala=[fala(ROBO, "Engrenagem C. Vizinhas giram ao contrário.", "r")],
      revela=[fala(NEURO, "Ele acertou essa...", "n"), fala(NEURO, "Ponto pro Calculino!", "x")], ponto=ROBO),
 dict(id="r4", tipo="rodada", n=4, final=True, titulo="RODADA FINAL", texto=["1+1+1+1+1+1+1+1+1+1×0"],
      opcoes=["0", "9", "10"], certa=1, robo=0, visual="conta",
      pergunta=[fala(NEURO, "Rodada final!", "x"), fala(NEURO, "Quanto dá essa conta?", "q")],
      roboFala=[fala(ROBO, "Zero. Tudo vezes zero é zero.", "r")],
      revela=[fala(NEURO, "Nove!", "x"), fala(NEURO, "A multiplicação vem primeiro!", "n"), fala(NEURO, "Um vezes zero dá zero, e sobram nove!", "n")],
      depois=[fala(ROBO, "Erro. Erro. Reiniciando.", "r")], ponto=NEURO),
 dict(id="vitoria", tipo="vitoria", falas=[fala(NEURO, "Três a um! Vencemos o Calculino!", "x")], cauda=0.4),
 dict(id="outro", tipo="outro", falas=[fala(NEURO, "Quantas vidas sobraram?", "q"), fala(NEURO, "Três? Gênio do torneio!", "q"), fala(NEURO, "Uma ou duas? Classificado!", "q"), fala(NEURO, "Nenhuma? Eliminado!", "q"), fala(NEURO, "Segue o Neuro pro próximo rival!", "x")], cauda=0.8),
]
CONTAGEM = 2.5

# ---------------- MONTAGEM DA LINHA DO TEMPO ----------------
clips = []      # audio global
timeline = {"fps": FPS, "transicao": T_TRANS, "cenas": []}
sfx = []        # (segundos globais, tipo, extra)
inicio = 0      # frame global de inicio da cena

def bloco(falas, t_local, acc):
    """posiciona uma lista de falas a partir de t_local (s); devolve fim e lista de clipes da cena"""
    for q, txt, e in falas:
        a, w = tts(txt, q, e)
        acc.append(dict(quem=q, texto=txt, ini=t_local, dur=len(a) / SR, palavras=[[x, round(s, 3), round(f, 3)] for x, s, f in w], _a=a))
        t_local += len(a) / SR + 0.16
    return t_local

for i, c in enumerate(CENAS):
    pad = T_TRANS / FPS + 0.08
    cl = []; ev = {}
    if c["tipo"] == "rodada":
        t = bloco(c["pergunta"], pad, cl)
        ev["roboEm"] = t + 0.1
        t = bloco(c["roboFala"], t + 0.1, cl)
        ev["contaIni"] = t + 0.1; ev["contaFim"] = ev["contaIni"] + CONTAGEM
        ev["revelaEm"] = ev["contaFim"]
        t = bloco(c["revela"], ev["revelaEm"] + 0.35, cl)
        ev["pontoEm"] = ev["revelaEm"] + 0.9
        if c.get("depois"):
            ev["bugEm"] = t + 0.05
            t = bloco(c["depois"], t + 0.1, cl)
        dur = t + 0.5
    else:
        t = bloco(c["falas"], pad, cl)
        # inicio de cada fala (para sincronizar elementos)
        ev["falas"] = [round(x["ini"], 3) for x in cl]
        dur = t + c.get("cauda", 0.3)
    dframes = int(round(dur * FPS))
    cena = {k: v for k, v in c.items() if k not in ("falas", "pergunta", "roboFala", "revela", "depois")}
    cena.update(inicio=inicio, duracao=dframes, eventos={k: (round(v, 3) if isinstance(v, float) else v) for k, v in ev.items()})
    cena["clipes"] = [{k: v for k, v in x.items() if k != "_a"} for x in cl]
    timeline["cenas"].append(cena)
    for x in cl: clips.append((inicio / FPS + x["ini"], x["quem"], x["_a"]))
    # efeitos sonoros
    sfx.append((inicio / FPS, "whoosh"))
    if c["tipo"] == "rodada":
        g = inicio / FPS
        sfx.append((g + ev["roboEm"], "bip"))
        sfx.append((g + ev["contaIni"], "rufar", CONTAGEM))
        for s in range(int(CONTAGEM)): sfx.append((g + ev["contaIni"] + s, "tick"))
        certo = c["certa"] == c["robo"]
        sfx.append((g + ev["revelaEm"], "prato"))
        sfx.append((g + ev["revelaEm"] + 0.05, "ding" if True else ""))
        if not certo: sfx.append((g + ev["revelaEm"] + 0.45, "erro"))
        sfx.append((g + ev["pontoEm"], "moeda"))
        if ev.get("bugEm"): sfx.append((g + ev["bugEm"], "glitch")); sfx.append((g + ev["bugEm"] + 0.6, "glitch"))
    if c["tipo"] in ("hook", "intro", "vitoria"): sfx.append((inicio / FPS + 0.05, "boom"))
    if i < len(CENAS) - 1: inicio += dframes - T_TRANS
    else: inicio += dframes

TOTAL = inicio; timeline["total"] = TOTAL
N = int(TOTAL / FPS * SR) + SR

# ---------------- AUDIO ----------------
def put(arr, s, sig):
    s = int(s); e = min(len(arr), s + len(sig))
    if 0 <= s < len(arr): arr[s:e] += sig[:e - s]
voz = np.zeros(N, np.float32); vozq = {NEURO: np.zeros(N, np.float32), ROBO: np.zeros(N, np.float32)}
for st, q, a in clips:
    put(voz, st * SR, a); put(vozq[q], st * SR, a)

# boca: rms por frame, por personagem
boca = {}
for q, arr in vozq.items():
    hop = SR // FPS; n = TOTAL
    v = np.array([np.sqrt(np.mean(arr[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(arr) else 0 for i in range(n)])
    v = np.clip(v * 7.5, 0, 1); v = np.convolve(v, [0.25, 0.5, 0.25], "same")
    boca[q] = [round(float(x), 2) for x in v]
timeline["boca"] = boca

# trilha: 120 bpm, C G Am F
t_ = np.arange(N) / SR; bpm = 118; beat = 60 / bpm
mus = np.zeros(N, np.float32)
def nota(m): return 440 * 2 ** ((m - 69) / 12)
acordes = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
kick = lambda L: np.sin(2 * np.pi * np.cumsum(np.linspace(130, 45, L)) / SR) * np.exp(-np.arange(L) / SR * 14)
snare = lambda L: (rng.standard_normal(L) * 0.8 + 0.4 * np.sin(2 * np.pi * 190 * np.arange(L) / SR)) * np.exp(-np.arange(L) / SR * 20)
hat = lambda L: np.diff(np.concatenate([[0], rng.standard_normal(L)])) * np.exp(-np.arange(L) / SR * 80)
b = 0
while b * beat < TOTAL / FPS:
    s = int(b * beat * SR); bar = b // 4; ac = acordes[bar % 4]
    put(mus, s, 0.85 * kick(int(.3 * SR)))
    if b % 2 == 1: put(mus, s, 0.3 * snare(int(.22 * SR)))
    for h in (0.5,): put(mus, s + int(h * beat * SR), 0.12 * hat(int(.05 * SR)))
    put(mus, s + int(0.75 * beat * SR), 0.06 * hat(int(.03 * SR)))
    Lb = int(beat * 0.9 * SR); tt = np.arange(Lb) / SR
    put(mus, s, 0.22 * np.tanh(2 * np.sin(2 * np.pi * nota(ac[0] - 24) * tt)) * np.exp(-tt * 4))
    for k_ in range(2):  # arpejo em colcheias
        m = ac[(b * 2 + k_) % 3] + 12; La = int(beat / 2 * SR); ta = np.arange(La) / SR
        put(mus, s + k_ * La, 0.07 * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * nota(m) * ta)) * np.exp(-ta * 9))
    if b % 4 == 0:  # pad
        Lp = int(beat * 4 * SR); tp = np.arange(Lp) / SR; env = np.minimum(1, tp / 0.4) * np.minimum(1, (tp[::-1]) / 0.5)
        pad = sum(np.sin(2 * np.pi * nota(m) * tp) + 0.3 * np.sin(2 * np.pi * nota(m) * 2.003 * tp) for m in ac)
        put(mus, s, 0.035 * pad * env)
    b += 1
env = np.convolve((np.abs(voz) > 0.015).astype(np.float32), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
duck = 1 - 0.62 * np.clip(env * 3, 0, 1)

fx = np.zeros(N, np.float32)
for e in sfx:
    st, k = e[0], e[1]; s = st * SR
    if k == "tick": L = int(.06 * SR); tt = np.arange(L) / SR; put(fx, s, 0.3 * np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt * 70))
    elif k == "bip": L = int(.25 * SR); tt = np.arange(L) / SR; put(fx, s, 0.18 * np.sign(np.sin(2 * np.pi * np.where(tt < .12, 880, 1320) * tt)) * np.exp(-tt * 6))
    elif k == "ding": L = int(.9 * SR); tt = np.arange(L) / SR; put(fx, s, 0.28 * (np.sin(2 * np.pi * 1318 * tt) + .5 * np.sin(2 * np.pi * 1976 * tt)) * np.exp(-tt * 4.5))
    elif k == "erro": L = int(.5 * SR); tt = np.arange(L) / SR; put(fx, s, 0.22 * np.sign(np.sin(2 * np.pi * 120 * tt)) * np.exp(-tt * 3.5))
    elif k == "moeda": L = int(.4 * SR); tt = np.arange(L) / SR; put(fx, s, 0.22 * np.sin(2 * np.pi * np.where(tt < .08, 988, 1319) * tt) * np.exp(-tt * 6))
    elif k == "whoosh":
        L = int(.4 * SR); n_ = np.convolve(rng.standard_normal(L), np.ones(9) / 9, "same"); w = np.sin(np.pi * np.arange(L) / L) ** 2; put(fx, s, 0.4 * n_ * w)
    elif k == "boom": L = int(.8 * SR); tt = np.arange(L) / SR; put(fx, s, 0.6 * np.sin(2 * np.pi * np.cumsum(np.linspace(95, 32, L)) / SR) * np.exp(-tt * 4.5))
    elif k == "prato": L = int(1.4 * SR); tt = np.arange(L) / SR; n_ = rng.standard_normal(L); n_ = n_ - np.convolve(n_, np.ones(5) / 5, "same"); put(fx, s, 0.3 * n_ * np.exp(-tt * 2.6))
    elif k == "glitch": L = int(.4 * SR); put(fx, s, 0.25 * rng.standard_normal(L) * (np.sign(np.sin(2 * np.pi * 21 * np.arange(L) / SR)) > 0) * np.exp(-np.arange(L) / SR * 4))
    elif k == "rufar":
        D = e[2]; tt = 0.0
        while tt < D:
            put(fx, s + tt * SR, (0.06 + 0.2 * tt / D) * snare(int(.07 * SR))); tt += 0.11 - 0.07 * tt / D
mix = np.tanh((0.16 * mus * duck + 1.05 * voz + fx) * 1.05) * 0.9
L = int(TOTAL / FPS * SR); mix = mix[:L]
os.makedirs(os.path.join(STUDIO, "public", "s2e1"), exist_ok=True)
bruto = os.path.join(CACHE, "mix_bruto.wav")
with wave.open(bruto, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
# loudness padrao das redes (skill video-editing): -14 LUFS, pico -1.5 dB
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", bruto, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2",
                os.path.join(STUDIO, "public", "s2e1", "mix.wav")], check=True)
os.makedirs(os.path.join(STUDIO, "src", "data"), exist_ok=True)
json.dump(timeline, open(os.path.join(STUDIO, "src", "data", "s2e1.json"), "w"), ensure_ascii=False)
print("total", round(TOTAL / FPS, 1), "s;", len(timeline["cenas"]), "cenas")
for c in timeline["cenas"]: print(f'  {c["id"]:8s} ini {c["inicio"]/FPS:6.1f}s dur {c["duracao"]/FPS:5.1f}s')
