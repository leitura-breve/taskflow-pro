"""Dados dos produtos Leitura Breve para cadastro na Cakto.

Estrutura: 38 livros como produtos individuais + 1 produto-assinatura.
Cada item tem nome, descricao curta, descricao longa, preco, categoria e
caminho do arquivo PDF.

Esses dados sao consumidos por cakto_sync.py.
"""

import os

OUT_DIR = "/home/user/taskflow-pro"

# Preço padrão por unidade (em reais). Ajuste conforme estratégia.
PRECO_INDIVIDUAL = 1990   # R$ 19,90  (em centavos)
PRECO_ASSINATURA_MENSAL = 1990  # R$ 19,90/mês
PRECO_ASSINATURA_ANUAL = 14900  # R$ 149,00/ano (desconto)

# ─────────────────────────────────────────────────────
# 38 LIVROS
# ─────────────────────────────────────────────────────
# Cada linha: (vol, id, titulo, autor, categoria_kicker, tese, headline_quote, pdf)
BOOKS_META = [
    ("01", "habitos_atomicos",    "Hábitos Atômicos",                              "James Clear",                "Comportamento · Desenvolvimento pessoal",        "Você não se eleva ao nível das suas metas — cai ao nível dos seus sistemas.", "Hábitos são os juros compostos do autoaperfeiçoamento.", "Habitos_Atomicos_Resumo.pdf"),
    ("02", "alquimista",          "O Alquimista",                                  "Paulo Coelho",               "Fábula · Filosófico · Literatura brasileira",    "Quando você quer alguma coisa, todo o universo conspira para que você realize o seu desejo.", "Maktub. Está escrito.", "O_Alquimista_Resumo.pdf"),
    ("03", "sutil_arte",          "A Sutil Arte de Ligar o F*da-Se",               "Mark Manson",                "Desenvolvimento pessoal · Contraintuitivo",       "Não dar a mínima não é apatia. É escolher exatamente sobre o que se importar.", "Escolha o seu sofrimento.", "A_Sutil_Arte_Resumo.pdf"),
    ("04", "poder_habito",        "O Poder do Hábito",                             "Charles Duhigg",             "Comportamento · Neurociência · Negócios",         "Todo hábito é um loop deixa → rotina → recompensa. Compreender o loop é o começo de transformá-lo.", "A vida toda, tal como a conhecemos, é uma massa de hábitos.", "Vol_04_poder_habito.pdf"),
    ("05", "mindset",             "Mindset",                                       "Carol S. Dweck",             "Psicologia · Educação · Aprendizagem",            "Não é o talento que define a sua trajetória, é a mentalidade com que você encara o esforço, a falha e a crítica.", "O passe que você consegue dar não é mais importante do que o passe que você ainda não consegue dar.", "Vol_05_mindset.pdf"),
    ("06", "milagre_manha",       "O Milagre da Manhã",                            "Hal Elrod",                  "Rotina · Disciplina · Manhã",                     "A forma como você acorda determina a qualidade do seu dia.", "O nível de sucesso que você alcança raramente ultrapassa o nível do seu desenvolvimento pessoal.", "Vol_06_milagre_manha.pdf"),
    ("07", "pai_rico",            "Pai Rico, Pai Pobre",                           "Robert T. Kiyosaki",         "Finanças · Educação financeira · Mentalidade",    "Não é o quanto você ganha — é o quanto você guarda, faz crescer e quantas gerações você banca com isso.", "Os ricos compram ativos. Os pobres só têm despesas.", "Vol_07_pai_rico.pdf"),
    ("08", "sete_habitos",        "Os 7 Hábitos das Pessoas Altamente Eficazes",   "Stephen R. Covey",           "Liderança · Eficácia · Princípios",                "Eficácia é caráter — não técnica. E caráter se constrói por princípios universais postos em hábito.", "Entre estímulo e resposta há um espaço. Nesse espaço está a nossa liberdade.", "Vol_08_sete_habitos.pdf"),
    ("09", "amigos",              "Como Fazer Amigos e Influenciar Pessoas",       "Dale Carnegie",              "Comunicação · Relações · Persuasão",              "Quase todo conflito humano nasce da necessidade não atendida de se sentir importante.", "Você pode fazer mais amigos em dois meses interessando-se pelos outros do que em dois anos tentando o contrário.", "Vol_09_amigos.pdf"),
    ("10", "babilonia",           "O Homem Mais Rico da Babilônia",                "George S. Clason",           "Finanças · Parábola · Sabedoria antiga",          "Riqueza não é mistério antigo nem privilégio moderno — é uma técnica simples que poucos têm a paciência de aplicar.", "Uma parte de tudo o que você ganha é sua para guardar.", "Vol_10_babilonia.pdf"),
    ("11", "monge",               "O Monge e o Executivo",                         "James C. Hunter",            "Liderança · Servidora · Parábola",                "Liderança não é autoridade conferida por um cargo — é influência ganha por serviço, caráter e amor.", "Liderar é identificar e satisfazer as necessidades legítimas das pessoas.", "Vol_11_monge.pdf"),
    ("12", "ie",                  "Inteligência Emocional",                        "Daniel Goleman",             "Psicologia · Neurociência · Relações",            "QE pode importar mais que QI. Quem domina as próprias emoções e lê as dos outros, lidera, prospera e ama melhor.", "Em um sentido muito real, todos nós temos duas mentes — uma que pensa e outra que sente.", "Vol_12_ie.pdf"),
    ("13", "rapido_devagar",      "Rápido e Devagar",                              "Daniel Kahneman",            "Cognição · Decisão · Vieses",                     "Você não é a voz da razão. É dois sistemas em conflito — e o rápido decide mais do que você imagina.", "Confiança não é um índice de acurácia. É um índice de coerência.", "Vol_13_rapido_devagar.pdf"),
    ("14", "trabalhe4h",          "Trabalhe 4 Horas por Semana",                   "Timothy Ferriss",            "Tempo · Lifestyle Design · Empreendedorismo",     "Não trabalhe mais — trabalhe menos, melhor. A vida é projetada, não passada.", "A questão não é aposentadoria — é mini-aposentadorias.", "Vol_14_trabalhe4h.pdf"),
    ("15", "mente_milionaria",    "Os Segredos da Mente Milionária",               "T. Harv Eker",               "Mentalidade · Finanças · Crenças",                "Sua conta bancária reflete o seu plano interno do dinheiro.", "Pensamento → Sentimento → Ação → Resultado.", "Vol_15_mente_milionaria.pdf"),
    ("16", "dom_casmurro",        "Dom Casmurro",                                  "Machado de Assis",           "Literatura brasileira · Romance · Ciúme",         "A questão do livro não é 'Capitu traiu?' — é 'Bento merece ser acreditado?'.", "Capitu, olhos de ressaca.", "Vol_16_dom_casmurro.pdf"),
    ("17", "capitaes_areia",      "Capitães da Areia",                             "Jorge Amado",                "Literatura brasileira · Bahia · Justiça social",  "Crianças abandonadas ao próprio destino se organizam — e a sociedade que as abandona é a verdadeira ré.", "Eles tinham na carne a mesma queimadura do sol.", "Vol_17_capitaes_areia.pdf"),
    ("18", "pequeno_principe",    "O Pequeno Príncipe",                            "Antoine de Saint-Exupéry",   "Fábula · Filosofia · Conto",                      "O essencial é invisível aos olhos.", "Tu te tornas eternamente responsável por aquilo que cativas.", "Vol_18_pequeno_principe.pdf"),
    ("19", "comece_porque",       "Comece pelo Porquê",                            "Simon Sinek",                "Liderança · Propósito · Negócios",                "As pessoas não compram o que você faz; compram o porquê você faz.", "Inspirar começa pelo porquê.", "Vol_19_comece_porque.pdf"),
    ("20", "coragem_imperfeito",  "A Coragem de Ser Imperfeito",                   "Brené Brown",                "Vulnerabilidade · Vergonha · Coragem",            "Vulnerabilidade não é fraqueza — é o nascimento da coragem.", "Aparecer e deixar-se ver — isso é vulnerabilidade.", "Vol_20_coragem_imperfeito.pdf"),
    ("21", "essencialismo",       "Essencialismo",                                 "Greg McKeown",               "Foco · Prioridades · Decisão",                    "Menos, mas melhor. Quem não escolhe suas prioridades, é escolhido pelas dos outros.", "Se você não prioriza sua vida, alguém vai fazê-lo por você.", "Vol_21_essencialismo.pdf"),
    ("22", "antifragil",          "Antifrágil",                                    "Nassim Taleb",               "Risco · Filosofia · Decisão sob incerteza",       "O oposto de frágil não é robusto. É antifrágil — o que ganha com o estresse, a incerteza e o caos.", "Frágil quebra com volatilidade. Antifrágil prospera.", "Vol_22_antifragil.pdf"),
    ("23", "arte_guerra",         "A Arte da Guerra",                              "Sun Tzu",                    "Estratégia · Liderança · Clássico chinês",        "A maior vitória é vencer sem precisar lutar.", "Conheça o inimigo e a si mesmo, e em cem batalhas não correrá perigo.", "Vol_23_arte_guerra.pdf"),
    ("24", "meditacoes",          "Meditações",                                    "Marco Aurélio",              "Estoicismo · Diário · Clássico romano",           "O que está em seu poder não é o que acontece — é o que você pensa sobre o que acontece.", "Você tem poder sobre sua mente — não sobre os eventos.", "Vol_24_meditacoes.pdf"),
    ("25", "leis_poder",          "As 48 Leis do Poder",                           "Robert Greene",              "Poder · Estratégia · Polêmico",                   "O poder é jogo eterno entre humanos. Conhecer as regras é defesa.", "Nunca ofusque o senhor.", "Vol_25_leis_poder.pdf"),
    ("26", "oceano_azul",         "A Estratégia do Oceano Azul",                   "W. Chan Kim & R. Mauborgne", "Estratégia · Inovação · Mercado",                 "Empresas que vencem por décadas competem em um lugar onde quase ninguém está.", "A única forma de vencer a concorrência é parar de competir com ela.", "Vol_26_oceano_azul.pdf"),
    ("27", "zero_a_um",           "De Zero a Um",                                  "Peter Thiel",                "Empreendedorismo · Tecnologia · Inovação",        "Cópia leva o mundo de 1 a n. Inovação leva de 0 a 1.", "O próximo Bill Gates não vai criar um sistema operacional.", "Vol_27_zero_a_um.pdf"),
    ("28", "tudo_foda",           "Tudo é F*da",                                   "Mark Manson",                "Filosofia · Esperança · Contraintuitivo",         "Esperança não é virtude — é a substância que nos faz adiar a vida.", "Vida é como ler um romance sabendo o final.", "Vol_28_tudo_foda.pdf"),
    ("29", "busca_sentido",       "O Homem em Busca de Sentido",                   "Viktor Frankl",              "Logoterapia · Sobrevivência · Sentido",           "Quem tem um porquê pode suportar qualquer como.", "A última das liberdades humanas é a de escolher a atitude.", "Vol_29_busca_sentido.pdf"),
    ("30", "vidas_secas",         "Vidas Secas",                                   "Graciliano Ramos",           "Literatura brasileira · Sertão · Modernismo",     "Há sofrimentos tão antigos que tomaram a forma de paisagem.", "Pareciam mudos. Falavam pouco.", "Vol_30_vidas_secas.pdf"),
    ("31", "bras_cubas",          "Memórias Póstumas de Brás Cubas",               "Machado de Assis",           "Literatura brasileira · Realismo · Sátira",       "A vida é absurda — e o melhor humor sobre ela vem depois da morte.", "Não tive filhos, não transmiti a nenhuma criatura o legado da nossa miséria.", "Vol_31_bras_cubas.pdf"),
    ("32", "hora_estrela",        "A Hora da Estrela",                             "Clarice Lispector",          "Literatura brasileira · Modernismo · Solidão",    "Existem vidas que ninguém narra.", "Quem é mais pobre? Eu, que tenho a palavra, ou ela, que não tem nada?", "Vol_32_hora_estrela.pdf"),
    ("33", "quarto_despejo",      "Quarto de Despejo",                             "Carolina Maria de Jesus",    "Diário · Favela · Brasil real",                   "Existe um Brasil que escreve com lápis curto sobre cadernos achados no lixo.", "A favela é o quintal onde São Paulo joga o lixo.", "Vol_33_quarto_despejo.pdf"),
    ("34", "cem_anos",            "Cem Anos de Solidão",                           "Gabriel García Márquez",     "Realismo mágico · Saga · América Latina",         "Há famílias condenadas a repetir. Quem nomeia o ciclo, quebra-o.", "As estirpes condenadas a cem anos de solidão não têm uma segunda oportunidade.", "Vol_34_cem_anos.pdf"),
    ("35", "1984",                "1984",                                          "George Orwell",              "Distopia · Vigilância · Poder",                   "A liberdade é poder dizer que dois mais dois são quatro.", "Quem controla o passado, controla o futuro.", "Vol_35_1984.pdf"),
    ("36", "anne_frank",          "O Diário de Anne Frank",                        "Anne Frank",                 "Holocausto · Memória · Adolescência",             "Humanidade não desaparece — é apagada.", "Apesar de tudo, eu ainda acredito que as pessoas são, no fundo, boas.", "Vol_36_anne_frank.pdf"),
    ("37", "revolucao_bichos",    "A Revolução dos Bichos",                        "George Orwell",              "Alegoria · Política · Revolução",                 "Toda revolução fala em igualdade enquanto faz; algumas, depois, traduzem 'iguais' por 'mais iguais'.", "Todos os animais são iguais. Mas alguns animais são mais iguais que outros.", "Vol_37_revolucao_bichos.pdf"),
    ("38", "sapiens",             "Sapiens",                                       "Yuval Noah Harari",          "História · Antropologia · Big history",            "Sapiens domina o planeta por uma habilidade única: contar histórias em que muita gente acredita ao mesmo tempo.", "Há 70 mil anos, sapiens era um primata insignificante.", "Vol_38_sapiens.pdf"),
    ("39", "poder_agora",         "O Poder do Agora",                              "Eckhart Tolle",              "Presença · Espiritualidade · Mente",               "Você não é a sua mente. Todo sofrimento real acontece quando você abandona o agora.", "Perceba profundamente que o momento presente é tudo o que você sempre terá.", "Vol_39_poder_agora.pdf"),
    ("40", "pense_enriqueca",     "Quem Pensa Enriquece",                          "Napoleon Hill",              "Riqueza · Mentalidade · Clássico americano",        "Riqueza começa como estado mental: desejo definido, fé, plano e persistência.", "Tudo o que a mente pode conceber e acreditar, ela pode alcançar.", "Vol_40_pense_enriqueca.pdf"),
    ("41", "linguagens_amor",     "As Cinco Linguagens do Amor",                   "Gary Chapman",               "Amor · Casal · Comunicação",                       "As pessoas falam línguas de amor diferentes. Quase todo casamento em crise é dois monolíngues gritando.", "O amor que você sente não chega ao outro se for entregue na língua errada.", "Vol_41_linguagens_amor.pdf"),
    ("42", "cnv",                 "Comunicação Não-Violenta",                      "Marshall Rosenberg",         "Comunicação · Empatia · Conflito",                  "Por trás de toda agressão há uma necessidade não atendida falando errado.", "Toda crítica é a expressão trágica de uma necessidade não atendida.", "Vol_42_cnv.pdf"),
    ("43", "coragem_nao_agradar", "A Coragem de Não Agradar",                      "Ichiro Kishimi & Fumitake Koga", "Liberdade · Psicologia de Adler · Diálogo",     "Toda liberdade começa quando você aceita a possibilidade de não ser aprovado.", "A liberdade é ser capaz de ser detestado por outras pessoas.", "Vol_43_coragem_nao_agradar.pdf"),
    ("44", "12_regras",           "12 Regras para a Vida",                         "Jordan B. Peterson",         "Ordem · Responsabilidade · Sentido",                "A resposta ao sofrimento é assumir a maior carga de responsabilidade que você consegue carregar.", "Compare-se com quem você era ontem, não com quem outra pessoa é hoje.", "Vol_44_12_regras.pdf"),
    ("45", "garra",               "Garra",                                         "Angela Duckworth",           "Perseverança · Talento · Esforço",                  "Talento conta uma vez; esforço conta duas. Garra prevê quem chega melhor do que QI ou dom.", "Nosso potencial é uma coisa. O que fazemos com ele é outra completamente diferente.", "Vol_45_garra.pdf"),
    ("46", "ansiedade_cury",      "Ansiedade — O Mal do Século",                   "Augusto Cury",               "Ansiedade · Mente · Autor brasileiro",              "A ansiedade moderna não é falta de calma — é excesso de pensamento.", "Não somos vítimas dos nossos pensamentos. Somos os autores — que esqueceram que podem editar.", "Vol_46_ansiedade_cury.pdf"),
    ("47", "mulheres_lobos",      "Mulheres que Correm com os Lobos",              "Clarissa Pinkola Estés",     "Arquétipos · Psicologia junguiana · Feminino",      "Dentro de toda mulher vive uma natureza instintiva e selvagem que a civilização ensinou a domesticar.", "Agradar aos outros exige que nos exilemos de nós mesmas.", "Vol_47_mulheres_lobos.pdf"),
    ("48", "menina_livros",       "A Menina que Roubava Livros",                   "Markus Zusak",               "Romance · Guerra · Narrado pela Morte",             "As mesmas palavras que Hitler usou para destruir, uma menina usou para sobreviver.", "Eu odiei as palavras e as amei.", "Vol_48_menina_livros.pdf"),
    ("49", "cabana",              "A Cabana",                                      "William P. Young",           "Fé · Luto · Perdão",                                "A pergunta do livro não é 'Deus existe?'. É 'onde Deus estava quando aconteceu o pior?'", "Dor tem um jeito de cortar nossas asas e nos impedir de voar.", "Vol_49_cabana.pdf"),
    ("50", "cortico",             "O Cortiço",                                     "Aluísio Azevedo",            "Naturalismo · Brasil do século XIX · Clássico",     "O protagonista não é uma pessoa — é o cortiço. O meio devora o indivíduo e o dinheiro devora a todos.", "Era um mundo, uma coisa viva.", "Vol_50_cortico.pdf"),
    ("51", "policarpo",           "Triste Fim de Policarpo Quaresma",              "Lima Barreto",               "Pré-modernismo · Patriotismo · Tragédia",           "Policarpo amou o Brasil em três atos — e foi punido pelos três.", "A pátria que quisera ter era um mito.", "Vol_51_policarpo.pdf"),
    ("52", "crime_castigo",       "Crime e Castigo",                               "Fiódor Dostoiévski",         "Literatura russa · Culpa · Consciência",            "O castigo não vem da polícia — vem de dentro. O romance é a anatomia dessa punição interna.", "Não foi a velha que eu matei. Foi a mim mesmo.", "Vol_52_crime_castigo.pdf"),
    ("53", "metamorfose",         "A Metamorfose",                                 "Franz Kafka",                "Kafka · Absurdo · Modernidade",                     "O horror não é o homem virar inseto. É a família descobrir, aliviada, que pode viver sem ele.", "Quando Gregor Samsa despertou, encontrou-se metamorfoseado num inseto monstruoso.", "Vol_53_metamorfose.pdf"),
]


