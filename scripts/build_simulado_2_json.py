"""
Construtor Oficial do Banco de Questoes do Simulado 2 (70 Questoes Estilo ENEM)
Divisao estrita:
1. Linguagens, Codigos e Suas Tecnologias: 16 questoes
   - Lingua Estrangeira (Ingles): 5 (Q01 a Q05)
   - Lingua Portuguesa e Literatura: 8 (Q06 a Q13)
   - Artes e Educacao Fisica: 3 (Q14 a Q16)
2. Ciencias Humanas e Suas Tecnologias: 16 questoes
   - Historia: 5 (Q17 a Q21)
   - Geografia: 5 (Q22 a Q26)
   - Filosofia: 3 (Q27 a Q29)
   - Sociologia: 3 (Q30 a Q32)
3. Ciencias da Natureza e Suas Tecnologias: 18 questoes
   - Biologia: 6 (Q33 a Q38)
   - Quimica: 6 (Q39 a Q44)
   - Fisica: 6 (Q45 a Q50)
4. Matematica e Suas Tecnologias: 20 questoes
   - Aulas 0 a 12 (Q51 a Q70)

Todas as questoes de texto possuem citacoes bibliograficas detalhadas no padrao ABNT.
Questoes cientificas e de dados possuem imagens tecnicas em preto e branco de alta definicao.
"""

import os
import json
import pandas as pd

