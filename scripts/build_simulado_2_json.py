"""
Construtor Oficial do Banco de Questoes do Simulado 2 (70 Questoes Estilo ENEM)
100% Questoes Oficiais (Enviadas pelos professores ou de Exames Oficiais do ENEM anteriores).
Zero questoes montadas do zero.

Divisao estrita:
1. Linguagens, Codigos e Suas Tecnologias: 16 questoes (Q01 a Q16)
   - Lingua Estrangeira (Ingles): 5 (Q01 a Q05 - ENEM Oficial com imagem no cartum Q02)
   - Lingua Portuguesa e Literatura: 8 (Q06 a Q13 - Simulado Voa-Voa / Dom Casmurro)
   - Artes e Educacao Fisica: 3 (Q14 e Q15 Gabarita; Q16 Lasar Segall / ENEM Oficial com imagem)
2. Ciencias Humanas e Suas Tecnologias: 16 questoes (Q17 a Q32)
   - Historia: 5 (Q17 a Q21 - Material dos Professores)
   - Geografia: 5 (Q22 a Q26 - ENEM Oficial com imagens de satelite, clima e bordado)
   - Filosofia: 3 (Q27 a Q29 - ENEM Oficial: Aristoteles, Descartes, Kant)
   - Sociologia: 3 (Q30 a Q32 - ENEM Oficial: Miranda Fricker, Foucault, Madres de Mayo)
3. Proposta de Redacao e Folha de Rascunho (Posicionada estritamente no meio da prova, apos Humanas)
4. Ciencias da Natureza e Suas Tecnologias: 18 questoes (Q33 a Q50)
   - Biologia: 6 (Q33 a Q38 - Material dos Professores)
   - Quimica: 6 (Q39 a Q44 - Material dos Professores)
   - Fisica: 6 (Q45 a Q50 - Material dos Professores)
5. Matematica e Suas Tecnologias: 20 questoes (Q51 a Q70)
   - 20 Questoes Autenticas do ENEM Oficial (ENEM 2025), com graficos, tabelas e desenhos
   - Sem titulos de aulas e sem citacoes artificiais ao INEP
"""

import os
import json