def short_description(book):
    """Descrição curta (até ~150 caracteres) — para listagem."""
    vol, _id, titulo, autor, categoria, tese, _quote, _pdf = book
    return f"Resumo editorial de \"{titulo}\" ({autor}). 25-39 páginas com tese, capítulos comentados, citações e caderno de leitura."


def long_description(book):
    """Descrição longa (HTML simples) — para página de venda."""
    vol, _id, titulo, autor, categoria, tese, quote, _pdf = book
    return f"""<h2>Resumo editorial de <em>{titulo}</em></h2>
<p><strong>Autor:</strong> {autor}<br>
<strong>Categoria:</strong> {categoria}<br>
<strong>Coleção:</strong> Leitura Breve · Vol. {vol}</p>

<h3>A tese, em uma frase</h3>
<p><em>{tese}</em></p>

<h3>O que você recebe</h3>
<ul>
  <li>Resumo editorial completo em PDF (formato A4, design minimalista moderno)</li>
  <li>Tese central destacada</li>
  <li>Capítulos comentados com pontos-chave</li>
  <li>Citações em destaque (parede de citações)</li>
  <li>Insights e inversões</li>
  <li>Aplicação prática (passo a passo)</li>
  <li>Cronograma de 4 semanas para implantar as ideias</li>
  <li>Caderno de leitura com espaço para anotações</li>
  <li>Provocações pessoais para reflexão</li>
</ul>

<h3>Para quem é</h3>
<ul>
  <li>Quem quer entender a essência do livro em uma sessão de leitura</li>
  <li>Quem já leu e quer um caderno de revisão</li>
  <li>Quem prefere aplicar ideias a apenas ler sobre elas</li>
</ul>

<blockquote>"{quote}" — {autor}</blockquote>

<p>Parte da <strong>Coleção Leitura Breve</strong> — 53 volumes editoriais sobre os bestsellers que mais venderam no Brasil. Cada volume é um caderno completo, pensado para uma única sessão de leitura.</p>"""