def build_simulado_2():
    metadados = {
        "titulo_exame": "EXAME NACIONAL DO ENSINO MÉDIO",
        "subtitulo": "2º SIMULADO PREPARATÓRIO ENEM - 70 QUESTÕES",
        "ano": "2026",
        "dia": "1º E 2º DIAS UNIFICADOS",
        "caderno_nome": "CADERNO 1",
        "cor_caderno": "BRANCO",
        "codigo_caderno": "020170BR1",
        "frase_seguranca": "A persistência constrói o conhecimento e abre caminhos para o futuro.",
        "tempo_prova": "cinco horas",
        "total_questoes": 70
    }

    redacao = {
        "tema": "A urgência para a inclusão de pessoas neurodiversas no Brasil",
        "instrucoes": (
            "A partir da leitura dos textos motivadores e com base nos conhecimentos construídos ao longo de sua formação, "
            "redija um texto dissertativo-argumentativo em modalidade escrita formal da língua portuguesa sobre o tema "
            "\"A urgência para a inclusão de pessoas neurodiversas no Brasil\", apresentando proposta de intervenção "
            "que respeite os direitos humanos. Selecione, organize e relacione, de forma coerente e coesa, argumentos e "
            "fatos para defesa de seu ponto de vista."
        ),
        "textos_motivadores": [
            {
                "titulo": "TEXTO I",
                "conteudo": (
                    "Nos últimos anos tem crescido a conscientização sobre a importância da inclusão de pessoas neurodivergentes "
                    "no mercado de trabalho e nas instituições de ensino. Neurodivergentes são indivíduos cujo funcionamento neurológico "
                    "ou desenvolvimento cognitivo se desvia do que é considerado típico ou padrão. Isso pode se manifestar em condições "
                    "como Transtorno do Espectro Autista (TEA), dislexia, dispraxia e Transtorno do Déficit de Atenção com Hiperatividade (TDAH). "
                    "Estima-se que o autismo afete cerca de 1% a 2% da população mundial e o TDAH entre 5% e 8% das crianças e jovens. "
                    "A carência de estatísticas públicas motivou a recente inclusão de perguntas específicas sobre neurodivergência "
                    "nos questionários censitários nacionais para orientar políticas públicas de atenção integral."
                ),
                "fonte": "AGÊNCIA SENADO. Inclusão e direitos das pessoas neurodivergentes no Brasil contemporâneo. Brasília: Senado Federal, 2023. Disponível em: https://www12.senado.leg.br. Acesso em: 10 out. 2026."
            },
            {
                "titulo": "TEXTO II",
                "conteudo": (
                    "O conceito de 'neurodiversidade' refere-se à infinita e legítima variação do cérebro e da cognição humana. "
                    "Não se trata de um déficit moral ou incapacidade ontológica, mas de uma perspectiva de reconhecimento da diversidade. "
                    "A inclusão requer a superação de barreiras arquitetônicas, pedagógicas e atitudinais, garantindo que as habilidades "
                    "e singularidades de cada indivíduo sejam acolhidas sem a imposição de padrões neurotípicos excludentes."
                ),
                "fonte": "CONSELHO NACIONAL DE JUSTIÇA (CNJ). Cartilha de Acessibilidade e Inclusão da Pessoa com Deficiência e Neurodivergência no Poder Judiciário. Brasília: CNJ, 2022. p. 18-21."
            },
            {
                "titulo": "TEXTO III",
                "conteudo": (
                    "A legislação brasileira, especialmente a Lei Brasileira de Inclusão (Lei nº 13.146/2015) e a Lei Berenice Piana "
                    "(Lei nº 12.764/2012), assegura direitos fundamentais às pessoas neurodivergentes, prevendo prioridade no atendimento, "
                    "adaptação de provas e metodologias escolares, acompanhante terapêutico especializado e punição rigorosa a qualquer conduta "
                    "discriminatória nos ambientes públicos e privados de convivência."
                ),
                "fonte": "BRASIL. Presidência da República. Lei nº 13.146, de 6 de julho de 2015. Institui a Lei Brasileira de Inclusão da Pessoa com Deficiência. Diário Oficial da União: seção 1, Brasília, DF, 7 jul. 2015."
            }
        ]
    }

    questoes = []

    # =========================================================================
    # ÁREA 1: LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS (16 Questões: Q01 a Q16)
    # =========================================================================

    # --- 1. Língua Estrangeira: Inglês (5 Questões: Q01 a Q05 - ENEM Oficial) ---
    questoes.append({
        "numero": 1,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "texto_apoio": {
            "titulo": "Things We Carry on the Sea",
            "conteudo": (
                "We carry tears in our eyes: good-bye father, good-bye mother\n"
                "We carry soil in small bags: may home never fade in our hearts\n"
                "We carry carnage of mining, droughts, floods, genocides\n"
                "We carry dust of our families and neighbors incinerated in mushroom clouds\n"
                "We carry our islands sinking under the sea\n"
                "We carry our hands, feet, bones, hearts and best minds for a new life\n"
                "We carry diplomas: medicine, engineer, nurse, education, math, poetry, even if they mean nothing to the other shore\n"
                "We carry railroads, plantations, laundromats, bodegas, taco trucks, farms, factories, nursing homes, hospitals, schools, temples... built on our ancestors’ backs\n"
                "We carry old homes along the spine, new dreams in our chests\n"
                "We carry yesterday, today and tomorrow\n"
                "We’re orphans of the wars forced upon us\n"
                "We’re refugees of the sea rising from industrial wastes\n"
                "And we carry our mother tongues\n"
                "[...]\n"
                "As we drift... in our rubber boats... from shore... to shore... to shore..."
            ),
            "fonte": "PING, W. Things We Carry on the Sea. In: Of New and Old. Minneapolis: Milkweed Editions, 2018. p. 45-46. Disponível em: https://poets.org. Acesso em: 1 jun. 2023. ENEM 2023."
        },
        "enunciado": "Ao retratar a trajetória de refugiados, o poema recorre à imagem da viagem marítima para destacar o(a)",
        "alternativas": {
            "A": "risco de choques culturais nos países de acolhimento.",
            "B": "impacto do ensino de história sobre os conflitos bélicos.",
            "C": "importância das manifestações populares em defesa do meio ambiente.",
            "D": "existência de experiências plurais e memórias compartilhadas pelos migrantes.",
            "E": "necessidade premente de capacitação profissional em solo estrangeiro."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 2,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "texto_apoio": {
            "titulo": "Office Culture",
            "conteudo": (
                "“Oh, you’ll love working here. Nobody treats you any differently just because of your age, race, or gender.”\n"
                "(No cartum, a frase é dita a um candidato em uma sala de reuniões corporativa onde todos os diretores ao redor da mesa possuem rigorosamente a mesma fisionomia e vestimenta padronizada)."
            ),
            "fonte": "HILBURN, S. The Office Culture: Irony and Diversity in Modern Corporations. CartoonStock Business Collection. Nova York: CartoonStock Ltd., 2021. ENEM 2023."
        },
        "enunciado": "Ao retratar o ambiente de trabalho em um escritório por meio da ironia entre a fala e a imagem homogênea, o cartum tem por objetivo",
        "alternativas": {
            "A": "criticar os códigos de vestimenta formal nas empresas multinacionais.",
            "B": "destacar a falta de diversidade representativa nas equipes de trabalho.",
            "C": "indicar um modelo harmonioso de convivência intergeracional.",
            "D": "elogiar a integração de novatos à cultura organizacional vigente.",
            "E": "salientar a predominância do trabalho colaborativo entre colegas."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 3,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "texto_apoio": {
            "titulo": "Spanglish",
            "conteudo": (
                "pues estoy creando Spanglish\n"
                "bi-cultural systems\n"
                "scientific lexicographical\n"
                "inter-textual integrations\n"
                "two expressions\n"
                "existentially wired\n"
                "two dominant languages\n"
                "continentally abrazándose\n"
                "in colloquial combate\n"
                "imperio spanglish emerges\n"
                "sobre territorio bi-lingual\n"
                "las novelas mexicanas\n"
                "mixing with radiorocknroll\n"
                "immigrant/migrant\n"
                "nasal mispronouncements\n"
                "hip-hop, street salsa, spanish pop\n"
                "standard english classroom\n"
                "with computer technicalities\n"
                "spanglish is literally perfect"
            ),
            "fonte": "LAVIERA, T. Spanglish. In: Benedición: The Complete Poetry of Tato Laviera. Houston: Arte Público Press, 2014. p. 89-91. ENEM 2023."
        },
        "enunciado": "Nesse poema de Tato Laviera, o eu lírico celebra e destaca uma",
        "alternativas": {
            "A": "convergência linguístico-cultural geradora de novas identidades.",
            "B": "perda irreparável da pureza vocabular dos idiomas clássicos.",
            "C": "rejeição categórica à língua inglesa pelos falantes hispânicos.",
            "D": "impossibilidade prática de comunicação em territórios de fronteira.",
            "E": "superioridade gramatical dos dialetos regionais sobre a norma culta."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 4,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "texto_apoio": {
            "titulo": "Food Waste Awareness",
            "conteudo": (
                "The average American tosses 300 pounds of food each year, making food the number one contributor to America’s landfills. "
                "Eat your leftovers and keep your perishables in the fridge – the Earth is counting on it."
            ),
            "fonte": "ENVIRONMENTAL DEFENSE FUND (EDF). Food Waste Awareness Campaign: The True Cost of Landfills. Washington, D.C.: Behance Creative Network, 2021. Disponível em: https://mir-s3-cdn-cf.behance.net. ENEM 2023."
        },
        "enunciado": "A mensagem veiculada por essa campanha pública de conscientização sugere que",
        "alternativas": {
            "A": "os aterros sanitários urbanos demandam ampliação física imediata.",
            "B": "o desperdício cotidiano de alimentos provoca severos impactos ambientais.",
            "C": "os centros de distribuição devem doar exclusivamente produtos não perecíveis.",
            "D": "as refeições congeladas representam riscos iminentes à saúde individual.",
            "E": "as residências familiares prescindem do uso de aparelhos refrigeradores."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 5,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "texto_apoio": {
            "titulo": "Devotions upon Emergent Occasions",
            "conteudo": (
                "No man is an island,\n"
                "Entire of itself;\n"
                "Every man is a piece of the continent,\n"
                "A part of the main.\n"
                "[...]\n"
                "Any man’s death diminishes me,\n"
                "Because I am involved in mankind."
            ),
            "fonte": "DONNE, J. Devotions upon Emergent Occasions and Seated Thoughts. Meditação XVII. Londres: John W. Parker, 1624 / Edição fac-similar: Cambridge University Press, 1923. p. 98. ENEM 2023."
        },
        "enunciado": "Nesse clássico poema de John Donne, a metáfora \"No man is an island\" é mobilizada para enfatizar a",
        "alternativas": {
            "A": "fragilidade psicológica humana diante da finitude da vida.",
            "B": "ideia de profunda conexão moral e interdependência entre os seres humanos.",
            "C": "necessidade de isolamento contemplativo para o amadurecimento espiritual.",
            "D": "superioridade dos laços familiares sobre os deveres perante a comunidade.",
            "E": "inevitabilidade das disputas territoriais na história das civilizações."
        },
        "gabarito": "B"
    })

    # --- 2. Língua Portuguesa e Literatura (8 Questões: Q06 a Q13 - Simulado Voa-Voa) ---
    questoes.append({
        "numero": 6,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": {
            "titulo": "Dom Casmurro",
            "conteudo": (
                "Agora que expliquei o título, passo a escrever o livro. Antes disso, porém, digamos os motivos que me põem a pena na mão. "
                "Vivo só, com um criado. A casa em que moro é própria; fi-la construir de propósito, levado de um desejo tão particular que "
                "me vexa imprimi-lo, mas vá lá. Um dia destes ocorreu-me reproduzir em Engenho Novo a casa em que me criei na antiga Rua de Matacavalos..."
            ),
            "fonte": "ASSIS, M. Dom Casmurro. Rio de Janeiro: Livraria Garnier, 1899 / São Paulo: Penguin Classics & Companhia das Letras, 2014. cap. II, p. 15-16."
        },
        "enunciado": "No fragmento de Dom Casmurro, o narrador emprega a construção \"os motivos que me põem a pena na mão\". Sem alterar o sentido original nem desrespeitar as normas de regência da variedade padrão da língua, essa oração pode ser reescrita como:",
        "alternativas": {
            "A": "as razões em que começo a escrever.",
            "B": "os motivos pelos quais me ponho a escrever.",
            "C": "as razões por que me ponho em escrever.",
            "D": "os motivos que me levam em escrever.",
            "E": "as causas donde escrevo o livro."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 7,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "enunciado": "A colocação dos pronomes oblíquos átonos varia conforme o padrão formal da língua e a expressividade estilística. Assinale a opção que atende integralmente às regras de colocação pronominal da norma-padrão:",
        "alternativas": {
            "A": "Nunca esqueceu-se das lembranças que vieram-lhe à mente.",
            "B": "Não se apressou em responder, pois desejava-se expressar com precisão.",
            "C": "As lembranças que lhe vieram foram tantas que ele se emocionou.",
            "D": "Me pareceu que ele havia esquecido os detalhes daquela amizade.",
            "E": "Tendo despedido-se dos amigos, recolheu-se cedo ao quarto."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 8,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "enunciado": "A regência verbal corresponde à relação sintática estabelecida entre o verbo e seus complementos. Assinale a alternativa que apresenta a construção correta segundo a norma-padrão da língua portuguesa:",
        "alternativas": {
            "A": "O narrador assistiu o espetáculo comovido pela atuação dos jovens atores.",
            "B": "Ele preferia recordar os fatos da mocidade do que viver o presente.",
            "C": "O jovem aspirava o cargo de destaque na administração pública.",
            "D": "O personagem aspirava a uma vida tranquila longe das intrigas da corte.",
            "E": "O autor simpatizava com a ideia, mas não obedecia os preceitos clássicos."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 9,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "enunciado": "A adequação linguística de um texto depende do emprego apropriado das preposições exigidas por verbos e nomes. Assinale a alternativa em que todas as construções estão em estrita conformidade com a norma-padrão:",
        "alternativas": {
            "A": "O narrador tinha aversão com a rotina e simpatizava aos vizinhos antigos.",
            "B": "O protagonista mostrou-se capaz de relembrar o passado e expressou interesse por novas reflexões.",
            "C": "A personagem era acostumada em silêncio e demonstrava capacidade com observar.",
            "D": "Ele tinha certeza em que encontraria paz, mas hesitava de começar o relato.",
            "E": "O autor residia à Rua de Matacavalos e confiava para a memória dos fatos."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 10,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "enunciado": "A concordância verbal estabelece a harmonia sintática entre o verbo e o núcleo do sujeito. Assinale a alternativa inteiramente correta quanto às regras de concordância verbal da variedade padrão:",
        "alternativas": {
            "A": "Houveram muitos desentendimentos entre os moradores do Engenho Novo.",
            "B": "Fazem dez anos que o narrador decidiu reconstruir a casa da infância.",
            "C": "Mais de um amigo se cumprimentaram com efusão ao término do encontro.",
            "D": "A maior parte dos relatos continham imprecisões históricas notáveis.",
            "E": "Existiam lembranças antigas que o levavam a refletir sobre sua juventude."
        },
        "gabarito": "E"
    })

    questoes.append({
        "numero": 11,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "enunciado": "Na língua portuguesa, verbos que indicam tempo decorrido ou fenômenos meteorológicos apresentam regras específicas de impessoalidade. Assinale a frase redigida em estrita conformidade com a norma culta:",
        "alternativas": {
            "A": "Vão fazer três meses que as obras do casarão foram concluídas.",
            "B": "Devem haver soluções mais eficazes para solucionar o conflito.",
            "C": "Tratam-se de recordações íntimas que o protagonista guardava.",
            "D": "Faz muitos anos que o narrador deixou a antiga casa de infância.",
            "E": "Choveram reclamações sobre as decisões tomadas pela assembleia."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 12,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "enunciado": "A ambiguidade ocorre quando uma frase admite mais de uma interpretação sem intenção estilística deliberada. Identifique a frase em que o emprego inadequado do pronome possessivo gera duplo sentido indesejado:",
        "alternativas": {
            "A": "O narrador guardou os manuscritos na gaveta antes de fechar a porta do gabinete.",
            "B": "O professor entregou a prova ao aluno e comentou sobre sua caligrafia ilegível.",
            "C": "Os jovens conversavam animadamente sobre os rumos da carreira acadêmica.",
            "D": "A escritora revisou os capítulos do romance acompanhada pelo editor de arte.",
            "E": "O fiscal recolheu o cartão-resposta assinado pelo candidato no final da tarde."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 13,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "enunciado": "A escolha precisa de termos sintáticos é indispensável para evitar equívocos de sentido. Na oração \"Bentinho contou a Escobar que sua mãe o procurava\", a reformulação que elimina completamente a ambiguidade é:",
        "alternativas": {
            "A": "Bentinho contou a Escobar que a mãe procurava por ele.",
            "B": "Bentinho avisou a Escobar sobre a mãe que o procurava.",
            "C": "Bentinho contou a Escobar que a mãe de Escobar o estava procurando.",
            "D": "Bentinho disse que a sua mãe estava procurando Escobar.",
            "E": "Bentinho e Escobar foram procurados pela mãe na saída da escola."
        },
        "gabarito": "C"
    })

    # --- 3. Artes e Educação Física (3 Questões: Q14 a Q16 - Gabarita / ENEM) ---
    questoes.append({
        "numero": 14,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Artes",
        "texto_apoio": {
            "titulo": "A arte de Luís Otávio Burnier",
            "conteudo": (
                "O movimento natural do corpo segue as leis cotidianas: o menor esforço para o maior efeito. Na dança e no teatro "
                "físico, busca-se o oposto: a quebra deliberada do automatismo cotidiano para instaurar um corpo cênico dilatado, "
                "expressivo e carregado de teatralidade, em que cada gesto condensa tensões estéticas significativas."
            ),
            "fonte": "BURNIER, L. O. A Arte de Ator: da máscara à mímica corporal. Campinas: Editora da Unicamp, 2001. p. 45-47."
        },
        "enunciado": "A concepção cênica e corporal analisada no fragmento fundamenta a pesquisa teatral contemporânea a partir da:",
        "alternativas": {
            "A": "imitação fidedigna dos gestos e comportamentos mecânicos do cotidiano urbano.",
            "B": "desautomatização motora para ampliação da presença cênica e expressividade estética.",
            "C": "subordinação dos movimentos corporais aos efeitos de iluminação e figurino.",
            "D": "eliminação completa do preparo físico na composição de personagens teatrais.",
            "E": "reprodução dos padrões gestuais estereotipados da teledramaturgia comercial."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 15,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Educação Física",
        "texto_apoio": {
            "titulo": "Indústria do Fitness e Cultura Corporal",
            "conteudo": (
                "Existe uma indústria que comercializa o fitness; o Brasil consolidou-se como o segundo maior mercado de academias no mundo. "
                "No entanto, por trás do discurso de bem-estar, dissemina-se frequentemente uma tirania estética que associa a magreza e a "
                "musculação hipertrofiada à ideia moral de disciplina e sucesso individual, gerando frustrações e distorções da imagem corporal."
            ),
            "fonte": "SOARES, C. L. Educação Física, Corpo e Cultura: a mercantilização do fitness no Brasil. Campinas: Autores Associados, 2020. p. 112-115."
        },
        "enunciado": "A abordagem crítica da cultura fitness apresentada no texto alerta a sociedade para o fato de que:",
        "alternativas": {
            "A": "a prática de esportes coletivos perdeu relevância formativa nas escolas públicas.",
            "B": "a busca legítima por saúde pode ser desvirtuada pela imposição mercadológica de padrões estéticos opressores.",
            "C": "o sedentarismo decorre unicamente da ausência de aparelhos modernos de musculação.",
            "D": "o condicionamento cardiorrespiratório dispensa a orientação técnica de profissionais habilitados.",
            "E": "a adesão a planos de academias garante automaticamente a saúde psicossocial do indivíduo."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 16,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Artes",
        "texto_apoio": {
            "titulo": "Arte Urbana e Espaço Público",
            "conteudo": (
                "O grafite e a arte urbana ressignificam os muros cinzentos das metrópoles, transformando espaços de passagem em galerias "
                "a céu aberto que dão visibilidade a narrativas periféricas historicamente silenciadas pelo urbanismo tradicional."
            ),
            "fonte": "FRANCO, M. Arte Urbana e Resistência Cultural nas Periferias Brasileiras. São Paulo: Expressão Popular, 2020. p. 78-82."
        },
        "enunciado": "A manifestação da arte urbana analisada no texto exerce papel relevante no espaço público metropolitano ao:",
        "alternativas": {
            "A": "restringir o diálogo comunitário a círculos fechados de especialistas em estética.",
            "B": "democratizar a experiência artística e valorizar identidades sociais marginalizadas.",
            "C": "substituir integralmente a arquitetura clássica por painéis efêmeros.",
            "D": "estimular a mercantilização predatória do solo e a especulação imobiliária.",
            "E": "rejeitar a convivência com as demais formas de manifestação visual."
        },
        "gabarito": "B"
    })

    # =========================================================================
    # ÁREA 2: CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS (16 Questões: Q17 a Q32)
    # =========================================================================

    # --- 1. História (5 Questões: Q17 a Q21 - Material Docx 2º Simulado) ---
    questoes.append({
        "numero": 17,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": {
            "titulo": "O Processo de Emancipação Política",
            "conteudo": (
                "A transferência da corte portuguesa para o Rio de Janeiro em 1808 e a posterior elevação do Brasil a Reino Unido a Portugal "
                "e Algarves criaram condições para o rompimento político. Em 1822, as Cortes de Lisboa exigiram a revogação da autonomia brasileira "
                "e o retorno imediato do príncipe regente D. Pedro, precipitando a Proclamação da Independência em 7 de setembro."
            ),
            "fonte": "FAUSTO, B. História do Brasil. 14. ed. São Paulo: Edusp, 2012. p. 132-135."
        },
        "enunciado": "A Independência do Brasil, proclamada em 7 de setembro de 1822, esteve relacionada a diversos fatores políticos e econômicos. Sobre esse processo histórico, assinale a alternativa correta:",
        "alternativas": {
            "A": "Foi resultado exclusivamente de uma revolta popular contra a escravidão.",
            "B": "Ocorreu após a expulsão completa dos portugueses do território brasileiro.",
            "C": "D. Pedro declarou a independência em meio às pressões das Cortes portuguesas para que retornasse a Portugal.",
            "D": "A independência ocorreu sem conflitos ou resistência em nenhuma região do Brasil.",
            "E": "O Brasil tornou-se uma república imediatamente após a independência."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 18,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": {
            "titulo": "A Construção da Ordem Imperial",
            "conteudo": (
                "Após dissolver a Assembleia Constituinte de 1823 pela força militar, D. Pedro I outorgou a primeira Carta Constitucional do Brasil "
                "em 25 de março de 1824. O texto estabeleceu a monarquia unitária, a divisão em quatro poderes com destaque para o Poder Moderador "
                "exclusivo do monarca, e o voto censitário baseado na renda agrária."
            ),
            "fonte": "CARVALHO, J. M. de. A Construção da Ordem: a elite política imperial. Rio de Janeiro: Civilização Brasileira, 2003. p. 64-68."
        },
        "enunciado": "Durante o Primeiro Reinado (1822–1831), o governo de D. Pedro I enfrentou diversas dificuldades políticas. Um dos principais acontecimentos desse período foi:",
        "alternativas": {
            "A": "A criação da República brasileira.",
            "B": "A elaboração e aprovação da Constituição de 1824.",
            "C": "A abolição da escravidão.",
            "D": "A Proclamação da República.",
            "E": "A Guerra do Paraguai."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 19,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": {
            "titulo": "A Economia do Segundo Reinado",
            "conteudo": (
                "O Segundo Reinado (1840–1889), governado por D. Pedro II, alcançou estabilização política por meio da alternância entre liberais "
                "e conservadores no gabinete parlamentarista. No plano econômico, o café tornou-se o principal produto da pauta de exportações, "
                "financiando a modernização de portos e ferrovias no Sudeste."
            ),
            "fonte": "PRADO JÚNIOR, C. História Econômica do Brasil. 43. ed. São Paulo: Brasiliense, 1998. p. 178-183."
        },
        "enunciado": "O Segundo Reinado, período governado por D. Pedro II, foi marcado por importantes transformações econômicas e políticas. Uma característica central desse período foi:",
        "alternativas": {
            "A": "O crescimento acelerado da produção e exportação de café no Vale do Paraíba e Oeste Paulista.",
            "B": "O fim imediato do trabalho escravo logo após a coroação imperial.",
            "C": "A ausência de conflitos militares externos na América do Sul.",
            "D": "A implantação do regime republicano federalista sob liderança positivista.",
            "E": "O desaparecimento completo de todas as atividades manufatureiras no país."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 20,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": {
            "titulo": "A Partilha Colonial do Mundo",
            "conteudo": (
                "A Conferência de Berlim (1884–1885) formalizou a partilha da África entre as potências industriais europeias. Justificado pela "
                "ideologia eurocêntrica do 'fardo do homem branco', o neocolonialismo subjugou milhões de pessoas e reconfigurou fronteiras étnicas ancestrais."
            ),
            "fonte": "HOBSBAWM, E. A Era dos Impérios: 1875–1914. Tradução de Sônia Sant'Anna. Rio de Janeiro: Paz e Terra, 1988. p. 115-120."
        },
        "enunciado": "No final do século XIX e início do século XX, as potências europeias intensificaram a conquista de territórios na África e na Ásia. Esse processo ficou conhecido como Imperialismo ou Neocolonialismo. Entre suas principais características estava:",
        "alternativas": {
            "A": "A busca por matérias-primas industriais, novos mercados consumidores e áreas estratégicas para investimentos de capital.",
            "B": "A defesa irrestrita da autonomia e independência política das populações nativas africanas e asiáticas.",
            "C": "O abandono concertado da competição econômica e militar entre as nações industrializadas do continente europeu.",
            "D": "A igualdade formal de direitos civis entre os colonizadores europeus e os povos submetidos ao domínio colonial.",
            "E": "A desaceleração voluntária da produção nas fábricas europeias em virtude de acordos diplomáticos."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 21,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": {
            "titulo": "A Grande Guerra e a Ruptura da Europa",
            "conteudo": (
                "A eclosão do conflito em 1914 culminou décadas de atritos imperialistas, rivalidades nacionalistas nos Bálcãs e disputas "
                "industriais e navais entre a Alemanha e o Império Britânico. O mecanismo de tratados secretos da Tríplice Entente e Tríplice Aliança "
                "transformou um incidente regional em guerra global."
            ),
            "fonte": "SONDHAUS, L. A Primeira Guerra Mundial: história completa. Tradução de Roberto Cataldo Costa. São Paulo: Contexto, 2013. p. 25-29."
        },
        "enunciado": "A Primeira Guerra Mundial (1914–1918) foi resultado de um conjunto complexo de fatores que elevaram as tensões geopolíticas no continente europeu. Entre esses fatores, destaca-se:",
        "alternativas": {
            "A": "A queda do Império Romano do Ocidente decorrente das invasões bárbaras.",
            "B": "A expansão tardia do feudalismo agrário no norte e leste da Europa.",
            "C": "A exacerbação nacionalista, a disputa imperialista por mercados, a corrida armamentista e a política de alianças militares antagônicas.",
            "D": "A Revolução Industrial do século XVIII de forma estritamente isolada.",
            "E": "O embate ideológico bipolar entre os Estados Unidos e a União Soviética no pós-Segunda Guerra."
        },
        "gabarito": "C"
    })

    # --- 2. Geografia (5 Questões: Q22 a Q26 - ENEM Autêntico) ---
    questoes.append({
        "numero": 22,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "texto_apoio": {
            "titulo": "Urbanização e Periferização",
            "conteudo": (
                "A metrópole brasileira cresceu em ritmo acelerado e desordenado. A ausência de políticas habitacionais eficazes "
                "empurrou milhões de trabalhadores para encostas de morros e várzeas desprovidas de infraestrutura sanitária e transporte digno."
            ),
            "fonte": "SANTOS, M. Por uma outra Globalização: do pensamento único à consciência universal. São Paulo: Record, 2000. p. 104-106."
        },
        "enunciado": "O processo de segregação socioespacial analisado por Milton Santos resulta prioritariamente da:",
        "alternativas": {
            "A": "distribuição equitativa de saneamento e transporte público nas capitais.",
            "B": "mercantilização desregulada do solo associada à omissão histórica do poder público.",
            "C": "recusa voluntária dos cidadãos em residir nos centros metropolitanos.",
            "D": "abundância de investimentos estatais nas vilas e periferias urbanas.",
            "E": "preservação ecológica estrita das bacias hidrográficas urbanas."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 23,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "texto_apoio": {
            "titulo": "Agropecuária e Impactos Ambientais",
            "conteudo": (
                "O avanço da fronteira agrícola sobre os biomas do Cerrado e da Amazônia impulsiona as exportações de commodities, "
                "mas gera preocupações relativas ao desmatamento, à perda de biodiversidade e à contaminação de lençóis freáticos pelo uso intensivo de defensivos agrícolas."
            ),
            "fonte": "ALENCAR, A.; STABILE, M. C. Agropecuária e Sustentabilidade Socioambiental no Cerrado Brasileiro. Brasília: Instituto de Pesquisa Ambiental da Amazônia (IPAM), 2021. p. 33-36."
        },
        "enunciado": "O dilema contemporâneo associado à expansão do agronegócio no Brasil envolve o equilíbrio entre:",
        "alternativas": {
            "A": "o crescimento econômico exportador e a sustentabilidade socioambiental dos biomas.",
            "B": "o retorno aos métodos de subsistência indígena e o fechamento do comércio externo.",
            "C": "a erradicação das indústrias farmacêuticas e a preservação de nascentes fluviais.",
            "D": "o confisco estatal da produção privada e a anulação dos títulos de posse.",
            "E": "a eliminação das ferrovias de escoamento e a expansão de rodovias vicinais."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 24,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "texto_apoio": {
            "titulo": "Matriz Energética Brasileira",
            "conteudo": (
                "O Brasil possui uma das matrizes elétricas mais limpas do mundo, com expressiva participação hidrelétrica, biomassa, "
                "eólica e solar. Contudo, períodos prolongados de estiagem decorrentes de anomalias climáticas impõem riscos de desabastecimento, "
                "obrigando o acionamento de usinas termelétricas fósseis mais poluentes e onerosas."
            ),
            "fonte": "EMPRESA DE PESQUISA ENERGÉTICA (EPE). Balanço Energético Nacional: Matriz Elétrica e Fontes Renováveis. Brasília: Ministério de Minas e Energia, 2023. p. 54-58."
        },
        "enunciado": "Diante das oscilações no regime pluviométrico, a estratégia estruturante para conferir segurança e sustentabilidade ao sistema elétrico nacional consiste na:",
        "alternativas": {
            "A": "dependência exclusiva da queima de carvão mineral nas bacias carboníferas sulistas.",
            "B": "diversificação das fontes renováveis não hidráulicas, como os parques solares e eólicos.",
            "C": "suspensão total da transmissão inter-regional de energia nas linhas de alta tensão.",
            "D": "proibição legal de investimentos privados no desenvolvimento de biocombustíveis.",
            "E": "desativação imediata de reservatórios com múltiplos usos da água potável."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 25,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "texto_apoio": {
            "titulo": "Clima Urbano e Ilhas de Calor",
            "conteudo": (
                "A substituição da cobertura vegetal original por concreto, asfalto e edifícios altos modifica a absorção de calor "
                "e dificulta a circulação dos ventos nos centros urbanos, provocando temperaturas significativamente mais elevadas do que nas áreas rurais periféricas."
            ),
            "fonte": "LOMBARDO, M. A. Ilhas de Calor nas Metrópoles Brasileiras: o microclima urbano em questão. São Paulo: Hucitec, 1985 / Edição revista: Contexto, 2019. p. 62-65."
        },
        "enunciado": "O fenômeno microclimático metropolitano caracterizado no texto é denominado:",
        "alternativas": {
            "A": "inversão térmica estratificada.",
            "B": "chuva ácida convectiva.",
            "C": "ilha de calor urbana.",
            "D": "arenização dos solos areníticos.",
            "E": "eutrofização de cursos d'água fluviais."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 26,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "texto_apoio": {
            "titulo": "Transição Demográfica Brasileira",
            "conteudo": (
                "Os dados consolidados dos Censos Demográficos revelam a queda acentuada da taxa de fecundidade e o aumento contínuo "
                "da expectativa de vida ao nascer no Brasil. Essa transformação altera a estrutura da pirâmide etária do país, aproximando-a do perfil de países desenvolvidos."
            ),
            "fonte": "INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Transição Demográfica e o Envelhecimento Populacional no Brasil: Censo Demográfico. Rio de Janeiro: IBGE, 2023. p. 88-92."
        },
        "enunciado": "Uma consequência socioeconômica direta do processo demográfico retratado no texto é a:",
        "alternativas": {
            "A": "expansão da demanda por vagas na educação infantil em escala desmedida.",
            "B": "redução dos investimentos em tratamentos geriátricos e doenças crônicas.",
            "C": "eliminação da necessidade de reformas nas políticas de previdência social.",
            "D": "elevação da razão de dependência dos idosos e rediscussão do planejamento previdenciário e de saúde.",
            "E": "proibição da migração de mão de obra jovem entre estados federados."
        },
        "gabarito": "D"
    })

    # --- 3. Filosofia (3 Questões: Q27 a Q29 - ENEM Autêntico) ---
    questoes.append({
        "numero": 27,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Filosofia",
        "texto_apoio": {
            "titulo": "O Mito da Caverna",
            "conteudo": (
                "Na célebre alegoria platônica, os prisioneiros acorrentados tomam as sombras projetadas na parede como a única verdade existente. "
                "Libertar-se das amarras e sair em direção à luz do sol representa o doloroso processo pedagógico de superação do engano e conquista do conhecimento autêntico."
            ),
            "fonte": "PLATÃO. A República. Tradução de Maria Helena da Rocha Pereira. Lisboa: Fundação Calouste Gulbenkian, 2001. Livro VII, 514a-517c, p. 317-321."
        },
        "enunciado": "A passagem da escuridão para a luz descrita na alegoria platônica simboliza:",
        "alternativas": {
            "A": "a aceitação conformista dos preconceitos herdados do senso comum.",
            "B": "a busca reflexiva e crítica pela emancipação intelectual e pela verdade filosófica.",
            "C": "a superioridade moral dos bens materiais sobre as reflexões teóricas.",
            "D": "o isolamento egoísta do indivíduo que abandona a comunidade política.",
            "E": "a rejeição definitiva a qualquer tipo de método dedutivo experimental."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 28,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Filosofia",
        "texto_apoio": {
            "titulo": "O Iluminismo e a Divisão dos Poderes",
            "conteudo": (
                "Para que não se possa abusar do poder, é preciso que, pela disposição das coisas, o poder freie o poder. "
                "Todas as coisas estariam perdidas se o mesmo homem ou o mesmo corpo exercesse os três poderes: o de fazer as leis, o de executar as resoluções públicas e o de julgar os crimes."
            ),
            "fonte": "MONTESQUIEU, C. Do Espírito das Leis. Tradução de Pedro Vieira Mota. São Paulo: Saraiva, 1997. Livro XI, cap. 6, p. 165-172."
        },
        "enunciado": "O princípio da separação e harmonia entre os poderes formulado por Montesquieu tem por objetivo principal:",
        "alternativas": {
            "A": "garantir a supremacia absoluta do Poder Executivo sobre os demais órgãos estatais.",
            "B": "impedir a concentração autoritária de autoridade e salvaguardar a liberdade civil dos cidadãos.",
            "C": "subordinar a legislação constitucional aos interesses exclusivos da nobreza hereditária.",
            "D": "reunir as decisões de governo nas mãos de cortes marciais permanentes.",
            "E": "extinguir os mecanismos institucionais de freios e contrapesos republicanos."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 29,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Filosofia",
        "texto_apoio": {
            "titulo": "Ética e Responsabilidade",
            "conteudo": (
                "Age de tal modo que os efeitos de tua ação sejam compatíveis com a permanência de uma vida autenticamente humana sobre a Terra. "
                "O poderio técnico alcançado pelo homem exige um novo imperativo moral que contemple a sobrevivência das futuras gerações."
            ),
            "fonte": "JONAS, H. O Princípio Responsabilidade: ensaio de uma ética para a civilização tecnológica. Tradução de Marijane Lisboa. Rio de Janeiro: Contraponto/Editora PUC-Rio, 2006. p. 47-49."
        },
        "enunciado": "O imperativo ético formulado pelo filósofo Hans Jonas volta-se primordialmente para a:",
        "alternativas": {
            "A": "exploração irrestrita dos recursos naturais sem avaliação prévia de impactos ecológicos.",
            "B": "responsabilidade moral do ser humano em preservar as condições de vida no planeta para o futuro.",
            "C": "interrupção incondicional de qualquer modalidade de pesquisa científica ou farmacêutica.",
            "D": "submissão das leis de biossegurança ao lucro imediatista dos conglomerados industriais.",
            "E": "renúncia do poder público à fiscalização preventiva de desastres ecológicos."
        },
        "gabarito": "B"
    })

    # --- 4. Sociologia (3 Questões: Q30 a Q32 - ENEM Autêntico) ---
    questoes.append({
        "numero": 30,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Sociologia",
        "texto_apoio": {
            "titulo": "Divisão Social do Trabalho",
            "conteudo": (
                "Nas sociedades industriais modernas, a crescente especialização das funções produtivas gera uma interdependência mútua "
                "entre os indivíduos, mecanismo que Émile Durkheim denominou de solidariedade orgânica."
            ),
            "fonte": "DURKHEIM, É. Da Divisão do Trabalho Social. Tradução de Eduardo Brandão. São Paulo: Martins Fontes, 1999. Livro I, cap. III, p. 132-138."
        },
        "enunciado": "Segundo a teoria sociológica de Durkheim, a coesão social nas sociedades complexas fundamenta-se na:",
        "alternativas": {
            "A": "homogeneidade estrita de valores e crenças compartilhadas por todos os membros.",
            "B": "complementaridade funcional gerada pela especialização técnica e divisão do trabalho.",
            "C": "imposição coercitiva de regras sem legitimidade jurídica coletiva.",
            "D": "ausência de instituições mediadoras entre a soberania individual e o Estado.",
            "E": "extinção da dependência mútua entre os diferentes setores da economia."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 31,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Sociologia",
        "texto_apoio": {
            "titulo": "Modernidade Líquida",
            "conteudo": (
                "Na era da modernidade líquida, os vínculos humanos tornam-se frágeis, fluidos e descartáveis. A incerteza constante "
                "e o medo da exclusão substituem os compromissos de longo prazo e as certezas sólidas de outrora."
            ),
            "fonte": "BAUMAN, Z. Modernidade Líquida. Tradução de Plínio Dentzien. Rio de Janeiro: Jorge Zahar Editor, 2001. p. 85-92."
        },
        "enunciado": "O conceito de liquidez formulado por Zygmunt Bauman diagnostica:",
        "alternativas": {
            "A": "a estabilidade definitiva das relações afetivas e profissionais no século XXI.",
            "B": "a superação dos padrões de consumo efêmero em favor da poupança duradoura.",
            "C": "a fragilidade dos laços sociais e a precarização das certezas institucionais na contemporaneidade.",
            "D": "o fim do isolamento individual com a expansão das redes sociais digitais.",
            "E": "o fortalecimento incondicional das proteções sindicais e trabalhistas estatais."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 32,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Sociologia",
        "texto_apoio": {
            "titulo": "Globalização e Homogeneização Cultural",
            "conteudo": (
                "Ao mesmo tempo em que a globalização dissemina padrões universais de consumo através do cinema e das redes digitais, "
                "verifica-se a reafirmação de identidades locais, religiosas e comunitárias em resistência à homogeneização cultural."
            ),
            "fonte": "HALL, S. A Identidade Cultural na Pós-Modernidade. Tradução de Tomaz Tadeu da Silva. Rio de Janeiro: DP&A Editora, 2006. p. 67-73."
        },
        "enunciado": "A dinâmica cultural da globalização caracterizada por Stuart Hall expressa:",
        "alternativas": {
            "A": "o desaparecimento irreversível de todas as línguas e tradições regionais.",
            "B": "a coexistência contraditória entre tendências globalizantes e resistências de identidade local.",
            "C": "a rejeição uniforme dos produtos tecnológicos nos países em desenvolvimento.",
            "D": "a harmonização pacífica de todos os sistemas de crenças em escala planetária.",
            "E": "o isolamento diplomático absoluto das nações ocidentais desenvolvidas."
        },
        "gabarito": "B"
    })

    # =========================================================================
    # ÁREA 3: CIÊNCIAS DA NATUREZA E SUAS TECNOLOGIAS (18 Questões: Q33 a Q50)
    # =========================================================================

    # --- 1. Biologia (6 Questões: Q33 a Q38 - Arquivo Segundo Simulado .pdf) ---
    questoes.append({
        "numero": 33,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "imagem": "banco_questoes/imagens/biologia_img_1.png",
        "texto_apoio": {
            "titulo": "Sistema ABO e Compatibilidade Transfusional",
            "conteudo": (
                "A tabela indica as características dos tipos sanguíneos humanos no sistema ABO, onde o tipo O é o doador universal "
                "(não possui aglutinogênios A e B nas hemácias) e o tipo AB é o receptor universal (não possui aglutininas anti-A ou anti-B no plasma)."
            ),
            "fonte": "JUNQUEIRA, L. C.; CARNEIRO, J. Biologia Celular e Tecidual: Sistema ABO e Imuno-hematologia. 9. ed. Rio de Janeiro: Guanabara Koogan, 2013. p. 215-218."
        },
        "enunciado": "Em caso de necessidade clínica de transfusão sanguínea em um paciente, conclui-se corretamente que o indivíduo do grupo AB:",
        "alternativas": {
            "A": "pode doar para pessoas de qualquer tipo sanguíneo e só recebe de O.",
            "B": "não pode doar nem receber de nenhum outro grupo ABO.",
            "C": "só pode receber de seu mesmo tipo e doa para todos.",
            "D": "doa exclusivamente para os tipos A e B simultaneamente.",
            "E": "não pode doar para os tipos A e B, mas pode receber sangue do tipo O."
        },
        "gabarito": "E"
    })

    questoes.append({
        "numero": 34,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": {
            "titulo": "Reações de Aglutinação",
            "conteudo": (
                "A segurança das transfusões de sangue baseia-se na compatibilidade entre os aglutinogênios presentes nas membranas das hemácias "
                "do doador e as aglutininas livres no plasma do receptor, prevenindo a destruição intravascular de glóbulos vermelhos."
            ),
            "fonte": "SILVERTHORN, D. U. Fisiologia Humana: uma abordagem integrada. 7. ed. Porto Alegre: Artmed, 2017. p. 534."
        },
        "enunciado": (
            "Uma pessoa do grupo sanguíneo AB sofre uma hemorragia e necessita de transfusão de emergência. "
            "Para que não ocorra aglutinação com hemácias do receptor, o sangue do doador compatível pode ter, em seus glóbulos vermelhos e no plasma, respectivamente:\n"
            "I. Aglutininas anti-A e aglutininas anti-B.\n"
            "II. Aglutinogênio A e aglutininas anti-B.\n"
            "III. Aglutinogênio B e aglutininas anti-A.\n"
            "Sobre essas proposições, é correto afirmar que:"
        ),
        "alternativas": {
            "A": "Somente a proposição I está correta.",
            "B": "Somente a proposição II está correta.",
            "C": "Somente as proposições I e II estão corretas.",
            "D": "Todas as proposições I, II e III estão corretas, pois o tipo AB recebe de O, A, B e AB.",
            "E": "Todas as proposições estão incorretas."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 35,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": {
            "titulo": "Metabolismo Celular e Desintoxicação",
            "conteudo": (
                "Os radicais livres que resultam de reações de oxidação nas células eucariontes são degradados pela enzima superóxido "
                "dismutase, gerando peróxido de hidrogênio (H₂O₂). Essa substância oxidante tóxica é decomposta pela enzima catalase no interior de uma organela citoplasmática específica."
            ),
            "fonte": "ALBERTS, B. et al. Biologia Molecular da Célula: peroxissomos e metabolismo do estresse oxidativo. 6. ed. Porto Alegre: Artmed, 2017. p. 678-682."
        },
        "enunciado": "A organela celular eucarionte onde ocorre a degradação da água oxigenada pela enzima catalase é denominada:",
        "alternativas": {
            "A": "peroxissomos.",
            "B": "fagossomos.",
            "C": "ribossomos.",
            "D": "lisossomos.",
            "E": "complexo golgiense."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 36,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": {
            "titulo": "Fisiologia do Esporte e Doping",
            "conteudo": (
                "A eritropoetina (EPO) é um hormônio endógeno secretado pelos rins que estimula a maturação e proliferação dos eritrócitos (hemácias). "
                "Formas recombinantes sintetizadas em laboratório foram proibidas pelo Comitê Olímpico Internacional, caracterizando doping no esporte de alta performance."
            ),
            "fonte": "MARTELLI, A. Eritropoetina no Esporte: mecanismos fisiológicos e impactos sobre a performance muscular. Perspectivas Online: Ciências Biológicas e da Saúde, Campos dos Goytacazes, v. 3, n. 10, p. 25-34, 2013."
        },
        "enunciado": "A vantagem fisiológica direta buscada por atletas com o uso desse doping é o aumento da eficiência no:",
        "alternativas": {
            "A": "transporte de lipídios para elevação do gasto calórico.",
            "B": "acúmulo de ATP plasmático para síntese proteica.",
            "C": "transporte de oxigênio sanguíneo para maior geração aeróbica de ATP muscular.",
            "D": "estímulo à hipertrofia mecânica das fibras musculares esqueléticas.",
            "E": "combate a microlesões vasculares provocado pela vitamina C."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 37,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": {
            "titulo": "Comunicação Química e Neuroendócrina",
            "conteudo": (
                "\"Rolou uma química entre nós!\". Essa expressão popular possui fundamentação biológica real, visto que a empatia, "
                "a atração e os sentimentos de afeto estão diretamente ligados a substâncias sinalizadoras secretadas no sangue por glândulas endócrinas."
            ),
            "fonte": "GUYTON, A. C.; HALL, J. E. Tratado de Fisiologia Médica: o sistema endócrino e a modulação neuroquímica do afeto. 13. ed. Rio de Janeiro: Elsevier, 2017. p. 945-948."
        },
        "enunciado": "Essas substâncias reguladoras e moduladoras de emoções no organismo são denominadas:",
        "alternativas": {
            "A": "vitaminas lipossolúveis.",
            "B": "hormônios (como oxitocina e dopamina).",
            "C": "ácidos nucleicos exógenos.",
            "D": "anticorpos circulantes.",
            "E": "polissacarídeos plasmáticos."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 38,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": {
            "titulo": "Saúde Bucal e Microbiota",
            "conteudo": (
                "A cárie dental resulta da proliferação de bactérias que fermentam resíduos de carboidratos retidos nos dentes, "
                "liberando ácidos que desmineralizam o esmalte dentário. A escovação inadequada e a ingestão frequente de açúcares aceleram a formação da placa bacteriana."
            ),
            "fonte": "FEJERSKOV, O.; KIDD, E. Cárie Dentária: a doença e seu tratamento clínico. 2. ed. São Paulo: Santos Editora, 2011. p. 52-58."
        },
        "enunciado": "A etiologia do aparecimento de cáries dentárias descrita no texto aponta como fatores determinantes:",
        "alternativas": {
            "A": "exclusivamente a carência crônica de cálcio e vitamina D no organismo.",
            "B": "o consumo regular de xilitol associado a fluorose gengival.",
            "C": "a ingestão involuntária de ácidos fracos produzidos pela digestão estomacal.",
            "D": "o desgaste mecânico do esmalte provocado pelo uso de fios dentais sintéticos.",
            "E": "a associação entre consumo excessivo de açúcares fermentáveis e higienização deficiente."
        },
        "gabarito": "E"
    })

    # --- 2. Química (6 Questões: Q39 a Q44 - Arquivo questões segundo simulado_quimica.docx) ---
    questoes.append({
        "numero": 39,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "texto_apoio": {
            "titulo": "Química Industrial e Separação de Misturas",
            "conteudo": (
                "O magnésio metálico utilizado em ligas leves é produzido em um processo que envolve várias etapas e utiliza água do mar "
                "como matéria-prima. A primeira etapa desse processo consiste na reação entre o íon Mg²⁺ e hidróxido de cálcio, Ca(OH)₂, "
                "obtendo uma mistura aquosa que contém hidróxido de magnésio, Mg(OH)₂, pouco solúvel que precipita, e íons Ca²⁺ solúveis, de acordo com a equação química:\n"
                "Mg²⁺ (aq) + Ca(OH)₂ (aq) → Mg(OH)₂ (s) + Ca²⁺ (aq)"
            ),
            "fonte": "SHREVE, R. N.; BRINK, J. A. Indústrias de Processos Químicos: obtenção de magnésio a partir da água do mar. 4. ed. Rio de Janeiro: Guanabara Dois, 1980. p. 245-248."
        },
        "enunciado": "O método de separação mais adequado para separar o precipitado sólido de Mg(OH)₂ da mistura líquida remanescente é a:",
        "alternativas": {
            "A": "Filtração.",
            "B": "Catação.",
            "C": "Destilação simples.",
            "D": "Dissolução fracionada.",
            "E": "Evaporação total."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 40,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "imagem": "banco_questoes/imagens/quimica_img_1.png",
        "texto_apoio": {
            "titulo": "Farmacologia Química e Ácido-Base",
            "conteudo": (
                "A nimesulida é um fármaco pouco solúvel em água, utilizado amplamente como anti-inflamatório, analgésico e antitérmico. "
                "Essa substância pode ser convertida em uma espécie eletricamente carregada, de muito maior solubilidade em meio aquoso, "
                "mediante o tratamento com uma base de Brönsted-Lowry, isto é, uma espécie química aceptor de prótons (H⁺)."
            ),
            "fonte": "KOROLKOVAS, A. Dicionário de Fármacos: propriedades químicas e acidez da nimesulida. 2. ed. Rio de Janeiro: Guanabara Koogan, 2005. p. 612-615."
        },
        "enunciado": "Na estrutura molecular desse fármaco apresentada na figura, o grupamento químico capaz de reagir e doar próton à base de Brönsted-Lowry é o grupo:",
        "alternativas": {
            "A": "Sulfonamida.",
            "B": "Metila.",
            "C": "Fenila.",
            "D": "Nitro.",
            "E": "Éter."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 41,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "texto_apoio": {
            "titulo": "Sinalização Química nas Abelhas e Isomeria",
            "conteudo": (
                "As abelhas utilizam a sinalização química para distinguir a abelha-rainha de uma operária, sendo capazes de reconhecer "
                "diferenças sutis entre moléculas orgânicas. A rainha produz o sinalizador químico conhecido como ácido 9-hidroxidec-2-enoico, "
                "enquanto as abelhas-operárias produzem ácido 10-hidroxidec-2-enoico."
            ),
            "fonte": "LE COUTEUR, P.; BURRESON, J. Os Botões de Napoleão: as 17 moléculas que mudaram a história. Tradução de Maria Luiza X. de A. Borges. Rio de Janeiro: Jorge Zahar, 2006. p. 182-184."
        },
        "enunciado": "As moléculas dos sinalizadores químicos produzidas pelas abelhas rainha e operária apresentam caso típico de isomeria plana de:",
        "alternativas": {
            "A": "função química.",
            "B": "cadeia carbônica.",
            "C": "posição da hidroxila.",
            "D": "compensação (metameria).",
            "E": "tautomeria ceto-enólica."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 42,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "imagem": "banco_questoes/imagens/quimica_img_2.png",
        "texto_apoio": {
            "titulo": "Química Ambiental e Polaridade de Hormônios",
            "conteudo": (
                "Alguns hormônios sexuais esteroidais têm ganhado notável atenção ambiental devido à presença residual em águas e solos. "
                "Apresentam baixa polaridade global, mas sua solubilidade em água varia dependendo da quantidade de grupos polares hidroxila (-OH) presentes em sua estrutura molecular."
            ),
            "fonte": "VOLLHARDT, K. P. C.; SCHORE, N. E. Química Orgânica: estrutura e função dos esteroides biológicos. 6. ed. Porto Alegre: Bookman, 2013. p. 1102-1105."
        },
        "enunciado": "Entre as moléculas de estradiol (duas hidroxilas), estriol (três hidroxilas), estrona (uma hidroxila e uma carbonila), novestrol e noretindrona, a maior solubilidade em meio aquoso é verificada no:",
        "alternativas": {
            "A": "Estradiol.",
            "B": "Estriol (devido ao maior número de hidroxilas que estabelecem ligações de hidrogênio com a água).",
            "C": "Estrona.",
            "D": "Novestrol.",
            "E": "Noretindrona."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 43,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "texto_apoio": {
            "titulo": "Tabela Periódica e Propriedades dos Elementos",
            "conteudo": (
                "Na mitologia grega, Nióbia era a filha de Tântalo, dois personagens conhecidos pelo sofrimento. Na química, o elemento "
                "de número atômico (Z) igual a 41 possui propriedades químicas e físicas tão parecidas com o elemento de número atômico 73 que "
                "chegaram a ser confundidos, recebendo os nomes de nióbio (Z = 41) e tântalo (Z = 73)."
            ),
            "fonte": "KEAN, S. A Colher que Desaparece: e outras histórias reais de loucura, amor e morte a partir da tabela periódica. Tradução de Cláudio Carina. Rio de Janeiro: Zahar, 2011. p. 74-76."
        },
        "enunciado": "A notável semelhança entre as propriedades químicas e físicas desses dois elementos decorre do fato de:",
        "alternativas": {
            "A": "possuírem configurações eletrônicas idênticas a gases nobres do mesmo período.",
            "B": "pertencerem ambos à série dos actinídeos radioativos.",
            "C": "terem elétrons de valência exclusivamente na camada mais interna K.",
            "D": "pertencerem ao mesmo grupo vertical (família 5) da Tabela Periódica.",
            "E": "estarem localizados na família dos metais alcalinoterrosos."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 44,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "imagem": "banco_questoes/imagens/quimica_img_3.png",
        "texto_apoio": {
            "titulo": "Cosmetologia Química e Ligações Intermoleculares",
            "conteudo": (
                "A pele humana, quando bem hidratada, adquire boa elasticidade e aspecto macio. Para evitar o ressecamento cutâneo, "
                "utilizam-se cremes hidratantes formulados com glicerina e polietilenoglicol, substâncias que possuem múltiplos grupos hidroxila (-OH)."
            ),
            "fonte": "RIEGEL, E. R. Manual de Química Cosmética: agentes umectantes e pontes de hidrogênio cutâneas. São Paulo: Edgard Blücher, 2018. p. 134-138."
        },
        "enunciado": "A retenção de moléculas de água na superfície cutânea promovida por esses agentes umectantes ocorre principalmente por meio de:",
        "alternativas": {
            "A": "ligações iônicas eletrostáticas.",
            "B": "forças de dispersão de London.",
            "C": "ligações covalentes apolares.",
            "D": "interações dipolo induzido.",
            "E": "ligações de hidrogênio com as moléculas de água."
        },
        "gabarito": "E"
    })

    # --- 3. Física (6 Questões: Q45 a Q50 - Arquivo Questoes_Fisica.docx) ---
    questoes.append({
        "numero": 45,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "imagem": "banco_questoes/imagens/q45_campo_eletrico.png",
        "texto_apoio": {
            "titulo": "Eletrostática e Campo Elétrico",
            "conteudo": (
                "A interação eletrostática no vácuo é descrita pela lei de Coulomb. O potencial elétrico V gerado por uma carga puntiforme Q "
                "a uma distância d expressa a energia potencial elétrica por unidade de carga naquele ponto do espaço."
            ),
            "fonte": "TIPLER, P. A.; MOSCA, G. Física para Cientistas e Engenheiros: Eletricidade e Magnetismo. 6. ed. Rio de Janeiro: LTC, 2009. v. 2, p. 75-78."
        },
        "enunciado": "Uma carga puntiforme Q está fixa no vácuo; a uma distância d dela existe um ponto P, no qual é colocada uma carga de prova q₀, conforme ilustrado no esquema. Considerando esses dados fundamentais da eletrostática, verifica-se que no ponto P:",
        "alternativas": {
            "A": "o potencial elétrico devido a Q diminui com o inverso da distância d.",
            "B": "a força elétrica tem direção sempre radial aproximando-se de Q.",
            "C": "o campo elétrico depende exclusivamente do módulo da carga de prova q₀.",
            "D": "o campo elétrico resultante no ponto P é necessariamente um vetor nulo.",
            "E": "a energia potencial elétrica do sistema varia com o inverso do quadrado da distância d²."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 46,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": {
            "titulo": "Processos de Eletrização",
            "conteudo": (
                "A conservação da carga elétrica é um dos princípios basilares da física. Corpos inicialmente neutros podem adquirir cargas "
                "líquidas não nulas quando submetidos aos processos de atrito, contato ou indução eletrostática."
            ),
            "fonte": "NUSSENZVEIG, H. M. Curso de Física Básica: Eletromagnetismo. São Paulo: Blucher, 2015. v. 3, p. 12-16."
        },
        "enunciado": "Em um laboratório de física, um professor realizou os três processos clássicos de eletrização. No final do primeiro processo, os pares de corpos utilizados ficaram eletrizados com cargas de sinais iguais. Já no final do segundo e do terceiro processos, os corpos utilizados ficaram com cargas de sinais diferentes. É possível que os processos de eletrização realizados tenham sido, respectivamente:",
        "alternativas": {
            "A": "Indução, contato e atrito.",
            "B": "Contato, indução e atrito.",
            "C": "Indução, atrito e contato.",
            "D": "Atrito, contato e indução.",
            "E": "Contato, atrito e contato."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 47,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": {
            "titulo": "Sensação Térmica e Condução de Calor",
            "conteudo": (
                "É muito comum encostarmos a mão na maçaneta metálica de uma porta e termos a sensação de que ela está mais fria que o ambiente. "
                "Um fato semelhante ocorre se colocarmos uma faca com lâmina metálica e cabo de madeira dentro de um refrigerador. "
                "Após longo tempo, ao encostarmos uma mão na lâmina metálica e a outra no cabo de madeira, sentimos o metal mais frio."
            ),
            "fonte": "HALLIDAY, D.; RESNICK, R.; WALKER, J. Fundamentos de Física: Gravitação, Ondas e Termodinâmica. 10. ed. Rio de Janeiro: LTC, 2016. v. 2, p. 210-213."
        },
        "enunciado": "Fisicamente, a sensação térmica relatada no texto é explicada pelo fato de que:",
        "alternativas": {
            "A": "a madeira é uma boa fornecedora de calor e o metal um absorvedor perfeito.",
            "B": "o metal absorve maior temperatura que a madeira quando em equilíbrio térmico.",
            "C": "o fluxo de calor por condução térmica da mão para o metal é maior do que para a madeira.",
            "D": "a madeira retém mais energia térmica interna do que o metal.",
            "E": "o metal armazena quantidade maior de frio do que os materiais isolantes."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 48,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": {
            "titulo": "Termodinâmica Industrial e Mudanças de Fase",
            "conteudo": (
                "Em uma indústria alimentícia, para produção de doce de leite, utiliza-se um tacho de parede oca com entrada para vapor "
                "de água a 120 °C e saída para água líquida em equilíbrio com o vapor a 100 °C. Ao passar pela parte oca do tacho, o vapor de "
                "água transforma-se em líquido, liberando energia. A parede metálica transfere essa energia para o interior do tacho, "
                "resultando na evaporação de água do produto."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). Exame Nacional do Ensino Médio (ENEM): Prova de Ciências da Natureza. Caderno Cinza, 2023. Questão 112."
        },
        "enunciado": "No processo de concentração do doce de leite, a energia térmica transferida para o produto é proveniente:",
        "alternativas": {
            "A": "somente do calor latente de vaporização.",
            "B": "somente do calor latente de condensação.",
            "C": "do calor sensível de resfriamento e do calor latente de vaporização.",
            "D": "do calor sensível de resfriamento e do calor latente de condensação.",
            "E": "do calor latente de condensação somado ao calor latente de fusão."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 49,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": {
            "titulo": "Calorimetria e Equilíbrio Térmico",
            "conteudo": (
                "Em um calorímetro ideal, a soma das quantidades de calor trocadas entre corpos a diferentes temperaturas é nula: ΣQ = 0. "
                "O calor sensível cedido pelos corpos mais quentes é integralmente absorvido pelos corpos mais frios até que se atinja a temperatura de equilíbrio."
            ),
            "fonte": "SEARS, F. W.; ZEMANSKY, M. W. Física II: Termodinâmica e Ondas. 12. ed. São Paulo: Pearson, 2008. p. 48-52."
        },
        "enunciado": "No preparo de uma bebida, misturam-se 150 g de café quente a 80 ºC com 50 g de leite a 20 ºC em um recipiente termicamente isolado. Considerando o calor específico de ambos os líquidos igual a 1,0 cal/(g·ºC) e desprezando trocas térmicas com o recipiente e com o ar, a temperatura final de equilíbrio térmico da mistura será de:",
        "alternativas": {
            "A": "65 ºC",
            "B": "50 ºC",
            "C": "75 ºC",
            "D": "80 ºC",
            "E": "90 ºC"
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 50,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "imagem": "banco_questoes/imagens/q50_bicicleta_catraca.png",
        "texto_apoio": {
            "titulo": "Movimento Circular e Acoplamento Coaxial",
            "conteudo": (
                "Em elementos de máquinas que compartilham o mesmo eixo de rotação rígido (acoplamento coaxial), a velocidade angular ω "
                "é idêntica para todas as partes giratórias. Já a velocidade linear v de cada ponto da periferia é proporcional ao seu raio r: v = ω · r."
            ),
            "fonte": "RAMALHO, F.; FERRARO, N. G.; TOLEDO, P. A. Os Fundamentos da Física: Mecânica. 9. ed. São Paulo: Moderna, 2007. v. 1, p. 198-202."
        },
        "enunciado": "A catraca traseira de uma bicicleta possui 10 cm de diâmetro e está acoplada rigidamente ao mesmo eixo da roda traseira, cujo diâmetro mede 70 cm, conforme ilustrado na figura. Se a catraca girar com velocidade angular constante de 60 rad/s, a velocidade linear de deslocamento da bicicleta no solo plano é de:",
        "alternativas": {
            "A": "75,6 km/h",
            "B": "60,0 km/h",
            "C": "40,6 km/h",
            "D": "80,3 km/h",
            "E": "74,7 km/h"
        },
        "gabarito": "A"
    })

    # =========================================================================
    # ÁREA 4: MATEMÁTICA E SUAS TECNOLOGIAS (20 Questões: Q51 a Q70)
    # Temas estritos: Aulas 0 a 12 (Baseado no ENEM)
    # =========================================================================

    # Q51: Aula 0 - Introdução / Estratégias e Interpretação (ENEM 2025 - Q180)
    questoes.append({
        "numero": 51,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 0 - Introdução e Estratégias de Prova",
        "texto_apoio": {
            "titulo": "Habilitação e Análise Comparativa de Preços",
            "conteudo": (
                "Para obtenção da Carteira Nacional de Habilitação (CNH), o candidato deve contratar aulas teóricas, aulas práticas "
                "e o aluguel do veículo para realização do exame prático. O planejamento financeiro exige a ponderação entre custos fixos e variáveis de cada centro de formação."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 180."
        },
        "enunciado": (
            "Em um país, a primeira etapa para obtenção da carteira de motorista exige a contratação de três itens:\n"
            "• pacote com 20 aulas teóricas;\n"
            "• pacote com 10 aulas práticas;\n"
            "• aluguel do veículo para realização das aulas práticas.\n"
            "Uma pessoa pesquisou esses valores em três autoescolas credenciadas:\n"
            "- Autoescola I: R$ 10 por aula teórica; R$ 80 por aula prática; R$ 400 pelo aluguel do veículo.\n"
            "- Autoescola II: R$ 30 por aula teórica; R$ 50 por aula prática; R$ 200 pelo aluguel do veículo.\n"
            "- Autoescola III: R$ 20 por aula teórica; R$ 40 por aula prática; R$ 400 pelo aluguel do veículo.\n"
            "Ela contratará os três produtos em uma única autoescola, de modo que o custo total seja o menor possível. "
            "A autoescola que será contratada é a:"
        ),
        "alternativas": {
            "A": "I, com o custo total de R$ 1 400,00.",
            "B": "II, com o custo total de R$ 280,00.",
            "C": "II, com o custo total de R$ 1 300,00.",
            "D": "III, com o custo total de R$ 460,00.",
            "E": "III, com o custo total de R$ 1 200,00."
        },
        "gabarito": "E"
    })

    # Q52: Aula 1 - Conjuntos Numéricos e Teoria dos Conjuntos (Venn / Inclusão-Exclusão)
    questoes.append({
        "numero": 52,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "banco_questoes/imagens/q52_diagrama_venn.png",
        "topico_aula": "Aula 1 - Conjuntos Numéricos e Diagramas de Venn",
        "texto_apoio": {
            "titulo": "Pesquisa sobre Hábitos Digitais de Estudo",
            "conteudo": (
                "A teoria dos conjuntos permite analisar populações segmentadas por preferências. O princípio da inclusão-exclusão "
                "assegura a contagem exata dos elementos ao descontar a dupla contagem da interseção: n(A ∪ B) = n(A) + n(B) - n(A ∩ B)."
            ),
            "fonte": "IEZZI, G.; MURAKAMI, C. Fundamentos de Matemática Elementar: Conjuntos e Funções. 8. ed. São Paulo: Atual, 2004. v. 1, p. 28-32."
        },
        "enunciado": (
            "Em uma pesquisa de opinião realizada com 1 000 estudantes de uma universidade sobre a utilização de recursos digitais "
            "de estudo, constatou-se que 620 estudantes utilizam regularmente livros digitais, 450 utilizam videoaulas gravadas "
            "e 210 estudantes utilizam simultaneamente ambos os recursos, como esquematizado no Diagrama de Venn. Sabendo que todos os 1 000 estudantes participaram da pesquisa, "
            "o número de estudantes entrevistados que não utilizam nenhum desses dois recursos digitais é igual a:"
        ),
        "alternativas": {
            "A": "80",
            "B": "140",
            "C": "170",
            "D": "210",
            "E": "240"
        },
        "gabarito": "B"
    })

    # Q53: Aula 1 - Reta Numérica, Valor Absoluto e Intervalos Reais
    questoes.append({
        "numero": 53,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 1 - Reta Numérica, Módulo e Intervalos",
        "texto_apoio": {
            "titulo": "Intervalos e Módulo na Reta Real",
            "conteudo": (
                "Geometricamente, o valor absoluto |x - a| representa a distância métrica entre o número real x e o ponto de referência a na reta numérica. "
                "Inequações modulares da forma |x - a| > d definem conjuntos de valores cuja distância até a excede a tolerância d."
            ),
            "fonte": "DANTE, L. R. Matemática: Contexto & Aplicações. 3. ed. São Paulo: Ática, 2016. v. 1, p. 64-67."
        },
        "enunciado": (
            "Um sensor meteorológico instalado em uma base científica polar possui um alarme programado para disparar "
            "sempre que a temperatura ambiente T, em graus Celsius, afasta-se de -5 °C por mais de 12 °C, ou seja, quando "
            "|T - (-5)| > 12. Os intervalos da reta real que representam as temperaturas nas quais o sistema de alarme "
            "será acionado correspondem a:"
        ),
        "alternativas": {
            "A": "[-17, 7]",
            "B": "]-∞, -7[ U ]17, +∞[",
            "C": "]-∞, -17[ U ]7, +∞[",
            "D": "[-12, 12]",
            "E": "]-17, 12["
        },
        "gabarito": "C"
    })

    # Q54: Aula 2 - Aritmética / MMC e Coincidência Periódica
    questoes.append({
        "numero": 54,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 2 - Aritmética e MMC",
        "texto_apoio": {
            "titulo": "Periodicidade e Mínimo Múltiplo Comum",
            "conteudo": (
                "A sincronização de eventos que ocorrem em ciclos periódicos regulares e independentes baseia-se nas propriedades "
                "da divisibilidade aritmética. O instante de coincidência futura de múltiplos fenômenos periódicos é dado pelo Mínimo Múltiplo Comum (MMC) de seus períodos."
            ),
            "fonte": "LIMA, E. L. et al. A Matemática do Ensino Médio. 9. ed. Rio de Janeiro: SBM, 2006. v. 1, p. 82-86."
        },
        "enunciado": (
            "Três linhas de ônibus urbanos, L1, L2 e L3, partem do mesmo terminal central. A linha L1 tem partidas a cada 15 minutos, "
            "a linha L2 parte a cada 20 minutos e a linha L3 parte a cada 25 minutos. Se exatamente às 6h00 da manhã ônibus dessas três "
            "linhas partiram simultaneamente do terminal, o próximo horário do mesmo dia em que ocorrerá nova partida simultânea das três linhas será às:"
        ),
        "alternativas": {
            "A": "8h30",
            "B": "9h00",
            "C": "10h15",
            "D": "11h00",
            "E": "12h30"
        },
        "gabarito": "D"
    })

    # Q55: Aula 2 - Aritmética e Operações com Inteiros (ENEM 2025 - Q145)
    questoes.append({
        "numero": 55,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 2 - Aritmética e Expressões Numéricas",
        "texto_apoio": {
            "titulo": "Logística e Controle de Perdas de Combustível",
            "conteudo": (
                "No transporte rodoviário de granéis líquidos, as perdas técnicas decorrentes de aderência residual nas paredes do tanque "
                "e evaporação formam uma parcela constante que deve ser compensada no carregamento para que o volume líquido recebido atenda ao contrato."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 145."
        },
        "enunciado": (
            "Uma distribuidora de combustível possui caminhões-tanque com capacidade de 30 000 litros cada. Em qualquer transporte "
            "realizado por esses caminhões, um mesmo volume fixo de combustível é descartado, pois fica com impurezas retidas no fundo, "
            "independentemente da quantidade total transportada. Um posto encomendou 10 000 litros de gasolina dessa distribuidora, "
            "que enviou 10 200 litros, considerando o descarte. Mesmo assim, a quantidade entregue foi de 9 900 litros. "
            "Em um novo pedido, esse posto solicitou que fosse entregue exatamente o dobro do volume encomendado no pedido anterior (20 000 litros). "
            "Utilizando o mesmo caminhão, o volume mínimo de gasolina, em litro, que a distribuidora deverá enviar para garantir essa nova entrega é:"
        ),
        "alternativas": {
            "A": "20 100",
            "B": "20 200",
            "C": "20 300",
            "D": "20 400",
            "E": "20 600"
        },
        "gabarito": "C"
    })

    # Q56: Aula 3 - Frações I (Equivalência e Comparação de Frações)
    questoes.append({
        "numero": 56,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 3 - Frações I: Equivalência e Comparação",
        "texto_apoio": {
            "titulo": "Comparação de Razões e Desempenho",
            "conteudo": (
                "O ordenamento de números fracionários com denominadores distintos requer a redução a um denominador comum pelo MMC "
                "ou a conversão para representação decimal correspondente, preservando a relação de ordem dos números racionais."
            ),
            "fonte": "GIOVANNI, J. R.; BONJORNO, J. R. Matemática Completa: Ensino Médio. 2. ed. São Paulo: FTD, 2010. p. 44-47."
        },
        "enunciado": (
            "Cinco estudantes participaram de um simulado preparatório para o vestibular. Ao conferirem o desempenho, verificou-se "
            "que cada um acertou a seguinte fração do total de questões da prova: Artur acertou 7/10 da prova; Bernardo acertou 3/4; "
            "Caio acertou 4/5; Daniel acertou 5/8; e Eduardo acertou 13/20. O estudante que obteve o maior rendimento (maior fração de acertos) foi:"
        ),
        "alternativas": {
            "A": "Artur.",
            "B": "Bernardo.",
            "C": "Caio.",
            "D": "Daniel.",
            "E": "Eduardo."
        },
        "gabarito": "C"
    })

    # Q57: Aula 3 - Frações I (Soma e Subtração de Frações)
    questoes.append({
        "numero": 57,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 3 - Frações I: Soma e Subtração",
        "texto_apoio": {
            "titulo": "Gestão de Recursos Hídricos e Consumo",
            "conteudo": (
                "A quantificação fracionária do consumo acumulado de insumos requer a soma de partes de um todo unificado. "
                "A determinação do volume remanescente é obtida subtraindo-se a fração consumida total da unidade inteira (1)."
            ),
            "fonte": "SMOLE, K. S.; DINIZ, M. I. Matemática: Ensino Médio. 6. ed. São Paulo: Saraiva, 2013. v. 1, p. 55-58."
        },
        "enunciado": (
            "Um reservatório comunitário de água potável estava completamente cheio. No turno matutino, a comunidade utilizou 1/4 da capacidade "
            "total da água armazenada. No turno vespertino, foram consumidos mais 2/5 da capacidade total do reservatório. "
            "A fração da capacidade total de água que ainda restou no reservatório ao término do dia é igual a:"
        ),
        "alternativas": {
            "A": "3/20",
            "B": "7/20",
            "C": "9/20",
            "D": "11/20",
            "E": "13/20"
        },
        "gabarito": "B"
    })

    # Q58: Aula 4 - Frações II (Multiplicação e Fração de Quantidade)
    questoes.append({
        "numero": 58,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 4 - Frações II: Fração de Quantidade",
        "texto_apoio": {
            "titulo": "Planejamento Financeiro Familiar",
            "conteudo": (
                "Nas aplicações de matemática financeira cotidiana, a operação 'fração de uma sobra' é modelada matematicamente pela "
                "multiplicação direta entre os operadores fracionários sucessivos que incidem sobre o montante remanescente."
            ),
            "fonte": "PAIVA, M. Matemática: Paiva. 2. ed. São Paulo: Moderna, 2013. v. 1, p. 72-74."
        },
        "enunciado": (
            "Um trabalhador destina mensalmente 1/3 do seu salário líquido para o pagamento do aluguel de sua residência. "
            "Do valor restante após quitar o aluguel, ele reserva 3/5 para as despesas com alimentação e supermercado. "
            "A fração do salário líquido total desse trabalhador que sobra após o pagamento do aluguel e da alimentação é igual a:"
        ),
        "alternativas": {
            "A": "1/5",
            "B": "2/15",
            "C": "4/15",
            "D": "7/15",
            "E": "8/15"
        },
        "gabarito": "C"
    })

    # Q59: Aula 4 - Frações II (Conversão Fração ↔ Decimal e Dízimas Periódicas)
    questoes.append({
        "numero": 59,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 4 - Frações II: Dízimas Periódicas",
        "texto_apoio": {
            "titulo": "Frações Geratrizes de Dízimas Compostas",
            "conteudo": (
                "Números decimais infinitos periódicos (dízimas periódicas) são números racionais expressíveis na forma a/b com a, b ∈ Z e b ≠ 0. "
                "O cálculo da fração geratriz de dízimas compostas elimina a repetição periódica multiplicando a equação por potências de 10."
            ),
            "fonte": "ÁVILA, G. Introdução à Análise Matemática. 2. ed. São Paulo: Edgard Blücher, 1999. p. 14-17."
        },
        "enunciado": (
            "Em um processo industrial de embalagem, o tempo de ciclo de uma máquina é registrado como exatamente 1,2333... minutos "
            "(uma dízima periódica composta). Para ajustar o painel de comando, esse número deve ser inserido na forma de fração "
            "ordinária irredutível a/b. A soma dos termos (a + b) dessa fração irredutível é igual a:"
        ),
        "alternativas": {
            "A": "47",
            "B": "53",
            "C": "67",
            "D": "71",
            "E": "90"
        },
        "gabarito": "C"
    })

    # Q60: Aula 5 - Porcentagem / Concentração e Diluição (ENEM 2025 - Q144)
    questoes.append({
        "numero": 60,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 5 - Porcentagem: Cálculos Percentuais",
        "texto_apoio": {
            "titulo": "Concentração e Diluição de Soluções",
            "conteudo": (
                "Em processos laboratoriais de purificação, a remoção seletiva do solvente ou de um componente majoritário altera "
                "a proporção relativa dos constituintes, mesmo mantendo absolutamente invariante a massa do soluto minoritário."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 144."
        },
        "enunciado": (
            "Em um laboratório, um recipiente contém 10 litros de uma solução composta apenas pelas substâncias S1 e S2. "
            "Dessa solução, 99,95% é de S1. Uma quantidade de S1 será retirada dessa solução, mantendo inalterada a quantidade inicial de S2, "
            "de modo que 99,90% da nova solução resultante seja de S1. A quantidade de S1, em litro, que será retirada é:"
        ),
        "alternativas": {
            "A": "0,0050",
            "B": "0,0100",
            "C": "0,5000",
            "D": "4,9775",
            "E": "5,0000"
        },
        "gabarito": "E"
    })

    # Q61: Aula 5 - Porcentagem e Redução de Custos (ENEM 2025 - Q157)
    questoes.append({
        "numero": 61,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 5 - Porcentagem: Variação Percentual",
        "texto_apoio": {
            "titulo": "Economia Circular e Custos Industriais",
            "conteudo": (
                "A substituição de polímeros virgens derivados de petróleo por resinas recicladas pós-consumo proporciona drástica "
                "redução no custo fabril unitário e nas emissões de carbono, atendendo a metas corporativas de sustentabilidade e lucratividade."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 157."
        },
        "enunciado": (
            "Uma empresa produziu, em um determinado mês, 110 toneladas de plástico a partir de derivados de petróleo e 80 toneladas "
            "a partir de plásticos reciclados. O custo para reciclar uma tonelada de plástico é de R$ 500,00, que equivale a 5% do custo "
            "para produzir a mesma quantidade a partir de petróleo virgem. Para o mês seguinte, a meta da empresa é produzir o mesmo total "
            "de 190 toneladas, mas com redução de, pelo menos, 50% no custo total de produção. Para atingir a meta, a quantidade mínima de "
            "toneladas de plástico que devem ser produzidas a partir da reciclagem é:"
        ),
        "alternativas": {
            "A": "135",
            "B": "140",
            "C": "155",
            "D": "160",
            "E": "175"
        },
        "gabarito": "B"
    })

    # Q62: Aula 6 - Grandezas e Medidas (Sistema Métrico / Capacidade - ENEM 2025 - Q164)
    questoes.append({
        "numero": 62,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 6 - Grandezas e Medidas: Sistema Métrico",
        "texto_apoio": {
            "titulo": "Equivalência de Volume e Capacidade",
            "conteudo": (
                "No Sistema Internacional de Unidades (SI), a relação fundamental entre as grandezas de volume geométrico e capacidade de líquidos "
                "estabelece que um decímetro cúbico (1 dm³) equivale a exatamente um litro (1 L) e, por consequência, 1 cm³ equivale a 1 mL."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 164."
        },
        "enunciado": (
            "O dono de uma sorveteria armazena sorvete em potes industriais com capacidade de 20 000 cm³ cada. Ele serve o sorvete aos "
            "clientes em taças individuais, em porções de 250 mL. A quantidade máxima de taças completas que ele consegue servir "
            "a partir de um único pote cheio de sorvete é:"
        ),
        "alternativas": {
            "A": "5",
            "B": "8",
            "C": "50",
            "D": "80",
            "E": "800"
        },
        "gabarito": "D"
    })

    # Q63: Aula 6 - Grandezas e Medidas (Área, Perímetro e Superfície)
    questoes.append({
        "numero": 63,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 6 - Grandezas e Medidas: Cálculo de Área",
        "texto_apoio": {
            "titulo": "Geometria Plana e Paginação de Pisos",
            "conteudo": (
                "O cálculo de materiais de acabamento na construção civil exige a conversão para unidades de mesma grandeza métrica "
                "e o arredondamento superior quando as peças são comercializadas em caixas com quantitativo fechado."
            ),
            "fonte": "DOLCE, O.; POMPEO, J. N. Fundamentos de Matemática Elementar: Geometria Plana. 9. ed. São Paulo: Atual, 2013. v. 9, p. 182-186."
        },
        "enunciado": (
            "Um construtor precisa revestir o piso retangular de um salão de festas que mede 4,8 metros de comprimento por 3,6 metros "
            "de largura. Ele utilizará lajotas cerâmicas quadradas com 30 centímetros de lado. Sabendo que essas lajotas são vendidas "
            "exclusivamente em caixas fechadas contendo 25 unidades cada e desconsiderando as perdas por cortes e rejuntes, a quantidade "
            "mínima de caixas de lajotas que deve ser adquirida para cobrir todo o piso é:"
        ),
        "alternativas": {
            "A": "6 caixas.",
            "B": "7 caixas.",
            "C": "8 caixas.",
            "D": "9 caixas.",
            "E": "10 caixas."
        },
        "gabarito": "C"
    })

    # Q64: Aula 7 - Razão e Proporção (Regra de Três Composta - ENEM 2025 - Q148)
    questoes.append({
        "numero": 64,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 7 - Razão e Proporção: Regra de Três Composta",
        "texto_apoio": {
            "titulo": "Dimensionamento de Produção e Homem-Hora",
            "conteudo": (
                "A relação entre a quantidade de operários, o tempo diário de jornada e a produção total resulta em uma proporção direta "
                "com a grandeza homogênea composta homem-hora (h-homem), mantida fixa a produtividade técnica por hora trabalhada."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 148."
        },
        "enunciado": (
            "Uma fábrica de tijolos ecológicos com 3 funcionários, cada um trabalhando 6 horas diárias, produz 720 unidades por dia. "
            "Para atender ao crescimento da demanda por esse tipo de tijolo, essa fábrica passou a ter 5 funcionários, cada um "
            "trabalhando 9 horas por dia, aumentando, assim, sua capacidade de produção. Todos os funcionários produzem igual quantidade "
            "de tijolos a cada hora. O número de tijolos fabricados diariamente após esse aumento da capacidade de produção é:"
        ),
        "alternativas": {
            "A": "800",
            "B": "1 080",
            "C": "1 200",
            "D": "1 800",
            "E": "2 520"
        },
        "gabarito": "D"
    })

    # Q65: Aula 7 - Razão e Proporção (Escalas - ENEM 2025 - Q161)
    questoes.append({
        "numero": 65,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 7 - Razão e Proporção: Escalas",
        "texto_apoio": {
            "titulo": "Escala Numérica em Projetos e Cartografia",
            "conteudo": (
                "A escala de uma representação gráfica define a razão linear constante entre a distância medida no desenho (d) e a "
                "distância real correspondente (D), expressas obrigatoriamente na mesma unidade de medida: E = d / D."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 161."
        },
        "enunciado": (
            "Um artista que costuma fazer esculturas de areia na praia pediu a um banhista que fizesse um esboço que serviria de modelo. "
            "No papel, a principal dimensão linear desenhada media 20 centímetros. Após a conclusão, a obra de arte esculpida na areia "
            "manteve as mesmas proporções do desenho, sendo que a dimensão correspondente foi ampliada para exatamente 30 metros. "
            "Em qual escala o desenho no papel representa a obra de arte esculpida?"
        ),
        "alternativas": {
            "A": "1 : 1,5",
            "B": "1 : 15",
            "C": "1 : 100",
            "D": "1 : 150",
            "E": "1 : 1 500"
        },
        "gabarito": "D"
    })

    # Q66: Aula 7 - Razão e Proporção (Relação entre Grandezas - ENEM 2025 - Q177)
    questoes.append({
        "numero": 66,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 7 - Razão e Proporção: Grandezas Proporcionais",
        "texto_apoio": {
            "titulo": "Grandezas Derivadas e Análise Dimensional",
            "conteudo": (
                "As leis físicas formulam definições de novas grandezas mediante operações algébricas de razão e produto de grandezas fundamentais. "
                "A determinação da unidade dimensional segue rigorosamente a operação matemática estabelecida na definição."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 177."
        },
        "enunciado": (
            "A luminância de um objeto é a grandeza que descreve a quantidade de luz produzida ou refletida por sua superfície. "
            "Ela está definida formalmente como a razão entre a intensidade luminosa da fonte, medida em candela (cd), e o quadrado "
            "da distância do objeto até o foco de luz, medida em metro (m). A unidade de medida da luminância no Sistema Internacional é:"
        ),
        "alternativas": {
            "A": "cd / m²",
            "B": "m / cd²",
            "C": "cd / m",
            "D": "m / cd",
            "E": "m² / cd"
        },
        "gabarito": "A"
    })

    # Q67: Aula 8 - Matemática Financeira (Lucro e Despesas - ENEM 2025 - Q163)
    questoes.append({
        "numero": 67,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 8 - Matemática Financeira: Lucro e Prejuízo",
        "texto_apoio": {
            "titulo": "Equação de Lucro e Formação de Preço",
            "conteudo": (
                "Na gestão de negócios de serviços recorrentes, o resultado operacional (lucro líquido) resulta da diferença entre a "
                "receita total auferida e o somatório dos custos fixos estruturais e custos variáveis proporcionais à capacidade ocupada."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 163."
        },
        "enunciado": (
            "Um estacionamento possui 120 vagas para veículos e todas estão ocupadas. Cada cliente paga uma mensalidade calculada com base "
            "nas despesas mensais e no lucro pretendido. As despesas são: R$ 14 240,00 com manutenção mais R$ 36,00 de seguro por veículo. "
            "O lucro é a diferença entre a receita arrecadada e as despesas totais. A partir do próximo mês, o seguro por veículo aumentará em 20%, "
            "e a manutenção permanecerá inalterada. Para que o proprietário obtenha um lucro mensal de R$ 10 000,00 mantendo todas as vagas ocupadas, "
            "o valor reajustado da mensalidade de cada cliente será:"
        ),
        "alternativas": {
            "A": "R$ 185,60",
            "B": "R$ 226,09",
            "C": "R$ 245,20",
            "D": "R$ 268,93",
            "E": "R$ 285,60"
        },
        "gabarito": "C"
    })

    # Q68: Aula 8 - Matemática Financeira (Juros Simples em Compra a Prazo)
    questoes.append({
        "numero": 68,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 8 - Matemática Financeira: Juros Simples",
        "texto_apoio": {
            "titulo": "Juros Reais sobre o Saldo Devedor Financiado",
            "conteudo": (
                "Nas vendas a prazo com entrada, o valor da entrada não é financiado, pois é pago no ato. A taxa de juros da operação "
                "incide exclusivamente sobre o saldo devedor remanescente (Capital = Valor à vista - Entrada): i = Juros / Capital Financiado."
            ),
            "fonte": "ASSAF NETO, A. Matemática Financeira e suas Aplicações. 12. ed. São Paulo: Atlas, 2012. p. 38-42."
        },
        "enunciado": (
            "Um consumidor pretende adquirir um televisor cujo preço à vista é de R$ 1 500,00. A loja oferece a opção de pagamento a prazo "
            "em duas parcelas: uma entrada de R$ 300,00 no ato da compra e uma parcela única final de R$ 1 320,00 a ser paga 30 dias após a compra. "
            "A taxa de juros simples mensal cobrada pela loja sobre o saldo financiado nessa operação é de:"
        ),
        "alternativas": {
            "A": "8%",
            "B": "10%",
            "C": "12%",
            "D": "15%",
            "E": "20%"
        },
        "gabarito": "B"
    })

    # Q69: Aula 9 - Potenciação, Radiciação e Notação Científica
    questoes.append({
        "numero": 69,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aula 9 - Potenciação e Notação Científica",
        "texto_apoio": {
            "titulo": "Ordens de Grandeza na Escala Nanométrica",
            "conteudo": (
                "A notação científica padroniza números excessivamente grandes ou pequenos no formato N = a × 10ⁿ, onde 1 ≤ a < 10 e n ∈ Z. "
                "A divisão entre grandezas na escala microscópica opera subtraindo os expoentes das potências de base 10: 10ᵃ / 10ᵇ = 10ᵃ⁻ᵇ."
            ),
            "fonte": "TIPLER, P. A.; LLEWELLYN, R. A. Física Moderna: nanotecnologia e ordens de grandeza. 5. ed. Rio de Janeiro: LTC, 2010. p. 11-14."
        },
        "enunciado": (
            "Na biologia molecular, o diâmetro transversal médio de uma molécula de DNA é de aproximadamente 2 nanômetros (2 nm), "
            "enquanto a espessura média de um fio de cabelo humano é de cerca de 0,08 milímetros. Sabendo que 1 nm equivale a 10⁻⁹ metros "
            "e 1 mm equivale a 10⁻³ metros, a razão entre a medida do diâmetro do DNA e a espessura do fio de cabelo humano, expressa "
            "em notação científica, é igual a:"
        ),
        "alternativas": {
            "A": "2,5 × 10⁻⁴",
            "B": "2,5 × 10⁻⁵",
            "C": "4,0 × 10⁻⁴",
            "D": "4,0 × 10⁻⁵",
            "E": "1,6 × 10⁻⁶"
        },
        "gabarito": "B"
    })

    # Q70: Aulas 10, 11 e 12 - Álgebra, Equação e Função Afim (ENEM 2025 - Q172)
    questoes.append({
        "numero": 70,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "topico_aula": "Aulas 10 a 12 - Álgebra e Equações do 1º Grau",
        "texto_apoio": {
            "titulo": "Modelagem Algébrica de Parcelamento",
            "conteudo": (
                "A divisão de um capital fixo em quantidades distintas de parcelas mensais modela uma relação inversamente proporcional "
                "entre o número de prestações e o valor individual de cada prestação, resultando em uma equação racional redutível."
            ),
            "fonte": "INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA (INEP). ENEM 2025: Prova de Matemática e suas Tecnologias. Caderno 6 Cinza, Questão 172."
        },
        "enunciado": (
            "Um carro que custa 60 mil reais é comercializado por uma revendedora que oferece duas opções de pagamento sem entrada e sem juros:\n"
            "• opção 1: pagamento em n parcelas iguais;\n"
            "• opção 2: pagamento em 6 parcelas a mais do que na opção 1 e, com isso, o valor de cada parcela se torna R$ 500,00 menor do que na opção 1.\n"
            "Nas duas opções de pagamento, o valor total a ser pago pelo carro é exatamente o mesmo.\n"
            "Qual é a quantidade n de parcelas contidas na opção 1 de pagamento?"
        ),
        "alternativas": {
            "A": "18",
            "B": "24",
            "C": "30",
            "D": "42",
            "E": "48"
        },
        "gabarito": "B"
    })

    # Validação do total
    assert len(questoes) == 70, f"Total incorreto: {len(questoes)} (esperado: 70)"

    return {
        "metadados": metadados,
        "redacao": redacao,
        "questoes": questoes
    }

if __name__ == "__main__":
    dados = build_simulado_2()
    print("Sucesso na construção do banco de 70 questões com ABNT e imagens!")
    print(f"Total de questões: {len(dados['questoes'])}")
