"""S3E1 - A Esfinge (Torneio Mundial, fase 1: Egito). Plano: ../../temporada3/plano-edicao.json"""
from motor import montar, fala, NEURO, RIVAL
N, E = NEURO, RIVAL
VOZ = {N: ("pt-BR-AntonioNeural", None), E: ("pt-BR-FranciscaNeural", "eco"), "voz": ("pt-BR-AntonioNeural", "eco")}
CENAS = [
 dict(id="gancho", tipo="ganchoEsfinge", boom=True, sfx=[(0.02, "glitch")],
      falas=[fala(E, "Responda... ou vire pedra!", "mistica"), fala(N, "Quase ninguém passa do terceiro enigma?", "q")], cauda=0.1),
 dict(id="intro", tipo="introMundo", sfx=[(0.3, "magia")],
      falas=[fala(N, "Oi! Eu sou o Neuro!", "x"), fala(N, "Torneio Mundial: Egito!", "x"), fala(N, "Três vidas. Bora?", "q")], cauda=0.1),
 dict(id="esfinge", tipo="apresentaEsfinge", boom=True, sfx=[(0.2, "riser", 1.0)],
      falas=[fala(E, "Eu sou a Esfinge.", "mistica"), fala(E, "Três enigmas. Errou... virou pedra!", "mistica")], cauda=0.1),
 dict(id="e1", tipo="rodada", n=1, titulo="ENIGMA 1", texto=["4 PERNAS DE MANHÃ,", "2 À TARDE, 3 À NOITE?"], opcoes=["Um gato", "O ser humano", "Um robô"],
      certa=1, robo=0, visual="pernas", balao="UM GATO?",
      pergunta=[fala(E, "O que anda com quatro pernas de manhã, duas à tarde, e três à noite?", "mq")],
      roboFala=[fala(E, "Muitos dizem: gato.", "mistica")],
      revela=[fala(N, "O ser humano!", "x"), fala(N, "Engatinha, anda, e usa bengala!", "n")], ponto=N),
 dict(id="e2", tipo="rodada", n=2, titulo="ENIGMA 2", texto=["QUANTO MAIS CRESCE,", "MENOS SE VÊ?"], opcoes=["A sombra", "A árvore", "A escuridão"],
      certa=2, robo=0, visual="escuro", balao="A SOMBRA?",
      pergunta=[fala(E, "O que é que, quanto mais cresce, menos se vê?", "mq")],
      roboFala=[fala(E, "A sombra, talvez?", "mistica")],
      revela=[fala(N, "A escuridão!", "x")], ponto=N),
 dict(id="e3", tipo="rodada", n=3, final=True, titulo="ENIGMA 3", texto=[], opcoes=["21", "17", "30"], certa=1, robo=0, visual="icones", balao="21?",
      bugTexto="VIROU PEDRA!", contagem=3.0,
      pergunta=[fala(E, "O último. Quase ninguém acerta.", "mistica"), ("marca", "linhas", ""), ("pausa", "1.2", ""), fala(E, "Quanto dá a última linha?", "mq")],
      roboFala=[fala(E, "Muitos dizem: vinte e um.", "mistica")],
      revela=[fala(N, "Dezessete!", "x"), fala(N, "A multiplicação vem primeiro!", "n")],
      depois=[fala(E, "Impossível!", "mistica")], ponto=N),
 dict(id="cta", tipo="ctaPedra", boom=True, sfx=[(0.1, "prato")], falas=[fala(N, "Três de três! Quantos você acertou? Comenta!", "x")], cauda=0.3),
 dict(id="continua", tipo="portaLabirinto", sfx=[(0.1, "boom"), (0.5, "riser", 1.8)],
      falas=[("pausa", "1.0", ""), fala("voz", "Bem-vindo... ao labirinto.", "grave"), fala(N, "Quem disse isso?!", "q")], cauda=1.9),
]
montar("s3e1", CENAS, VOZ, contagem=2.5, transicao=12, bpm=120, tom=-3, batida=True)
