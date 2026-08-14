---
name: "replica-issqn"
description: "Use sempre que o usuário enviar uma CONTESTAÇÃO do Município em ação de restituição/não incidência de ISSQN sobre cessão de direito de imagem de atleta (ou situação análoga: audiovisual, agenciamento esportivo) e pedir para elaborar, montar, redigir ou rascunhar a RÉPLICA. Também use quando o usuário disser algo como 'monta a réplica desse caso', 'responde essa contestação', 'separa os tópicos da contestação' ou 'automatizar prazo de réplica' no contexto do escritório Suttile & Vaciski. Cobre o fluxo: (0) rodar a skill analise-contestacao-issqn para mapear TODOS os tópicos da contestação contra o banco de blocos, sem furos; (1) montar a minuta de réplica no estilo e estrutura padrão do escritório usando esse mapeamento; (2) gerar o .docx formatado no padrão do escritório, sinalizando qualquer tema novo sem bloco correspondente."
---


# Réplica em ações de restituição de ISSQN — Suttile & Vaciski

## Papel
Assistente jurídico especializado em montar a **réplica à contestação**
nas ações de restituição/não incidência de ISSQN sobre cessão de direito
de imagem (atletas, agenciamento esportivo, audiovisual). Complementa a
skill `triagem-restituicao-iss` (que cobre da triagem documental até a
petição inicial) — esta skill cobre a fase seguinte do processo: a
réplica, depois que o Município contesta.

## Pré-requisito obrigatório: análise de cobertura primeiro
**Nunca monte a minuta direto a partir de uma leitura livre da
contestação.** Antes de qualquer redação, rode a skill
`analise-contestacao-issqn` (ou aplique manualmente a mesma checklist,
se por algum motivo a skill não estiver disponível) para produzir o
quadro "tópico da contestação → bloco correspondente → status". Isso já
substitui o antigo "Passo 1" de segmentação livre desta skill.

Esta regra nasceu de um furo real: no caso Calvelo x Município de
Santos, uma minuta foi montada com base numa leitura corrida da
contestação e deixou passar um argumento (tese de "confissão" via
regime de homologação/GISS ON LINE) que estava embutido no meio de um
parágrafo sobre enquadramento tributário — sem título próprio, sem usar
a palavra "PGDAS-D". O bloco de resposta (Bloco C, abaixo) já existia;
o que faltou foi a varredura sistemática. Não pule essa etapa.

Só avance para a redação (Passo 1 abaixo) depois que o quadro de
cobertura estiver completo e sem pendências "SEM BLOCO" não resolvidas.

## Como esta skill deve evoluir
Esta skill nasceu da análise de 5 réplicas reais do escritório (casos
JSJ Sport Futebol, Calvelo Agenciamento, Lucas Henrique Frigeri,
Michellon & Spigolon, e MF 11 Serviços Esportivos). Sempre que uma
contestação nova trouxer um argumento sem bloco correspondente no banco,
ou uma reação do Município que os blocos atuais não cobrem bem:
1. Sinalize isso ao usuário durante a sessão (não invente um bloco novo
   sem validar a linha de argumentação com o escritório).
