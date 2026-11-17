"""S2E2 - Madame Miragem (ilusoes de otica)."""
from motor import montar, fala, NEURO, RIVAL
N, M = NEURO, RIVAL
VOZ = {N: ("pt-BR-AntonioNeural", None), M: ("pt-BR-FranciscaNeural", "eco"), "turbo": ("pt-BR-ThalitaMultilingualNeural", None)}
INTRO = [fala(N, "Oi! Eu sou o Neuro!", "x"), fala(N, "Você tem três vidas.", "n"), fala(N, "Bora?", "q")]
CENAS = [
 dict(id="gancho", tipo="ganchoGrade", boom=True, falas=[fala(M, "Quantas bolinhas pretas você está vendo?", "mq"), fala(N, "Não responde ainda!", "x")], cauda=0.25),
 dict(id="intro", tipo="introCurta", falas=INTRO, cauda=0.2),
 dict(id="rival", tipo="apresentaRival", boom=True, sfx=[(0.3, "magia")],
      falas=[fala(M, "Eu sou a Madame Miragem!", "mistica"), fala(M, "Seus olhos vão te trair.", "mistica"), fala(N, "Ela responde primeiro... mas cuidado: ela adora enganar!", "n")], cauda=0.3),
 dict(id="r1", tipo="rodada", n=1, titulo="QUANTAS BOLINHAS PRETAS?", texto=[], opcoes=["12", "Nenhuma", "Infinitas"], certa=1, robo=0, visual="grade", balao="VEJO 12!",
      pergunta=[fala(N, "Quantas bolinhas pretas tem aqui?", "q")], roboFala=[fala(M, "Eu vejo doze!", "mistica")],
      revela=[fala(N, "Nenhuma!", "x"), fala(N, "Todas são brancas. O seu cérebro inventa as pretas!", "n")], ponto=N),
 dict(id="r2", tipo="rodada", n=2, titulo="QUAL ANDA MAIS RÁPIDO?", texto=[], opcoes=["Amarelo", "Azul", "Os dois iguais"], certa=2, robo=2, visual="velocidade", balao="OS DOIS IGUAIS!",
      pergunta=[fala(N, "Qual quadrado anda mais rápido?", "q")], roboFala=[fala(M, "Os dois iguais. Fácil!", "mistica")],
      revela=[fala(N, "Ela acertou...", "n"), fala(N, "Sem as listras, dá pra ver: andam juntinhos!", "n")], ponto=M),
 dict(id="r3", tipo="rodada", n=3, titulo="QUAL BARRA É MAIOR?", texto=[], opcoes=["A de cima", "A de baixo", "São iguais"], certa=1, robo=2, visual="trilhos", balao="SÃO IGUAIS!",
      pergunta=[fala(N, "E agora: qual barra é maior?", "q")], roboFala=[fala(M, "São iguais, claro. É uma ilusão!", "mistica")],
      revela=[fala(N, "A de baixo!", "x"), fala(N, "Dessa vez não era igual. Te peguei!", "x")], ponto=N),
 dict(id="r4", tipo="rodada", n=4, final=True, titulo="TRUQUE FINAL", texto=[], opcoes=["Leu sua mente", "Trocou todas", "Foi sorte"], certa=1, robo=0, visual="cartas",
      contagem=2.5, balao="LI SUA MENTE!", bugTexto="DESCOBERTA!",
      pergunta=[fala(N, "Rodada final!", "x"), fala(M, "Escolha uma carta, e guarde na cabeça.", "mistica"), ("marca", "memo", ""), ("pausa", "2.6", ""),
                ("marca", "troca", ""), fala(M, "Abracadabra! A sua carta sumiu!", "mistica"), fala(N, "Como ela fez isso?", "q")],
      roboFala=[fala(M, "Eu li a sua mente!", "mistica")],
      revela=[fala(N, "Ela trocou todas as cartas!", "x"), fala(N, "Nenhuma carta de antes voltou!", "n")],
      depois=[fala(M, "Descobriram o meu truque!", "mistica")], ponto=N),
 dict(id="vitoria", tipo="vitoriaGen", placar="TIME 3 × 1 MIRAGEM", boom=True, falas=[fala(N, "Três a um! Nenhuma ilusão engana a gente!", "x")], cauda=0.4),
 dict(id="outro", tipo="outroTeaser", tiers=[["3","OLHO DE ÁGUIA","#ffb300"],["1-2","QUASE LÁ","#1fb85c"],["0","ILUDIDO","#6b6b85"]], falas=[fala(N, "Quantas vidas sobraram? Comenta aí!", "q")], cauda=1.2),
 dict(id="gancho_final", tipo="cliffhanger", vilao="turbo", sfx=[(0.1, "glitch"), (2.6, "riser", 1.2)], falas=[fala(M, "Vocês me venceram... mas o meu amigo é muito mais rápido!", "mistica"), fala("turbo", "Alguém me chamou?", "rapido"), fala(N, "Quem é esse?!", "q")], cauda=1.6),
]
montar("s2e2", CENAS, VOZ, contagem=3.0)