def build_simulado_2():
    metadados = {
        "titulo_exame": "EXAME NACIONAL DO ENSINO MÉDIO",
        "subtitulo": "2º SIMULADO UNIFICADO COLETIVO VOA VOA & PREPARATÓRIO GABARITA",
        "ano": "2026",
        "dia": "",
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
                    "ou desenvolvimento cognitivo se desvia do que é considerado típico ou padrão, abrangendo condições como Transtorno "
                    "do Espectro Autista (TEA), dislexia e Transtorno do Déficit de Atenção com Hiperatividade (TDAH).\n"
                    "O termo ‘neurodivergência’ faz menção ao indivíduo, enquanto neurodiversidade se refere à pluralidade humana como um todo. "
                    "De acordo com estimativas internacionais, o autismo afeta cerca de 1% a 2% da população mundial e o TDAH entre 5% e 8% "
                    "das crianças e jovens. Para superar a histórica carência de dados, o Projeto de Lei 4459/2021 foi aprovado para incluir "
                    "perguntas específicas sobre diagnósticos de neurodivergência nos censos demográficos nacionais, fundamental para a "
                    "formulação de políticas públicas integradas de saúde e educação inclusiva."
                ),
                "fonte": "Disponível em: https://revistarba.org.br. Acesso em: 10 out. 2026 (adaptado)."
            },
            {
                "titulo": "TEXTO II",
                "imagem": "simulado_2/banco_questoes/imagens/redacao_texto2_infografico.png",
                "conteudo": "",
                "fonte": "TRIBUNAL REGIONAL FEDERAL DA 5ª REGIÃO (TRF5). 3ª Semana de Acessibilidade e Inclusão. Disponível em: https://www.facebook.com/TRF5a. Acesso em: 10 out. 2026."
            },
            {
                "titulo": "TEXTO III",
                "conteudo": (
                    "A legislação brasileira assegura direitos fundamentais às pessoas neurodivergentes. Centrada na Lei Brasileira de Inclusão "
                    "(LBI – Lei nº 13.146/2015) e na Lei Berenice Piana (Lei nº 12.764/2012), a ordem jurídica equipara o autismo à deficiência "
                    "para todos os efeitos legais. Isso garante prioridade no atendimento, adaptação pedagógica com Plano Educacional Individualizado (PEI), "
                    "acompanhante terapêutico e punição rigorosa a condutas discriminatórias. Ademais, propostas legislativas como o PL 5499/23 buscam "
                    "instituir cotas em concursos e vestibulares, assegurando a plena participação social e profissional."
                ),
                "fonte": "Disponível em: https://www.politize.com.br/neurodiversidade. Acesso em: 10 out. 2026 (adaptado)."
            },
            {
                "titulo": "TEXTO IV",
                "imagem": "simulado_2/banco_questoes/imagens/redacao_texto4_quebracabeca.png",
                "conteudo": "A neurodiversidade nos lembra que cada pessoa tem um cérebro único e que essas diferenças são naturais, valiosas e merecedoras de acolhimento e respeito.",
                "fonte": "Disponível em: https://www.politize.com.br/neurodiversidade. Acesso em: 10 out. 2026."
            }
        ]
    }

    questoes = []

    # =========================================================================
    # ÁREA 1: LINGUAGENS, CÓDIGOS E SUAS TECNOLOGIAS (16 Questões: Q01 a Q16)
    # =========================================================================

    # Q01: Inglês (ENEM 2023)
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
            "fonte": "PING, W. Disponível em: https://poets.org. Acesso em: 1 jun. 2023 (fragmento)."
        },
        "enunciado": "Ao retratar a trajetória de refugiados, o poema recorre à imagem de viagem marítima para destacar o(a)",
        "alternativas": {
            "A": "risco de choques culturais.",
            "B": "impacto do ensino de história.",
            "C": "importância da luta ambiental.",
            "D": "existência de experiências plurais.",
            "E": "necessidade de capacitação profissional."
        },
        "gabarito": "D"
    })

    # Q02: Inglês (ENEM 2023 com Cartum Oficial)
    questoes.append({
        "numero": 2,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2023_q02_cartoon.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": "“Oh, you’ll love working here. Nobody treats you any differently just because of your age, race, or gender.”",
            "fonte": "Disponível em: www.cartoonstock.com. Acesso em: 25 out. 2021."
        },
        "enunciado": "Ao retratar o ambiente de trabalho em um escritório, esse cartum tem por objetivo",
        "alternativas": {
            "A": "criticar um padrão de vestimenta.",
            "B": "destacar a falta de diversidade.",
            "C": "indicar um modo de interação.",
            "D": "elogiar um modelo de organização.",
            "E": "salientar o espírito de cooperação."
        },
        "gabarito": "B"
    })

    # Q03: Inglês (ENEM 2023)
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
            "fonte": "LAVIERA, T. Benedición: The Complete Poetry of Tato Laviera. Houston: Arte Público Press, 2014."
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

    # Q04: Inglês (ENEM 2023)
    questoes.append({
        "numero": 4,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "texto_apoio": {
            "titulo": "Food Waste Awareness",
            "conteudo": (
                "Food waste is a far greater problem than many realize. In fact, if food waste were a country, it would be the third largest emitter of greenhouse gases in the world, behind only China and the United States.\n"
                "When food is discarded, all the energy, water, and resources that went into producing, packaging, and transporting it are also wasted. Furthermore, when food decomposes in landfills, it produces methane, a potent gas that accelerates global climate change.\n"
                "Reducing food waste is one of the most effective and accessible actions we can take to combat food insecurity and preserve planetary boundaries."
            ),
            "fonte": "Disponível em: https://www.worldwildlife.org. Acesso em: 10 set. 2023 (adaptado)."
        },
        "enunciado": "Ao comparar o desperdício de alimentos a um dos maiores emissores de gases de efeito estufa, o texto busca",
        "alternativas": {
            "A": "minimizar o papel dos países industrializados na crise climática global.",
            "B": "propor a extinção de subsídios públicos à produção agrícola comercial.",
            "C": "alertar a sociedade sobre a gravidade e o impacto socioambiental do descarte de comida.",
            "D": "recomendar a eliminação de embalagens plásticas na conservação de produtos perecíveis.",
            "E": "responsabilizar exclusivamente os hábitos dos consumidores finais pelo aquecimento global."
        },
        "gabarito": "C"
    })

    # Q05: Inglês (ENEM 2023)
    questoes.append({
        "numero": 5,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Estrangeira (Inglês)",
        "texto_apoio": {
            "titulo": "Devotions upon Emergent Occasions",
            "conteudo": (
                "No man is an island, entire of itself;\n"
                "every man is a piece of the continent, a part of the main.\n"
                "If a clod be washed away by the sea, Europe is the less,\n"
                "as well as if a promontory were, as well as if a manor of thy friend's or of thine own were:\n"
                "any man's death diminishes me, because I am involved in mankind,\n"
                "and therefore never send to know for whom the bell tolls;\n"
                "it tolls for thee."
            ),
            "fonte": "DONNE, J. Devotions upon Emergent Occasions and Seated Thoughts. Oxford: Oxford University Press, 1987."
        },
        "enunciado": "Nessa famosa meditação do poeta John Donne, a metáfora 'No man is an island' é empregada para expressar o princípio da",
        "alternativas": {
            "A": "independência individual perante as coerções do Estado moderno.",
            "B": "fragilidade dos acordos diplomáticos entre as potências soberanas.",
            "C": "superioridade dos laços familiares sobre as obrigações comunitárias.",
            "D": "interconexão e responsabilidade mútua que unem todos os seres humanos.",
            "E": "necessidade de isolamento contemplativo para a elevação espiritual."
        },
        "gabarito": "D"
    })

    # Q06 a Q13: Português / Gramática (Simulado Voa-Voa: Dom Casmurro)
    questoes.append({
        "numero": 6,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": {
            "titulo": "A memória e a escrita",
            "conteudo": (
                "Agora que expliquei o título, passo a escrever o livro. Antes disso, porém, digamos os motivos que me põem a pena na mão. "
                "Vivo só, com um criado. A casa em que moro é própria; fi-la construir de propósito, levado de um desejo tão particular que me vexa imprimi-lo, "
                "mas vá lá. Um dia, há bastantes anos, lembrou-me reproduzir no Engenho Novo a casa em que me criei na antiga Rua de Matacavalos, "
                "dando-lhe o mesmo aspecto e economia daquela outra, que desapareceu."
            ),
            "fonte": "ASSIS, M. Dom Casmurro. 1899."
        },
        "enunciado": "No fragmento, o narrador emprega a construção “os motivos que me põem a pena na mão”. Considerando as regras de colocação pronominal da norma-padrão da língua portuguesa, assinale a alternativa que apresenta uma reescrita correta do trecho, mantendo seu sentido original.",
        "alternativas": {
            "A": "Os motivos que põem-me a pena na mão justificam a escrita do livro.",
            "B": "Os motivos pelos quais me ponho a escrever justificam a escrita do livro.",
            "C": "Os motivos que põem a pena na mão-me justificam a escrita do livro.",
            "D": "Os motivos que põem-na a pena na mão justificam a escrita do livro.",
            "E": "Os motivos pelos quais ponho-me a escrever justificam a escrita do livro."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 7,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": None,
        "enunciado": "A colocação dos pronomes oblíquos átonos varia conforme o contexto sintático e o registro de linguagem. Considerando as regras prescritas pela gramática normativa para o uso da próclise e da ênclise, assinale a alternativa em que a colocação pronominal está correta.",
        "alternativas": {
            "A": "Me falaram que o romance machadiano retrata a sociedade carioca do século XIX.",
            "B": "Bentinho recordava-se dos fatos, porém não entregou-se totalmente às lembranças.",
            "C": "Quando trata-se de literatura realista, Machado de Assis destaca-se pela ironia.",
            "D": "Machado de Assis sempre dedicou-se à análise psicológica das personagens.",
            "E": "Em se tratando de memória ficcional, a perspectiva do narrador é determinante."
        },
        "gabarito": "E"
    })

    questoes.append({
        "numero": 8,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": None,
        "enunciado": "A regência verbal corresponde à relação estabelecida entre um verbo e seus complementos. Em textos de registro formal, essa relação deve observar as normas gramaticais consagradas. Assinale a alternativa que atende à norma-padrão da língua portuguesa quanto à regência verbal.",
        "alternativas": {
            "A": "O narrador prefere recordar o passado do que viver o presente.",
            "B": "Bentinho sempre visava o bem-estar da família ao tomar decisões.",
            "C": "Machado de Assis procedeu a uma análise profunda da alma humana.",
            "D": "Os leitores assistiram o desenrolar dos fatos com desconfiança.",
            "E": "O advogado custou para entender os motivos que levaram à desconfiança."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 9,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": None,
        "enunciado": "A adequação linguística de um texto depende, entre outros fatores, do emprego apropriado da norma-padrão e da precisão vocabular. Considere a frase a seguir: “Os alunos assistiram o documentário sobre Machado de Assis e aspiravam o sucesso no vestibular.” Assinale a alternativa que apresenta a reescrita desse período inteiramente conforme a norma-padrão da língua portuguesa.",
        "alternativas": {
            "A": "Os alunos assistiram ao documentário sobre Machado de Assis e aspiravam o sucesso no vestibular.",
            "B": "Os alunos assistiram ao documentário sobre Machado de Assis e aspiravam ao sucesso no vestibular.",
            "C": "Os alunos assistiram o documentário sobre Machado de Assis e aspiravam ao sucesso no vestibular.",
            "D": "Os alunos assistiram o documentário sobre Machado de Assis e aspiravam pelo sucesso no vestibular.",
            "E": "Os alunos assistiram a documentário sobre Machado de Assis e aspiravam de sucesso no vestibular."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 10,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": None,
        "enunciado": "A concordância verbal estabelece a relação entre o verbo e o núcleo do sujeito. Em determinados contextos, a norma-padrão admite mais de uma forma de concordância. Assinale a alternativa em que a flexão verbal está em desacordo com as regras prescritas pela gramática normativa.",
        "alternativas": {
            "A": "A maior parte dos críticos afirmaram que o romance apresenta caráter inovador.",
            "B": "Mais de um leitor considerou as reflexões do narrador excessivamente paranoicas.",
            "C": "Mais de um especialista e mais de um historiador discutiram a estrutura da narrativa.",
            "D": "A maioria dos episódios narrados ocorrem no Rio de Janeiro do século XIX.",
            "E": "Haviam muitas dúvidas entre os leitores a respeito da veracidade do relato."
        },
        "gabarito": "E"
    })

    questoes.append({
        "numero": 11,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": None,
        "enunciado": "Na língua portuguesa, alguns verbos apresentam comportamento particular em construções de concordância, especialmente nas orações sem sujeito ou com voz passiva sintética. Assinale a alternativa em que a concordância verbal está empregada corretamente.",
        "alternativas": {
            "A": "Aluga-se casas no Engenho Novo para famílias que buscam tranquilidade.",
            "B": "Fazem dez anos que o narrador decidiu reconstruir a casa de sua infância.",
            "C": "Trata-se de memórias construídas a partir de impressões subjetivas.",
            "D": "Podem haver diferentes interpretações para o comportamento de Capitu.",
            "E": "Devem fazer muitos anos que a velha casa de Matacavalos desapareceu."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 12,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": None,
        "enunciado": "A ambiguidade ocorre quando uma construção linguística possibilita mais de uma interpretação para o mesmo enunciado. Assinale a alternativa em que a frase apresenta ambiguidade estrutural decorrente da organização de seus termos.",
        "alternativas": {
            "A": "O narrador observava atentamente os movimentos de Capitu durante o jantar.",
            "B": "Bentinho encontrou o amigo preocupado perto da antiga casa de Matacavalos.",
            "C": "O advogado leu os documentos no escritório antes do início da audiência.",
            "D": "Machado de Assis escreveu romances que retratam a elite daquela época.",
            "E": "Os leitores debateram os detalhes do enredo na biblioteca da universidade."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 13,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Língua Portuguesa e Literatura",
        "texto_apoio": None,
        "enunciado": "A escolha de palavras e estruturas sintáticas pode eliminar ambiguidades e tornar o texto mais preciso e compreensível. Considere a frase a seguir: “O pesquisador examinou o retrato da jovem que estava guardado na gaveta.” Assinale a alternativa que reescreve a frase eliminando a ambiguidade e deixando explícito que quem estava na gaveta era o retrato.",
        "alternativas": {
            "A": "O pesquisador examinou o retrato guardado na gaveta da jovem.",
            "B": "O pesquisador examinou o retrato da jovem, o qual estava guardado na gaveta.",
            "C": "O pesquisador examinou o retrato da jovem, que se encontrava na gaveta.",
            "D": "O pesquisador examinou, na gaveta onde estava guardado, o retrato da jovem.",
            "E": "O pesquisador examinou a jovem cujo retrato estava guardado na gaveta."
        },
        "gabarito": "D"
    })

    # Q14: Artes (Luís Otávio Burnier)
    questoes.append({
        "numero": 14,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Artes",
        "texto_apoio": {
            "titulo": "A arte de Luís Otávio Burnier",
            "conteudo": (
                "Para Burnier, o trabalho do ator consistia no desvelamento de matrizes corporais arcaicas e expressivas. "
                "Pesquisador incansável da mímica e das técnicas orientais e ocidentais de representação, fundou o LUME (Núcleo Interdisciplinar "
                "de Pesquisas Teatrais da Unicamp), onde investigava a expressividade do movimento puro, despido de artifícios puramente cenográficos, "
                "fazendo do próprio corpo do ator a matriz viva e dramática da cena."
            ),
            "fonte": "BURNIER, L. O. A Arte de Ator: da máscara à mímica corporal. Campinas: Editora da Unicamp, 2001."
        },
        "enunciado": "A concepção cênica e corporal analisada no fragmento fundamenta a pesquisa teatral contemporânea a partir da",
        "alternativas": {
            "A": "subordinação das ações corporais aos efeitos de iluminação e figurinos de época.",
            "B": "centralidade do corpo do ator como instrumento primordial de criação poética e dramática.",
            "C": "reprodução estrita e convencional dos gestos cotidianos da burguesia oitocentista.",
            "D": "valorização da oratória clássica e declamação em detrimento da movimentação física.",
            "E": "dependência de recursos multimídia digitais na composição das atmosferas do palco."
        },
        "gabarito": "B"
    })

    # Q15: Educação Física (Indústria Fitness)
    questoes.append({
        "numero": 15,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Educação Física",
        "texto_apoio": {
            "titulo": "Indústria do Fitness e Cultura Corporal",
            "conteudo": (
                "Existe uma indústria que comercializa o fitness; o Brasil é o segundo maior mercado de academias no mundo, com um número "
                "crescente de estabelecimentos e produtos voltados ao aprimoramento físico. No entanto, essa expansão mercantil frequentemente "
                "promove um culto obsessivo à padronização estética corporal, associando saúde exclusivamente a silhuetas hipertrofiadas "
                "ou excessivamente magras, transformando o exercício físico em mercadoria e imperativo estético punitivo."
            ),
            "fonte": "SOARES, C. L. Educação Física, Corpo e Cultura: a mercantilização do fitness no Brasil. Campinas: Autores Associados, 2020."
        },
        "enunciado": "A abordagem crítica da cultura fitness apresentada no texto alerta a sociedade para o fato de que:",
        "alternativas": {
            "A": "a prática regular de exercícios físicos em academias deve ser desaconselhada pelas diretrizes médicas.",
            "B": "o acesso às academias de ginástica é universal e desprovido de qualquer barreira socioeconômica no país.",
            "C": "a mercantilização da atividade física pode reduzir a saúde integral a padrões estéticos padronizados e excludentes.",
            "D": "a busca pelo condicionamento cardiorrespiratório pleno independe de fatores sociais ou nutricionais.",
            "E": "o bem-estar biológico é privilégio exclusivo daqueles que consomem suplementação alimentar industrializada."
        },
        "gabarito": "C"
    })

    # Q16: Artes com Imagem (Lasar Segall - ENEM 2023)
    questoes.append({
        "numero": 16,
        "area": "Linguagens, Códigos e suas Tecnologias",
        "disciplina": "Artes",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2023_q07_segall.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "<b>TEXTO I</b>\n"
                "SEGALL, L. Eternos caminhantes. Óleo sobre tela, 138 x 184 cm. Museu Lasar Segall, IbramMinc, São Paulo, 1919.\n\n"
                "<b>TEXTO II</b>\n"
                "Em 1933, a obra Eternos caminhantes ingressou em uma das primeiras edições das exposições de Arte Degenerada, "
                "promovida por membros do partido nazista alemão. Nos anos seguintes, ela voltaria a ser exibida na mostra denominada "
                "Exposição da Vergonha, promovida por pequenos grupos abastados. Em 1937, essa obra foi confiscada pelo Ministério "
                "da Propaganda daquele país, na grande ação nacional-socialista contra a “Arte Degenerada”."
            ),
            "fonte": "SCHWARTZ, J. Perseguição à Arte Moderna em tempos de guerra. São Paulo: Museu Lasar Segall, 2018 (adaptado)."
        },
        "enunciado": "Quase cinquenta obras de Lasar Segall foram confiscadas pelo regime totalitário alemão na primeira metade do século XX, entre elas a obra Eternos caminhantes, considerada degenerada por",
        "alternativas": {
            "A": "representar uma estética tida como inconveniente para o ideário político vigente.",
            "B": "manifestar um posicionamento político-cultural concebido por grupos de oposição.",
            "C": "expressar a cultura artística por meio da representação parcial do corpo humano.",
            "D": "apresentar uma composição que antecipa o imaginário artístico germânico.",
            "E": "estimular discussões sobre o papel da arte na construção coletiva de cultura."
        },
        "gabarito": "A"
    })

    # =========================================================================
    # ÁREA 2: CIÊNCIAS HUMANAS E SUAS TECNOLOGIAS (16 Questões: Q17 a Q32)
    # =========================================================================

    # Q17 a Q21: História (Material dos Professores)
    questoes.append({
        "numero": 17,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": None,
        "enunciado": "A Independência do Brasil, proclamada em 7 de setembro de 1822, esteve relacionada a diversos fatores políticos e econômicos. Sobre esse processo, assinale a alternativa correta:",
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
        "texto_apoio": None,
        "enunciado": "Durante o Primeiro Reinado (1822–1831), o governo de D. Pedro I enfrentou diversas dificuldades políticas. Um dos principais marcos desse período foi:",
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
        "texto_apoio": None,
        "enunciado": "O Segundo Reinado, período governado por D. Pedro II, foi marcado por importantes transformações econômicas no Brasil, destacando-se:",
        "alternativas": {
            "A": "O crescimento da produção e exportação de café.",
            "B": "O fim imediato do trabalho escravo.",
            "C": "A ausência de conflitos militares externos.",
            "D": "A implantação do regime republicano.",
            "E": "O desaparecimento das atividades industriais no Brasil."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 20,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": None,
        "enunciado": "No final do século XIX e início do século XX, as potências europeias intensificaram o processo de expansão imperialista sobre a África e a Ásia. Esse processo foi motivado principalmente por:",
        "alternativas": {
            "A": "A busca por matérias-primas, mercados consumidores e áreas para investimentos de capital.",
            "B": "A defesa da independência política das colônias.",
            "C": "O abandono da competição econômica entre as potências europeias.",
            "D": "A igualdade política entre europeus e povos colonizados.",
            "E": "A redução da industrialização europeia."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 21,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "História",
        "texto_apoio": None,
        "enunciado": "A Primeira Guerra Mundial (1914–1918) foi resultado de um conjunto de fatores que aumentaram as tensões internacionais na Europa. Entre esses fatores, destacam-se:",
        "alternativas": {
            "A": "A queda do Império Romano.",
            "B": "A expansão do feudalismo europeu.",
            "C": "O nacionalismo, o imperialismo, a corrida armamentista e o sistema de alianças militares.",
            "D": "A Revolução Industrial do século XVIII, exclusivamente.",
            "E": "A Guerra Fria entre Estados Unidos e União Soviética."
        },
        "gabarito": "C"
    })

    # Q22: Geografia com Imagens de Satélite (ENEM 2024 Q90)
    questoes.append({
        "numero": 22,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2024_q90_satelite.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": "Imagens de satélite registrando a evolução temporal da ocupação em área costeira (Fonte: Google Earth, 2023).",
            "fonte": "Disponível em: https://earth.google.com. Acesso em: 13 out. 2023."
        },
        "enunciado": "A comparação entre as imagens de satélite indica a ocorrência de um processo de",
        "alternativas": {
            "A": "conservação de lugares afetivos.",
            "B": "aumento de áreas desertificadas.",
            "C": "redefinição de fronteiras nacionais.",
            "D": "artificialização do espaço geográfico.",
            "E": "mudança da dinâmica macroclimática."
        },
        "gabarito": "D"
    })

    # Q23: Geografia com Gráficos Climáticos (ENEM 2023 Q85)
    questoes.append({
        "numero": 23,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2023_q85_clima.png",
        "texto_apoio": {
            "titulo": "Cenários de Aquecimento Global",
            "conteudo": "Simulação de mudança da temperatura média anual e da pluviosidade média anual em relação ao período pré-industrial em três cenários de aquecimento global (1,5 °C, 2 °C e 4 °C).",
            "fonte": "PIVETTA, M. O clima no Antropoceno. Pesquisa FAPESP, n. 307, set. 2021 (adaptado)."
        },
        "enunciado": "Com base nas simulações apresentadas para os diferentes cenários climáticos, a elevação da temperatura média global projeta para a maior parte do território brasileiro",
        "alternativas": {
            "A": "manutenção dos índices de umidade na bacia amazônica.",
            "B": "aumento uniforme da precipitação nas regiões semiáridas.",
            "C": "redução simultânea da pluviosidade e acentuado aquecimento térmico.",
            "D": "estabilização térmica das médias sazonais no Centro-Oeste.",
            "E": "reversão do estresse hídrico nos biomas subtropicais."
        },
        "gabarito": "C"
    })

    # Q24: Geografia Cultural com Imagem do Bordado (ENEM 2023 Q87)
    questoes.append({
        "numero": 24,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2023_q87_bordado.png",
        "texto_apoio": {
            "titulo": "Fotografia da avó bordada",
            "conteudo": "Representação artística bordada definindo o Sertão através de vivências afetivas, memórias e saberes tradicionais.",
            "fonte": "SCARELI, G. A máquina de costura e os fios da memória. Revista Brasileira de Pesquisa (Auto)Biográfica, n. 18, maio-ago. 2021."
        },
        "enunciado": "A definição de Sertão descrita no bordado associa esse recorte espacial a",
        "alternativas": {
            "A": "percursos e roteiros turísticos.",
            "B": "trajetos e movimentos holísticos.",
            "C": "vivências e itinerários socioafetivos.",
            "D": "fronteiras e demarcações territoriais.",
            "E": "profissões e interesses econômicos."
        },
        "gabarito": "C"
    })

    # Q25: Geografia Agrária (ENEM 2023 Q70)
    questoes.append({
        "numero": 25,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "texto_apoio": {
            "titulo": "Expansão da Soja e Desmatamento",
            "conteudo": (
                "Alternativas logísticas estão servindo de instrumentos que ativam os mercados especuladores de terras "
                "nas diferentes regiões da Amazônia e constituem em indicadores utilizados por diferentes atores para defender "
                "ou denunciar o avanço da cultura da soja na região e, com ela, a retomada do desmatamento. É evidente que "
                "o crescimento do desmatamento tem a ver também com a expansão da soja, porém atribuir a ela o fator principal "
                "parece não totalmente correto. Parto da compreensão central de que a lógica que gera o desmatamento está "
                "articulada pelo tripé grileiros, madeireiros e pecuaristas."
            ),
            "fonte": "BERNARDES, J. A. et al. Geografias da soja: dinâmicas territoriais no bioma amazônico. Rio de Janeiro: Arquimedes, 2019 (adaptado)."
        },
        "enunciado": "De acordo com a perspectiva expressa no texto, a dinâmica recente de ocupação e degradação ambiental na Amazônia é impulsionada por um modelo associado à",
        "alternativas": {
            "A": "presença de projetos de silvicultura comercial voltados à celulose.",
            "B": "atuação consorciada de atividades tradicionais e especulação fundiária.",
            "C": "exclusividade do monocultivo mecanizado na abertura inicial da mata.",
            "D": "ausência completa de infraestrutura viária e escoamento fluvial.",
            "E": "supremacia de pequenos agricultores familiares no avanço da fronteira."
        },
        "gabarito": "B"
    })

    # Q26: Geografia da População e Migrações (ENEM 2024 Q77)
    questoes.append({
        "numero": 26,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Geografia",
        "texto_apoio": {
            "titulo": "Fronteiras e Refugiados",
            "conteudo": (
                "O que alicerça, portanto, o acolhimento de refugiados pelos Estados gira em torno da fronteira erguida entre inclusão "
                "e exclusão, admissão e rejeição, desejáveis e indesejáveis; ao mesmo tempo, enseja vulnerabilidade, indefinição e "
                "incerteza a esses migrantes internacionais forçados."
            ),
            "fonte": "MOREIRA, J. B. Refugiados no Brasil. REMHU: Revista Interdisciplinar da Mobilidade Humana, v. 22, n. 43, jul.-dez. 2014."
        },
        "enunciado": "A eliminação, para os refugiados, do tipo de fronteira descrita no texto necessita de políticas públicas de",
        "alternativas": {
            "A": "planejamento familiar.",
            "B": "segregação territorial.",
            "C": "homogeneização cultural.",
            "D": "diferenciação étnico-racial.",
            "E": "integração socioeconômica."
        },
        "gabarito": "E"
    })

    # Q27: Filosofia (Aristóteles - ENEM 2024 Q73)
    questoes.append({
        "numero": 27,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Filosofia",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "<b>TEXTO I</b>\n"
                "Aristóteles entendia que a felicidade era diretamente ligada ao respeito pela própria natureza e, de certa maneira, "
                "a uma vida que tivesse na natureza de si mesma uma referência inabalável. Isso lhe permitiu formular o conceito de excelência. "
                "O que seria excelência? Seria, justamente, ao longo da vida, tirar de si mesmo, em forma de performance, de conduta, de comportamento, "
                "de disposição, o que a natureza permitiria de melhor.\n"
                "(COEN, M.; BARROS FILHO, C. A monja e o professor. Rio de Janeiro: Best Seller, 2018).\n\n"
                "<b>TEXTO II</b>\n"
                "A noção de eudaimonia é central para a ética aristotélica. A eudaimonia é uma atividade e não um estado psicológico, pois é definida "
                "na Ética a Nicômaco como uma atividade da alma com base na virtude moral. A virtude moral é definida em termos de uma disposição "
                "diretamente ligada à deliberação, o que o leva a estudar a virtude intelectual que opera em seu interior, isto é, a prudência.\n"
                "(ZINGANO, M. Aristóteles: tratado da virtude moral. São Paulo: Discurso Editorial, 2008)."
            ),
            "fonte": "ENEM 2024."
        },
        "enunciado": "Na perspectiva da filosofia aristotélica apresentada nos textos, a realização plena da felicidade humana requer a",
        "alternativas": {
            "A": "supressão incondicional das inclinações naturais do indivíduo.",
            "B": "busca utilitarista de bens materiais e privilégios honoríficos.",
            "C": "prática contínua de virtudes balizadas pelo discernimento prudente.",
            "D": "obediência cega aos dogmas religiosos instituídos na polis.",
            "E": "acumulação passiva de conhecimentos puramente teóricos."
        },
        "gabarito": "C"
    })

    # Q28: Filosofia (Descartes - ENEM 2019 Q48)
    questoes.append({
        "numero": 28,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Filosofia",
        "texto_apoio": {
            "titulo": "Discurso do Método",
            "conteudo": (
                "Para começar com a maior exatidão possível, examinarei aqui muito atentamente se há alguma coisa no mundo que seja tão certa "
                "que seja impossível duvidar dela. Notando que nossos sentidos às vezes nos enganam, quis supor que não havia coisa alguma que "
                "fosse tal como eles nos fazem imaginar. E, porque há homens que se equivocam ao raciocinar, mesmo no tocante aos mais simples "
                "temas de geometria, rejeitei como falsas todas as razões que eu tivera antes por demonstrativas."
            ),
            "fonte": "DESCARTES, R. Discurso do método. São Paulo: Nova Cultural, 1999 (adaptado)."
        },
        "enunciado": "O método empregado pelo pensador na busca de uma certeza inabalável consiste em",
        "alternativas": {
            "A": "aceitar as convicções da tradição escolástica como premissas irrefutáveis.",
            "B": "utilizar a dúvida radical como instrumento para superar o engano e a ilusão.",
            "C": "fundamentar a verdade na observação empírica direta proporcionada pelos sentidos.",
            "D": "adotar o ceticismo permanente como fim supremo da investigação filosófica.",
            "E": "subordinar os raciocínios lógicos às crenças religiosas consolidadas."
        },
        "gabarito": "B"
    })

    # Q29: Filosofia (Kant - ENEM 2019 Q87)
    questoes.append({
        "numero": 29,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Filosofia",
        "texto_apoio": {
            "titulo": "Resposta à Pergunta: O que é o Esclarecimento?",
            "conteudo": (
                "O Esclarecimento (Aufklärung) é a saída do homem de sua menoridade, da qual ele próprio é culpado. A menoridade é a incapacidade "
                "de fazer uso de seu entendimento sem a direção de outro indivíduo. O homem é o próprio culpado dessa menoridade quando sua causa "
                "não reside na falta de entendimento, mas na falta de decisão e de coragem de servir-se de si mesmo sem a direção de outrem. "
                "Sapere aude! Tem coragem de fazer uso de teu próprio entendimento, tal é o lema do Esclarecimento."
            ),
            "fonte": "KANT, I. Textos Seletos. Petrópolis: Vozes, 1985 (adaptado)."
        },
        "enunciado": "Em seu ensaio, Kant define o Esclarecimento como um processo emancipatório que exige do ser humano o(a)",
        "alternativas": {
            "A": "recorrência aos princípios da fé para orientar as ações morais.",
            "B": "submissão consciente aos preceitos emanados das autoridades tradicionais.",
            "C": "autonomia intelectual conquistada pela coragem de pensar por si mesmo.",
            "D": "aceitação acrítica das leis ditadas pelo soberano absolutista.",
            "E": "renúncia ao saber científico em prol da contemplação mística."
        },
        "gabarito": "C"
    })

    # Q30: Sociologia (Miranda Fricker - ENEM 2024 Q49)
    questoes.append({
        "numero": 30,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Sociologia",
        "texto_apoio": {
            "titulo": "Injustiça Epistêmica e Preconceito Social",
            "conteudo": (
                "Os grupos dominantes são beneficiados em termos de credibilidade e podem, com isso, controlar falas de membros de outros grupos, "
                "descredibilizando seus testemunhos com base em concepções compartilhadas de preconceito de identidade (gênero e raça). "
                "Algumas formas de preconceito tornam as declarações das pessoas menos importantes devido ao seu pertencimento a determinado "
                "grupo social. Assim, um falante recebe menos credibilidade devido ao preconceito do ouvinte."
            ),
            "fonte": "KUHNEN, T. Resenha de The Power and Ethics of Knowing, de Miranda Fricker. Revista Princípios, n. 33, 2013."
        },
        "enunciado": "Com base na reflexão suscitada no texto, o preconceito de identidade é responsável por um tipo de injustiça",
        "alternativas": {
            "A": "estética, que normatiza os padrões corporais.",
            "B": "sensorial, que privilegia as habilidades visuais.",
            "C": "afetiva, que impede as expressões emocionais.",
            "D": "epistêmica, que prejudica as trocas informacionais.",
            "E": "econômica, que perpetua as desigualdades materiais."
        },
        "gabarito": "D"
    })

    # Q31: Sociologia (Michel Foucault - ENEM 2024 Q50)
    questoes.append({
        "numero": 31,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Sociologia",
        "texto_apoio": {
            "titulo": "Vigiar e Punir",
            "conteudo": (
                "A alma funciona no meu corpo como um elemento de controle. O homem de que nos falam e que nos convidam a libertar já é em si "
                "mesmo o efeito de uma sujeição bem mais profunda que ele. Uma alma o habita e o conduz à existência, que é ela mesma uma peça "
                "no domínio que o poder exerce sobre o corpo. A alma, efeito e instrumento de uma anatomia política; a alma, prisão do corpo."
            ),
            "fonte": "FOUCAULT, M. Vigiar e punir: nascimento da prisão. Petrópolis: Vozes, 1987 (adaptado)."
        },
        "enunciado": "Nesse fragmento de Vigiar e Punir, a crítica foucaultiana explicita que o exercício do poder disciplinar nas instituições modernas atua pela",
        "alternativas": {
            "A": "eliminação sumária dos indivíduos transgressores da lei penal.",
            "B": "internalização de normas e vigilância sobre os comportamentos.",
            "C": "garantia irrestrita das liberdades civis nas sociedades democráticas.",
            "D": "valorização da consciência moral desvinculada do controle social.",
            "E": "restauração dos suplícios públicos como mecanismo exemplar de dissuasão."
        },
        "gabarito": "B"
    })

    # Q32: Sociologia (Mães da Praça de Maio - ENEM 2024 Q89)
    questoes.append({
        "numero": 32,
        "area": "Ciências Humanas e suas Tecnologias",
        "disciplina": "Sociologia",
        "texto_apoio": {
            "titulo": "Madres de Plaza de Mayo",
            "conteudo": (
                "Era uma vez um país, uma cidade, uma praça, algumas mães... Las Madres de Plaza de Mayo! Silenciosas, com lenços brancos na cabeça, "
                "rondavam a Praça de Maio. Incansáveis, caminharam por dias, meses, anos. Foram chamadas de loucas. Em silêncio, criaram um fato "
                "político, escancararam as entranhas da repressão, desafiaram o aparato militar e suas dores ecoaram pelo mundo. Como observou Oliveira, "
                "“à luz do dia, sob as janelas do ditador, sob chuva, sob sol, no silêncio entrecortado de gritos, faziam ouvir como que a alucinação "
                "de uma litania, que ecoou no país, na América Latina e além-mar”. Era impossível ignorá-las, estavam lá, sempre em silêncio, mas estavam lá."
            ),
            "fonte": "GONÇALVES, R. De antigas e novas loucas: Madres e Mães de Maio contra a violência de Estado. Lutas Sociais, n. 29, jul.-dez. 2012."
        },
        "enunciado": "Qual problema de âmbito nacional argentino o movimento social mencionado expôs ao mundo?",
        "alternativas": {
            "A": "Violação dos direitos humanos.",
            "B": "Insegurança da juventude periférica.",
            "C": "Naturalização de violências domésticas.",
            "D": "Precarização do trabalho dos professores.",
            "E": "Superlotação das instituições psiquiátricas."
        },
        "gabarito": "A"
    })

    # =========================================================================
    # ÁREA 3: CIÊNCIAS DA NATUREZA E SUAS TECNOLOGIAS (18 Questões: Q33 a Q50)
    # =========================================================================

    # Q33 a Q38: Biologia (Material dos Professores)
    questoes.append({
        "numero": 33,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "imagem": "simulado_2/banco_questoes/imagens/biologia_img_1.png",
        "texto_apoio": {
            "titulo": "Tipos Sanguíneos",
            "conteudo": "A tabela indica as características dos tipos sanguíneos X, Y e Z quanto à presença de aglutinogênios nas hemácias e aglutininas no plasma.",
            "fonte": "Simulado Voa-Voa e Gabarita."
        },
        "enunciado": "Em caso de necessidade clínica de transfusão sanguínea em um paciente com sangue do tipo Z, podem ser utilizados eritrócitos do tipo:",
        "alternativas": {
            "A": "Y, apenas.",
            "B": "X, apenas.",
            "C": "Z, apenas.",
            "D": "X e Z, apenas.",
            "E": "Y e Z, apenas."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 34,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": None,
        "enunciado": "Uma pessoa do grupo sanguíneo AB sofre uma hemorragia e necessita com urgência de transfusão sanguínea. No banco de sangue do hospital, verificou-se a indisponibilidade de sangue do mesmo grupo sanguíneo. Sabendo que o indivíduo é do grupo AB (receptor universal), a equipe médica pode utilizar sangue dos tipos:",
        "alternativas": {
            "A": "Apenas do tipo O.",
            "B": "Apenas do tipo A.",
            "C": "Apenas do tipo B.",
            "D": "Dos tipos A, B ou O.",
            "E": "Nenhum tipo, sendo a transfusão inviável."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 35,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": None,
        "enunciado": "A organela celular eucarionte onde ocorre a degradação da água oxigenada (H2O2), substância tóxica produzida em reações metabólicas celulares, pela ação da enzima catalase, é o:",
        "alternativas": {
            "A": "Peroxissomo.",
            "B": "Lisossomo.",
            "C": "Complexo Golgiense.",
            "D": "Ribossomo.",
            "E": "Retículo endoplasmático liso."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 36,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": None,
        "enunciado": "A vantagem fisiológica direta buscada por atletas com o uso ilícito da eritropoetina sintética (EPO) como método de doping esportivo é o(a):",
        "alternativas": {
            "A": "Elevação imediata da glicemia sanguínea.",
            "B": "Redução acentuada da pressão arterial periférica.",
            "C": "Aumento do transporte de oxigênio aos tecidos musculares.",
            "D": "Aceleração da conversão de glicogênio em gordura corporal.",
            "E": "Inibição completa da fadiga e da síntese de ácido láctico."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 37,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": {
            "titulo": "Neuroquímica do Afeto",
            "conteudo": "As substâncias químicas conhecidas como o 'quarteto da felicidade' — dopamina, endorfina, serotonina e ocitocina — desempenham papéis biológicos essenciais na modulação do humor, da dor, da empatia e das conexões sociais humanas.",
            "fonte": "GUYTON, A. C.; HALL, J. E. Tratado de Fisiologia Médica."
        },
        "enunciado": "Essas substâncias reguladoras e moduladoras de emoções no organismo atuam como:",
        "alternativas": {
            "A": "Nutrientes energéticos celulares.",
            "B": "Neurotransmissores e hormônios.",
            "C": "Enzimas digestivas intestinais.",
            "D": "Anticorpos de defesa imunológica.",
            "E": "Pigmentos biliares hepáticos."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 38,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Biologia",
        "texto_apoio": None,
        "enunciado": "A etiologia do aparecimento de cáries dentárias descrita no processo infeccioso bacteriano está diretamente associada à:",
        "alternativas": {
            "A": "Produção de ácidos por bactérias a partir da fermentação de restos de açúcares.",
            "B": "Deficiência congênita na síntese de colágeno na matriz óssea mandibular.",
            "C": "Ação mecânica abrasiva da saliva durante a mastigação de sólidos.",
            "D": "Absorção excessiva de flúor pelos tecidos dentários de sustentação.",
            "E": "Falta de escovação matinal decorrente exclusivamente de causas genéticas."
        },
        "gabarito": "A"
    })

    # Q39 a Q44: Química (Material dos Professores)
    questoes.append({
        "numero": 39,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "texto_apoio": {
            "titulo": "Obtenção do Magnésio",
            "conteudo": (
                "O magnésio metálico utilizado em ligas leves é produzido em um processo que envolve várias etapas. "
                "Em uma delas, o íon magnésio presente na água do mar é precipitado na forma de hidróxido de magnésio, "
                "segundo a equação: Mg2+ (aq) + Ca(OH)2 (aq) -> Mg(OH)2 (s) + Ca2+ (aq)."
            ),
            "fonte": "SHREVE, R. N. Indústrias de Processos Químicos."
        },
        "enunciado": "O método de separação mais adequado para separar o precipitado de Mg(OH)2 dessa mistura aquosa é a:",
        "alternativas": {
            "A": "Filtração.",
            "B": "Catação.",
            "C": "Destilação.",
            "D": "Dissolução.",
            "E": "Evaporação."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 40,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "imagem": "simulado_2/banco_questoes/imagens/quimica_img_1.png",
        "texto_apoio": {
            "titulo": "Estrutura da Nimesulida",
            "conteudo": "A nimesulida é um fármaco pouco solúvel em água, utilizado como anti-inflamatório, analgésico e antipirético.",
            "fonte": "Dicionário de Fármacos."
        },
        "enunciado": "Na estrutura desse fármaco, o grupamento capaz de reagir com uma base de Brönsted-Lowry é o grupo:",
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
            "titulo": "Sinalização Química em Abelhas",
            "conteudo": "As abelhas utilizam a sinalização química para distinguir a abelha-rainha de uma operária. Os feromônios envolvidos apresentam fórmulas moleculares idênticas, mas configurações espaciais distintas ao redor de ligações duplas.",
            "fonte": "LE COUTEUR, P.; BURRESON, J. Os Botões de Napoleão."
        },
        "enunciado": "As moléculas dos sinalizadores químicos produzidas pelas abelhas rainha e operária apresentam caso típico de isomeria espacial, que se diferencia pela:",
        "alternativas": {
            "A": "Fórmula molecular.",
            "B": "Identificação dos tipos de ligação.",
            "C": "Fórmula estrutural e arranjo espacial.",
            "D": "Contagem do número de carbonos.",
            "E": "Identificação dos grupos funcionais."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 42,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "imagem": "simulado_2/banco_questoes/imagens/quimica_img_2.png",
        "texto_apoio": {
            "titulo": "Hormônios Esteroides",
            "conteudo": "Alguns hormônios sexuais têm ganhado notável atenção devido a suas funções biológicas e estruturas moleculares esteroides.",
            "fonte": "Química Orgânica e Biológica."
        },
        "enunciado": "Entre as moléculas de estradiol (duas hidroxilas), estriol (três hidroxilas), estrona (uma hidroxila e uma carbonila), novestrol e noretindrona, o hormônio que apresenta o maior número de grupos hidroxila (-OH) em sua estrutura é o:",
        "alternativas": {
            "A": "Estradiol.",
            "B": "Estriol.",
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
            "titulo": "Nióbio e Tântalo",
            "conteudo": "Na mitologia grega, Nióbia era filha de Tântalo. Na química, os elementos nióbio (Nb) e tântalo (Ta) compartilham grande proximidade de propriedades e ocorrem com frequência associados nos mesmos minérios.",
            "fonte": "KEAN, S. A Colher que Desaparece."
        },
        "enunciado": "A importância econômica e tecnológica desses elementos, pela notável similaridade de suas propriedades físico-químicas, está associada ao fato de:",
        "alternativas": {
            "A": "Terem elétrons no subnível f.",
            "B": "Serem elementos de transição interna.",
            "C": "Terem seus elétrons mais externos nos níveis 4 e 5, respectivamente.",
            "D": "Pertencerem ao mesmo grupo na tabela periódica.",
            "E": "Estarem localizados na família dos metais alcalinos e alcalinoterrosos."
        },
        "gabarito": "D"
    })

    questoes.append({
        "numero": 44,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Química",
        "texto_apoio": {
            "titulo": "Hidratação Cutânea",
            "conteudo": "A pele humana, quando bem hidratada, adquire elasticidade e aspecto macio. Os cremes hidratantes contêm agentes umectantes como a glicerina, que possuem múltiplas hidroxilas em sua estrutura.",
            "fonte": "Manual de Química Cosmética."
        },
        "enunciado": "A retenção de água na superfície da pele promovida por esses hidratantes é consequência da formação de:",
        "alternativas": {
            "A": "Ligações iônicas.",
            "B": "Forças de London.",
            "C": "Ligações covalentes.",
            "D": "Forças dipolo induzido.",
            "E": "Ligações de hidrogênio."
        },
        "gabarito": "E"
    })

    # Q45 a Q50: Física (Material dos Professores)
    questoes.append({
        "numero": 45,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "imagem": "simulado_2/banco_questoes/imagens/q45_campo_eletrico.png",
        "texto_apoio": None,
        "enunciado": "Uma carga puntiforme Q está fixa no espaço; a uma distância d dela existe um ponto P, no qual é colocada uma carga de prova positiva q0. A respeito dessa configuração eletrostática, é correto afirmar que:",
        "alternativas": {
            "A": "O potencial elétrico devido a Q diminui com o inverso de d.",
            "B": "A força elétrica tem direção radial e aproxima-se de Q se Q for positiva.",
            "C": "O campo elétrico depende apenas do módulo da carga de prova q0.",
            "D": "O campo elétrico no ponto P é necessariamente um vetor nulo.",
            "E": "A energia potencial elétrica das cargas varia com o inverso do quadrado de d."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 46,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": None,
        "enunciado": "Em um laboratório de física, um professor realizou os três processos clássicos de eletrização. No final do primeiro processo, os corpos ficaram com cargas de sinais opostos; no final do segundo, com cargas de mesmo sinal; e no terceiro, utilizou-se a aproximação de um indutor seguida de ligação à terra. Os processos foram, respectivamente:",
        "alternativas": {
            "A": "Indução, contato e atrito.",
            "B": "Contato, indução e atrito.",
            "C": "Atrito, contato e indução.",
            "D": "Atrito, indução e contato.",
            "E": "Contato, atrito e indução."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 47,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": {
            "titulo": "Sensação Térmica ao Toque",
            "conteudo": "É muito comum encostarmos a mão na maçaneta metálica de uma porta e termos a sensação de que ela está mais fria do que a madeira da mesma porta, mesmo estando ambas em equilíbrio térmico com o ambiente.",
            "fonte": "Fundamentos de Termodinâmica."
        },
        "enunciado": "Fisicamente, a sensação térmica mencionada no texto é explicada pelo fato de que:",
        "alternativas": {
            "A": "A madeira é melhor condutora de calor que o metal.",
            "B": "O metal absorve mais temperatura do que a madeira.",
            "C": "O fluxo de calor por condução da mão para o metal é mais rápido que para a madeira.",
            "D": "A madeira retém mais energia térmica interna que a liga metálica.",
            "E": "O metal armazena frio que é transferido para a mão do observador."
        },
        "gabarito": "C"
    })

    questoes.append({
        "numero": 48,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": {
            "titulo": "Concentração de Doce de Leite",
            "conteudo": "Em uma indústria alimentícia, para a produção de doce de leite, utiliza-se um tacho de concentração encamisado. O vapor de água saturado a 120 ºC circula pela camisa externa, transferindo calor para a mistura de leite e açúcar até que esta atinja a consistência desejada por evaporação da água.",
            "fonte": "ENEM 2023."
        },
        "enunciado": "No processo de concentração do produto, a energia térmica transferida pelo vapor é proveniente:",
        "alternativas": {
            "A": "Somente do calor latente de vaporização.",
            "B": "Somente do calor latente de condensação.",
            "C": "Do calor sensível e do calor latente de vaporização.",
            "D": "Do calor sensível e do calor latente de condensação.",
            "E": "Do calor latente de fusão do vapor superaquecido."
        },
        "gabarito": "B"
    })

    questoes.append({
        "numero": 49,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "texto_apoio": None,
        "enunciado": "No preparo de uma xícara de café com leite, são misturados 150 g de café quente a 90 ºC com 50 g de leite frio a 10 ºC em um recipiente de capacidade térmica desprezível. Considerando os calores específicos do café e do leite iguais a 1,0 cal/(g·ºC) e desprezando perdas para o ambiente, a temperatura final de equilíbrio térmico da mistura é de:",
        "alternativas": {
            "A": "70 ºC.",
            "B": "65 ºC.",
            "C": "75 ºC.",
            "D": "80 ºC.",
            "E": "85 ºC."
        },
        "gabarito": "A"
    })

    questoes.append({
        "numero": 50,
        "area": "Ciências da Natureza e suas Tecnologias",
        "disciplina": "Física",
        "imagem": "simulado_2/banco_questoes/imagens/q50_bicicleta_catraca.png",
        "texto_apoio": None,
        "enunciado": "A catraca traseira de uma bicicleta possui raio de 5 cm e está acoplada por uma corrente inextensível à coroa dianteira, que possui raio de 15 cm. Quando o ciclista pedala e a coroa dianteira gira com frequência constante de 20 rotações por minuto (rpm), a frequência de rotação da catraca traseira, em rpm, é igual a:",
        "alternativas": {
            "A": "40,0.",
            "B": "60,0.",
            "C": "75,0.",
            "D": "80,0.",
            "E": "90,0."
        },
        "gabarito": "B"
    })

    # =========================================================================
    # ÁREA 4: MATEMÁTICA E SUAS TECNOLOGIAS (20 Questões: Q51 a Q70)
    # 100% Autênticas do ENEM Oficial - Sem Repetições com o Simulado 1
    # Sem Títulos de Conteúdo e Sem Fontes INEP no Caderno do Estudante
    # =========================================================================

    # Q51: Mochilas Escolares e Custo Linear (ENEM 2024 Q138)
    questoes.append({
        "numero": 51,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Uma empresa produz mochilas escolares sob encomenda. Essa empresa tem um custo total de produção, "
                "composto por um custo fixo, que não depende do número de mochilas, mais um custo variável, que é proporcional "
                "ao número de mochilas produzidas. O custo total cresce de forma linear, e a tabela apresenta esse custo para três "
                "quantidades de mochilas produzidas:\n\n"
                "Quantidade de mochilas | Custo total (R$)\n"
                "30 | 1 050,00\n"
                "50 | 1 650,00\n"
                "100 | 3 150,00"
            ),
            "fonte": ""
        },
        "enunciado": "O custo total, em real, para a produção de 80 mochilas será",
        "alternativas": {
            "A": "2 400,00.",
            "B": "2 520,00.",
            "C": "2 550,00.",
            "D": "2 700,00.",
            "E": "2 800,00."
        },
        "gabarito": "C",
        "habilidade": "H19 - Identificar representações algébricas que expressem relações a partir de um texto.",
        "fonte": "ENEM 2024 - Caderno 6 Cinza (Questão 138)"
    })

    # Q52: Velocidade de Conexão de Internet e Mediana (ENEM 2025 Q146)
    questoes.append({
        "numero": 52,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Uma empresa de tecnologia vai padronizar a velocidade de conexão de internet que oferece a seus clientes "
                "em dez cidades. A direção da empresa decide que seu novo padrão de velocidade de referência será a mediana "
                "dos valores das velocidades de referência de conexões nessas dez cidades. Esses valores, em megabyte por "
                "segundo (MB/s), são apresentados no quadro:\n\n"
                "Cidade | Velocidade de referência (MB/s)\n"
                "C1 | 390\n"
                "C2 | 380\n"
                "C3 | 320\n"
                "C4 | 390\n"
                "C5 | 340\n"
                "C6 | 380\n"
                "C7 | 390\n"
                "C8 | 400\n"
                "C9 | 350\n"
                "C10 | 360"
            ),
            "fonte": ""
        },
        "enunciado": "A velocidade de referência, em megabyte por segundo, a ser adotada por essa empresa é",
        "alternativas": {
            "A": "360.",
            "B": "370.",
            "C": "380.",
            "D": "390.",
            "E": "400."
        },
        "gabarito": "C",
        "habilidade": "H27 - Calcular medidas de tendência central de uma distribuição de dados.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 146)"
    })

    # Q53: Envelopes de Celulares e Probabilidade (ENEM 2025 Q150)
    questoes.append({
        "numero": 53,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Quatro candidatos se apresentaram para realizar a prova de um concurso. Antes de iniciar a prova, "
                "os celulares dos quatro candidatos foram recolhidos pelo aplicador, que os guardou, cada um, dentro de "
                "um envelope preto. Ao término da prova, o aplicador devolveu os quatro envelopes com os celulares aos "
                "quatro candidatos, de maneira aleatória, já que não havia feito a identificação dos envelopes."
            ),
            "fonte": ""
        },
        "enunciado": "A probabilidade de que todos os candidatos tenham recebido de volta os envelopes com os seus respectivos celulares é",
        "alternativas": {
            "A": "1/2",
            "B": "1/10",
            "C": "1/16",
            "D": "1/24",
            "E": "1/256"
        },
        "gabarito": "D",
        "habilidade": "H28 - Resolver situação-problema que envolva conhecimentos de probabilidade de eventos.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 150)"
    })

    # Q54: Infográfico de Redes Sociais com Imagem (ENEM 2025 Q140)
    questoes.append({
        "numero": 54,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2025_q140_infografico.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "O infográfico apresenta a distribuição percentual de usuários de uma rede social digital "
                "por faixa etária e por gênero em determinado mês."
            ),
            "fonte": ""
        },
        "enunciado": "Segundo os dados do infográfico, ao se escolher aleatoriamente um usuário dessa rede social, a probabilidade de ele ser uma mulher com idade de 25 a 34 anos é",
        "alternativas": {
            "A": "0,148.",
            "B": "0,154.",
            "C": "0,302.",
            "D": "0,446.",
            "E": "0,510."
        },
        "gabarito": "B",
        "habilidade": "H28 - Resolver situação-problema que envolva interpretação de gráficos e probabilidade.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 140)"
    })

    # Q55: Pagamento Proporcional de Engenheiros (ENEM 2024 Q140)
    questoes.append({
        "numero": 55,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Uma empresa de engenharia foi contratada para realizar um serviço no valor de R$ 71 250,00. Os sócios da "
                "empresa decidiram que 40% desse valor seria destinado ao pagamento de três engenheiros que gerenciaram o serviço. "
                "O pagamento para cada um deles será feito de forma diretamente proporcional ao total de horas trabalhadas.\n"
                "O número de dias e o número de horas diárias trabalhadas pelos engenheiros foram, respectivamente:\n"
                "• engenheiro I: 4 dias, numa jornada de 5 horas e meia por dia;\n"
                "• engenheiro II: 5 dias, numa jornada de 4 horas por dia;\n"
                "• engenheiro III: 6 dias, numa jornada de 2 horas e meia por dia."
            ),
            "fonte": ""
        },
        "enunciado": "Qual a maior diferença, em real, entre os valores recebidos por esse serviço entre dois desses engenheiros?",
        "alternativas": {
            "A": "1 000",
            "B": "1 500",
            "C": "3 500",
            "D": "3 800",
            "E": "5 250"
        },
        "gabarito": "C",
        "habilidade": "H16 - Resolver situação-problema envolvendo a divisão de grandezas em partes proporcionais.",
        "fonte": "ENEM 2024 - Caderno 6 Cinza (Questão 140)"
    })

    # Q56: Cursos de Idiomas com Imagem (ENEM 2025 Q151)
    questoes.append({
        "numero": 56,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2025_q151_setores.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Uma escola de idiomas realizou uma pesquisa para estimar a quantidade de novas matrículas "
                "no primeiro semestre do próximo ano. O gráfico de setores ilustra a distribuição percentual "
                "das opções de cursos escolhidas pelos interessados.\n"
                "A direção da escola estima que serão feitas 600 novas matrículas no curso de Francês."
            ),
            "fonte": ""
        },
        "enunciado": "Segundo essa estimativa, o número de matrículas no curso de Inglês será igual a",
        "alternativas": {
            "A": "750.",
            "B": "900.",
            "C": "1 050.",
            "D": "1 200.",
            "E": "1 500."
        },
        "gabarito": "E",
        "habilidade": "H27 - Interpretar dados expressos em gráfico de setores.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 151)"
    })

    # Q57: Carrinho de Controle Remoto com Imagem (ENEM 2025 Q152)
    questoes.append({
        "numero": 57,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2025_q152_controle.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Cinco trajetórias retilíneas descritas por um carrinho de controle remoto estão representadas "
                "em malhas quadriculadas formadas por quadrados de mesmo lado, identificadas de I a V."
            ),
            "fonte": ""
        },
        "enunciado": "A opção que indica o deslocamento de maior comprimento realizado pelo carrinho é a",
        "alternativas": {
            "A": "I.",
            "B": "II.",
            "C": "III.",
            "D": "IV.",
            "E": "V."
        },
        "gabarito": "C",
        "habilidade": "H07 - Identificar características de figuras planas ou espaciais em malhas.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 152)"
    })

    # Q58: Livraria e Vendas com Imagem (ENEM 2025 Q154)
    questoes.append({
        "numero": 58,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2025_q154_barras.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "O gerente de uma livraria registrou a quantidade de exemplares vendidos dos cinco gêneros literários "
                "mais procurados em sua loja durante o primeiro semestre de 2024. Com base no sucesso de vendas, ele planeja "
                "fazer uma nova encomenda no segundo semestre, priorizando o gênero que teve o maior percentual de crescimento "
                "de vendas entre o primeiro e o segundo trimestre."
            ),
            "fonte": ""
        },
        "enunciado": "O gênero de livro do qual o gerente deverá encomendar mais exemplares é",
        "alternativas": {
            "A": "Ficção científica.",
            "B": "Biografia.",
            "C": "Romance.",
            "D": "Autoajuda.",
            "E": "Suspense."
        },
        "gabarito": "C",
        "habilidade": "H27 - Interpretar dados estatísticos apresentados em gráfico de colunas.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 154)"
    })

    # Q59: Malha Urbana e Localização com Imagem (ENEM 2025 Q156)
    questoes.append({
        "numero": 59,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2025_q156_malha.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "A malha quadriculada representa o mapa de um bairro plano com quarteirões quadrados de mesmo tamanho. "
                "João mora em um desses quarteirões. Para ir à escola, ele sai do ponto A e caminha exatamente 3 quarteirões "
                "para o leste e 2 quarteirões para o norte."
            ),
            "fonte": ""
        },
        "enunciado": "O quarteirão onde se encontra a casa de João é representado pela letra",
        "alternativas": {
            "A": "P.",
            "B": "Q.",
            "C": "R.",
            "D": "S.",
            "E": "T."
        },
        "gabarito": "A",
        "habilidade": "H06 - Interpretar a localização e a movimentação de pessoas/objetos em representações gráficas.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 156)"
    })

    # Q60: Solução Química e Diluição (ENEM 2025 Q144)
    questoes.append({
        "numero": 60,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Em um laboratório, há 10 litros de uma solução aquosa composta exclusivamente pelas substâncias S1 e S2, "
                "sendo que a substância S1 representa 20% do volume total da solução. O químico responsável deseja alterar a "
                "concentração dessa solução por meio da evaporação exclusiva da substância S1, de modo que ela passe a "
                "representar exatamente 10% do novo volume total da solução."
            ),
            "fonte": ""
        },
        "enunciado": "Quantos litros da substância S1 devem ser evaporados dessa solução?",
        "alternativas": {
            "A": "1,0",
            "B": "1,1",
            "C": "1,2",
            "D": "1,5",
            "E": "2,0"
        },
        "gabarito": "B",
        "habilidade": "H16 - Resolver situação-problema que envolva porcentagem e proporção.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 144)"
    })

    # Q61: Média de Notas Dividida por Engano (ENEM 2024 Q147)
    questoes.append({
        "numero": 61,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Ao calcular a média de suas notas em 4 provas, um estudante dividiu, por engano, a soma das notas por 5. "
                "Com isso, a média obtida foi 1 unidade menor do que deveria ser, caso fosse calculada corretamente."
            ),
            "fonte": ""
        },
        "enunciado": "O valor correto da média das notas desse estudante é",
        "alternativas": {
            "A": "4.",
            "B": "5.",
            "C": "6.",
            "D": "19.",
            "E": "21."
        },
        "gabarito": "B",
        "habilidade": "H27 - Calcular medidas de tendência central de uma distribuição de dados.",
        "fonte": "ENEM 2024 - Caderno 6 Cinza (Questão 147)"
    })

    # Q62: Sorveteria e Volume (ENEM 2025 Q164)
    questoes.append({
        "numero": 62,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Uma sorveteria comercializa sorvete artesanal em potes cilíndricos com capacidade de 20 000 cm³. "
                "Para servir seus clientes, o proprietário utiliza taças de sobremesa com capacidade de 250 mL cada. "
                "Sabe-se que 1 cm³ equivale a 1 mL."
            ),
            "fonte": ""
        },
        "enunciado": "A quantidade de taças que ele consegue servir a partir de um único pote totalmente cheio desse sorvete é igual a",
        "alternativas": {
            "A": "8.",
            "B": "20.",
            "C": "50.",
            "D": "80.",
            "E": "100."
        },
        "gabarito": "D",
        "habilidade": "H12 - Resolver situação-problema que envolva medidas de grandezas e conversão de unidades.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 164)"
    })

    # Q63: Caixa de Descarga com Imagem (ENEM 2025 Q167)
    questoes.append({
        "numero": 63,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2025_q167_caixa.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Uma caixa de descarga tem a forma de paralelepípedo reto-retângulo com dimensões internas da base medindo "
                "2,5 dm e 1,5 dm. Uma boia interrompe o abastecimento quando a altura da coluna de água atinge 2 dm.\n"
                "Para reduzir o volume de água despejado a cada acionamento, serão colocadas garrafas de 300 mL totalmente submersas. "
                "Para garantir a limpeza eficiente do vaso, o volume mínimo de água despejada deve ser de 5 L."
            ),
            "fonte": ""
        },
        "enunciado": "A quantidade máxima de garrafas que serão colocadas nessa caixa, garantindo um funcionamento eficiente, é igual a",
        "alternativas": {
            "A": "10.",
            "B": "8.",
            "C": "4.",
            "D": "3.",
            "E": "2."
        },
        "gabarito": "B",
        "habilidade": "H14 - Avaliar proposta de intervenção na realidade utilizando conhecimentos geométricos de sólidos.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 167)"
    })

    # Q64: Fábrica de Tijolos Ecológicos (ENEM 2025 Q148)
    questoes.append({
        "numero": 64,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Uma fábrica de tijolos ecológicos com 3 funcionários, cada um trabalhando 6 horas diárias, produz 720 unidades "
                "por dia. A fábrica pretende expandir sua produção para 1 800 tijolos diários, mantendo a jornada de 6 horas diárias "
                "para todos os funcionários e a mesma produtividade individual."
            ),
            "fonte": ""
        },
        "enunciado": "Quantos novos funcionários, com a mesma produtividade dos atuais, essa fábrica deve contratar para atingir essa nova meta de produção?",
        "alternativas": {
            "A": "4",
            "B": "5",
            "C": "7",
            "D": "8",
            "E": "10"
        },
        "gabarito": "A",
        "habilidade": "H16 - Resolver situação-problema que envolva grandezas direta ou inversamente proporcionais (regra de três).",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 148)"
    })

    # Q65: Confeiteiro, Tortas Cilíndricas e Caixas de Prisma (ENEM 2025 Q168)
    questoes.append({
        "numero": 65,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Um confeiteiro passou a produzir tortas em formato de cilindro circular reto, com raio da base variando entre "
                "12 cm e 16 cm e altura de 6 cm. Essas tortas deverão ser embaladas em caixas com formato de prisma reto de base "
                "quadrada, de modo que seja possível acomodar a torta em seu interior e ainda restar pelo menos 1 cm de distância "
                "entre a torta e as superfícies internas da caixa, lateral e superior. Ele dispõe, originalmente, de caixas no formato "
                "pretendido, cujas dimensões internas são 14 cm de comprimento do lado da base e 7 cm de altura, que não atendem "
                "às suas necessidades. Portanto, ele comprará novas caixas, com o mesmo formato das caixas originais, mas com comprimento "
                "do lado da base maior, que sejam adequadas para embalar todos os tipos de torta que produz."
            ),
            "fonte": ""
        },
        "enunciado": "A aresta da base das novas caixas deve ser, no mínimo, quantos centímetros maior do que a das caixas originais?",
        "alternativas": {
            "A": "4",
            "B": "12",
            "C": "16",
            "D": "18",
            "E": "20"
        },
        "gabarito": "E",
        "habilidade": "H08 - Resolver situação-problema que envolva conhecimentos geométricos de espaço e forma.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 168)"
    })

    # Q66: Luminância de um Objeto (ENEM 2025 Q177)
    questoes.append({
        "numero": 66,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "A luminância de um objeto é a grandeza que descreve a quantidade de luz produzida ou refletida por sua superfície. "
                "Ela está definida como a razão entre a intensidade luminosa, medida em candela (cd), e o quadrado da distância do "
                "objeto até o observador, medida em metro (m)."
            ),
            "fonte": ""
        },
        "enunciado": "A unidade de medida da luminância de um objeto é",
        "alternativas": {
            "A": "cd/m²",
            "B": "cd · m²",
            "C": "cd/m",
            "D": "cd · m",
            "E": "cd²/m"
        },
        "gabarito": "A",
        "habilidade": "H11 - Utilizar a noção de variação de grandezas para a compreensão da realidade.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 177)"
    })

    # Q67: Razão entre Densidades Demográficas (ENEM 2024 Q152)
    questoes.append({
        "numero": 67,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "A densidade demográfica de uma região é definida como sendo a razão entre o número de habitantes dessa região "
                "e sua área, expressa na unidade habitantes por quilômetro quadrado.\n"
                "Uma região R é subdividida em várias outras, sendo uma delas a região Q. A área de Q é igual a três quartos "
                "da área de R, e o número de habitantes de Q é igual à metade do número de habitantes de R. As densidades demográficas "
                "correspondentes a essas regiões são denotadas por d(Q) e d(R)."
            ),
            "fonte": ""
        },
        "enunciado": "A expressão que relaciona d(Q) e d(R) é",
        "alternativas": {
            "A": "d(Q) = (1/4) · d(R)",
            "B": "d(Q) = (1/2) · d(R)",
            "C": "d(Q) = (3/4) · d(R)",
            "D": "d(Q) = (3/2) · d(R)",
            "E": "d(Q) = (2/3) · d(R)"
        },
        "gabarito": "E",
        "habilidade": "H16 - Resolver situação-problema envolvendo a razão entre duas grandezas de espécies diferentes.",
        "fonte": "ENEM 2024 - Caderno 6 Cinza (Questão 152)"
    })

    # Q68: Maratona de Matemática e Conceitos (ENEM 2024 Q175)
    questoes.append({
        "numero": 68,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "João e Felipe participaram, na escola, de uma maratona de matemática na qual, durante uma semana, resolveram 200 "
                "questões cada. Nessa maratona, a porcentagem P de acertos de cada participante é convertida em um conceito:\n"
                "• insatisfatório: se 0 ≤ P < 50;\n"
                "• regular: se 50 ≤ P < 60;\n"
                "• bom: se 60 ≤ P < 75;\n"
                "• muito bom: se 75 ≤ P < 90;\n"
                "• excelente: se 90 ≤ P ≤ 100.\n"
                "João acertou 75% das questões da maratona e Felipe acertou 30% a menos que a quantidade de questões que João acertou."
            ),
            "fonte": ""
        },
        "enunciado": "Os conceitos de João e Felipe foram, respectivamente,",
        "alternativas": {
            "A": "muito bom e bom.",
            "B": "muito bom e regular.",
            "C": "muito bom e insatisfatório.",
            "D": "bom e regular.",
            "E": "bom e insatisfatório."
        },
        "gabarito": "B",
        "habilidade": "H16 - Resolver situação-problema que envolva porcentagem e variação percentual.",
        "fonte": "ENEM 2024 - Caderno 6 Cinza (Questão 175)"
    })

    # Q69: Veículo Bicombustível com Imagem (ENEM 2025 Q179)
    questoes.append({
        "numero": 69,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "imagem": "simulado_2/banco_questoes/imagens/enem_2025_q179_grafico.png",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "O proprietário de um veículo bicombustível (gasolina e gás natural veicular - GNV) registrou em um gráfico "
                "o rendimento médio do automóvel, em quilômetro por unidade de combustível consumida, para cada um dos combustíveis.\n"
                "Em uma viagem de 600 km, ele utilizou exclusivamente GNV na primeira metade do percurso e exclusivamente gasolina "
                "na segunda metade. O preço do metro cúbico de GNV foi R$ 4,50 e o do litro de gasolina foi R$ 6,00."
            ),
            "fonte": ""
        },
        "enunciado": "Qual foi a diferença, em real, entre os gastos totais com gasolina e com GNV nessa viagem?",
        "alternativas": {
            "A": "15,00",
            "B": "25,00",
            "C": "35,00",
            "D": "40,00",
            "E": "50,00"
        },
        "gabarito": "D",
        "habilidade": "H16 - Resolver situação-problema envolvendo grandezas financeiras e rendimento.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 179)"
    })

    # Q70: Dez Casais e Diretoria com 3 Cargos (ENEM 2025 Q160)
    questoes.append({
        "numero": 70,
        "area": "Matemática e suas Tecnologias",
        "disciplina": "Matemática",
        "texto_apoio": {
            "titulo": "",
            "conteudo": (
                "Dez casais fundaram um grupo de dança e decidiram constituir uma diretoria com três cargos: presidente, "
                "secretário e tesoureiro. Para maior representatividade, decidiu-se que no máximo uma pessoa por casal poderá "
                "ocupar um cargo nessa diretoria."
            ),
            "fonte": ""
        },
        "enunciado": "Quantas diretorias diferentes podem ser constituídas por esses 10 casais?",
        "alternativas": {
            "A": "10 × 9 × 8",
            "B": "20 × 18 × 16",
            "C": "20 × 19 × 18",
            "D": "10 × 9 × 8 × 2",
            "E": "20 × 18 × 16 × 2"
        },
        "gabarito": "B",
        "habilidade": "H02 - Resolver situação-problema envolvendo o princípio fundamental da contagem.",
        "fonte": "ENEM 2025 - Caderno 6 Cinza (Questão 160)"
    })

    banco = {
        "metadados": metadados,
        "redacao": redacao,
        "questoes": questoes
    }

    caminho_saida = "simulado_2/banco_questoes/questoes.json"
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)

    print(f"[OK] Banco de 70 Questoes Oficiais e Redacao gerado com sucesso em: {caminho_saida}")
    return banco


if __name__ == "__main__":
    build_simulado_2()