def get_products():
    """Retorna lista de dicionarios com todos os produtos (38 livros + assinatura)."""
    products = []
    for b in BOOKS_META:
        vol, _id, titulo, autor, categoria, tese, quote, pdf = b
        products.append({
            "type": "digital",
            "external_id": f"leitura_breve_vol_{vol}",
            "vol": vol,
            "name": f"Vol. {vol} · {titulo} — Resumo Leitura Breve",
            "short_description": short_description(b),
            "long_description": long_description(b),
            "price_cents": PRECO_INDIVIDUAL,
            "category": categoria.split(" · ")[0],
            "tags": [t.strip() for t in categoria.split("·")] + [autor, "Leitura Breve"],
            "file_path": os.path.join(OUT_DIR, pdf),
            "delivery": "download",
        })
    # Assinatura
    products.append({
        "type": "subscription",
        "external_id": "leitura_breve_assinatura_mensal",
        "name": "Assinatura Leitura Breve — Mensal",
        "short_description": "Acesso a todos os 53 volumes da Coleção Leitura Breve + novos volumes que forem lançados.",
        "long_description": ASSINATURA_DESCRICAO,
        "price_cents": PRECO_ASSINATURA_MENSAL,
        "billing_cycle": "monthly",
        "category": "Assinatura",
        "tags": ["Assinatura", "Coleção completa", "Leitura Breve"],
        "delivery": "members_area",
    })
    products.append({
        "type": "subscription",
        "external_id": "leitura_breve_assinatura_anual",
        "name": "Assinatura Leitura Breve — Anual (37% off)",
        "short_description": "Acesso a todos os 53 volumes + novos lançamentos. Cobrança anual com desconto.",
        "long_description": ASSINATURA_DESCRICAO,
        "price_cents": PRECO_ASSINATURA_ANUAL,
        "billing_cycle": "yearly",
        "category": "Assinatura",
        "tags": ["Assinatura anual", "Coleção completa", "Leitura Breve"],
        "delivery": "members_area",
    })
    return products


