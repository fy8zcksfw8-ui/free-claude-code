"""S2E5 - A grande final: o time devolve a memoria do Neuro e enfrenta o Doutor. Gancho: convite para o Torneio Mundial."""
from motor import montar, fala, NEURO, RIVAL
N, D = NEURO, RIVAL
C, M, T = "calculino", "miragem", "turbo"
VOZ = {N: ("pt-BR-AntonioNeural", None), D: ("pt-BR-AntonioNeural", "eco"), C: ("pt-BR-AntonioNeural", "robo"),
       M: ("pt-BR-FranciscaNeural", "eco"), T: ("pt-BR-ThalitaMultilingualNeural", None)}
CENAS = [
 dict(id="gancho", tipo="ganchoAmnesiaAbre", boom=True, sfx=[(0.05, "glitch")], falas=[fala(N, "Onde eu estou? Quem sou eu?", "q")], cauda=0.3),
 dict(id="intro", tipo="introAmnesia", falas=[fala(N, "Oi! Eu sou o... o...", "q"), fala(C, "Neuro! Você é o Neuro!", "r"), fala(N, "Isso! Eu sou o Neuro! Você tem três vidas. Bora?", "x")], cauda=0.2),
 dict(id="time", tipo="timeReune", sfx=[(0.3, "magia")],
      falas=[fala(M, "A gente veio ajudar!", "mistica"), fala(T, "Rapidinho!", "rapido"), fala(N, "Cada desafio certo devolve um pedaço da minha memória!", "x")], cauda=0.3),
 dict(id="r1", tipo="rodada", n=1, titulo="DESAFIO DO CALCULINO", texto=["QUANTOS NOVES TEM", "DE 1 A 100?"], opcoes=["10", "11", "20"], certa=2, robo=0, visual="noves",
      quemDesafia="calculino", memAntes=0.1, memDepois=0.4, balao="SÓ DEZ!",
      pergunta=[fala(C, "Desafio do Calculino!", "r"), fala(C, "Quantos noves existem de um a cem?", "r")],
      roboFala=[fala(D, "Dez! Não confia neles!", "grave")], revela=[fala(N, "Vinte!", "x"), fala(N, "Contando o noventa e nove duas vezes!", "n")], ponto=N),
 dict(id="r2", tipo="rodada", n=2, titulo="DESAFIO DA MIRAGEM", texto=["AS LINHAS CINZAS SÃO..."], opcoes=["Tortas", "Retas"], certa=1, robo=0, visual="cafe",
      quemDesafia="miragem", memAntes=0.4, memDepois=0.7, balao="TORTAS!",
      pergunta=[fala(M, "Desafio da Miragem!", "mistica"), fala(M, "Essas linhas são tortas ou retas?", "mq")],
      roboFala=[fala(D, "Tortas, ha!", "grave")], revela=[fala(N, "Retas!", "x"), fala(N, "É a ilusão da parede do café!", "n")], ponto=N),
 dict(id="r3", tipo="rodada", n=3, titulo="DESAFIO DO TURBO", texto=["RÁPIDO: O QUE A VACA BEBE?"], opcoes=["Leite", "Água"], certa=1, robo=0, visual="vaca", contagem=2.0,
      quemDesafia="turbo", memAntes=0.7, memDepois=1.0, balao="LEITE!",
      pergunta=[fala(T, "Desafio do Turbo! Rápido:", "rapido"), fala(T, "O que a vaca bebe?", "rapido")],
      roboFala=[fala(D, "Leite!", "grave")], revela=[fala(N, "Água!", "x"), fala(N, "Lembrei de tudo! Eu sou o Neuro!", "x")], ponto=N),
 dict(id="vs", tipo="vsBatalha", boom=True, sfx=[(0.35, "boom")], falas=[fala(D, "Chega! Agora é eu contra você!", "grave"), fala(N, "Contra a gente, Doutor!", "x")], cauda=0.3),
 dict(id="r4", tipo="rodada", n=4, final=True, titulo="ÚLTIMA PERGUNTA", texto=[], opcoes=["A cobra", "A garrafa", "A tartaruga"], certa=1, robo=0, visual="garrafa",
      balao="A COBRA!", bugTexto="NÃÃÃO!",
      pergunta=[fala(D, "Última pergunta!", "grave"), fala(D, "O que tem pescoço, mas não tem cabeça?", "grave")],
      roboFala=[fala(D, "A cobra, ha!", "grave")], revela=[fala(N, "A garrafa!", "x"), fala(N, "Agora, todos juntos!", "x")],
      depois=[fala(D, "Não! Eu vou esquecer tudo!", "grave")], ponto=N),
 dict(id="ataque", tipo="superAtaque", sfx=[(0.1, "riser", 1.5), (1.6, "boom"), (1.65, "prato"), (2.6, "boom")], falas=[fala(N, "Super ataque do time!", "x"), ("pausa", "1.4", "")], cauda=0.6),
 dict(id="vitoria", tipo="vitoriaTime", boom=True, falas=[fala(N, "Vencemos o torneio! Valeu, time!", "x"), fala(N, "Quantas vidas sobraram? Comenta!", "q")], cauda=0.3),
 dict(id="gancho_final", tipo="convite", sfx=[(0.2, "magia"), (2.4, "riser", 1.2)],
      falas=[fala(N, "Ué... uma carta?", "q"), fala(N, "Convite para o Torneio Mundial dos Gênios?!", "x")], cauda=1.9),
]
montar("s2e5", CENAS, VOZ, contagem=3.0, transicao=10)
