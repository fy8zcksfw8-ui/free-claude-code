"""S2E3 - Turbo (rodada relampago)."""
from motor import montar, fala, NEURO, RIVAL
N, T = NEURO, RIVAL
VOZ = {N: ("pt-BR-AntonioNeural", None), T: ("pt-BR-ThalitaMultilingualNeural", None), "doutor": ("pt-BR-AntonioNeural", "eco")}
INTRO = [fala(N, "Oi! Eu sou o Neuro!", "x"), fala(N, "Você tem três vidas.", "n"), fala(N, "Bora?", "q")]
def r(n, q, robo_fala, opcoes, certa, robo, revela, ponto, texto, **kw):
    return dict(id=f"r{n}", tipo="rodada", n=n, titulo=f"PERGUNTA {n}/6", texto=texto, opcoes=opcoes, certa=certa, robo=robo, visual="pergunta",
                contagem=2.0, pergunta=[fala(N, q, "q")], roboFala=[fala(T, robo_fala, "rapido")], revela=revela, ponto=ponto, cauda=0.1, **kw)
CENAS = [
 dict(id="gancho", tipo="ganchoTurbo", boom=True, falas=[fala(T, "Você responde em dois segundos?", "rapido"), fala(T, "Eu respondo em zero!", "rapido")], cauda=0.2),
 dict(id="intro", tipo="introCurta", falas=INTRO, cauda=0.2),
 dict(id="rival", tipo="apresentaRival", boom=True, sfx=[(0.2, "riser", 1.0)],
      falas=[fala(T, "Turbo na área! O mais rápido do universo!", "rapido"), fala(N, "Rodada relâmpago: seis perguntas, dois segundos cada!", "x")], cauda=0.2),
 r(1, "Quanto é metade de dois, mais dois?", "Dois!", ["3", "2"], 0, 1, [fala(N, "Três! Metade de dois é um, mais dois!", "x")], N, ["METADE DE 2 + 2 = ?"]),
 r(2, "Você tem três maçãs e tira duas. Quantas você tem?", "Uma!", ["1", "2"], 1, 0, [fala(N, "Duas! As que você tirou!", "x")], N, ["3 MAÇÃS, VOCÊ TIRA 2.", "QUANTAS VOCÊ TEM?"]),
 r(3, "Um tijolo pesa um quilo, mais meio tijolo. Quanto pesa o tijolo?", "Um quilo e meio!", ["2 kg", "1,5 kg"], 0, 1, [fala(N, "Dois quilos!", "x")], N, ["TIJOLO = 1 KG + MEIO TIJOLO"]),
 r(4, "Quantas vezes dá pra tirar dez de cem?", "Dez vezes!", ["10", "1"], 1, 0, [fala(N, "Uma! Depois já é noventa!", "x")], N, ["QUANTAS VEZES DÁ PRA", "TIRAR 10 DE 100?"]),
 r(5, "Se ontem foi sexta, que dia é depois de amanhã?", "Segunda!", ["Segunda", "Domingo"], 0, 0, [fala(N, "Ele acertou essa. Segunda!", "n")], T, ["ONTEM FOI SEXTA.", "DEPOIS DE AMANHÃ É...?"]),
 r(6, "O pai do Pedro tem três filhos: Huguinho, Zezinho, e...?", "Luizinho!", ["Luizinho", "Pedro"], 1, 0, [fala(N, "Pedro! Tava na pergunta!", "x")], N, ["O PAI DO PEDRO TEM 3 FILHOS:", "HUGUINHO, ZEZINHO E...?"],
   final=True, bugTexto="RÁPIDO DEMAIS!", depois=[fala(T, "Fui rápido demais...", "rapido")]),
 dict(id="vitoria", tipo="vitoriaGen", placar="TIME 5 × 1 TURBO", boom=True, falas=[fala(N, "Cinco a um! Mais rápido que o Turbo!", "x")], cauda=0.4),
 dict(id="outro", tipo="outroTeaser", tiers=[["3","CÉREBRO TURBO","#ffb300"],["1-2","RAPIDINHO","#1fb85c"],["0","DEVAGAR E SEMPRE","#6b6b85"]], falas=[fala(N, "Quantas vidas sobraram? Comenta aí!", "q")], cauda=1.2),
 dict(id="gancho_final", tipo="cliffhanger", vilao="doutor", sfx=[(0.1, "glitch"), (1.4, "glitch"), (1.5, "boom")], falas=[fala(N, "Ufa... vencemos!", "n"), fala("doutor", "Sentiram a minha falta, Neuro?", "grave"), fala(N, "Não pode ser... o Doutor Esquecido voltou?!", "q")], cauda=1.6),
]
montar("s2e3", CENAS, VOZ, bpm=132, tom=2)