ASSINATURA_DESCRICAO = """<h2>Assinatura Leitura Breve</h2>
<p>Acesso completo a <strong>todos os 53 volumes</strong> da Coleção Leitura Breve, mais os novos volumes que forem lançados durante a sua assinatura.</p>

<h3>O que você recebe</h3>
<ul>
  <li><strong>53 resumos editoriais</strong> em PDF (formato A4 minimalista) dos bestsellers que mais venderam no Brasil</li>
  <li><strong>Catálogo completo</strong> com fichas e índice navegável</li>
  <li><strong>Novos volumes</strong> incluídos automaticamente enquanto a assinatura estiver ativa</li>
  <li><strong>Atualizações</strong> dos volumes existentes (versões revisadas)</li>
</ul>

<h3>Coleção atual (53 volumes)</h3>
<p>Desenvolvimento pessoal · Negócios · Filosofia · Estoicismo · Literatura brasileira · Literatura mundial · Antropologia · História.</p>

<ul>
  <li>Hábitos Atômicos · O Alquimista · A Sutil Arte de Ligar o F*da-Se</li>
  <li>O Poder do Hábito · Mindset · O Milagre da Manhã</li>
  <li>Pai Rico, Pai Pobre · Os 7 Hábitos · Como Fazer Amigos</li>
  <li>Babilônia · O Monge e o Executivo · Inteligência Emocional</li>
  <li>Rápido e Devagar · 4 Horas por Semana · Mente Milionária</li>
  <li>Dom Casmurro · Capitães da Areia · O Pequeno Príncipe</li>
  <li>Comece pelo Porquê · A Coragem de Ser Imperfeito · Essencialismo</li>
  <li>Antifrágil · A Arte da Guerra · Meditações · 48 Leis do Poder</li>
  <li>Oceano Azul · De Zero a Um · Tudo é F*da</li>
  <li>Em Busca de Sentido · Vidas Secas · Brás Cubas</li>
  <li>A Hora da Estrela · Quarto de Despejo · Cem Anos de Solidão</li>
  <li>1984 · Diário de Anne Frank · A Revolução dos Bichos · Sapiens</li>
  <li>O Poder do Agora · Quem Pensa Enriquece · As 5 Linguagens do Amor</li>
  <li>Comunicação Não-Violenta · A Coragem de Não Agradar · 12 Regras para a Vida</li>
  <li>Garra · Ansiedade (Cury) · Mulheres que Correm com os Lobos</li>
  <li>A Menina que Roubava Livros · A Cabana · O Cortiço</li>
  <li>Policarpo Quaresma · Crime e Castigo · A Metamorfose</li>
</ul>

<h3>Como funciona</h3>
<ul>
  <li>Acesso imediato após a confirmação do pagamento</li>
  <li>Cobrança recorrente automática (cartão de crédito)</li>
  <li>Cancele a qualquer momento, sem multa</li>
  <li>Versão mensal: ideal para experimentar</li>
  <li>Versão anual: 37% de desconto, ideal para o leitor compromissado</li>
</ul>

<h3>Para quem é</h3>
<ul>
  <li>Quem lê muito e quer um arquivo organizado de resumos</li>
  <li>Quem nunca tem tempo de ler livro inteiro</li>
  <li>Quem prefere aplicar a só ler</li>
  <li>Quem quer um caderno de leitura para a vida toda</li>
</ul>"""


if __name__ == "__main__":
    # Auditoria rápida
    products = get_products()
    print(f"Total de produtos: {len(products)}")
    print(f"  - {sum(1 for p in products if p['type'] == 'digital')} livros individuais")
    print(f"  - {sum(1 for p in products if p['type'] == 'subscription')} assinaturas")
    # Verificar que todos os PDFs existem
    for p in products:
        if p.get("file_path") and not os.path.exists(p["file_path"]):
            print(f"  [AVISO] PDF não encontrado: {p['file_path']}")
        else:
            if p.get("file_path"):
                size_kb = os.path.getsize(p["file_path"]) // 1024
                print(f"  [OK]  {p['name'][:60]:60s} · {size_kb} KB")