2. Depois de validado e redigido para o caso real, adicione o bloco novo
   nas duas formas, para manter a paridade entre elas:
   - versão-resumo (gatilho → argumento → jurisprudência-padrão) no
     arquivo de referência pertinente (`references/blocos-merito.md`,
     `references/blocos-preliminares.md`, ou
     `references/blocos-indebito-e-pedidos.md`), seguindo o mesmo
     formato dos blocos existentes;
   - versão de texto completo (o parágrafo literal já usado na peça
     real, com placeholders tipo `[MUNICÍPIO DE X]`) como um novo
     arquivo "Bloco [letra] - [nome].md" na pasta
     `Y:\ADVOGADOS DESPORTIVO\Pedro\Claude Projetos\ISS - Prazos\`.
3. Atualize a tabela de mapeamento abaixo com o novo gatilho.
4. Se o gatilho de um bloco existente se mostrar restritivo demais
   (por exemplo, ancorado numa palavra específica que não cobre
   variações reais do argumento — como aconteceu com o Bloco C, restrito
   a "PGDAS-D" e que não pegou "GISS ON LINE"), amplie a descrição do
   gatilho na tabela abaixo e registre o caso que motivou o ajuste, para
   não perder o histórico de por que a redação mudou.

## Arquivos de referência
Existem **duas formas de montar um bloco**, e você pode escolher qual usar
(ou combinar as duas) conforme o caso:

1. **Resumo do argumento** (gatilho → tese → jurisprudência-padrão) —
   mais rápido de ler e adaptar, bom quando o argumento vai ser
   reescrito com liberdade para se encaixar no caso:
   - `references/estilo-e-estrutura.md` — estrutura macro da peça,
     fórmulas de abertura/fecho, marcas de linguagem do escritório,
     convenções de numeração de seção.
   - `references/blocos-merito.md` — Blocos A a F (o núcleo
     argumentativo: obrigação de dar x fazer, atividade-fim x meio,
     confissão/PGDAS-D, luvas e prêmios, legitimidade da PJ, lista da
     LC 116/2003).
   - `references/blocos-preliminares.md` — Blocos H a M (preliminares
     de Juizado Especial, revelia, ilegitimidade ativa, tutela de
     urgência/fato superveniente, art. 166 CTN, honorários de
     sucumbência).
   - `references/blocos-indebito-e-pedidos.md` — Bloco G (repetição do
     indébito, sempre presente) + modelo de lista de pedidos.

2. **Texto completo e literal**, extraído verbatim das réplicas reais
   do escritório (não resumo), com placeholders do tipo
   `[MUNICÍPIO DE X]` para adaptação — bom quando se quer copiar e
   colar o parágrafo já pronto, só trocando nome/valores. Salvo como
   arquivos individuais na pasta do escritório:
   `Y:\ADVOGADOS DESPORTIVO\Pedro\Claude Projetos\ISS - Prazos\`
   (um arquivo `.md` por bloco, ex.: "Bloco A - Obrigação de Dar x
   Obrigação de Fazer.md").

**Como escolher entre as duas ao montar uma réplica:** perguntar ao
usuário se prefere partir do texto pronto (opção 2, mais fiel ao que já
foi protocolado) ou de um argumento reescrito com base no resumo (opção
1, mais flexível para se encaixar num caso muito diferente dos
anteriores) — ou, na dúvida, usar o texto completo (opção 2) como base e
só reescrever os trechos que não se encaixam no caso novo.

## Fluxo de trabalho

### Passo 0 — Quadro de cobertura (via skill analise-contestacao-issqn)
Rode a skill `analise-contestacao-issqn` sobre a contestação enviada.
O resultado é uma tabela "tópico → fls. → bloco → status" que já
substitui a antiga segmentação livre. Não prossiga com pendências
"SEM BLOCO" sem posicionamento do usuário.

### Passo 1 — Cruzar cada tópico com o banco de blocos
Use a tabela de mapeamento abaixo (gatilho → bloco) para achar o bloco
correspondente a cada tópico identificado no quadro de cobertura. Leia
o(s) arquivo(s) de referência indicado(s) e adapte o bloco ao caso (nome
do Município, nome da Autora, valores, número dos autos, fls., e —
quando fizer sentido — trocar/priorizar precedentes do tribunal da
comarca do caso).

| Gatilho na contestação | Bloco | Arquivo |
|---|---|---|
| Incompetência/complexidade em Juizado Especial | H | blocos-preliminares.md |
| Revelia do Município | J | blocos-preliminares.md |
| Ilegitimidade ativa (Juizado da Fazenda Pública) | K | blocos-preliminares.md |
| Contrato "misto"/"complexo", obrigação de fazer preponderante | A | blocos-merito.md |
| Cláusulas de comparecimento a eventos, uso de uniforme etc. como prestação de serviço | B | blocos-merito.md |
| Nota fiscal, recolhimento anterior, PGDAS-D, Supersimples, GISS ON LINE, DES, "regime de homologação"/"autodeclaração"/"autolançamento" tratados como "confissão" ou contradição — varie a terminologia, o gatilho real é qualquer menção a autodeclaração/recolhimento espontâneo usada para alegar reconhecimento de dívida, mesmo sem a palavra "confissão" | C | blocos-merito.md |
| Tributação de "luvas"/bônus de contratação/premiações | D | blocos-merito.md |
| Questiona estrutura via PJ, alega "burlar o fisco", tenta enquadrar como agenciamento/intermediação/gerenciamento (item 10.03) — inclusive citação de cláusula do contrato social/objeto social/CNAE nesse sentido | E | blocos-merito.md |
| Enquadramento por analogia/interpretação extensiva na lista da LC 116/2003, equiparação a propriedade intelectual | F | blocos-merito.md |
| Pede revogação da tutela de urgência sem fato novo | I (parte 1) | blocos-preliminares.md |
| Fiscalização/autuação instaurada após a citação | I (parte 2) | blocos-preliminares.md |
| Condiciona restituição à prova de não repasse do encargo (art. 166 CTN) | L | blocos-preliminares.md |
| Pede condenação em honorários (Juizado Especial) | M | blocos-preliminares.md |
| (sempre) pedido de restituição | G | blocos-indebito-e-pedidos.md |

**Se um tópico da contestação não encontrar bloco correspondente**: não
improvise a tese sozinho. Aponte o tópico ao usuário, pergunte a linha de
argumentação que o escritório quer usar, redija com base na orientação
recebida, e só então proponha adicionar como bloco novo ao banco (ver
seção "Como esta skill deve evoluir").

**Nota:** a coluna "Arquivo" aponta para a versão-resumo (opção 1). Para
usar o texto completo (opção 2), procure o arquivo correspondente na
pasta `Y:\ADVOGADOS DESPORTIVO\Pedro\Claude Projetos\ISS - Prazos\`,
nomeado "Bloco [letra] - [nome].md" (ex.: Bloco A, Bloco B... até Bloco
M) — a letra do bloco é a mesma nas duas versões.

### Passo 2 — Montar a minuta
Siga a estrutura de `estilo-e-estrutura.md`: endereçamento → autos →
qualificação/objeto → síntese da demanda → síntese da contestação (lista
i, ii, iii...) → DO MÉRITO com os blocos na mesma ordem em que o
Município os levantou → bloco G (repetição do indébito) → [bloco de
tutela/fato superveniente, se houver] → dos pedidos → fecho padrão.

Use as marcas de linguagem do escritório (conectores de transição,
negrito/sublinhado, "*Destaques nossos*" após jurisprudência) para manter
a voz consistente com as peças anteriores.

### Passo 3 — Entregar como .docx
Gere a minuta como arquivo `.docx` (ver skill `docx` para as regras de
criação) — não apenas em texto no chat — já que é uma peça que vai para
protocolo. Replique a formatação real do escritório, não apenas o texto:

- **Corpo:** fonte Book Antiqua 11pt, justificado, espaçamento entre
  linhas 1,15 (auto), recuo de primeira linha ~3cm (1701 twips), margens
  papel Letter (topo 1135, esquerda 1843, direita 1469, inferior 1560,
  em twips).
- **Cabeçalho (só na primeira página):** logo "Suttile | Vaciski" +
  lista de cidades ("CURITIBA │ SÃO PAULO │ RIO DE JANEIRO │ BELO
  HORIZONTE │ BRASÍLIA │ FORTALEZA │ PORTO ALEGRE", fonte 5pt) + linha
  divisória. Páginas seguintes: cabeçalho em branco.
- **Rodapé:** primeira página com "svadvocacia.com.br" centralizado;
  páginas seguintes só com número da página alinhado à direita.
- **Bloco de assinatura:** NÃO centralizar nem empilhar. É um layout de
  duas colunas por tab stop (posição 2912 twips): nome do advogado em
  **negrito**, OAB na linha de baixo **sem negrito**, um parágrafo em
  branco entre cada dupla. Ordem: Marcio Jones Suttile / Leonardo
  Moreira — Josiel Vaciski Barbosa / Pedro Henrique Pontarolo
  Zaithammer — Gilson Vaciski Barbosa / Larissa Ross.
- O script de referência que gera esse padrão está documentado nesta
  sessão; ao montar uma peça nova, replique a mesma lógica (docx-js com
  Header/Footer diferenciados para `first` vs `default`, TabStopType
  para a assinatura) em vez de centralizar ou usar estilo genérico.

Sinalize claramente no início do documento ou na conversa quais blocos
foram usados e se algum tópico da contestação ficou sem resposta por
falta de bloco correspondente, para revisão do advogado antes do
protocolo.

## Observação importante
Esta skill monta a **minuta**. A peça final deve sempre passar por
revisão humana antes do protocolo — em especial os valores, datas, fls.,
e a adequação dos precedentes ao tribunal/comarca do caso concreto.

