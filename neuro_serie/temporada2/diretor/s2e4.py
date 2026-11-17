"""S2E4 - O Doutor voltou (memoria) -> gancho: Neuro perde a memoria."""
from motor import montar, fala, NEURO, RIVAL
N, D = NEURO, RIVAL
VOZ = {N: ("pt-BR-AntonioNeural", None), D: ("pt-BR-AntonioNeural", "eco")}
INTRO = [fala(N, "Oi! Eu sou o Neuro!", "x"), fala(N, "Você tem três vidas.", "n"), fala(N, "Bora?", "q")]
CENAS = [
 dict(id="gancho", tipo="ganchoDoutor", boom=True, sfx=[(0.05, "glitch")], falas=[fala(D, "Sentiram a minha falta?", "grave"), fala(N, "O Doutor Esquecido voltou!", "x")], cauda=0.2),
 dict(id="intro", tipo="introCurta", falas=INTRO, cauda=0.2),
 dict(id="rival", tipo="apresentaRival", boom=True, sfx=[(0.2, "glitch")],
      falas=[fala(D, "Eu invadi o torneio!", "grave"), fala(D, "E vou apagar a sua memória!", "grave"), fala(N, "Cada resposta certa protege a nossa memória!", "x")], cauda=0.3),
 dict(id="r1", tipo="rodada", n=1, titulo="O QUE SUMIU?", texto=[], opcoes=["A estrela", "A lua", "O raio"], certa=1, robo=0, visual="objetos", balao="A ESTRELA!",
      pergunta=[fala(N, "Memoriza esses seis desenhos!", "x"), ("marca", "memo", ""), ("pausa", "2.4", ""), ("marca", "apaga", ""), fala(D, "Apaguei um! Qual sumiu?", "grave")],
      roboFala=[fala(D, "Foi a estrela!", "grave")], revela=[fala(N, "A lua!", "x"), fala(N, "Memória protegida!", "n")], ponto=N,
),
 dict(id="r2", tipo="rodada", n=2, titulo="QUAL ERA A 3ª SETA?", texto=[], opcoes=["Pra cima", "Pra esquerda", "Pra baixo"], certa=1, robo=0, visual="setas", balao="PRA CIMA!",
      pergunta=[fala(N, "Agora, presta atenção nas setas!", "x"), ("marca", "memo", ""), ("pausa", "3.2", ""), ("marca", "apaga", ""), fala(N, "Qual era a terceira seta?", "q")],
      roboFala=[fala(D, "Pra cima!", "grave")], revela=[fala(N, "Pra esquerda!", "x")], ponto=N),
 dict(id="r3", tipo="rodada", n=3, titulo="PERGUNTA DE FÃ", texto=["QUEM DISSE:", "\"HUMANOS SÃO LENTOS\"?"], opcoes=["Calculino", "Miragem", "Turbo"], certa=0, robo=1, visual="fas", balao="A MIRAGEM!",
      pergunta=[fala(N, "Pergunta de fã!", "x"), fala(N, "Quem disse: humanos são lentos?", "q")],
      roboFala=[fala(D, "Foi a Miragem!", "grave")], revela=[fala(N, "O Calculino!", "x"), fala(N, "Lá no episódio um!", "n")], ponto=N),
 dict(id="r4", tipo="rodada", n=4, final=True, titulo="ENIGMA DO DOUTOR", texto=[], opcoes=["A toalha", "O guarda-chuva", "A esponja"], certa=0, robo=2, visual="enigma",
      balao="A ESPONJA!", bugTexto="GRRR!",
      pergunta=[fala(D, "Agora, o meu enigma!", "grave"), fala(D, "O que é que, quanto mais seca, mais molhada fica?", "grave")],
      roboFala=[fala(D, "A esponja, é claro!", "grave")], revela=[fala(N, "A toalha!", "x"), fala(N, "Quanto mais ela seca você, mais molhada ela fica!", "n")],
      depois=[fala(D, "Grrr... vocês vão ver!", "grave")], ponto=N),
 dict(id="vitoria", tipo="vitoriaGen", placar="TIME 4 × 0 DOUTOR", boom=True, falas=[fala(N, "Quatro a zero! Quantas vidas sobraram? Comenta!", "x")], cauda=0.3),
 dict(id="gancho_final", tipo="ganchoAmnesia", sfx=[(0.1, "glitch"), (1.0, "riser", 1.0), (2.1, "boom"), (2.15, "glitch")],
      falas=[fala(D, "Mas eu guardei um último raio!", "grave"), ("pausa", "0.7", ""), fala(N, "Ai... onde eu estou?", "q"), fala(N, "Quem... sou eu?", "q")], cauda=1.8),
]
montar("s2e4", CENAS, VOZ, contagem=3.0, transicao=10)
