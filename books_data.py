"""Dados dos Vols. 08-18 — Books Data Module.

Cada livro segue o mesmo esquema usado em generate_catalog.py.
"""

MORE_BOOKS = [
    # ─── 08 · Os 7 Hábitos das Pessoas Altamente Eficazes ───
    {
        "id": "sete_habitos", "vol": "08",
        "title_main": "Os 7", "title_sub": "Hábitos.",
        "short_title": "Os 7 Hábitos",
        "subtitle": "Lições poderosas para a transformação pessoal.",
        "author": "Stephen R. Covey",
        "year_orig": "1989", "year_br": "1991", "publisher": "Best Seller",
        "pages": "Aproximadamente 432 páginas", "pages_count": 25,
        "genre": "Liderança · Desenvolvimento pessoal",
        "category_kicker": "Liderança · Eficácia · Princípios",
        "motif": "seven",
        "palette": {"paper": "#F0EDE3", "ink": "#1C1C1C", "accent": "#7A2025",
                    "muted": "#7A7569", "hairline": "#CFC8B5", "subink": "#2A2A2A",
                    "paper_dark": "#DFDBD0"},
        "abstract": ("Resumo de <b>Os 7 Hábitos das Pessoas Altamente Eficazes</b>, "
                     "de Stephen R. Covey. Sintetiza os três hábitos da vitória privada "
                     "(eu), os três da vitória pública (com outros), e o sétimo da renovação."),
        "thesis": "Eficácia é caráter — não técnica. E caráter se constrói por princípios universais postos em hábito.",
        "headline_quote": "Entre estímulo e resposta há um espaço. Nesse espaço está a nossa liberdade.",
        "about_author": [
            "<b>Stephen R. Covey</b> (1932–2012) foi um educador, palestrante e consultor norte-"
            "americano, autor de uma das obras mais influentes do desenvolvimento pessoal "
            "do século XX.",
            "Doutorou-se em religião e treinou líderes de governos, multinacionais e forças armadas. "
            "<i>Os 7 Hábitos</i> (1989) consolidou décadas de leitura da literatura de auto-aperfeiçoamento "
            "americana — Covey afirmou ter notado que, a partir dos anos 1920, a ênfase migrou de "
            "<b>caráter</b> para <b>personalidade</b>. Seu projeto foi recuperar o eixo do caráter.",
            "Vendeu mais de 40 milhões de exemplares globalmente. É leitura obrigatória em programas "
            "de MBA, em academias militares e em treinamentos corporativos no mundo todo."],
        "big_idea": ("A eficácia é uma função de hábitos profundos, alinhados com princípios "
                     "universais. Covey organiza esses hábitos em três camadas: <b>vitória "
                     "privada</b> (sobre si), <b>vitória pública</b> (com outros) e <b>renovação</b> "
                     "(manutenção do sistema)."),
        "big_idea_extra": [
            "Os primeiros três hábitos te tiram da dependência e te levam à independência. "
            "Os três seguintes te levam da independência à <b>interdependência</b> — modo de "
            "operação mais maduro. O sétimo é o que mantém os outros seis afiados."],
        "chapters": [
            {"num": "01", "kicker": "Vitória privada",
             "title": "Seja proativo",
             "intro": ("Entre estímulo e resposta há um espaço, e nesse espaço mora a liberdade "
                       "humana. Pessoas proativas usam esse espaço para escolher; reativas o pulam "
                       "e culpam o estímulo."),
             "bullets": [
                 "<b>Linguagem reativa</b>: 'eu tenho que', 'eles me obrigaram', 'não posso'.",
                 "<b>Linguagem proativa</b>: 'eu escolho', 'eu prefiro', 'eu vou'.",
                 "Foque no círculo de influência (o que está em suas mãos), não no de preocupação.",
                 "Erros são para aprender — não para se identificar.",
             ],
             "callout_label": "REGRA",
             "callout": "A primeira responsabilidade da vida adulta é cuidar do espaço entre estímulo e resposta."},

            {"num": "02", "kicker": "Vitória privada",
             "title": "Comece com o objetivo em mente",
             "intro": ("Antes de mover, defina onde quer chegar. Covey sugere o exercício do "
                       "próprio funeral: imagine quem fala, o que dizem, o que faltou ser dito. "
                       "Esse é o seu compasso."),
             "bullets": [
                 "Escreva sua <b>missão pessoal</b>: 1–2 parágrafos, princípio + papéis principais.",
                 "Revise anualmente. Use como filtro de decisões.",
                 "Comece pelo fim — só assim você sabe que está caminhando, não correndo em círculos.",
                 "Liderança = subir na escada e ver se está apoiada na parede certa.",
             ],
             "callout_label": "EXERCÍCIO",
             "callout": "Escreva, esta semana, o que você gostaria que dissessem no seu funeral. É o seu mapa real."},

            {"num": "03", "kicker": "Vitória privada",
             "title": "Primeiro o mais importante",
             "intro": ("A matriz de Covey — Urgente × Importante. A maioria vive no Quadrante I "
                       "(urgente importante: crises) ou no III (urgente não-importante: "
                       "interrupções). A vida fica no <b>II</b>: importante, não-urgente."),
             "bullets": [
                 "Q I — Crises. Q II — Construção. Q III — Falsas urgências. Q IV — Desperdício.",
                 "Liderança vive no Q II: planejamento, relacionamentos, prevenção, recreação.",
                 "Reuniões semanais consigo: agenda do Q II antes da agenda do Q I.",
                 "Aprenda a dizer 'não' ao bom — para poder dizer 'sim' ao melhor.",
             ],
             "quote": "A chave não é priorizar o que está na agenda — é colocar suas prioridades na agenda.",
             "callout_label": "MATRIZ",
             "callout": "Quem só apaga incêndios nunca constrói. Reserve, esta semana, 3 horas de Q II antes que o Q I as tome."},

            {"num": "04", "kicker": "Vitória pública",
             "title": "Pensar ganha-ganha",
             "intro": ("Em qualquer relação humana, há cinco posturas possíveis: ganha-ganha, "
                       "ganha-perde, perde-ganha, perde-perde, e 'ganha-ganha ou não tem acordo'. "
                       "Só a primeira (e a última) constroem confiança a longo prazo."),
             "bullets": [
                 "Ganha-ganha é hábito, não técnica. Exige caráter de abundância.",
                 "Caráter de escassez vê toda vitória do outro como derrota sua.",
                 "Sem confiança, todo acordo desmonta — mesmo se escrito.",
                 "'Ganha-ganha ou nada' deixa portas abertas; pressão fecha-as.",
             ],
             "callout_label": "ABUNDÂNCIA",
             "callout": "Há bolo suficiente. Não é mentalidade ingênua — é a única coerente com cooperação humana de longo prazo."},

            {"num": "05", "kicker": "Vitória pública",
             "title": "Procure primeiro entender, depois ser entendido",
             "intro": ("A maioria escuta para responder, não para entender. Covey propõe a escuta "
                       "<b>empática</b>: ouvir até de fato reproduzir o sentimento e a lógica do "
                       "outro. Só então propor."),
             "bullets": [
                 "Quatro níveis de escuta: ignorar, fingir, ouvir seletivo, ouvir atentamente.",
                 "O quinto, raro: <b>escuta empática</b> — entrar no quadro do outro.",
                 "Diagnóstico antes de receita: médico que prescreve sem escutar é incompetente; conversa também.",
                 "Quando o outro se sente entendido, baixa a defesa e escuta de volta.",
             ],
             "callout_label": "REGRA DE OURO",
             "callout": "Primeiro entender. Não é simpatia — é diagnóstico. Sem diagnóstico, qualquer 'solução' que você propuser será irrelevante."},

            {"num": "06", "kicker": "Vitória pública",
             "title": "Sinergia",
             "intro": ("Sinergia é 1+1=3. Acontece quando duas pessoas com posturas ganha-ganha e "
                       "escuta empática criam algo que nenhuma delas teria criado sozinha. É a "
                       "essência da equipe."),
             "bullets": [
                 "Sinergia exige diferença — pessoas iguais não geram terceira via.",
                 "Comece valorizando a diferença em vez de buscar o consenso raso.",
                 "Resistência criativa: 'eu vejo diferente — vamos juntos achar uma terceira via'.",
                 "Sem hábitos 4 e 5, sinergia é só conflito mal-resolvido.",
             ],
             "callout_label": "FÓRMULA",
             "callout": "1+1=3 = ganha-ganha + escuta empática + valorização da diferença."},

            {"num": "07", "kicker": "Renovação",
             "title": "Afiar o instrumento",
             "intro": ("Você é o instrumento. Sem afiar, o resto se embota. Covey propõe quatro "
                       "dimensões de renovação: <b>física</b> (exercício, sono, alimentação), "
                       "<b>mental</b> (leitura, escrita, planejamento), <b>social/emocional</b> "
                       "(relações, serviço) e <b>espiritual</b> (sentido, meditação)."),
             "bullets": [
                 "Sem renovação, hábitos eficazes corroem-se com o tempo.",
                 "Hora por dia, dia por semana, semana por ano — renovação tem cadência.",
                 "Não é luxo: é manutenção. Atleta que não treina degenera.",
                 "Quatro frentes em paralelo: nenhuma compensa a ausência de outra.",
             ],
             "quote": "Afiar o instrumento não é fazer mais — é tornar sustentável fazer.",
             "callout_label": "MANUTENÇÃO",
             "callout": "1 hora por dia em renovação multiplica as 15 horas seguintes. Quem pula a primeira paga nas próximas."},

            {"num": "08", "kicker": "Síntese",
             "title": "Da dependência à interdependência",
             "intro": ("Covey fecha o livro com a tese de que os 7 hábitos formam um caminho: "
                       "dependência → independência → interdependência. A maioria fica parada na "
                       "passagem; alguns chegam à independência; poucos seguem à interdependência."),
             "bullets": [
                 "<b>Dependência</b>: 'você cuida de mim'.",
                 "<b>Independência</b>: 'eu cuido de mim'.",
                 "<b>Interdependência</b>: 'nós cuidamos uns dos outros melhor do que sozinhos'.",
                 "A meta não é virar autossuficiente — é virar capaz de cooperar profundamente.",
             ],
             "callout_label": "DESTINO",
             "callout": "Independência é vitória sobre infância. Interdependência é maturidade. Não pare na metade."},
        ],
        "insights": [
            ("01", "Caráter > Personalidade",
             "Covey nota que de 1776 a 1920 a literatura americana de sucesso era 'caráter' (Franklin); depois virou 'personalidade' (técnicas). Ele propõe recuperar o eixo do caráter."),
            ("02", "O espaço entre estímulo e resposta é o lar da liberdade humana",
             "Frase emprestada de Viktor Frankl. Cuidar desse espaço é a primeira tarefa adulta."),
            ("03", "Q II é onde se constrói a vida",
             "Quase tudo o que importa é importante mas não urgente: saúde, relacionamentos, planejamento, prevenção. Reserve tempo para o Q II antes que o Q I o devore."),
            ("04", "Escuta empática desarma 80% dos conflitos",
             "Quando o outro percebe que está sendo entendido, baixa a defesa. Aí, e só aí, conversa avança."),
            ("05", "Sinergia exige diferença",
             "Times de pessoas iguais não criam terceira via. Diferença é matéria-prima."),
            ("06", "Renovação tem 4 frentes — nenhuma compensa outra",
             "Físico, mental, emocional, espiritual. Ignorar uma corrompe as três."),
        ],
        "application": [
            ("Escreva sua missão pessoal", "1–2 parágrafos com princípios + papéis. Revise mensalmente."),
            ("Mapeie sua semana pela matriz", "Marque cada compromisso como I, II, III ou IV. Onde está a maioria do seu tempo?"),
            ("Reserve 3h de Q II por semana", "Bloco fixo. Planejamento, exercício, leitura, relacionamento — não-negociável."),
            ("Pratique escuta empática", "Em 1 conversa por dia, comprometa-se a só fazer perguntas — não argumentar — pelos primeiros 5 minutos."),
            ("Aprenda a dizer não ao bom", "Liste, esta semana, 3 'sins' que você precisa virar 'nãos' para preservar os 'sins' que importam."),
            ("Implante 1 hábito de renovação por frente", "1 físico, 1 mental, 1 emocional, 1 espiritual. Diários, simples, sustentáveis."),
        ],
        "quotes": [
            ("Entre estímulo e resposta há um espaço.", "Stephen Covey / Frankl"),
            ("Comece com o objetivo em mente.", "Hábito 2"),
            ("Primeiro entender, depois ser entendido.", "Hábito 5"),
            ("Sinergia é 1+1=3.", "Hábito 6"),
            ("Afiar o instrumento não é luxo — é manutenção.", "Hábito 7"),
            ("Dependência → Independência → Interdependência.", "Síntese"),
            ("A liderança sobe na escada antes de escalar.", "Síntese leitor"),
        ],
        "reflections": [
            "Qual a sua linguagem dominante hoje — reativa ou proativa? Anote 3 frases que você diz com frequência.",
            "Se você morresse este ano, o que você gostaria que dissessem — e quanto disso a sua vida hoje sustenta?",
            "Que 3 'sins' você precisa virar 'nãos' para que o seu Q II ganhe espaço?",
            "Em qual conflito recente você tentou ser entendido antes de entender — e como acabou?",
            "Que diferença num colaborador, parceiro ou filho seu você está combatendo quando deveria estar usando?",
            "Quais das 4 frentes (física, mental, emocional, espiritual) você está mais negligenciando — e há quanto tempo?",
        ],
        "last_word_title": "Sete hábitos. Uma vida.",
        "last_word_quote": "Eficácia é tudo o que sobra quando você para de tentar parecer eficaz e começa a viver pelos princípios que admira.",
    },

    # ─── 09 · Como Fazer Amigos e Influenciar Pessoas ───
    {
        "id": "amigos", "vol": "09",
        "title_main": "Como", "title_sub": "Fazer Amigos.",
        "short_title": "Como Fazer Amigos",
        "subtitle": "E influenciar pessoas.",
        "author": "Dale Carnegie",
        "year_orig": "1936", "year_br": "1947", "publisher": "Companhia Editora Nacional",
        "pages": "Aproximadamente 256 páginas", "pages_count": 25,
        "genre": "Comunicação · Habilidades sociais",
        "category_kicker": "Comunicação · Relações · Persuasão",
        "motif": "handshake",
        "palette": {"paper": "#F2EBD8", "ink": "#1A1F33", "accent": "#9C6B1F",
                    "muted": "#857B62", "hairline": "#CFC7B0", "subink": "#272D45",
                    "paper_dark": "#E3DBC0"},
        "abstract": ("Resumo do clássico de Dale Carnegie. Reúne os princípios para tratar "
                     "pessoas, fazer amizades, persuadir sem ofender e liderar sem ferir — "
                     "publicado em 1936 e ainda atual."),
        "thesis": "Quase todo conflito humano nasce da necessidade não atendida de se sentir importante. Quem reconhece isso, lidera relações.",
        "headline_quote": "Você pode fazer mais amigos em dois meses interessando-se pelos outros do que em dois anos tentando que os outros se interessem por você.",
        "about_author": [
            "<b>Dale Carnegie</b> (1888–1955) foi um educador americano nascido em uma "
            "fazenda do Missouri. Trabalhou como vendedor antes de descobrir a vocação como "
            "professor de oratória adulta.",
            "Em 1912 abriu o Dale Carnegie Course, ainda hoje uma das maiores escolas de "
            "comunicação do mundo. <i>Como Fazer Amigos e Influenciar Pessoas</i> (1936) "
            "destila quase 30 anos de observação clínica de adultos tentando se comunicar.",
            "O livro vendeu mais de 30 milhões de exemplares e mudou para sempre o vocabulário "
            "da auto-ajuda. Pode soar datado em superfície, mas seu núcleo — a fome humana "
            "por reconhecimento — segue intacto."],
        "big_idea": ("A pessoa média subestima radicalmente o impacto que tem nas relações — e "
                     "superestima a inteligência dos próprios argumentos. Carnegie inverte: o "
                     "que move outros não é a lógica do que você diz, é como você os faz se sentir. "
                     "Daí dezenas de princípios concretos, todos derivados desse insight central."),
        "chapters": [
            {"num": "01", "kicker": "Parte 1 · Tratar pessoas",
             "title": "Não critique, não condene, não reclame",
             "intro": ("Crítica raramente muda quem é criticado — quase sempre só endurece a defesa. "
                       "Carnegie abre o livro pedindo um exercício radical: trinta dias sem criticar "
                       "ninguém. Quase ninguém consegue."),
             "bullets": [
                 "Crítica fere o ego — e ego ferido contra-ataca, não muda.",
                 "Mesmo criminosos quase sempre se acham injustamente julgados.",
                 "Antes de criticar, pergunte: o que essa pessoa precisaria para mudar — e a crítica entrega isso?",
             ],
             "callout_label": "REGRA",
             "callout": "Crítica raramente educa. Quase sempre só ensina a esconder."},

            {"num": "02", "kicker": "Parte 1",
             "title": "Faça apreço sincero",
             "intro": ("Não bajulação — apreço. A diferença: bajulação é insincera, focada no que "
                       "se quer obter; apreço nota algo real e o nomeia. A maioria das pessoas vive "
                       "anos sem ouvir um apreço genuíno."),
             "bullets": [
                 "Note algo específico. Diga em voz alta. Sem pedir nada em troca.",
                 "Apreço é alimento; a maioria das pessoas vive desnutrida.",
                 "Bajulação morre na primeira repetição; apreço cresce com ela.",
                 "Carnegie cita William James: o desejo mais profundo é o de ser apreciado.",
             ],
             "callout_label": "PRATIQUE",
             "callout": "Faça hoje, sem aviso, um elogio específico a três pessoas. Observe o que volta nas semanas seguintes."},

            {"num": "03", "kicker": "Parte 1",
             "title": "Desperte um desejo no outro",
             "intro": ("Você não vai conseguir o que quer pedindo o que quer. Vai conseguir "
                       "mostrando ao outro como o que você quer atende ao que <b>ele</b> quer. "
                       "É a base da persuasão honesta."),
             "bullets": [
                 "Antes de pedir: 'o que essa pessoa quer mesmo?'",
                 "Conecte o pedido ao desejo dela — não ao seu.",
                 "Persuasão honesta é traduzir, não manipular.",
                 "Ford: 'Se há um segredo no sucesso, é olhar pelo ponto de vista do outro.'",
             ],
             "callout_label": "FÓRMULA",
             "callout": "Pedido eficaz = sua necessidade + como ela serve à necessidade do outro."},

            {"num": "04", "kicker": "Parte 2 · Fazer amigos",
             "title": "Interesse-se sinceramente pelos outros",
             "intro": ("Toda relação humana começa pela mesma porta: alguém se interessa de "
                       "verdade pelo outro. Não fingido. Não estratégico. Genuíno."),
             "bullets": [
                 "Cães sabem disso há milênios — daí serem o exemplo de Carnegie no cap. 4.",
                 "Pergunte com paciência. Lembre-se de respostas. Volte ao assunto na próxima conversa.",
                 "Interesse sincero é raro — e por isso, vale ouro.",
                 "Sorria. Lembre-se de nomes. Use o nome da pessoa na conversa.",
             ],
             "quote": "O nome de uma pessoa é, para ela, o som mais doce e importante de qualquer idioma.",
             "callout_label": "PRÁTICA",
             "callout": "Repita o nome 3 vezes na primeira conversa. Anote o nome na sua agenda. Use-o na próxima."},

            {"num": "05", "kicker": "Parte 2",
             "title": "Faça o outro se sentir importante",
             "intro": ("O desejo mais profundo, segundo Carnegie/James/Dewey: ser apreciado, "
                       "importante. Fazer alguém se sentir importante — honestamente — é o gesto "
                       "social mais valioso disponível."),
             "bullets": [
                 "Importância falsa é detectada e rejeitada.",
                 "Importância real é nota: o tempo dedicado, a memória do detalhe, o cumprimento sincero.",
                 "Empregados, garçons, motoristas — todos sentem.",
                 "Quem entrega importância recebe lealdade.",
             ],
             "callout_label": "PRINCÍPIO",
             "callout": "Toda pessoa que cruza seu dia tem alguma coisa pela qual te é superior. Encontre essa coisa e reconheça."},

            {"num": "06", "kicker": "Parte 3 · Persuadir",
             "title": "Evite discussões — ganhe-as sem brigar",
             "intro": ("A única forma de ganhar uma discussão é evitá-la. Mesmo ganhando, você "
                       "perde — perde a pessoa, a chance, o crédito futuro. Quem discute por "
                       "esporte está fora do jogo das relações duradouras."),
             "bullets": [
                 "Discordar sem brigar: 'Posso estar errado, mas...'",
                 "Admita seu erro depressa e enfaticamente — antes que o outro acuse.",
                 "Inicie de forma amigável. Faça o outro dizer 'sim' várias vezes antes de chegar ao tópico.",
                 "Mostre respeito pelas opiniões alheias — mesmo as que você considera tolas.",
             ],
             "callout_label": "REGRA",
             "callout": "Você nunca vai vencer pelo argumento. Pode vencer pelo respeito. Escolha qual."},

            {"num": "07", "kicker": "Parte 4 · Liderar",
             "title": "Liderar sem ferir",
             "intro": ("Liderar é fazer pessoas mudarem sem que se sintam menosprezadas. Carnegie "
                       "lista uma série de princípios para corrigir, sugerir, delegar — todos "
                       "com o mesmo eixo: preserve o ego do outro enquanto pede mudança."),
             "bullets": [
                 "Comece com elogio sincero, depois mencione o erro, depois sugira correção.",
                 "Critique 'a coisa' (a entrega, o trabalho), não a pessoa.",
                 "Faça perguntas em vez de dar ordens.",
                 "Deixe o outro 'salvar a face' — mesmo quando errou.",
             ],
             "callout_label": "LIDERANÇA",
             "callout": "Quem fere pra liderar lidera por enquanto. Quem preserva o ego enquanto pede mudança lidera por décadas."},

            {"num": "08", "kicker": "Síntese",
             "title": "A engrenagem por trás de tudo",
             "intro": ("Todos os princípios derivam de uma única chave: cada pessoa quer se sentir "
                       "importante, ouvida, reconhecida. Quem entrega essas três coisas vira referência "
                       "social — sem precisar de cargo ou poder formal."),
             "bullets": [
                 "Importância, escuta, reconhecimento — a tríade.",
                 "Sinceridade é o ingrediente que separa o método da manipulação.",
                 "Carnegie é um livro de caráter disfarçado de livro de técnica.",
                 "A diferença entre influência e manipulação é se o outro saberia, se descobrisse o seu motivo.",
             ],
             "quote": "Se há um único segredo do sucesso, é a capacidade de ver as coisas do ponto de vista do outro tão bem quanto do seu próprio.",
             "callout_label": "TESTE",
             "callout": "Se o outro soubesse exatamente seu motivo, ele se sentiria respeitado ou usado? Esse é o teste."},
        ],
        "insights": [
            ("01", "Ego ferido não muda — endurece",
             "Crítica raramente educa. Quase sempre só ensina a esconder."),
            ("02", "Apreço é alimento; nome é doce; pergunta sincera é raridade",
             "Três gestos pequenos que poucos fazem — e que, juntos, mudam qualquer relação."),
            ("03", "Persuasão honesta = traduzir, não manipular",
             "Conectar o seu pedido ao desejo do outro não é manipulação — desde que o desejo seja real e a tradução honesta."),
            ("04", "Discutir é perder, mesmo ganhando",
             "Provar que o outro está errado fere o ego — e ego ferido contra-ataca."),
            ("05", "Liderar é pedir mudança preservando ego",
             "O líder eficaz é o que faz as pessoas mudarem sem se sentirem diminuídas."),
            ("06", "Sinceridade separa método de manipulação",
             "Os mesmos passos podem ser influência (com motivo honesto) ou manipulação (com motivo oculto). A diferença é interna."),
        ],
        "application": [
            ("Trinta dias sem criticar", "Comece esta semana. Cada vez que ia criticar, pause. Observe o efeito nas relações."),
            ("Três apreços por dia", "Note algo real em três pessoas e diga em voz alta — sem pedir nada em troca."),
            ("Lembre nomes", "Repita o nome 3× na primeira conversa. Anote em algum lugar."),
            ("Pergunte e escute", "Em cada conversa hoje, faça 2 perguntas reais — e ouça até o outro terminar."),
            ("Pratique o sanduíche", "Quando precisar corrigir, comece com elogio sincero, mencione o ajuste, termine com confiança no outro."),
            ("Olhe pelo ângulo do outro", "Antes de cada pedido importante, escreva 1 frase: 'pelo ponto de vista dele, isso parece...'."),
        ],
        "quotes": [
            ("O nome é o som mais doce de qualquer idioma.", "Princípio do nome"),
            ("Você pode fazer mais amigos em dois meses interessando-se pelos outros do que em dois anos tentando o contrário.", "Carnegie"),
            ("A única forma de ganhar uma discussão é evitá-la.", "Carnegie"),
            ("Pessoas querem se sentir importantes.", "Princípio-mãe"),
            ("Crítica é como um pombo-correio: sempre volta.", "Provérbio Carnegie"),
            ("Olhe pelo ângulo do outro.", "Henry Ford, em Carnegie"),
            ("Conduzir é fazer as pessoas mudarem sem se sentirem feridas.", "Síntese"),
        ],
        "reflections": [
            "Quem te criticou esta semana? E você criticou — direta ou indiretamente — quantas pessoas?",
            "Quantos elogios sinceros e específicos você fez nos últimos sete dias?",
            "Em qual conversa recente você tentou ganhar uma discussão — e o que isso custou na relação?",
            "Qual pessoa próxima você não conhece o suficiente — porque nunca perguntou direito?",
            "Em qual relação você está pedindo mudança sem preservar o ego do outro?",
            "Se o outro soubesse seu motivo real ao influenciá-lo, ele se sentiria respeitado ou usado?",
        ],
        "last_word_title": "Pequenas cortesias.",
        "last_word_quote": "Influenciar pessoas é, no fim, levar a sério o desejo que cada uma tem de ser tratada como importa.",
    },

    # ─── 10 · O Homem Mais Rico da Babilônia ───
    {
        "id": "babilonia", "vol": "10",
        "title_main": "O Homem", "title_sub": "da Babilônia.",
        "short_title": "O Homem Mais Rico da Babilônia",
        "subtitle": "Os princípios eternos do sucesso financeiro.",
        "author": "George S. Clason",
        "year_orig": "1926", "year_br": "1953", "publisher": "HarperCollins",
        "pages": "Aproximadamente 192 páginas", "pages_count": 25,
        "genre": "Educação financeira · Parábola",
        "category_kicker": "Finanças · Parábola · Sabedoria antiga",
        "motif": "column",
        "palette": {"paper": "#EFE7CE", "ink": "#2E1B0F", "accent": "#8C6F1A",
                    "muted": "#7E704F", "hairline": "#D2C8A8", "subink": "#3D2A1E",
                    "paper_dark": "#E0D6B5"},
        "abstract": ("Resumo de <b>O Homem Mais Rico da Babilônia</b>, parábola de George S. Clason "
                     "que organiza em forma de história os princípios universais do enriquecimento "
                     "pessoal: pague-se primeiro, controle gastos, faça o ouro multiplicar."),
        "thesis": "Riqueza não é mistério antigo nem privilégio moderno — é uma técnica simples que poucos têm a paciência de aplicar.",
        "headline_quote": "Uma parte de tudo o que você ganha é sua para guardar.",
        "about_author": [
            "<b>George Samuel Clason</b> (1874–1957) foi um soldado da guerra hispano-americana, "
            "editor de mapas e empresário norte-americano. Em 1926 começou a publicar pequenas "
            "parábolas sobre dinheiro em folhetos distribuídos por bancos e seguradoras.",
            "As parábolas se ambientam na antiga Babilônia — primeira civilização a documentar "
            "extensivamente comércio, juros e poupança. Clason usa o cenário para tornar atemporais "
            "princípios que, no século XX, soariam moralistas.",
            "<i>O Homem Mais Rico da Babilônia</i> nunca saiu de catálogo desde 1926. É leitura "
            "obrigatória em programas de educação financeira de governos e ONGs no mundo todo."],
        "big_idea": ("Os sete remédios para uma carteira vazia, transmitidos pelo personagem "
                     "Arkad ao príncipe da Babilônia, sintetizam o que toda família com algum "
                     "patrimônio descobre cedo ou tarde: <b>guarde 10% sempre, controle gastos, "
                     "invista, proteja-se, tenha casa, garanta renda futura, aumente sua "
                     "capacidade de ganhar</b>."),
        "chapters": [
            {"num": "01", "kicker": "Remédio 1",
             "title": "Engorde a sua bolsa",
             "intro": ("Pague-se primeiro. De cada dez moedas que entram, guarde uma. Não nove — "
                       "uma. A regra de Arkad é a mais simples e a mais ignorada da história "
                       "financeira."),
             "bullets": [
                 "10% para você, antes de qualquer despesa. Automático.",
                 "Não 'sobra' do mês — sai primeiro.",
                 "Aplicado por décadas, esse 10% se torna a maior fonte de renda da família.",
                 "Ricos famosos quase sempre começam por essa regra.",
             ],
             "callout_label": "REGRA 1",
             "callout": "10% de TUDO o que você ganha é seu para guardar. Antes do aluguel, do mercado, do imposto."},

            {"num": "02", "kicker": "Remédio 2",
             "title": "Controle os gastos",
             "intro": ("Sem controle, qualquer renda evapora. Não é uma questão de salário — é de "
                       "estrutura. O que não tem orçamento vira despesa; o que tem orçamento vira "
                       "decisão."),
             "bullets": [
                 "Liste tudo que entra. Liste tudo que sai. Compare.",
                 "Distinga necessidades de desejos. A maioria mistura.",
                 "Sem orçamento, o dinheiro pertence aos seus impulsos.",
                 "Quem ganha pouco e controla termina mais rico que quem ganha muito e não controla.",
             ],
             "callout_label": "REGRA 2",
             "callout": "Sem orçamento, salários se vaporizam. Com orçamento, qualquer renda começa a render."},

            {"num": "03", "kicker": "Remédio 3",
             "title": "Multiplique o ouro",
             "intro": ("Guardar não basta — é preciso fazer o dinheiro trabalhar. Investir é "
                       "transformar moedas paradas em <b>servos</b> que trabalham por você."),
             "bullets": [
                 "Cada moeda investida é um servo silencioso.",
                 "Os filhos das suas moedas também trabalham — juros compostos.",
                 "Comece pequeno. O importante é começar.",
                 "Sem juros, mesmo grandes patrimônios desaparecem em uma geração.",
             ],
             "callout_label": "REGRA 3",
             "callout": "Cada moeda parada é um servo dormindo. Empregue todas — mesmo se for trabalho leve."},

            {"num": "04", "kicker": "Remédio 4",
             "title": "Proteja seu ouro do prejuízo",
             "intro": ("Investir sem proteger é caminho para perder tudo. Arkad alerta: estude "
                       "antes de investir, busque conselho de quem entende, não corra atrás de "
                       "promessas extraordinárias."),
             "bullets": [
                 "Estude antes. Não invista no que não entende.",
                 "Procure aconselhar-se com quem prosperou no campo — não com quem fala bonito.",
                 "Promessas extraordinárias quase sempre são golpes.",
                 "Proteja o principal antes de tentar ganhos extras.",
             ],
             "callout_label": "REGRA 4",
             "callout": "Primeira regra do investidor: não perca dinheiro. Segunda regra: não esqueça a primeira."},

            {"num": "05", "kicker": "Remédio 5",
             "title": "Tenha a sua casa",
             "intro": ("Casa própria, para Arkad, não é luxo — é o pilar da segurança familiar. "
                       "Aluguel é despesa permanente; casa é despesa que termina e vira patrimônio."),
             "bullets": [
                 "Casa não para investir — casa para morar e ter base.",
                 "Termina um dia. Aluguel não termina nunca.",
                 "Cuidado para que a casa não vire um passivo gigante (cuidado também citado por Kiyosaki, séculos depois).",
                 "Comprar na medida certa, não na medida da vaidade.",
             ],
             "callout_label": "REGRA 5",
             "callout": "Compre casa proporcional à sua vida, não à sua aparência. A maior parte das ruínas financeiras começa aí."},

            {"num": "06", "kicker": "Remédio 6",
             "title": "Garanta renda futura",
             "intro": ("Você vai envelhecer. Vai parar de trabalhar. Garanta, desde já, que haja "
                       "renda para essa fase — para você e para os seus."),
             "bullets": [
                 "Previdência (privada, pública), seguros, patrimônio que rende.",
                 "Quanto antes começa, menor o esforço mensal.",
                 "Pensar na velhice é um ato de amor presente, não de medo.",
                 "Sem renda futura, dependência da família é certa.",
             ],
             "callout_label": "REGRA 6",
             "callout": "A pessoa de 40 que não pensa nos 70 é a de 70 que dependerá dos 40 dos outros."},

            {"num": "07", "kicker": "Remédio 7",
             "title": "Aumente a sua capacidade de ganhar",
             "intro": ("Não basta poupar do que se ganha — é preciso ganhar mais. Educação, "
                       "habilidade, reputação. Quanto mais você vale para o mundo, mais ele paga."),
             "bullets": [
                 "Estude. Especialize-se. Aprenda algo novo todo trimestre.",
                 "Pague suas dívidas — reputação é parte do salário.",
                 "Cuide do corpo, da família, da palavra dada.",
                 "Reputação se constrói lenta e se perde rápido.",
             ],
             "quote": "Quem busca conhecimento agarrado ao trabalho, dobra a colheita.",
             "callout_label": "REGRA 7",
             "callout": "Pague suas dívidas. Estude todo trimestre. Cuide do nome. As três coisas, juntas, multiplicam renda."},

            {"num": "08", "kicker": "Síntese",
             "title": "As cinco leis do ouro",
             "intro": ("Arkad consolida tudo em cinco leis: o ouro vai de bom grado a quem o poupa, "
                       "a quem o multiplica com sabedoria, a quem o protege com cautela; foge "
                       "de quem o usa em negócios que não domina; foge de quem segue conselhos "
                       "de quem não entende."),
             "bullets": [
                 "Lei 1 — O ouro vem em fluxo crescente para quem poupa 10%.",
                 "Lei 2 — O ouro trabalha de bom grado para quem o emprega com sabedoria.",
                 "Lei 3 — O ouro se mantém com quem o protege com investimentos sólidos.",
                 "Lei 4 — O ouro escapa de quem investe no que não domina.",
                 "Lei 5 — O ouro foge de quem segue conselhos românticos ou de inexperientes.",
             ],
             "callout_label": "SÍNTESE",
             "callout": "As cinco leis do ouro têm 2.500 anos. Ainda funcionam. Só esquecem da existência delas as gerações que se acham especiais."},
        ],
        "insights": [
            ("01", "10% é o número universal",
             "Apareceu na Babilônia, na Bíblia, em Carnegie, em Kiyosaki. Não é mágico — é matemática composta aplicada a renda média."),
            ("02", "Salário não enriquece — sistema enriquece",
             "Quem ganha pouco e poupa termina mais rico que quem ganha muito e gasta tudo. É sempre verdade."),
            ("03", "Investir sem entender é apostar",
             "A maioria das ruínas financeiras vem de investimentos em o que o investidor 'achava que sabia'."),
            ("04", "Casa pode ser segurança — ou armadilha",
             "Casa proporcional é base de família. Casa desproporcional é hipoteca da liberdade."),
            ("05", "Velhice começa aos 30",
             "Quem pensa em aposentadoria aos 30 chega bem. Quem deixa para os 50 fica refém da família."),
            ("06", "Reputação é parte do salário",
             "O quanto você cobra é função do quanto você vale — e isso inclui o nome, não só a competência."),
        ],
        "application": [
            ("Comece com 10% imediatamente", "Mesmo se for 10% de pouco. O hábito vale mais do que o valor."),
            ("Automatize a poupança", "Antes que o salário chegue ao corrente, ele vai para a poupança/investimento. Sem decisão mensal."),
            ("Faça seu primeiro orçamento", "Liste todos os gastos do último mês. Categorize. Veja o tamanho do estrago."),
            ("Estude antes de investir", "Não invista no que não entende. Cada produto financeiro merece 1 hora de pesquisa."),
            ("Compre casa pela sua vida", "Não pela aparência. Não financie 30 anos do seu salário em vaidade."),
            ("Aumente capacidade de ganhar", "1 curso por semestre. 1 livro por mês. 1 nova habilidade por ano."),
        ],
        "quotes": [
            ("Uma parte do que você ganha é sua para guardar.", "Primeira regra"),
            ("As moedas que você guarda são servos que trabalham por você.", "Arkad"),
            ("O ouro foge de quem investe no que não entende.", "Lei 4 do ouro"),
            ("Reputação é parte do salário.", "Síntese"),
            ("A casa é proporcional à vida, não à aparência.", "Regra 5"),
            ("Quem busca conhecimento dobra a colheita.", "Arkad"),
            ("Não é o quanto você ganha — é o quanto você guarda.", "Síntese"),
        ],
        "reflections": [
            "Que percentual da sua renda foi automaticamente para poupança/investimento neste mês?",
            "Em qual gasto recente, no fundo, você sabia que estava trocando 'desejo' por 'necessidade'?",
            "Quanto você sabe sobre os investimentos onde seu dinheiro está hoje?",
            "Que parte da sua vida adulta está sustentada por aluguel ou financiamento desproporcional?",
            "O que você está fazendo agora para garantir renda quando parar de trabalhar?",
            "Que habilidade nova você aprendeu nos últimos 12 meses — e quanto ela aumentou sua capacidade de cobrar?",
        ],
        "last_word_title": "Sete remédios.",
        "last_word_quote": "Riqueza não é um segredo da Babilônia — é uma disciplina silenciosa que cabe em sete frases.",
    },

    # ─── 11 · O Monge e o Executivo ───
    {
        "id": "monge", "vol": "11",
        "title_main": "O Monge", "title_sub": "e o Executivo.",
        "short_title": "O Monge e o Executivo",
        "subtitle": "Uma história sobre a essência da liderança.",
        "author": "James C. Hunter",
        "year_orig": "1998", "year_br": "2004", "publisher": "Sextante",
        "pages": "Aproximadamente 144 páginas", "pages_count": 25,
        "genre": "Liderança · Parábola",
        "category_kicker": "Liderança · Servidora · Parábola",
        "motif": "mountain",
        "palette": {"paper": "#EBEDE5", "ink": "#1F2A30", "accent": "#557361",
                    "muted": "#76817A", "hairline": "#C5CCC1", "subink": "#293740",
                    "paper_dark": "#D9DCCF"},
        "abstract": ("Resumo de <b>O Monge e o Executivo</b>, parábola de James C. Hunter sobre "
                     "liderança servidora. Um executivo em crise passa uma semana em um mosteiro "
                     "e descobre, com um monge improvável, que liderar é servir."),
        "thesis": "Liderança não é autoridade conferida por um cargo — é influência ganha por serviço, caráter e amor.",
        "headline_quote": "Liderar é identificar e satisfazer as necessidades legítimas das pessoas e remover os obstáculos para que se sobressaiam.",
        "about_author": [
            "<b>James C. Hunter</b> é um consultor em gestão e liderança norte-americano. Após "
            "anos no mercado corporativo, dedicou-se a treinar líderes em empresas como GM, "
            "Best Buy e Procter & Gamble.",
            "<i>O Monge e o Executivo</i> (1998) é o seu livro mais conhecido. Em formato de "
            "parábola — cinco dias num retiro num mosteiro — sintetiza décadas de leitura de "
            "Robert Greenleaf (liderança servidora) e a tradição cristã sobre amor ágape.",
            "É leitura recorrente em programas corporativos de liderança no Brasil e nos EUA. "
            "Hunter publicou também <i>Como se Tornar um Líder Servidor</i>, expandindo o método."],
        "big_idea": ("O executivo John, em crise familiar e profissional, passa cinco dias em um "
                     "mosteiro liderado por irmão Simeão — que descobrimos ser um ex-CEO de Wall "
                     "Street. Ao longo da semana, Simeão desconstrói a ideia ocidental de "
                     "liderança como poder e propõe outra: liderança como serviço."),
        "chapters": [
            {"num": "01", "kicker": "Dia 1",
             "title": "Definições",
             "intro": ("Liderança não é o que se exerce sobre pessoas — é o que se exerce com "
                       "elas. Hunter define liderança como influência: capacidade de fazer com que "
                       "os outros trabalhem com entusiasmo pelos objetivos do grupo."),
             "bullets": [
                 "<b>Poder</b>: forçar alguém a fazer o que você quer. Funciona, mas desgasta a relação.",
                 "<b>Autoridade</b>: fazer alguém querer fazer o que você quer. Funciona e fortalece.",
                 "Cargo dá poder; caráter dá autoridade.",
                 "Liderar pela autoridade é o objetivo — não pelo poder.",
             ],
             "callout_label": "DEFINIÇÃO",
             "callout": "Poder se exerce pelo cargo. Autoridade se exerce pelo caráter. Quem sabe a diferença começa a liderar."},

            {"num": "02", "kicker": "Dia 2",
             "title": "Modelos antigos vs novo paradigma",
             "intro": ("Liderança piramidal antiga: o chefe no topo, todos servindo o chefe. "
                       "Liderança servidora: o líder na base, identificando o que cada um precisa "
                       "para fazer seu melhor — e removendo obstáculos."),
             "bullets": [
                 "Pirâmide invertida: cliente no topo, líder na base.",
                 "Líder serve o time. Time serve o cliente.",
                 "Servir não é submissão — é colocar a missão antes do ego.",
                 "Servir é diferente de bajular. Servir cobra resultados.",
             ],
             "callout_label": "INVERSÃO",
             "callout": "Inverta a pirâmide. Cliente no alto. Você na base. Veja como as decisões mudam."},

            {"num": "03", "kicker": "Dia 3",
             "title": "Necessidades vs vontades",
             "intro": ("Liderança servidora não é fazer todo mundo feliz. É identificar as "
                       "<b>necessidades legítimas</b> da equipe (não as vontades). Pode incluir "
                       "feedback duro, cobrança, demissões."),
             "bullets": [
                 "<b>Vontade</b>: o que a pessoa diz que quer. Pode ser miopia momentânea.",
                 "<b>Necessidade legítima</b>: o que ela precisa para crescer. Inclui verdade.",
                 "Servir é entregar necessidades, mesmo quando contraria vontades.",
                 "Pais sábios sabem disso há séculos. Líderes precisam aprender.",
             ],
             "callout_label": "PRINCÍPIO",
             "callout": "Servir não é agradar. Servir é entregar o que constrói, mesmo quando o outro queria outra coisa."},

            {"num": "04", "kicker": "Dia 4",
             "title": "Amor ágape",
             "intro": ("Hunter resgata a palavra grega <i>ágape</i> — amor como ação, não "
                       "sentimento. Ágape é paciência, bondade, ausência de inveja, respeito, "
                       "perdão, honestidade, compromisso. Liderar pelo amor ágape é, na prática, "
                       "agir assim — independente do que se sente."),
             "bullets": [
                 "<b>Ágape</b> é verbo, não sentimento.",
                 "Paciente. Bondoso. Sem inveja. Sem vaidade. Sem arrogância.",
                 "Não guarda rancor. Não age egoisticamente. Não se irrita facilmente.",
                 "Liderança por ágape funciona em famílias, salas de aula e empresas.",
             ],
             "quote": "Amor — ágape — é o que constrói. Tudo o mais administra.",
             "callout_label": "ATITUDE",
             "callout": "Amor ágape não é sentimento. É ação. Você não precisa sentir — precisa fazer."},

            {"num": "05", "kicker": "Dia 5",
             "title": "Caráter como base",
             "intro": ("Tudo que Simeão ensina pressupõe caráter. Sem caráter, técnicas de "
                       "liderança viram manipulação. Caráter é cumprir promessas, agir com "
                       "integridade, sustentar princípios sob pressão."),
             "bullets": [
                 "Caráter é o que você faz quando ninguém está olhando.",
                 "Sem caráter, a equipe vê — e duvida.",
                 "Construído por escolhas pequenas, diárias, cumpridas.",
                 "Reconstruí-lo após quebra é trabalho de anos.",
             ],
             "callout_label": "BASE",
             "callout": "Toda técnica de liderança é maquiagem sobre caráter. Sem o segundo, a primeira é cosmética."},

            {"num": "06", "kicker": "Aplicação 1",
             "title": "Líder em casa",
             "intro": ("John percebe, no retiro, que seu maior fracasso não é profissional — é "
                       "familiar. Liderança servidora começa em casa: filhos, cônjuge. Quem "
                       "lidera bem o pequeno círculo lidera bem o grande."),
             "bullets": [
                 "Como você fala com seu filho quando está cansado revela o líder que você é.",
                 "Família é o laboratório onde a liderança se prova.",
                 "Cuidado com 'líder no escritório, ditador em casa'.",
                 "Servir em casa é exigente — não há crachá para escudar.",
             ],
             "callout_label": "TESTE",
             "callout": "Pergunte ao seu cônjuge e filhos como você lidera. A resposta vale mais que qualquer feedback corporativo."},

            {"num": "07", "kicker": "Aplicação 2",
             "title": "Mudar é decisão diária",
             "intro": ("John volta ao mundo com a decisão de mudar — mas Hunter alerta que mudar é "
                       "trabalho de uma vida, não de uma semana. A liderança servidora se torna "
                       "real só pela repetição."),
             "bullets": [
                 "Cada conversa é uma nova oportunidade de servir.",
                 "Pequenas escolhas constroem reputação de liderança.",
                 "Você vai voltar a ser o velho líder muitas vezes. Volte de novo.",
                 "Comunidades de prática (mentor, grupos) ajudam.",
             ],
             "callout_label": "VERDADE",
             "callout": "Você não vira líder servidor. Você decide ser, todo dia, em cada conversa, durante o resto da vida."},

            {"num": "08", "kicker": "Síntese",
             "title": "Liderar é servir",
             "intro": ("A síntese de Simeão: liderar é identificar e satisfazer necessidades "
                       "legítimas, remover obstáculos, e fazer isso com paciência, bondade e "
                       "honestidade. Não é teoria — é prática diária."),
             "bullets": [
                 "Identificar necessidades.",
                 "Remover obstáculos.",
                 "Atuar com ágape.",
                 "Sustentar pelo caráter.",
             ],
             "quote": "O melhor líder é aquele que serve, não o que é servido.",
             "callout_label": "DEFINIÇÃO FINAL",
             "callout": "Liderança = identificar necessidades + remover obstáculos + agir com ágape + sustentar pelo caráter. Quatro componentes. Uma vida."},
        ],
        "insights": [
            ("01", "Cargo dá poder; caráter dá autoridade",
             "Você pode ser chefe sem ser líder. Pode ser líder sem ser chefe. O cargo é da empresa; a autoridade, sua."),
            ("02", "Servir não é agradar",
             "Servir inclui dizer a verdade, dar feedback duro, demitir quando preciso. Não é gentileza débil."),
            ("03", "Vontade ≠ necessidade",
             "O time pode querer X mas precisar de Y. Liderança servidora entrega Y, com paciência."),
            ("04", "Ágape é verbo",
             "Não precisa sentir para fazer. Liderar por amor ágape é uma decisão de ação, não de sentimento."),
            ("05", "Família é o laboratório real",
             "Quem lidera bem no escritório e mal em casa não é líder — é gestor de aparências."),
            ("06", "Mudar é vida toda, não semana",
             "Não há transformação instantânea. Há decisão diária."),
        ],
        "application": [
            ("Inverta sua pirâmide mental", "Cliente no alto. Sua equipe no meio. Você na base. Tome as decisões da semana com essa imagem."),
            ("Identifique uma necessidade hoje", "Pergunte a 1 pessoa da sua equipe: 'do que você precisa esta semana para fazer seu melhor?' Entregue."),
            ("Remova 1 obstáculo", "Liste 5 obstáculos da sua equipe. Comprometa-se a remover 1 nos próximos 7 dias."),
            ("Aja com ágape em 1 conflito", "Paciência, bondade, ausência de mágoa, perdão. Em pelo menos 1 conflito da semana."),
            ("Lidere em casa", "Aplique os mesmos 4 princípios a 1 pessoa da família. Pode ser mais difícil que no trabalho."),
            ("Reveja semanalmente", "10 minutos. Em quais momentos eu liderei por poder? E por autoridade? O que faço diferente?"),
        ],
        "quotes": [
            ("Cargo dá poder; caráter dá autoridade.", "Hunter"),
            ("Liderar é servir.", "Tese central"),
            ("Servir não é agradar; é entregar o que constrói.", "Hunter"),
            ("Ágape é verbo, não sentimento.", "Capítulo 4"),
            ("Inverta a pirâmide.", "Princípio"),
            ("O melhor líder é o que serve.", "Hunter"),
            ("Caráter é o que você faz quando ninguém olha.", "Síntese"),
        ],
        "reflections": [
            "Em qual situação recente você liderou pelo poder do cargo, em vez da autoridade do caráter?",
            "Qual necessidade legítima da sua equipe (não vontade) você está adiando entregar?",
            "Como você lidera em casa? Pergunte ao seu cônjuge ou filhos — eles vão saber.",
            "Em qual relação você precisa praticar ágape como verbo, esta semana — não esperar sentir?",
            "Que obstáculo você poderia remover do caminho da sua equipe nos próximos 7 dias?",
            "Quais princípios você sustentaria sob pressão — e como você sabe?",
        ],
        "last_word_title": "Servir é liderar.",
        "last_word_quote": "Liderança é serviço repetido. Quem entende isso para de cobrar autoridade — e começa a recebê-la.",
    },

    # ─── 12 · Inteligência Emocional ───
    {
        "id": "ie", "vol": "12",
        "title_main": "Inteligência", "title_sub": "Emocional.",
        "short_title": "Inteligência Emocional",
        "subtitle": "A teoria revolucionária que redefine o que é ser inteligente.",
        "author": "Daniel Goleman",
        "year_orig": "1995", "year_br": "1996", "publisher": "Objetiva",
        "pages": "Aproximadamente 376 páginas", "pages_count": 25,
        "genre": "Psicologia · Neurociência aplicada",
        "category_kicker": "Psicologia · Neurociência · Relações",
        "motif": "heartbrain",
        "palette": {"paper": "#EFEEEA", "ink": "#26224A", "accent": "#C46266",
                    "muted": "#7B7682", "hairline": "#CCC9C2", "subink": "#322C5E",
                    "paper_dark": "#DFDED9"},
        "abstract": ("Resumo de <b>Inteligência Emocional</b>, de Daniel Goleman. Reúne os "
                     "cinco pilares (autoconsciência, autorregulação, motivação, empatia, "
                     "habilidade social), o sequestro da amígdala e o caso para que o QE "
                     "importe mais que o QI."),
        "thesis": "QE pode importar mais que QI. Quem domina as próprias emoções e lê as dos outros, lidera, prospera e ama melhor.",
        "headline_quote": "Em um sentido muito real, todos nós temos duas mentes — uma que pensa e outra que sente.",
        "about_author": [
            "<b>Daniel Goleman</b> é psicólogo americano, doutor em psicologia cognitiva por "
            "Harvard e ex-jornalista de ciência do <i>New York Times</i>. Estudou meditação na "
            "Índia, escreveu sobre neurociência durante duas décadas no NYT e popularizou conceitos "
            "que circulavam em laboratórios.",
            "<i>Inteligência Emocional</i> (1995) consolidou décadas de pesquisa em "
            "neurociência cognitiva (Joseph LeDoux, Antonio Damásio, Howard Gardner). O termo "
            "'inteligência emocional' havia sido cunhado por Salovey e Mayer em 1990 — Goleman "
            "o tirou do laboratório.",
            "Publicou outros livros essenciais: <i>Trabalhando com a Inteligência Emocional</i>, "
            "<i>Foco</i>, <i>Inteligência Social</i>. É um dos divulgadores científicos mais "
            "influentes do nosso tempo."],
        "big_idea": ("O sucesso na vida — pessoal e profissional — não é função primária do QI. "
                     "Estudos longitudinais mostram que <b>habilidades emocionais</b> "
                     "(autoconsciência, autocontrole, empatia, habilidade social) explicam mais "
                     "do que o QI sobre quem prospera. E essas habilidades podem ser aprendidas."),
        "chapters": [
            {"num": "01", "kicker": "Fundamento",
             "title": "As duas mentes",
             "intro": ("Temos uma mente racional (pensa) e uma mente emocional (sente). Em "
                       "situações de stress, a mente emocional toma o comando — milisegundos antes "
                       "de a racional sequer ouvir o estímulo."),
             "bullets": [
                 "Mente emocional = rápida, impulsiva, associativa, sintética.",
                 "Mente racional = lenta, deliberada, analítica.",
                 "As duas operam em paralelo e em conflito. Saúde mental é integração.",
                 "Não basta 'pensar racionalmente' — é preciso treinar a emoção.",
             ],
             "callout_label": "DEFINIÇÃO",
             "callout": "Você não 'controla' a emoção — você dialoga com ela. Quem só pensa em controlar, perde."},

            {"num": "02", "kicker": "Neurociência",
             "title": "O sequestro da amígdala",
             "intro": ("A amígdala, no centro do cérebro emocional, pode <b>sequestrar</b> a "
                       "corteza pré-frontal antes que ela tenha tempo de raciocinar. É o que "
                       "explica reações desproporcionais — gritos, agressões, lágrimas — que "
                       "depois nos surpreendem."),
             "bullets": [
                 "LeDoux descobriu uma 'via curta' do tálamo direto à amígdala — antes da consciência.",
                 "Sequestro = a emoção age antes de você pensar.",
                 "Não é fraqueza — é arquitetura. Pode ser desfeita, mas exige treino.",
                 "Pausa, respiração, observação: ferramentas para 'desfazer' o sequestro.",
             ],
             "callout_label": "EXPLICAÇÃO",
             "callout": "Quando você reage e depois pensa 'não fui eu', tecnicamente está certo — foi sua amígdala antes do seu córtex."},

            {"num": "03", "kicker": "Pilar 1",
             "title": "Autoconsciência",
             "intro": ("Primeiro pilar: reconhecer a emoção no momento em que ela acontece. "
                       "Sem isso, o sujeito vive em piloto automático emocional — reagindo "
                       "sem saber por quê."),
             "bullets": [
                 "Nomeie a emoção: 'estou com raiva', 'estou triste', 'estou com vergonha'.",
                 "Nomear ativa o córtex pré-frontal e reduz a intensidade.",
                 "Pessoas com vocabulário emocional rico regulam melhor.",
                 "Diário emocional acelera o aprendizado.",
             ],
             "callout_label": "PRÁTICA",
             "callout": "Aprenda nomes para os seus estados. Quem só tem 'bem' e 'mal' está cego para o próprio interior."},

            {"num": "04", "kicker": "Pilar 2",
             "title": "Autorregulação",
             "intro": ("Não suprimir emoções — gerenciá-las. Autorregulação é poder sentir a "
                       "raiva e, ainda assim, não bater a porta; sentir o medo e ainda assim agir."),
             "bullets": [
                 "Pausa de 6 segundos entre estímulo e resposta — ativa o córtex.",
                 "Respiração lenta e profunda interrompe o sequestro.",
                 "Reformule a história: 'ele me ofendeu' → 'algo nele está doendo'.",
                 "Exercício físico reduz o estado base de stress.",
             ],
             "callout_label": "TÉCNICA",
             "callout": "Entre o estímulo e a resposta, ganhe 6 segundos. É o que separa reação de escolha."},

            {"num": "05", "kicker": "Pilar 3",
             "title": "Motivação",
             "intro": ("Capacidade de orientar emoções rumo a objetivos. Adiar gratificação, "
                       "persistir, manter otimismo realista, recuperar-se de derrotas."),
             "bullets": [
                 "Estudo do marshmallow (Walter Mischel): crianças que adiam comer ganham anos depois — em escola, renda, saúde.",
                 "Otimismo realista = ver dificuldades, acreditar que se pode superar.",
                 "Resiliência = bater de novo após cair.",
                 "Flow (Csikszentmihalyi) = engajamento profundo em tarefas desafiadoras.",
             ],
             "callout_label": "ESCOLA",
             "callout": "Crianças que esperam o segundo marshmallow se tornam adultos que esperam o resultado composto. Você é qual?"},

            {"num": "06", "kicker": "Pilar 4",
             "title": "Empatia",
             "intro": ("Ler emoções alheias. Sem empatia, o brilho técnico desperdiça-se em "
                       "comunicações que não convencem, vendas que não fecham, lideranças que não "
                       "engajam, relações que se desgastam."),
             "bullets": [
                 "Empatia não é simpatia — é compreensão. Pode incluir discordar.",
                 "Lê-se a emoção alheia pelo rosto, tom, postura, escolha de palavras.",
                 "Empatia aprende-se: voltar a sua atenção ao outro com paciência.",
                 "Falta de empatia é a base da maioria dos conflitos crônicos.",
             ],
             "callout_label": "DIAGNÓSTICO",
             "callout": "Pessoas que vivem em conflito crônico frequentemente não são más — são surdas para emoções alheias."},

            {"num": "07", "kicker": "Pilar 5",
             "title": "Habilidade social",
             "intro": ("Tudo o anterior se combina aqui: gerir relações. Inspirar, persuadir, "
                       "negociar conflitos, construir times, colaborar. Goleman cita estudos "
                       "de empresas mostrando que líderes com QE alto têm equipes mais "
                       "produtivas e menos rotatividade."),
             "bullets": [
                 "Comunicação clara + escuta empática + autocontrole + autoconsciência = liderança.",
                 "Conflito não é problema — manejo de conflito é.",
                 "Networking real não é coleta de cartões — é cuidado de relações.",
                 "Vendas, ensino, gestão: todas se reduzem a habilidade social com técnica.",
             ],
             "callout_label": "INTEGRAÇÃO",
             "callout": "Habilidade social é os outros 4 pilares aplicados a um momento real. Sem os 4, é só técnica."},

            {"num": "08", "kicker": "Aplicação",
             "title": "Pode-se aprender QE",
             "intro": ("Boa notícia: QE não é fixo. Diferente de QI, que é relativamente estável "
                       "após a infância, QE pode crescer significativamente em qualquer idade — "
                       "com prática deliberada."),
             "bullets": [
                 "Programas escolares de educação emocional reduzem violência e melhoram desempenho.",
                 "Programas corporativos de QE aumentam produtividade e reduzem rotatividade.",
                 "Você pode treinar QE: diário, terapia, meditação, feedback, leitura.",
                 "30 minutos diários por 6 meses = mudanças mensuráveis.",
             ],
             "quote": "QI te leva ao primeiro emprego. QE te leva à sua décima promoção.",
             "callout_label": "OTIMISMO",
             "callout": "QE não é destino. É treino. Quem pratica colhe — em qualquer fase da vida."},
        ],
        "insights": [
            ("01", "Você tem duas mentes — não uma",
             "Saúde mental é integração das duas, não dominação de uma sobre a outra."),
            ("02", "Nomear acalma",
             "Quando você nomeia uma emoção, o córtex assume o comando. Antes de nomear, a amígdala dirige."),
            ("03", "Empatia não é simpatia",
             "Empatia é ler. Simpatia é concordar. Você pode ler e discordar — e ainda assim entender."),
            ("04", "Adiar gratificação é a habilidade-mestra",
             "Walter Mischel comprovou: crianças que adiam comer o marshmallow ganham vida adulta inteira."),
            ("05", "QE > QI para sucesso",
             "Em estudos longitudinais, QE explica mais variância em sucesso de vida do que QI."),
            ("06", "QE pode ser treinado",
             "Diferente de QI. Em qualquer idade. Com prática deliberada."),
        ],
        "application": [
            ("Diário emocional", "Toda noite, 3 minutos: 3 emoções que sentiu hoje, com nome específico e gatilho."),
            ("Pausa de 6 segundos", "Em conflitos, pratique 6 segundos de respiração antes de responder. Treina o córtex."),
            ("Aprenda 30 nomes de emoções", "Vocabulário emocional rico aumenta regulação. Faça uma lista."),
            ("Pratique empatia uma vez por dia", "Em 1 conversa, comprometa-se a só fazer perguntas — entender antes de opinar."),
            ("Reduza estado base de stress", "Exercício, sono, alimentação. Os 3 reduzem o nível inicial de cortisol."),
            ("Peça feedback emocional", "Pergunte a 2 pessoas próximas: 'qual emoção te faço sentir com mais frequência?'"),
        ],
        "quotes": [
            ("Temos duas mentes — uma que pensa, outra que sente.", "Goleman"),
            ("QI te leva ao primeiro emprego. QE te leva à décima promoção.", "Síntese"),
            ("Você não controla a emoção — você dialoga com ela.", "Princípio"),
            ("Nomear reduz o sequestro.", "LeDoux/Goleman"),
            ("Empatia é ler — não concordar.", "Definição"),
            ("Adiar gratificação é a habilidade-mestra.", "Mischel"),
            ("QE pode ser treinado em qualquer idade.", "Goleman"),
        ],
        "reflections": [
            "Qual a última vez que você foi 'sequestrado' pela amígdala — reagiu e depois se surpreendeu com a própria reação?",
            "Quantos nomes de emoções você usa no dia-a-dia, sinceramente?",
            "Em qual relação você costuma confundir empatia com simpatia — escuta com concordância?",
            "Em qual área da sua vida você se beneficiaria de adiar mais gratificação?",
            "Qual emoção você mais reprime — e quanto disso volta como sintoma?",
            "Que pessoa do seu entorno tem QE alto — e o que faz, concretamente, que você poderia copiar?",
        ],
        "last_word_title": "Sentir, pensar, escolher.",
        "last_word_quote": "Inteligência emocional não é ser sempre calmo. É reconhecer a tempestade — e ainda assim escolher a direção do barco.",
    },

    # ─── 13 · Rápido e Devagar ───
    {
        "id": "rapido_devagar", "vol": "13",
        "title_main": "Rápido e", "title_sub": "Devagar.",
        "short_title": "Rápido e Devagar",
        "subtitle": "Duas formas de pensar.",
        "author": "Daniel Kahneman",
        "year_orig": "2011", "year_br": "2012", "publisher": "Objetiva",
        "pages": "Aproximadamente 624 páginas", "pages_count": 25,
        "genre": "Economia comportamental · Psicologia",
        "category_kicker": "Cognição · Decisão · Vieses",
        "motif": "hourglass",
        "palette": {"paper": "#F1EEEA", "ink": "#10243B", "accent": "#A89E2A",
                    "muted": "#7A776E", "hairline": "#CCC8C0", "subink": "#1B344E",
                    "paper_dark": "#DEDAD3"},
        "abstract": ("Resumo de <b>Rápido e Devagar</b>, obra-síntese do Nobel Daniel Kahneman. "
                     "Reúne os dois sistemas de pensamento, principais heurísticas e vieses, e o "
                     "que isso significa para decisões pessoais e financeiras."),
        "thesis": "Você não é a voz da razão. É dois sistemas em conflito — e o rápido decide mais do que você imagina.",
        "headline_quote": "Confiança não é um índice de acurácia. É um índice de coerência.",
        "about_author": [
            "<b>Daniel Kahneman</b> (1934–2024) foi um psicólogo israelense-americano. Junto com "
            "Amos Tversky, fundou a economia comportamental — campo que mostra como humanos "
            "decidem de forma sistematicamente irracional.",
            "Recebeu o <b>Prêmio Nobel de Economia em 2002</b> — feito raro para um psicólogo. "
            "Trabalhou em Princeton, Berkeley e Hebraica de Jerusalém. <i>Rápido e Devagar</i> "
            "(2011) é sua obra-síntese, resultado de cinco décadas de pesquisa.",
            "O livro foi adotado por governos, bancos centrais, hospitais e empresas para repensar "
            "como humanos decidem em condições reais — incerteza, pressa, emoção."],
        "big_idea": ("Existem em você dois sistemas de pensamento. <b>Sistema 1</b>: rápido, "
                     "automático, intuitivo, emocional. <b>Sistema 2</b>: lento, deliberado, "
                     "racional, esforçado. A maior parte das suas decisões é do Sistema 1 — "
                     "mesmo quando você acha que estava racionando."),
        "chapters": [
            {"num": "01", "kicker": "Parte 1",
             "title": "Os dois sistemas",
             "intro": ("Kahneman apresenta a metáfora dos dois sistemas. Sistema 1 entrega "
                       "respostas instantâneas; Sistema 2 supervisiona, mas com preguiça. A "
                       "maior parte do tempo, o Sistema 2 ratifica o que o 1 já decidiu."),
             "bullets": [
                 "Sistema 1: automático, esforço mínimo. Reconhece rostos, lê palavras, soma 2+2.",
                 "Sistema 2: deliberado, esforço máximo. Resolve 17×24, dirige em chuva forte.",
                 "Sistema 2 cansa rápido. Por isso terceiriza para o 1 sempre que pode.",
                 "A maior parte das decisões diárias é Sistema 1 — automática, intuitiva, falível.",
             ],
             "callout_label": "REGRA",
             "callout": "Você acha que é racional. Estatisticamente, você é principalmente automático."},

            {"num": "02", "kicker": "Parte 1",
             "title": "Heurística da disponibilidade",
             "intro": ("Atalho mental: você julga a probabilidade de algo pela facilidade com que "
                       "exemplos vêm à mente. Acidentes de avião parecem comuns depois de uma "
                       "queda no telejornal; assaltos parecem frequentes em bairros sobre os "
                       "quais ouvimos histórias."),
             "bullets": [
                 "Mídia amplifica eventos raros — e a disponibilidade os torna assustadores.",
                 "Decisões financeiras costumam ser dirigidas pela manchete da semana.",
                 "Antídoto: peça estatística, não memória.",
                 "Aplicação: você superestima riscos vistosos e subestima os silenciosos.",
             ],
             "callout_label": "VIÉS",
             "callout": "O que está fresco na cabeça parece comum. Não é. É só fresco."},

            {"num": "03", "kicker": "Parte 1",
             "title": "Heurística da ancoragem",
             "intro": ("Você se ancora no primeiro número que vê — mesmo quando ele é claramente "
                       "irrelevante. Negociação, preço, expectativa: tudo é puxado pela âncora "
                       "inicial."),
             "bullets": [
                 "Experimento clássico: gire roleta de 1 a 100, depois pergunte sobre % de países da África na ONU. Ancora.",
                 "Vendedores ancoram alto, depois 'concedem' descontos.",
                 "Antídoto: questione a âncora. De onde ela veio?",
                 "Aplicação: faça a primeira oferta sempre que possível.",
             ],
             "callout_label": "TÁTICA",
             "callout": "Quem ancora primeiro define o jogo. Em negociação séria, sempre ofereça antes."},

            {"num": "04", "kicker": "Parte 2",
             "title": "Aversão à perda",
             "intro": ("Perdas pesam ~2× mais do que ganhos equivalentes. Por isso pessoas "
                       "raramente trocam, pegam empréstimos arriscados, mantêm investimentos ruins. "
                       "É a base da teoria do prospect (Kahneman e Tversky)."),
             "bullets": [
                 "Perder R$100 dói mais do que ganhar R$100 alegra.",
                 "Por isso vendemos ativos vencedores e seguramos os perdedores (efeito disposição).",
                 "Status quo bias: preferimos manter o que temos, mesmo quando trocar seria melhor.",
                 "Antídoto: olhe para a decisão como se fosse zero a zero.",
             ],
             "callout_label": "ASSIMETRIA",
             "callout": "Você teme perder duas vezes mais do que adora ganhar. Isso explica por que decisões 50/50 te paralisam."},

            {"num": "05", "kicker": "Parte 2",
             "title": "Efeito enquadramento",
             "intro": ("A mesma informação, apresentada de duas formas, gera decisões opostas. "
                       "'90% de chance de viver' vs '10% de chance de morrer' — médicos, "
                       "pacientes, juízes decidem diferente."),
             "bullets": [
                 "Enquadramento muda decisão sem mudar fato.",
                 "Marqueteiros sabem disso. Políticos também. Você é alvo.",
                 "Antídoto: reformule mentalmente. Como soaria o oposto?",
                 "Frase-chave: 'qual versão dessa informação me deixa mais confortável — e por quê?'",
             ],
             "callout_label": "DEFESA",
             "callout": "Antes de decidir, reformule. 'Conserve' vs 'perca'. 'Ganhe' vs 'evite perder'. Pode mudar tudo."},

            {"num": "06", "kicker": "Parte 3",
             "title": "Excesso de confiança",
             "intro": ("Você sabe menos do que pensa, mas sente confiança proporcional à clareza "
                       "da sua narrativa — não à acurácia dela. Daí vêm bolhas, crises, "
                       "carreiras mal-escolhidas, casamentos apressados."),
             "bullets": [
                 "Confiança ≠ acurácia. É só coerência da história.",
                 "Especialistas são tão ruins quanto leigos em previsões de longo prazo.",
                 "Algoritmos simples batem especialistas em muitas decisões.",
                 "Antídoto: 'que evidência contrária você procurou?'",
             ],
             "callout_label": "VERDADE",
             "callout": "Quanto mais coerente é a sua narrativa, mais confiante você fica — e provavelmente, mais errado."},

            {"num": "07", "kicker": "Parte 4",
             "title": "Eu que recorda × eu que vivencia",
             "intro": ("Há dois 'eus' dentro de você. O <b>eu que vivencia</b> sente o agora. "
                       "O <b>eu que recorda</b> constrói a memória depois. O segundo pesa "
                       "principalmente o pico e o fim — não a média. Por isso decisões sobre "
                       "futuro são feitas com base em uma memória parcial."),
             "bullets": [
                 "Regra do pico-fim: experiências são lembradas pelo pico emocional e pelo final.",
                 "Colonoscopia mais longa, mas com final melhor, é lembrada como menos ruim.",
                 "Você escolhe férias futuras com base no que vai lembrar — não no que vai sentir.",
                 "Saber dessa cisão te ajuda a escolher por bem-estar, não por memória.",
             ],
             "quote": "O eu que recorda é um péssimo predizer do que o eu que vivencia vai sentir.",
             "callout_label": "DUAS VIDAS",
             "callout": "Você vive uma vida. Lembra de outra. Decida pela vida vivida, não pelo álbum de fotos."},

            {"num": "08", "kicker": "Síntese",
             "title": "Pensar devagar de propósito",
             "intro": ("Você não pode estar em Sistema 2 o tempo todo — é caro. Mas pode "
                       "<b>ativá-lo quando importa</b>: decisões grandes, irreversíveis, "
                       "estatísticas, contraintuitivas. A maturidade cognitiva é saber a hora."),
             "bullets": [
                 "Decisões pequenas e reversíveis: Sistema 1 está bem.",
                 "Decisões grandes ou irreversíveis: pause e ative o 2.",
                 "Cheque-lista, pré-mortem, segundas opiniões: ferramentas do 2.",
                 "Saber dos vieses não os elimina — mas reduz o estrago.",
             ],
             "callout_label": "REGRA FINAL",
             "callout": "Não viva em Sistema 2 — viva atento. Saber quando ativar o pensamento devagar é a verdadeira inteligência."},
        ],
        "insights": [
            ("01", "A maior parte do que você decide é automática",
             "Você se sente racional, mas estatisticamente está em piloto automático em quase tudo."),
            ("02", "Confiança não mede acurácia",
             "Quem se sente mais certo costuma ser quem teve menos contato com contraexemplos."),
            ("03", "Você perde duas vezes mais do que ganha",
             "Aversão à perda explica por que tantas decisões 50/50 nos paralisam."),
            ("04", "Enquadramento muda tudo",
             "A mesma informação em dois pacotes diferentes gera decisões opostas. Reformule antes de decidir."),
            ("05", "Especialistas erram quase tanto quanto leigos em prazo longo",
             "Em previsões de longo prazo, há limites. Algoritmos simples frequentemente batem intuição."),
            ("06", "Você tem dois 'eus' — viva atento a ambos",
             "O eu que vivencia × o eu que recorda. Frequentemente decidimos para o segundo, e o primeiro é quem paga."),
        ],
        "application": [
            ("Antes de decisões grandes, force o Sistema 2", "Reúna dados. Faça pré-mortem ('se isso desse errado em 1 ano, por quê?'). Peça segunda opinião contrária."),
            ("Use checklists em decisões repetitivas", "Como pilotos e cirurgiões. Reduz o domínio do Sistema 1 em momentos críticos."),
            ("Reformule antes de decidir", "Para cada decisão, escreva como soaria com enquadramento oposto. Veja se ainda decide o mesmo."),
            ("Pergunte: 'o que me faria estar errado?'", "Antídoto contra excesso de confiança. Force a busca por evidência contrária."),
            ("Distingue 'lembrarei' de 'viverei'", "Em decisões de tempo e dinheiro, pergunte: vou viver bem isso, ou só ter uma boa foto?"),
            ("Aceite que vieses sobrevivem", "Conhecer não elimina. Reduza estrago com sistemas (cheque-listas, esperas, segundas opiniões)."),
        ],
        "quotes": [
            ("Confiança é coerência, não acurácia.", "Kahneman"),
            ("Você tem duas mentes. A rápida e a devagar.", "Kahneman"),
            ("O que está fresco na cabeça parece comum.", "Heurística disponibilidade"),
            ("Perdas pesam duas vezes mais que ganhos.", "Teoria do prospect"),
            ("O eu que recorda é mau preditor do eu que vivencia.", "Pico-fim"),
            ("Saber do viés não elimina — só reduz o estrago.", "Kahneman"),
            ("Pensar é caro. Por isso terceirizamos para o atalho.", "Síntese"),
        ],
        "reflections": [
            "Em qual decisão importante recente você foi mais coerente do que correto?",
            "Em qual área da sua vida você sofre de aversão à perda — segurando o que deveria largar?",
            "Em qual conversa você ancorou numa expectativa que nem é sua — e ela continuou guiando?",
            "Quantas vezes na última semana você decidiu pela versão que vai lembrar, não pela vida que vai viver?",
            "Quem é o seu 'contra-opinador' designado — alguém que você consulta para discordar?",
            "Em qual decisão importante você usou apenas Sistema 1, sabendo que era Sistema 2?",
        ],
        "last_word_title": "Pense devagar quando importa.",
        "last_word_quote": "Não dá para pensar devagar o tempo todo. Mas dá para pensar devagar de propósito — exatamente quando importa.",
    },

    # ─── 14 · Trabalhe 4 Horas por Semana ───
    {
        "id": "trabalhe4h", "vol": "14",
        "title_main": "Trabalhe 4", "title_sub": "Horas/Semana.",
        "short_title": "Trabalhe 4 Horas por Semana",
        "subtitle": "Fuja do escritório, viaje pelo mundo e tenha mais renda.",
        "author": "Timothy Ferriss",
        "year_orig": "2007", "year_br": "2008", "publisher": "Planeta",
        "pages": "Aproximadamente 416 páginas", "pages_count": 25,
        "genre": "Estilo de vida · Negócios · Produtividade",
        "category_kicker": "Tempo · Lifestyle Design · Empreendedorismo",
        "motif": "clock4",
        "palette": {"paper": "#F4F1E9", "ink": "#0E0E0E", "accent": "#00AAA6",
                    "muted": "#7A7569", "hairline": "#CFC8B5", "subink": "#1F1F1F",
                    "paper_dark": "#E5E1D3"},
        "abstract": ("Resumo do best-seller de Tim Ferriss que popularizou o conceito de "
                     "<b>Nova Classe Rica</b> (NR). Reúne o método DEAL — Definir, Eliminar, "
                     "Automatizar, Liberar — e os princípios para projetar uma vida que "
                     "comporte tempo e renda."),
        "thesis": "Não trabalhe mais — trabalhe menos, melhor. A vida é projetada, não passada.",
        "headline_quote": "A questão não é 'aposentadoria' — é 'mini-aposentadorias'. Bem aproveitadas, ao longo da vida.",
        "about_author": [
            "<b>Timothy Ferriss</b> é empreendedor e investidor americano nascido em 1977. "
            "Trabalhou em vendas e em uma startup própria antes de publicar <i>A Semana de 4 "
            "Horas de Trabalho</i> (2007) — um dos manifestos mais influentes da geração "
            "millennial.",
            "Após o sucesso, virou podcaster (The Tim Ferriss Show), investidor-anjo precoce em "
            "Uber, Twitter e Facebook, e autor de mais 5 livros. Sua linha de pensamento "
            "popularizou o termo <b>lifestyle design</b> e influenciou a cultura do trabalho "
            "remoto antes da pandemia.",
            "Sua prática é experimental: testa hábitos, dietas, técnicas e relata. Estilo "
            "direto, irreverente — e bibliografia surpreendentemente densa."],
        "big_idea": ("A Nova Classe Rica (NR) prefere <b>tempo</b> e <b>mobilidade</b> a "
                     "patrimônio. Não busca aposentadoria — busca mini-aposentadorias. Não busca "
                     "salário maior — busca menos horas com a mesma renda. O método "
                     "<b>DEAL</b> organiza essa busca."),
        "chapters": [
            {"num": "D", "kicker": "Letra D",
             "title": "Definir",
             "intro": ("Antes de mudar, você precisa saber o que quer. Ferriss propõe o "
                       "<b>dreamlining</b>: liste o que faria, comprou e seria se tempo e dinheiro "
                       "não fossem problema. Depois calcule o custo mensal dessa vida — "
                       "geralmente muito menor do que se imagina."),
             "bullets": [
                 "Liste 5 coisas para FAZER (ações), TER (objetos), SER (estados).",
                 "Defina prazo: 6 ou 12 meses.",
                 "Calcule o custo mensal real da vida ideal — surpresa, é pequeno.",
                 "Renda alvo (TMI — Target Monthly Income) costuma ser inferior ao salário atual.",
             ],
             "callout_label": "DREAMLINING",
             "callout": "A vida ideal costuma custar menos do que a vida atual. A maioria nunca calcula."},

            {"num": "E", "kicker": "Letra E",
             "title": "Eliminar",
             "intro": ("80/20 (Pareto) + Lei de Parkinson. Identifique os 20% das tarefas que "
                       "geram 80% dos resultados, e os 20% das pessoas/projetos que geram 80% dos "
                       "problemas. Corte os segundos."),
             "bullets": [
                 "<b>Pareto</b>: 80% dos resultados vêm de 20% do que você faz.",
                 "<b>Parkinson</b>: o trabalho expande para encher o tempo disponível.",
                 "Reduza o tempo disponível e veja a produtividade subir.",
                 "Dieta de baixa informação: jornais, e-mails, redes — corte 80%.",
             ],
             "callout_label": "DUPLA",
             "callout": "Pareto + Parkinson: faça menos, com menos tempo. O resultado é o mesmo — ou melhor."},

            {"num": "A", "kicker": "Letra A",
             "title": "Automatizar",
             "intro": ("Construa um negócio (uma 'musa') que rode quase sozinho. Não para crescer "
                       "infinitamente — para cobrir o seu TMI sem precisar do seu tempo. "
                       "Terceirização, software, sistemas, fornecedores."),
             "bullets": [
                 "Pergunta-chave: o que pode rodar sem mim?",
                 "Use assistentes virtuais (geo-arbitragem de tempo).",
                 "Automatize processos repetitivos — eles são a maior parte.",
                 "Crie uma musa: produto/serviço que gera renda passiva ou semi-passiva.",
             ],
             "callout_label": "PRINCÍPIO",
             "callout": "Negócio não é proporcional a horas — é proporcional a sistemas. Quem só vende horas, vende a vida."},

            {"num": "L", "kicker": "Letra L",
             "title": "Liberar",
             "intro": ("Com tempo livre e renda mínima, libere-se geograficamente: trabalho "
                       "remoto, mini-aposentadorias, geo-arbitragem (ganhar em moeda forte, gastar "
                       "em fraca)."),
             "bullets": [
                 "Mini-aposentadorias: 1-6 meses em outro país, várias vezes ao longo da vida.",
                 "Geo-arbitragem: ganhar em dólar, viver em país barato.",
                 "Trabalho remoto: documente, prove, peça.",
                 "Vida não é 40 anos no escritório + 20 aposentado. É integração ao longo do percurso.",
             ],
             "callout_label": "INVERSÃO",
             "callout": "Aposentadoria é um produto da indústria do século XX. Mini-aposentadorias são o produto do XXI."},

            {"num": "05", "kicker": "Conceito 1",
             "title": "A Nova Classe Rica",
             "intro": ("Ferriss distingue 'classe rica' (alto patrimônio, pouco tempo) de 'NR' "
                       "(patrimônio suficiente, muito tempo). Para a NR, o ativo escasso não é "
                       "dinheiro — é tempo livre de qualidade."),
             "bullets": [
                 "Pergunta da NR: 'quantos dias livres e quanta renda passiva eu tenho?'",
                 "Aposentar tarde para gastar 'no fim' é mau negócio matemático.",
                 "Riqueza absoluta importa menos do que 'riqueza relativa' (tempo + renda + mobilidade).",
                 "Espalhe a 'liberdade' pela vida, em vez de empilhar para os 70 anos.",
             ],
             "callout_label": "REPENSAR",
             "callout": "Não tente ser rico aos 70. Tente ter tempo livre aos 30, aos 40, aos 50 — vai render mais."},

            {"num": "06", "kicker": "Conceito 2",
             "title": "Medo é o filtro",
             "intro": ("A maior barreira ao DEAL não é dinheiro nem habilidade — é medo. Ferriss "
                       "propõe um exercício explícito: definir o pior cenário, criar plano para "
                       "ele e perceber que é tolerável."),
             "bullets": [
                 "Liste o pior cenário possível ao tentar.",
                 "Como você se recuperaria, se acontecesse?",
                 "Custo de não tentar (em 5, 10, 20 anos)?",
                 "Quase sempre o medo é pior do que o pior real.",
             ],
             "quote": "Pessoas escolhem rotinas miseráveis em vez de incertezas que poderiam ser maravilhosas.",
             "callout_label": "EXERCÍCIO",
             "callout": "Defina o pior cenário em papel. Você vai descobrir que ele é menor do que o medo o pintava."},

            {"num": "07", "kicker": "Polêmica",
             "title": "Mas isso vale para mim?",
             "intro": ("Críticos: 'eu sou médico, advogado, professor — não posso virar nômade'. "
                       "Ferriss responde: o método se aplica como princípio, não como receita. "
                       "Reduza horas, projete renda passiva paralela, faça mini-aposentadorias "
                       "anuais."),
             "bullets": [
                 "Você pode aplicar 30% das ideias — e já mudar a vida.",
                 "DEAL é princípio: definir, eliminar, automatizar, liberar.",
                 "Não precisa virar empreendedor — pode ser empregado com renda passiva paralela.",
                 "Adapte ao seu contexto, não copie o do autor.",
             ],
             "callout_label": "ADAPTAÇÃO",
             "callout": "Aplique 30% e já vai mudar a vida. Não precisa virar nômade pra ganhar tempo."},

            {"num": "08", "kicker": "Síntese",
             "title": "Tempo, mobilidade, propósito",
             "intro": ("A receita Ferriss tem três ingredientes: <b>tempo livre</b>, "
                       "<b>mobilidade geográfica</b> e <b>propósito</b>. Sem o terceiro, o "
                       "tempo livre vira tédio. Sem os dois primeiros, o propósito vira fantasia."),
             "bullets": [
                 "Tempo livre é matéria-prima.",
                 "Mobilidade é flexibilidade.",
                 "Propósito é direção.",
                 "Falta de qualquer um destrói os outros dois.",
             ],
             "callout_label": "RECEITA",
             "callout": "Tempo + mobilidade + propósito = NR. Falta um, falta tudo."},
        ],
        "insights": [
            ("01", "Sua vida ideal custa menos do que você acha",
             "Quase ninguém calcula. Quando se calcula, descobre-se que 5–8 mil reais/mês já compram a vida sonhada."),
            ("02", "Pareto + Parkinson = trabalhar menos com mesmo resultado",
             "80% dos resultados vêm de 20% das tarefas. E o trabalho expande para encher o tempo. Reduza tempo, mantenha foco."),
            ("03", "Mini-aposentadorias > aposentadoria",
             "Distribua a liberdade pela vida. Não empilhe tudo para o fim, quando talvez não dê tempo de gastar."),
            ("04", "Negócio é sistema, não horas",
             "Quem vende só horas, vende a vida. Quem cria sistemas, escala."),
            ("05", "Medo é maior do que o pior real",
             "O exercício de definir o pior cenário no papel quase sempre desinfla o medo."),
            ("06", "Geo-arbitragem é alavanca subutilizada",
             "Ganhar em moeda forte, viver em moeda fraca. Multiplica padrão de vida sem aumentar renda."),
        ],
        "application": [
            ("Faça o dreamlining hoje", "Liste 5 coisas para FAZER, TER, SER. Calcule custo mensal. Se assuste com o quanto é menor."),
            ("Identifique seu 20% Pareto", "Quais 20% das suas tarefas geram 80% dos seus resultados? Concentre o tempo nelas."),
            ("Corte 1 fonte de informação", "Jornal, e-mail, rede social. Pelos próximos 30 dias. Veja o que acontece."),
            ("Comece um pequeno sistema", "Um produto digital, um serviço terceirizado, uma assinatura. Algo que rode sem você todo dia."),
            ("Escreva o pior cenário", "1 página. Pior caso, plano de recuperação, custo de não tentar. Visualizar reduz medo."),
            ("Negocie 1 dia de remoto por mês", "Comece pequeno. Prove que entrega. Expanda. Trabalho remoto começa em 1 dia."),
        ],
        "quotes": [
            ("A questão não é aposentadoria. É mini-aposentadorias.", "Ferriss"),
            ("80% dos resultados vêm de 20% das ações.", "Pareto"),
            ("O trabalho expande para encher o tempo disponível.", "Parkinson"),
            ("Tempo é a única moeda que não volta.", "Síntese"),
            ("Não trabalhe mais — trabalhe melhor.", "Ferriss"),
            ("Vida não é 40 + 20 — é projetada todo dia.", "Lifestyle design"),
            ("Defina o pior cenário em papel. Ele encolhe.", "Ferriss"),
        ],
        "reflections": [
            "Se tempo e dinheiro não fossem problema, o que você faria nos próximos 12 meses?",
            "Quanto isso custaria por mês — realmente? Você já calculou?",
            "Quais 20% do seu tempo geram 80% do que te importa hoje?",
            "Onde você está vendendo horas em vez de criar sistemas?",
            "Qual o pior cenário se você tentasse trabalhar remoto/mudar/criar — e quão pior é do que o cenário atual?",
            "Quando foi a última vez que você teve 2 meses sem trabalho — e quanto você precisaria pra que acontecesse?",
        ],
        "last_word_title": "Tempo é o luxo.",
        "last_word_quote": "Os outros vão se aposentar aos 70. Você pode mini-aposentar várias vezes antes — se decidir projetar a vida em vez de assisti-la passar.",
    },

    # ─── 15 · Os Segredos da Mente Milionária ───
    {
        "id": "mente_milionaria", "vol": "15",
        "title_main": "Mente", "title_sub": "Milionária.",
        "short_title": "Os Segredos da Mente Milionária",
        "subtitle": "Aprenda a enriquecer mudando seus conceitos sobre o dinheiro.",
        "author": "T. Harv Eker",
        "year_orig": "2005", "year_br": "2006", "publisher": "Sextante",
        "pages": "Aproximadamente 216 páginas", "pages_count": 26,
        "genre": "Educação financeira · Mentalidade",
        "category_kicker": "Mentalidade · Finanças · Crenças",
        "motif": "diamond",
        "palette": {"paper": "#F5F1E5", "ink": "#0C1B47", "accent": "#B89A2E",
                    "muted": "#857C66", "hairline": "#D8D0B6", "subink": "#142157",
                    "paper_dark": "#E8E2CB"},
        "abstract": ("Resumo de <b>Os Segredos da Mente Milionária</b>, de T. Harv Eker. "
                     "Reúne o conceito de 'plano interno do dinheiro' e os 17 arquivos que "
                     "diferenciam mentalmente quem prospera de quem perpetua escassez."),
        "thesis": "Sua conta bancária reflete o seu plano interno do dinheiro. Mudar a conta sem mudar o plano é gastar tempo.",
        "headline_quote": "Pensamento → Sentimento → Ação → Resultado. Se você quer mudar o resultado, mude a raiz.",
        "about_author": [
            "<b>T. Harv Eker</b> é um empresário e palestrante canadense. Após vários fracassos "
            "empresariais — segundo ele, 14 negócios falidos —, percebeu que o problema não era "
            "técnico, era mental.",
            "Após mudar 'o plano interno do dinheiro', construiu um negócio bem-sucedido de "
            "treinamentos: o Millionaire Mind Intensive. Em 2005, sintetizou o método no livro "
            "<i>Os Segredos da Mente Milionária</i>.",
            "Sua abordagem mistura linguagem direta de seminarista com princípios de programação "
            "neuro-linguística e psicologia comportamental. Polariza opiniões, mas o impacto "
            "popular foi enorme."],
        "big_idea": ("Cada pessoa tem um 'plano interno do dinheiro' — um conjunto de crenças, "
                     "atitudes e padrões aprendidos na infância. Esse plano determina o teto de "
                     "renda que a pessoa atinge. Mudar o resultado sem mudar o plano é "
                     "impossível: a mente sabota inconscientemente."),
        "chapters": [
            {"num": "01", "kicker": "Conceito-base",
             "title": "O plano interno do dinheiro",
             "intro": ("Eker compara dinheiro a um termostato: seu interno está calibrado em uma "
                       "temperatura. Se a conta esquenta acima dela, mecanismos inconscientes "
                       "esfriam (gastos, dívidas, decisões ruins) até voltar ao normal calibrado."),
             "bullets": [
                 "Pensamento → Sentimento → Ação → Resultado. A raiz é o pensamento.",
                 "Pensamento é programado por: o que ouvimos, vivemos e modelamos na infância.",
                 "Sem mudar o plano, qualquer aumento de renda evapora.",
                 "Diagnóstico: 'qual era a minha relação com dinheiro em casa, dos 0 aos 12?'",
             ],
             "callout_label": "DEFINIÇÃO",
             "callout": "Conta bancária é resultado. Plano interno é causa. Tratar a conta sem tratar o plano é puxar gelo do termostato."},

            {"num": "02", "kicker": "Origem",
             "title": "Verbalização, modelagem e incidentes",
             "intro": ("Três fontes formam o plano: as <b>verbalizações</b> que ouvimos sobre "
                       "dinheiro ('rico é mau', 'dinheiro não dá em árvore'), a <b>modelagem</b> "
                       "(como os adultos lidavam) e os <b>incidentes</b> específicos (briga sobre "
                       "dinheiro, falência familiar, ganho súbito)."),
             "bullets": [
                 "Verbalizações criam crenças.",
                 "Modelagem cria hábitos.",
                 "Incidentes criam traumas.",
                 "Identificar as três é começo da reprogramação.",
             ],
             "callout_label": "EXERCÍCIO",
             "callout": "Liste 3 frases que ouviu em casa sobre dinheiro. Veja quantas você ainda repete — sem ter decidido."},

            {"num": "03", "kicker": "Arquivo 1",
             "title": "Ricos criam vida; pobres reagem à vida",
             "intro": ("Mentalidade rica trata a própria vida como projeto. Cria, escolhe, decide. "
                       "Mentalidade pobre trata a vida como destino. Reage, aceita, queixa."),
             "bullets": [
                 "'Eu crio a minha vida' vs 'as coisas acontecem comigo'.",
                 "Vítima nunca enriquece — porque enriquecer requer agência.",
                 "Primeira mudança: troque 'tenho que' por 'escolho'.",
                 "Você é o autor — não a personagem.",
             ],
             "callout_label": "ARQUIVO",
             "callout": "Mude a frase. 'Tenho que trabalhar' → 'Escolho trabalhar'. A mudança começa pela linguagem."},

            {"num": "04", "kicker": "Arquivo 5",
             "title": "Ricos pensam grande; pobres pensam pequeno",
             "intro": ("Mente rica pensa em servir muitas pessoas, em construir algo grande. Mente "
                       "pobre pensa em sobreviver. A diferença não é cobiça — é amplitude da "
                       "missão e da contribuição."),
             "bullets": [
                 "A renda é proporcional ao número de pessoas que você serve.",
                 "Pensar grande não é arrogância — é responsabilidade.",
                 "Pequenez é frequentemente medo disfarçado de modéstia.",
                 "Sua missão pode crescer; deixe.",
             ],
             "callout_label": "ESCALA",
             "callout": "Quantas pessoas você serve? Se você quer servir mais, vai precisar de mais recursos. Pensar grande não é vaidade — é matemática."},

            {"num": "05", "kicker": "Arquivo 8",
             "title": "Ricos administram bem o dinheiro; pobres não",
             "intro": ("Eker propõe o sistema dos <b>seis frascos</b>: divida toda renda recebida "
                       "em 6 contas/fins: necessidade (55%), liberdade financeira (10%), "
                       "educação (10%), lazer (10%), reservas (10%), doações (5%)."),
             "bullets": [
                 "55% necessidades.",
                 "10% liberdade financeira (investir, jamais gastar).",
                 "10% educação (cursos, livros, eventos).",
                 "10% lazer (gastar puro prazer, sem culpa).",
                 "10% reservas (médio prazo).",
                 "5% doações.",
             ],
             "callout_label": "SISTEMA",
             "callout": "Sem sistema, qualquer salário se vaporiza. Com sistema, qualquer salário começa a render."},

            {"num": "06", "kicker": "Arquivo 11",
             "title": "Ricos preferem ser pagos por resultados; pobres por tempo",
             "intro": ("Quem é pago por hora tem teto matemático. Quem é pago por resultado pode "
                       "escalar. Não é apenas empreender — é mudar o critério da relação com o "
                       "dinheiro."),
             "bullets": [
                 "Salário é confortável e plano. Resultado é arriscado e exponencial.",
                 "Vendas, royalties, participação societária, freelance por entrega.",
                 "Mesmo dentro de empregos formais, busque bonificações por resultado.",
                 "Vai exigir construir resultados — não só comparecer.",
             ],
             "callout_label": "TROCA",
             "callout": "Aceite ser pago menos por hora se isso te der piso de resultado. O segundo escala — o primeiro não."},

            {"num": "07", "kicker": "Arquivo 14",
             "title": "Ricos fazem o dinheiro trabalhar; pobres trabalham pelo dinheiro",
             "intro": ("Renda passiva é o destino. Investir é a ferramenta. Educar-se "
                       "financeiramente é o pré-requisito. Pular um desses passos costuma resultar "
                       "em ruína."),
             "bullets": [
                 "Construir renda passiva é trabalho de anos.",
                 "Educação financeira é gratuita ou barata — e a maioria pula.",
                 "Investir sem entender é apostar.",
                 "Cada R$ investido é um soldado que trabalha 24h por você.",
             ],
             "callout_label": "META",
             "callout": "Pergunta-mestra: quantos meses você poderia parar de trabalhar e sustentar o seu padrão?"},

            {"num": "08", "kicker": "Arquivo 17",
             "title": "Ricos aprendem continuamente; pobres acham que já sabem",
             "intro": ("Mentalidade rica é aprendiz vitalícia. Mentalidade pobre é defensiva — "
                       "tudo o que ouve, já sabia. O paradoxo: quanto mais você sabe, mais "
                       "humildade você tem em relação ao que não sabe."),
             "bullets": [
                 "Leia 1 livro por mês. Assista 1 curso por trimestre.",
                 "Cerque-se de pessoas que sabem mais que você.",
                 "Cuidado com a 'arrogância de iniciante' — fase perigosa.",
                 "Educação composta é o segredo silencioso dos ricos.",
             ],
             "quote": "Educação financeira é a única vacina contra a pobreza recorrente.",
             "callout_label": "DISCIPLINA",
             "callout": "Investir 30 minutos por dia em educação financeira durante 10 anos te coloca acima de 95% das pessoas."},

            {"num": "09", "kicker": "Síntese",
             "title": "Como reprogramar o plano",
             "intro": ("Eker resume o processo em quatro passos: <b>consciência</b> (reconhecer a "
                       "crença), <b>compreensão</b> (de onde vem), <b>dissociação</b> (escolher "
                       "que ela não te define mais), <b>recondicionamento</b> (substituir por "
                       "nova declaração e ação)."),
             "bullets": [
                 "Consciência: nomeie a crença.",
                 "Compreensão: ache a origem.",
                 "Dissociação: 'isso era da minha mãe, não é meu'.",
                 "Recondicionamento: nova declaração + ação repetida.",
             ],
             "callout_label": "PROTOCOLO",
             "callout": "Crença não muda só de pensar. Muda de declarar + agir conforme. Repetição vence padrão antigo."},
        ],
        "insights": [
            ("01", "Sua conta é espelho do seu plano",
             "Mudar conta sem mudar plano = aumento volátil. Mude o plano, e a conta segue."),
            ("02", "Linguagem é diagnóstico",
             "'Tenho que' = vítima. 'Escolho' = autor. Comece pela linguagem — depois vem a ação."),
            ("03", "Os 6 frascos transformam qualquer salário",
             "Não importa o valor — importa a divisão automática. Renda baixa com sistema rende mais do que renda alta sem."),
            ("04", "Resultado escala; hora não",
             "Negocie por entrega quando puder. Mesmo em empregos, busque bonificação por resultado."),
            ("05", "Pensar grande não é vaidade — é responsabilidade",
             "Renda é proporcional a quantas pessoas você serve. Não pode servir mais sem crescer."),
            ("06", "Aprendizado é o juro silencioso",
             "30 minutos por dia, durante 10 anos, te separam do resto."),
        ],
        "application": [
            ("Mapeie suas frases de infância", "Liste 5 frases que ouvia em casa sobre dinheiro. Veja quais você ainda repete."),
            ("Implante os 6 frascos", "Crie 6 contas/categorias. Divida o próximo salário nos percentuais propostos. Automatize."),
            ("Mude a linguagem por 30 dias", "Cada vez que se pegar dizendo 'tenho que', reformule para 'escolho'. Treina o autor."),
            ("Pague-se primeiro 10%", "A regra babilônica em forma de hábito. Antes do aluguel."),
            ("Estude 30 min por dia", "Educação financeira. Não precisa ser dramática. Compõe."),
            ("Negocie 1 pagamento por resultado", "Esta semana. Pode ser pequeno. Mas comece a mudar o critério."),
        ],
        "quotes": [
            ("Sua conta bancária reflete seu plano interno.", "Eker"),
            ("Mude a raiz, a flor vem.", "Síntese"),
            ("Renda é proporcional ao número de pessoas que você serve.", "Arquivo 5"),
            ("Pensar grande não é vaidade — é responsabilidade.", "Eker"),
            ("Educação financeira é vacina contra a pobreza recorrente.", "Eker"),
            ("Ricos criam vida; pobres reagem à vida.", "Arquivo 1"),
            ("Mude a linguagem, mude o resultado.", "Síntese"),
        ],
        "reflections": [
            "Quais 3 frases você ouvia em casa sobre dinheiro — e quantas você ainda repete sem ter decidido?",
            "Se sua relação com dinheiro fosse um termostato, em que temperatura ele estaria?",
            "Onde você usa 'tenho que' quando poderia usar 'escolho'?",
            "Como você dividiria seu próximo salário se aplicasse os 6 frascos?",
            "Você é pago por hora ou por resultado — e o que precisaria mudar para inverter?",
            "Quanto tempo você dedicou à sua educação financeira nos últimos 30 dias?",
        ],
        "last_word_title": "Raiz e fruto.",
        "last_word_quote": "Você não muda a sua conta bancária — você muda a sua relação com dinheiro. A conta segue.",
    },

    # ─── 16 · Dom Casmurro ───
    {
        "id": "dom_casmurro", "vol": "16",
        "title_main": "Dom", "title_sub": "Casmurro.",
        "short_title": "Dom Casmurro",
        "subtitle": "Romance de Machado de Assis · clássico brasileiro.",
        "author": "Machado de Assis",
        "year_orig": "1899", "year_br": "1899", "publisher": "Companhia das Letras",
        "pages": "Aproximadamente 256 páginas", "pages_count": 26,
        "genre": "Romance · Literatura brasileira",
        "category_kicker": "Literatura brasileira · Romance · Ciúme",
        "motif": "quill",
        "palette": {"paper": "#EDE5D2", "ink": "#1A1A12", "accent": "#7A2025",
                    "muted": "#7D7558", "hairline": "#D3CAA9", "subink": "#28281D",
                    "paper_dark": "#DCD3B7", "title_font": "Times-Bold"},
        "title_font": "Times-Bold",
        "abstract": ("Resumo de <b>Dom Casmurro</b>, romance-mestre de Machado de Assis. "
                     "Apresenta os personagens, o enredo da casa de Matacavalos às páginas finais, "
                     "o jogo do narrador não-confiável e os símbolos que organizam a leitura."),
        "thesis": "A questão do livro não é 'Capitu traiu?' — é 'Bento merece ser acreditado?'. Tudo o resto é consequência.",
        "headline_quote": "Capitu, olhos de ressaca: aqueles olhos que pareciam puxar o mundo para dentro deles.",
        "about_author": [
            "<b>Machado de Assis</b> (1839–1908) é o maior escritor da literatura brasileira. "
            "Nascido pobre, mulato, neto de escravos libertos, autodidata. Foi tipógrafo, "
            "tradutor, jornalista, contista, romancista, dramaturgo, poeta. Fundador e primeiro "
            "presidente da Academia Brasileira de Letras (1897).",
            "Sua obra divide-se em duas fases: a primeira, romântica e realista; a segunda, "
            "iniciada em <i>Memórias Póstumas de Brás Cubas</i> (1881), inaugura o que estudiosos "
            "chamam de 'humorismo machadiano' — narrativa irônica, fragmentada, "
            "metaliterária. <i>Dom Casmurro</i> (1899) é o ápice dessa fase.",
            "Influenciou Carlos Drummond, Clarice Lispector, Susan Sontag, Harold Bloom. Sua "
            "técnica do narrador não-confiável antecipou em décadas modernismo europeu e "
            "literatura americana do século XX."],
        "big_idea": ("Bento Santiago, agora velho ('Dom Casmurro'), tenta reconstruir a história "
                     "do seu amor por Capitu — desde a infância na rua de Matacavalos até a "
                     "suspeita de traição com o melhor amigo, Escobar. A genialidade do livro "
                     "está em que tudo é narrado <b>por ele</b>. O leitor nunca tem acesso a "
                     "Capitu sem o filtro de Bento."),
        "chapters": [
            {"num": "01", "kicker": "Estrutura",
             "title": "Quem é Dom Casmurro?",
             "intro": ("Bento Santiago, advogado aposentado, viúvo, reservado. Vive em casa "
                       "réplica da infância. Recebe o apelido 'Dom Casmurro' por silêncio "
                       "constante. Decide escrever para 'atar as duas pontas da vida' — "
                       "infância e velhice."),
             "bullets": [
                 "O apelido é dado por um poeta no trem, ofendido pelo silêncio de Bento.",
                 "Bento constrói livro como tentativa de remontar memória.",
                 "A narração é em primeira pessoa — o leitor só ouve a versão dele.",
                 "Crítica chama essa estrutura de <b>narrador não-confiável</b>.",
             ],
             "callout_label": "ATENÇÃO",
             "callout": "Tudo o que você vai ler vem de uma só pessoa. E essa pessoa tem motivos para distorcer."},

            {"num": "02", "kicker": "Cenário",
             "title": "A rua de Matacavalos",
             "intro": ("Bento e Capitu crescem como vizinhos no Rio de Janeiro do segundo "
                       "Império. Famílias de classe média alta, valores católicos, ambiente "
                       "patriarcal. Cenário de infância 'pura' — segundo Bento."),
             "bullets": [
                 "Casas próximas, muro baixo entre os quintais.",
                 "Crianças que crescem juntas — Bento, Capitu, Escobar, José Dias.",
                 "D. Glória, mãe de Bento, prometeu Bento ao seminário em troca da vida do filho.",
                 "Promessa religiosa que vai assombrar o resto da história.",
             ],
             "callout_label": "CENÁRIO",
             "callout": "Matacavalos é mais do que rua — é o paraíso que o narrador velho tenta preservar de qualquer dúvida."},

            {"num": "03", "kicker": "Personagens",
             "title": "Bento, Capitu, Escobar, Sancha",
             "intro": ("Bento — o narrador, retraído, intelectual, ciumento. Capitu — vizinha, "
                       "amada, descrita com 'olhos de ressaca'. Escobar — amigo de seminário, "
                       "depois cunhado, depois suspeito. Sancha — esposa de Escobar."),
             "bullets": [
                 "<b>Bento</b>: dependente da mãe, ambivalente entre fé e mundo.",
                 "<b>Capitu</b>: dois anos mais nova, dissimulada — segundo Bento.",
                 "<b>Escobar</b>: amigo de coração, atlético, prático.",
                 "<b>Sancha</b>: figura mais apagada — mas crucial nos últimos capítulos.",
             ],
             "callout_label": "AVISO",
             "callout": "Toda descrição é do narrador. Capitu nunca fala — Bento conta o que ela disse."},

            {"num": "04", "kicker": "Trama 1",
             "title": "O seminário e o desvio",
             "intro": ("Bento entra no seminário pela promessa da mãe. Ali conhece Escobar. "
                       "Juntos, descobrem que ambos têm uma 'vida fora' do seminário e — com "
                       "alguma manipulação familiar — conseguem ser dispensados."),
             "bullets": [
                 "Bento usa de astúcia para escapar do seminário sem quebrar a promessa formal.",
                 "Escobar é cúmplice da fuga.",
                 "A promessa é 'cumprida' pela ordenação de outro jovem no lugar de Bento.",
                 "Crítica vê aí a primeira mancha moral de Bento — uma trapaça religiosa.",
             ],
             "callout_label": "LEITURA",
             "callout": "O narrador que pede para acreditarmos nele já começou a vida quebrando uma promessa religiosa."},

            {"num": "05", "kicker": "Trama 2",
             "title": "Casamento, amizade, filho",
             "intro": ("Bento casa-se com Capitu. Escobar com Sancha. As duas famílias se "
                       "tornam íntimas. Bento e Capitu têm um filho — Ezequiel — "
                       "fisicamente parecido com o pai (e, mais tarde, com Escobar)."),
             "bullets": [
                 "Felicidade aparente nos anos iniciais.",
                 "Escobar morre afogado tentando provar coragem no mar.",
                 "No velório, Bento percebe Capitu olhando longamente para o defunto.",
                 "A semente da suspeita é plantada naquele instante.",
             ],
             "quote": "Capitu olhou o defunto durante alguns instantes; depois, sem retirar os olhos, voltou-se para mim, com um ar de meditação tão fixo, que pareceu sair de si.",
             "callout_label": "MOMENTO-CHAVE",
             "callout": "A passagem do velório é o ponto onde a história racha. Antes: amor. Depois: dúvida."},

            {"num": "06", "kicker": "Trama 3",
             "title": "Ezequiel — o filho",
             "intro": ("Ezequiel cresce parecido demais com Escobar — para o olho ciumento de "
                       "Bento. Bento começa a suspeitar de traição passada. Acaba afastando o "
                       "filho. Manda-o para a Europa. Capitu também é mandada para Suíça, "
                       "onde morre anos depois."),
             "bullets": [
                 "Bento desconfia que Ezequiel é filho de Escobar.",
                 "Não há prova material — só a semelhança e a 'leitura' do olhar de Capitu.",
                 "Bento age como se fosse traído — sem nunca ter certeza.",
                 "Capitu morre na Suíça. Ezequiel morre jovem na África.",
             ],
             "callout_label": "DESFECHO",
             "callout": "Bento toma decisões irreversíveis com base em uma suspeita que ele mesmo nunca prova."},

            {"num": "07", "kicker": "Símbolos",
             "title": "Olhos de ressaca, cigano oblíquo",
             "intro": ("Machado planta imagens recorrentes: os 'olhos de ressaca' de Capitu, "
                       "'oblíquos e dissimulados' — formulação que Bento atribui ao seu agregado "
                       "José Dias e depois adota como verdade definitiva. A imagem é a 'prova' — "
                       "mas é só uma metáfora repetida."),
             "bullets": [
                 "Olhos de ressaca: puxam, dissimulam, escondem.",
                 "<i>Oblíquos e dissimulados</i>: frase de José Dias, citada como se fosse evidência.",
                 "Mar como recorrência — morte de Escobar, olhar de Capitu.",
                 "Símbolos servem ao narrador, não à verdade.",
             ],
             "callout_label": "INSIGHT",
             "callout": "Machado mostra como uma metáfora repetida vira convicção. Não há prova — só imagem que cresce."},

            {"num": "08", "kicker": "Crítica",
             "title": "Capitu traiu?",
             "intro": ("Pergunta clássica da crítica brasileira. Décadas de leitura dividiram "
                       "professores e leitores. Helen Caldwell, em 1960, virou a chave: a "
                       "pergunta certa não é 'Capitu traiu?' — é 'podemos confiar em Bento?'."),
             "bullets": [
                 "Não há cena de traição. Tudo é deduzido por Bento.",
                 "Bento tem todos os sinais clássicos de ciúme patológico.",
                 "Capitu, no livro, sempre nega — e Bento ignora.",
                 "Leitura moderna: o livro é sobre uma <b>injustiça</b>, não sobre uma <b>traição</b>.",
             ],
             "quote": "A vontade de viver, com Capitu, tornou-se vontade de saber se Capitu vivia comigo.",
             "callout_label": "VIRADA CRÍTICA",
             "callout": "A pergunta antiga: 'Capitu traiu?'. A pergunta moderna: 'Bento é um narrador confiável?'. Tudo muda."},

            {"num": "09", "kicker": "Síntese",
             "title": "O que sobra ao leitor",
             "intro": ("Machado deixa o leitor sem resposta — de propósito. A obra-prima está em "
                       "obrigar cada um a escolher em quem acredita. Quem acredita em Capitu vê "
                       "uma vida destruída por ciúme. Quem acredita em Bento vê uma traição vingada."),
             "bullets": [
                 "Não há gabarito.",
                 "A escolha do leitor diz mais sobre o leitor do que sobre o livro.",
                 "Releia ano após ano: a sua resposta vai mudar.",
                 "Esse é o gênio de Machado: criar um espelho.",
             ],
             "callout_label": "EXPERIÊNCIA",
             "callout": "O que você acredita sobre Capitu, hoje, diz algo sobre quem você é, hoje. Releia em dez anos."},
        ],
        "insights": [
            ("01", "Narrador não-confiável é o coração do livro",
             "Sem perceber isso, lemos como história de traição. Percebendo, lemos como história de injustiça."),
            ("02", "Bento começa quebrando uma promessa",
             "A primeira informação moral sobre o narrador é que ele manipulou para escapar do seminário. Isso não é detalhe."),
            ("03", "Capitu nunca fala",
             "Toda fala dela é citada por Bento. Não temos contato direto. Isso é central."),
            ("04", "Metáfora vira prova quando repetida",
             "'Olhos oblíquos e dissimulados' — repetida 100x — vira evidência. Mas é só metáfora."),
            ("05", "Ciúme é diagnóstico clínico no livro",
             "Bento tem todos os sintomas de paranoia ciumenta. A literatura antecipa a psicologia em quase 100 anos."),
            ("06", "Cada leitor encontra o seu livro",
             "Quem acredita em Bento lê uma tragédia. Quem acredita em Capitu lê outra. Mesma obra; duas vidas."),
        ],
        "application": [
            ("Releia sem pressa", "Reserve uma semana. Anote em quais momentos você sente Bento sendo sincero — e em quais sendo conveniente."),
            ("Conte só o que Capitu diz", "Faça uma lista de todas as falas dela no livro. Quão pouco resta — depois de tirar a interpretação de Bento."),
            ("Note os símbolos repetidos", "Olhos, mar, dissimulação. Veja como Machado planta — e como elas servem ao narrador, não à história."),
            ("Compare com sua memória", "Você lê esse livro como Bento ou como Capitu? E na sua vida, você narra os conflitos como Bento (sem testemunha) ou ouve testemunhos?"),
            ("Leia Helen Caldwell", "Ensaio de 1960 que virou a chave da crítica brasileira. 50 páginas que mudam a leitura para sempre."),
            ("Reveja em 10 anos", "A sua resposta vai mudar. E aí o livro te diz outra coisa sobre você."),
        ],
        "quotes": [
            ("Capitu, olhos de ressaca.", "Machado, narrador Bento"),
            ("Oblíquos e dissimulados.", "José Dias, citado por Bento"),
            ("A vontade de viver com Capitu tornou-se vontade de saber se Capitu vivia comigo.", "Bento"),
            ("Não tive pais, não tive irmãos: tive a casa de Matacavalos.", "Bento"),
            ("Capitu nunca falou. Bento sempre falou por ela.", "Síntese moderna"),
            ("O ciúme não pede prova — pede confirmação.", "Síntese leitor"),
            ("Toda história tem dois lados; este livro tem um — e nos pede para escolher.", "Síntese"),
        ],
        "reflections": [
            "Você acreditou em Bento na primeira leitura — e por quê?",
            "Em qual relação da sua vida você narrou um conflito sem ouvir o outro lado?",
            "Que metáfora repetida virou 'verdade' para você sobre alguém — sem nunca ter sido provada?",
            "Que pessoa próxima sua nunca teve a chance de falar — porque você sempre falou primeiro?",
            "Você confia em narradores em primeira pessoa — ou desconfia naturalmente? Por quê?",
            "Se você reler o livro daqui a 10 anos e mudar de leitura, o que isso diz sobre você?",
        ],
        "last_word_title": "Em quem você acredita.",
        "last_word_quote": "Dom Casmurro não termina com Capitu — termina em você. Sua resposta é o resto do livro.",
    },

    # ─── 17 · Capitães da Areia ───
    {
        "id": "capitaes_areia", "vol": "17",
        "title_main": "Capitães", "title_sub": "da Areia.",
        "short_title": "Capitães da Areia",
        "subtitle": "Romance de Jorge Amado · Salvador anos 1930.",
        "author": "Jorge Amado",
        "year_orig": "1937", "year_br": "1937", "publisher": "Companhia das Letras",
        "pages": "Aproximadamente 280 páginas", "pages_count": 26,
        "genre": "Romance · Literatura brasileira · Social",
        "category_kicker": "Literatura brasileira · Bahia · Justiça social",
        "motif": "wave",
        "palette": {"paper": "#EDE2C6", "ink": "#3A2317", "accent": "#9C5E1F",
                    "muted": "#8C7857", "hairline": "#D2C39E", "subink": "#4B2E1D",
                    "paper_dark": "#DBCFA8", "title_font": "Times-Bold"},
        "title_font": "Times-Bold",
        "abstract": ("Resumo de <b>Capitães da Areia</b>, romance de Jorge Amado sobre um "
                     "grupo de meninos de rua em Salvador. Reúne personagens, episódios "
                     "principais, temas sociais e a denúncia que fez o livro ser queimado pela "
                     "ditadura em 1937."),
        "thesis": "Crianças abandonadas ao próprio destino se organizam — em sobrevivência, em violência, e às vezes em amor. A sociedade que as abandona é a verdadeira ré.",
        "headline_quote": "Eles tinham na carne a mesma queimadura do sol e a mesma fome no peito.",
        "about_author": [
            "<b>Jorge Amado</b> (1912–2001) é o escritor brasileiro mais traduzido do século XX. "
            "Nascido em Itabuna, Bahia, fez do estado-litoral a sua matéria-prima. Militante "
            "comunista nos anos 1930-40, preso e exilado várias vezes.",
            "<i>Capitães da Areia</i> (1937) foi seu quarto romance, escrito aos 25 anos. "
            "Publicado em outubro de 1937, no mesmo mês em que o presidente Getúlio Vargas "
            "instaurou o Estado Novo — o livro foi queimado em praças públicas pelo regime, "
            "junto com outras obras de Amado.",
            "Sua trajetória vai do realismo militante para a abundância sensorial dos romances "
            "tardios (<i>Gabriela</i>, <i>Dona Flor</i>, <i>Tieta</i>). Jorge é a Bahia traduzida "
            "para o mundo."],
        "big_idea": ("Cerca de 50 meninos vivem em um trapiche abandonado da praia de Salvador. "
                     "Sem família, sem escola, sem proteção. Sobrevivem de roubo, briga e "
                     "afeto entre si. O livro acompanha a turma e três personagens principais — "
                     "Pedro Bala, Pirulito, Professor — pelos meses em que cada um decide o que "
                     "fazer da vida adulta que se aproxima."),
        "chapters": [
            {"num": "01", "kicker": "Cenário",
             "title": "O trapiche e a cidade",
             "intro": ("Salvador, 1930s. Cidade dividida entre a elite branca da parte alta e a "
                       "população negra/pobre da parte baixa. Os meninos vivem em um trapiche "
                       "(armazém abandonado) na praia. Da cidade, são ignorados — exceto quando "
                       "fazem perda na imprensa."),
             "bullets": [
                 "Trapiche velho da Baía: chão de areia, telhado vazado, vento e mar.",
                 "Os meninos são apelidados 'capitães da areia' por jornalistas.",
                 "Sem mãe, sem pai, sem nome — só apelidos.",
                 "Idades entre 8 e 18 anos.",
             ],
             "callout_label": "GEOGRAFIA",
             "callout": "A literatura urbana de Amado é a partir do litoral. Mar, areia, mercado, igrejas — Salvador é personagem."},

            {"num": "02", "kicker": "Personagens 1",
             "title": "Pedro Bala, o chefe",
             "intro": ("Pedro Bala é o líder. Branco, loiro, filho de operário grevista morto pela "
                       "polícia. Tem a justiça do pai no sangue. É o personagem que mais cresce — "
                       "do banditismo de rua à consciência política."),
             "bullets": [
                 "15 anos no início. Filho de Raimundo Bala, líder grevista morto.",
                 "Comanda os meninos com violência justa e coragem.",
                 "Conhecerá Dora — único amor real do livro.",
                 "Vai terminar como militante operário.",
             ],
             "callout_label": "ARCO",
             "callout": "Pedro começa marginal e termina militante. O livro é a história dessa virada."},

            {"num": "03", "kicker": "Personagens 2",
             "title": "Professor, Pirulito, Sem-Pernas",
             "intro": ("<b>Professor</b>: lê tudo, desenha, será pintor. <b>Pirulito</b>: o místico, "
                       "convertido ao catolicismo, vai virar padre. <b>Sem-Pernas</b>: o coxo, "
                       "amargo, abandonado por todos os adultos, decide morrer cedo. Cada um é "
                       "uma rota possível da pobreza."),
             "bullets": [
                 "<b>Professor</b>: vai estudar, virar pintor reconhecido.",
                 "<b>Pirulito</b>: vai para o seminário, vira padre.",
                 "<b>Sem-Pernas</b>: salta da janela do Aljube — caminho do suicídio.",
                 "<b>Gato</b>: vai para o crime organizado.",
             ],
             "callout_label": "GALERIA",
             "callout": "Amado mostra: a mesma origem produz cinco destinos diferentes. O determinismo da pobreza não é total — mas a maioria perde."},

            {"num": "04", "kicker": "Episódios",
             "title": "Roubos, brigas, afetos",
             "intro": ("A vida dos capitães é feita de pequenas operações: assaltos a casas ricas, "
                       "brigas com outras turmas, dias de praia, festas no candomblé, "
                       "encontros sexuais. Amado evita romantizar — há violência, há fome, há "
                       "doença."),
             "bullets": [
                 "Roubam para sobreviver — não acumulam patrimônio.",
                 "Lealdade entre eles é o único código moral aprendido.",
                 "Religiões populares (candomblé, catolicismo) entrelaçadas.",
                 "Sexo cedo, frequentemente em condições precárias.",
             ],
             "callout_label": "REALISMO",
             "callout": "Amado não estiliza. O livro mostra a infância pobre como ela era — incluindo o que a moral classe média prefere não ver."},

            {"num": "05", "kicker": "Trama central",
             "title": "Dora, o amor",
             "intro": ("Dora, órfã recém-chegada à cidade, é acolhida pelos capitães. Primeiro "
                       "como 'irmã'; depois, como esposa simbólica de Pedro Bala. Sua entrada "
                       "muda o trapiche — introduz cuidado, afeto, tristeza. Sua morte por "
                       "tuberculose é o eixo emocional do livro."),
             "bullets": [
                 "Dora vira mãe substituta de todos.",
                 "Romance com Pedro Bala — o único amor sério do livro.",
                 "Adoece de tuberculose, doença típica da pobreza urbana.",
                 "Morre — Pedro Bala perde a única figura feminina amorosa da vida.",
             ],
             "quote": "Dora veio para o trapiche e o trapiche teve mãe.",
             "callout_label": "PERSONAGEM-CHAVE",
             "callout": "Dora é catalisador. Antes dela: bando. Depois dela: pessoas. Sua morte é também a do trapiche."},

            {"num": "06", "kicker": "Conflito",
             "title": "O reformatório",
             "intro": ("Vários capitães são presos e levados ao reformatório — instituição "
                       "supostamente educadora, na prática prisão para crianças pobres. O livro "
                       "descreve a violência sistemática do lugar — espancamento, abuso, fome — "
                       "como denúncia explícita."),
             "bullets": [
                 "Pedro Bala é preso por roubo.",
                 "No reformatório, sofre violência física e sexual.",
                 "Foge — e volta ao trapiche transformado.",
                 "O 'sistema' que deveria recuperar quebra ainda mais.",
             ],
             "callout_label": "DENÚNCIA",
             "callout": "O reformatório no livro é o que Foucault analisaria décadas depois: instituição que produz, em vez de curar, o que pretende eliminar."},

            {"num": "07", "kicker": "Consciência",
             "title": "Pedro Bala e o pai",
             "intro": ("Já mais velho, Pedro encontra ex-companheiros do pai — operários "
                       "grevistas, comunistas perseguidos. Reconhece o sangue. Decide trocar a "
                       "bandidagem pela militância política — entendendo que o roubo individual é "
                       "sintoma; a injustiça social é causa."),
             "bullets": [
                 "Encontra João de Adão, sapateiro velho amigo do pai.",
                 "Lê textos de operários — primeira educação política.",
                 "Decide deixar os capitães e entrar no movimento sindical.",
                 "É o único arco do livro com final 'redentor' — embora ainda incerto.",
             ],
             "callout_label": "VIRADA",
             "callout": "Pedro entende: o roubo é resposta ao roubo maior — o da sociedade que rouba dele o pai, a escola, a infância."},

            {"num": "08", "kicker": "Crítica",
             "title": "Por que o livro foi queimado",
             "intro": ("Estado Novo (1937–45) queimou <i>Capitães da Areia</i> em fogueiras "
                       "públicas. Razão: o livro denuncia desigualdade brasileira, descreve "
                       "violência policial e termina com a redenção de um comunista. Tudo o que o "
                       "regime queria silenciar."),
             "bullets": [
                 "Outubro de 1937: Estado Novo é decretado.",
                 "Novembro: livros de Amado, Graciliano e outros são queimados.",
                 "Amado é preso e depois exilado.",
                 "O livro só voltou a circular livremente nos anos 1940 — mas nunca saiu de catálogo.",
             ],
             "callout_label": "HISTÓRIA",
             "callout": "Livros queimados costumam ser livros que dizem o que o poder não quer ouvir. <i>Capitães</i> dizia."},

            {"num": "09", "kicker": "Síntese",
             "title": "Por que ainda lemos",
             "intro": ("85 anos depois, o livro permanece atual: meninos de rua continuam "
                       "existindo, reformatórios continuam violentos, polícia continua matando "
                       "filhos de operários. O Brasil não cumpriu a denúncia."),
             "bullets": [
                 "Pedro Bala existe ainda hoje — em qualquer cidade grande brasileira.",
                 "A reforma de sistema socioeducativo continua incompleta.",
                 "Amado nos pede algo difícil: olhar para essas crianças sem desviar.",
                 "Quem desviou em 1937 deixou o Brasil onde está em 2026.",
             ],
             "callout_label": "PERMANÊNCIA",
             "callout": "Não é livro do passado. É livro do presente. Se o leitor olha pelo trem para o trapiche, o trapiche está olhando de volta."},
        ],
        "insights": [
            ("01", "Pobreza não produz monstros — produz pessoas em situações monstruosas",
             "Os capitães roubam, brigam, mentem. Mas amam, riem, sonham. A diferença não é moral — é estrutural."),
            ("02", "Cinco crianças, cinco destinos",
             "Pedro vira militante. Professor, pintor. Pirulito, padre. Sem-Pernas, suicida. Gato, criminoso. O determinismo é parcial — mas a maioria perde."),
            ("03", "Reformatório é fábrica de criminosos",
             "Foucault diria isso 40 anos depois. Amado já mostrava em 1937."),
            ("04", "Lealdade é o único código aprendido",
             "Sem família nem escola, os capitães criam ética interna baseada em fidelidade ao grupo. É frágil, mas é o que há."),
            ("05", "Dora é o feminino que falta",
             "O livro é majoritariamente masculino. Dora aparece e mostra o que poderia ter sido — antes de morrer."),
            ("06", "Livros queimados queimam menos do que vergonha guardada",
             "O Estado Novo queimou o livro. Vendeu mais. O que o poder quer esquecer, a literatura insiste em lembrar."),
        ],
        "application": [
            ("Pesquise sobre crianças em situação de rua hoje", "Quantas existem na sua cidade? Que ONGs atuam? O que muda em 85 anos?"),
            ("Visite o sistema socioeducativo da sua cidade", "Como funciona o equivalente moderno do reformatório? O que mudou?"),
            ("Apoie 1 ONG que cuida da causa", "Doe, voluntarie, divulgue. O livro pede ação, não apenas leitura."),
            ("Conheça outros livros de denúncia social brasileiros", "<i>Vidas Secas</i> (Graciliano), <i>Quarto de Despejo</i> (Carolina Maria de Jesus), <i>Cidade de Deus</i> (Paulo Lins)."),
            ("Releia em outro contexto", "Releia o capítulo do reformatório depois de ver um documentário sobre Fundação Casa, por exemplo."),
            ("Converse com jovens sobre o livro", "Se você tem filho, sobrinho, aluno — leia junto. As perguntas que eles fazem mudam a sua leitura."),
        ],
        "quotes": [
            ("Eles tinham na carne a mesma queimadura do sol.", "Amado"),
            ("Dora veio para o trapiche e o trapiche teve mãe.", "Capítulo Dora"),
            ("A cidade os ignorava — exceto quando faziam perda na imprensa.", "Narrador"),
            ("Pedro Bala era loiro como o sol da Bahia.", "Descrição"),
            ("O reformatório os recebia para devolvê-los criminosos.", "Síntese leitor"),
            ("Os capitães não tinham nome — tinham apelido.", "Narrador"),
            ("Eles eram os meninos de quem ninguém quis ser pai.", "Síntese"),
        ],
        "reflections": [
            "Quantos 'capitães da areia' existem na sua cidade hoje — e você sabe os números?",
            "Em qual cena recente da sua vida você viu uma criança sem proteção — e desviou?",
            "Que serviços públicos da sua cidade equivalem ao reformatório do livro — e como eles funcionam?",
            "Que ONG, abrigo ou projeto da sua cidade trabalha com esses meninos — e você nunca soube?",
            "Que conforto você tem hoje que pressupõe a invisibilidade dessas crianças?",
            "Que ato concreto, esta semana, te aproxima dessa realidade — em vez de te afastar?",
        ],
        "last_word_title": "Os meninos da areia.",
        "last_word_quote": "85 anos depois do livro, os meninos continuam na areia — agora em outras cidades, com outros nomes, mas com a mesma fome. Lembrar deles é o mínimo.",
    },

    # ─── 18 · O Pequeno Príncipe ───
    {
        "id": "pequeno_principe", "vol": "18",
        "title_main": "O Pequeno", "title_sub": "Príncipe.",
        "short_title": "O Pequeno Príncipe",
        "subtitle": "Fábula filosófica de Antoine de Saint-Exupéry · 1943.",
        "author": "Antoine de Saint-Exupéry",
        "year_orig": "1943", "year_br": "1954", "publisher": "Agir / Harper",
        "pages": "Aproximadamente 96 páginas", "pages_count": 26,
        "genre": "Fábula · Filosófico · Infanto-juvenil",
        "category_kicker": "Fábula · Filosofia · Conto",
        "motif": "star",
        "palette": {"paper": "#EDF3F6", "ink": "#0E2C46", "accent": "#C2A030",
                    "muted": "#7D8590", "hairline": "#CCD8DF", "subink": "#173A5C",
                    "paper_dark": "#DDE8EF", "title_font": "Times-Bold"},
        "title_font": "Times-Bold",
        "abstract": ("Resumo de <b>O Pequeno Príncipe</b>, fábula filosófica do aviador "
                     "francês Antoine de Saint-Exupéry. Apresenta o enredo do deserto e dos "
                     "planetas, os encontros simbólicos, e os ensinamentos sobre amor, perda e "
                     "responsabilidade."),
        "thesis": "O essencial é invisível aos olhos. Adultos esqueceram disso; o livro pede que voltemos a ver.",
        "headline_quote": "Tu te tornas eternamente responsável por aquilo que cativas.",
        "about_author": [
            "<b>Antoine de Saint-Exupéry</b> (1900–1944) foi um aviador, escritor e ensaísta "
            "francês. Pioneiro da aviação postal — voou correspondências em rotas perigosas pela "
            "África, América do Sul, deserto do Saara.",
            "Em 1935 caiu com seu avião no Saara — sobreviveu três dias sem água até ser "
            "resgatado por beduínos. Essa experiência inspira <i>O Pequeno Príncipe</i> (1943), "
            "escrito durante o exílio em Nova York durante a 2ª Guerra Mundial.",
            "Saint-Exupéry morreu em 1944, em missão de reconhecimento, abatido pela Luftwaffe "
            "sobre o Mediterrâneo. Seu livro infantil-filosófico é o mais traduzido do mundo "
            "depois da Bíblia, em mais de 500 idiomas."],
        "big_idea": ("Um aviador cai no Saara e encontra um menino vindo de um asteróide. O "
                     "menino conta sua história: a rosa que amava, os 7 planetas que visitou, "
                     "cada um com um adulto curioso e triste. Por fim chega à Terra, encontra a "
                     "raposa, descobre o amor e decide voltar."),
        "chapters": [
            {"num": "01", "kicker": "Abertura",
             "title": "O desenho da jiboia",
             "intro": ("O livro abre com o aviador-narrador lembrando: aos 6 anos desenhou uma "
                       "jiboia digerindo um elefante. Os adultos enxergaram um chapéu. Aprendeu, "
                       "então, a não falar com adultos sobre essas coisas — e a falar 'sobre "
                       "bridge, golfe, política, gravatas'."),
             "bullets": [
                 "Adultos perdem a capacidade de ver o invisível.",
                 "Crianças vêem; adultos categorizam.",
                 "A maioria dos diálogos com adultos é sobre o exterior — não sobre o que importa.",
                 "O narrador escolhe seu interlocutor pelo desenho da jiboia.",
             ],
             "callout_label": "ABERTURA",
             "callout": "Toda a obra é dirigida a quem ainda enxerga jiboia. Se você só vê chapéu, é tarde para começar — mas dá pra tentar."},

            {"num": "02", "kicker": "Encontro",
             "title": "O aviador no deserto",
             "intro": ("O aviador-narrador cai no Saara com avaria no motor. Sozinho, longe de "
                       "tudo. No primeiro amanhecer, é despertado por uma voz pequena: 'Por "
                       "favor... desenha-me um carneiro.' É o Pequeno Príncipe."),
             "bullets": [
                 "Cenário: deserto absoluto, isolamento total.",
                 "Aparição inexplicada — o livro nunca tenta explicar.",
                 "O aviador desenha. O Príncipe rejeita os três primeiros. Aceita o quarto: uma caixa com furos.",
                 "Aceitar a invisibilidade é a condição de comunicação.",
             ],
             "callout_label": "PEDIDO",
             "callout": "O Príncipe não pede um carneiro real — pede uma caixa onde ele possa imaginá-lo. O essencial é o que se imagina, não o que se vê."},

            {"num": "03", "kicker": "Asteróide B-612",
             "title": "A rosa do Príncipe",
             "intro": ("O Príncipe vem de um pequeno asteróide. Ali ele tem três vulcões — dois "
                       "ativos e um adormecido —, e uma rosa única. A rosa é vaidosa, exigente, "
                       "tossendo de propósito. O Príncipe se cansa, se sente enganado, parte."),
             "bullets": [
                 "Rosa é o primeiro amor — bonito mas difícil.",
                 "Princípio: amor real exige paciência com defeitos.",
                 "O Príncipe parte achando que se desligaria. Não consegue.",
                 "Antes de partir, arruma o planeta: limpa vulcões, arranca baobás.",
             ],
             "callout_label": "ALEGORIA",
             "callout": "A rosa é todo amor inicial. A pessoa parte porque acha que pode esquecer — depois descobre que cativou e foi cativado."},

            {"num": "04", "kicker": "Sete planetas",
             "title": "Os adultos",
             "intro": ("O Príncipe visita 7 planetas, cada um com um adulto. Rei (obsessão por "
                       "ordem), Vaidoso (obsessão por elogio), Bêbado (vergonha em loop), "
                       "Homem de negócios (acumulação sem sentido), Acendedor (rotina mecânica), "
                       "Geógrafo (saber sem experiência), Terra (todos os anteriores juntos)."),
             "bullets": [
                 "<b>Rei</b>: governa sozinho, dá ordens razoáveis demais para o nada.",
                 "<b>Vaidoso</b>: só ouve elogios.",
                 "<b>Bêbado</b>: bebe para esquecer que tem vergonha de beber.",
                 "<b>Homem de negócios</b>: conta estrelas; não as olha.",
                 "<b>Acendedor</b>: bom de coração; preso em rotina absurda.",
                 "<b>Geógrafo</b>: registra, mas nunca viaja.",
             ],
             "callout_label": "DIAGNÓSTICO",
             "callout": "Cada adulto perdeu uma faceta da inteireza. Reconheça-se em qual deles você passa a maior parte do dia."},

            {"num": "05", "kicker": "Terra 1",
             "title": "Cinco mil rosas",
             "intro": ("Na Terra, o Príncipe encontra um jardim com 5 mil rosas. Choca-se — "
                       "achava que sua rosa era única no universo. Tem uma crise: sua rosa não "
                       "era especial; era só uma a mais. A descoberta o derruba."),
             "bullets": [
                 "Crise da unicidade: o que ele amava era comum.",
                 "Acha-se 'um príncipe muito pobre'.",
                 "Choro genuíno — primeira queda do menino.",
                 "Está pronto para o ensinamento da raposa.",
             ],
             "callout_label": "QUEDA",
             "callout": "Quase todo amor passa pela descoberta de que o ser amado é comum. É aí que o amor pode terminar — ou começar de verdade."},

            {"num": "06", "kicker": "Terra 2",
             "title": "A raposa",
             "intro": ("A raposa pede para ser <b>cativada</b>. Ensina a palavra: 'criar laços'. "
                       "Cativar é assumir responsabilidade. Quando cativados, deixamos de ser "
                       "comuns para o outro — é o tempo dedicado que faz a diferença. Sua rosa "
                       "é única porque ele cuidou dela."),
             "bullets": [
                 "<b>Cativar</b>: criar laços. Antes éramos estranhos; depois somos únicos.",
                 "O essencial é invisível aos olhos.",
                 "Tu te tornas eternamente responsável por aquilo que cativas.",
                 "Tempo dedicado é o que faz a coisa importante.",
             ],
             "quote": "É o tempo que perdeste com a tua rosa que tornou tua rosa tão importante.",
             "callout_label": "ENSINAMENTO CENTRAL",
             "callout": "Cativar é assumir responsabilidade. Esse é o pacto adulto que o livro pede que você lembre."},

            {"num": "07", "kicker": "Terra 3",
             "title": "A serpente, a partida",
             "intro": ("O Príncipe percebe que ama a rosa e precisa voltar. Encontra uma serpente "
                       "amarela — promete picá-lo para 'devolvê-lo às estrelas'. O Príncipe se "
                       "despede do aviador e aceita a mordida. Cai como se dormisse."),
             "bullets": [
                 "O corpo é pesado demais para voltar ao asteróide.",
                 "A serpente é instrumento da volta — não vilã.",
                 "Despedida sem drama, como criança que vai dormir.",
                 "Aviador encontra o corpo na areia ao amanhecer — desaparecerá depois.",
             ],
             "callout_label": "LEITURA",
             "callout": "Saint-Exupéry usa a morte como retorno à origem. É leitura possível — a sua, talvez, seja outra."},

            {"num": "08", "kicker": "Encerramento",
             "title": "Mas as estrelas riem",
             "intro": ("O aviador conserta o motor e parte. Carrega consigo um segredo: agora, "
                       "ao olhar para as estrelas, ele sabe que em uma delas vive o Príncipe e a "
                       "rosa. As estrelas riem para ele. Cada vez que olha, são presente."),
             "bullets": [
                 "Olhar para o céu nunca mais é igual.",
                 "Para quem cativou, o universo inteiro fala.",
                 "O aviador pede ao leitor: se algum dia encontrar uma criança loura no deserto, escreva.",
                 "Final aberto, terno, melancólico.",
             ],
             "callout_label": "PEDIDO",
             "callout": "Saint-Exupéry termina pedindo cuidado. O Príncipe pode aparecer em qualquer canto. Olhe."},

            {"num": "09", "kicker": "Síntese",
             "title": "Por que ainda lemos",
             "intro": ("O livro foi escrito durante a 2ª Guerra. Saint-Exupéry, em exílio, "
                       "vivendo a derrocada da França. A obra é o oposto da guerra: ternura, "
                       "infância, vínculo. Por isso atravessou décadas — porque o que ele "
                       "descreve não passa de moda."),
             "bullets": [
                 "O essencial é invisível aos olhos — verdade que cada geração precisa redescobrir.",
                 "Cativar é assumir responsabilidade — definição de amor que precede contratos.",
                 "Os 7 adultos são alegorias atuais.",
                 "Releia adulto. O livro infantil é, na verdade, para adultos cansados.",
             ],
             "callout_label": "VOLTA",
             "callout": "O livro tem 26 páginas no caderno — mas vai te seguir o resto da vida. Volte a ele toda vez que se sentir um dos sete adultos."},
        ],
        "insights": [
            ("01", "Adultos esquecem o invisível",
             "Não por maldade — por treino. A escola, o trabalho, as cobranças nos treinam a só ver o quantificável."),
            ("02", "Cativar é responsabilidade vitalícia",
             "Esta é, talvez, a frase mais ética do livro. Pessoas, animais, projetos: quando cativamos, assumimos. Não dá para 'sair'."),
            ("03", "Tempo dedicado é o que faz a unicidade",
             "A rosa do Príncipe não era genética — era cuidada. Tudo o que amamos é assim."),
            ("04", "Os 7 adultos são você em diferentes dias",
             "Rei (no dia mandão), Vaidoso (no dia inseguro), Homem de negócios (no dia produtivista), etc. Não há herói — só fragmentos."),
            ("05", "Crise da unicidade é parte do amor",
             "Descobrir que o ser amado é comum derruba o amor inicial. É aí que o amor maduro pode começar."),
            ("06", "Voltar é tão importante quanto partir",
             "O Príncipe parte e volta. A jornada não termina no oásis — termina na rosa de novo."),
        ],
        "application": [
            ("Releia hoje", "26 páginas em duas horas. Diferente de qualquer leitura que você fez aos 10."),
            ("Identifique o seu 'rei interno'", "Em qual dos 7 adultos você passa mais horas por semana? E o que faria diferente?"),
            ("Faça a sua lista de 'cativados'", "Liste 10 pessoas, projetos, lugares que você cativou — e portanto, por quem é responsável."),
            ("Visite 1 'rosa' que você abandonou", "Alguém ou algo que você cativou e desistiu. Reabra o contato esta semana."),
            ("Pratique 'desenho da jiboia'", "Em alguma conversa esta semana, fale do invisível — sentimento, sonho, dúvida. Veja quem ainda enxerga."),
            ("Compartilhe com alguém de 8 anos", "Leia para uma criança próxima. As perguntas dela vão te ensinar."),
        ],
        "quotes": [
            ("O essencial é invisível aos olhos.", "A raposa"),
            ("Tu te tornas eternamente responsável por aquilo que cativas.", "A raposa"),
            ("É o tempo que perdeste com a tua rosa que torna tua rosa tão importante.", "A raposa"),
            ("Os adultos são muito estranhos.", "O Pequeno Príncipe"),
            ("Mas as estrelas riem, para ele.", "Final do aviador"),
            ("Por favor, desenha-me um carneiro.", "Primeira fala"),
            ("Toda gente grande começou sendo criança — mas pouca lembra.", "Saint-Exupéry"),
        ],
        "reflections": [
            "Qual dos 7 adultos do livro melhor descreve você na maior parte das semanas?",
            "Quem foi a sua rosa — e o quanto você ainda é responsável por ela?",
            "Que cativado recente você está adiando responsabilidade — pessoa, projeto, animal, lugar?",
            "Em qual conversa essa semana você desenhou apenas o chapéu, quando podia desenhar a jiboia?",
            "Que ato pequeno (5 minutos) você pode fazer hoje para cuidar de algo que você cativou?",
            "Que invisível você precisa voltar a enxergar — porque os adultos te ensinaram a ignorar?",
        ],
        "last_word_title": "Cativar.",
        "last_word_quote": "O essencial não cabe nos olhos — só no tempo. Quanto tempo você dedica ao que disse que amava?",
    },
]
