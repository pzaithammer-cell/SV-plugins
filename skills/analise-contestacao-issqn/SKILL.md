---
name: "analise-contestacao-issqn"
description: "Use sempre que o usuário enviar/anexar uma CONTESTAÇÃO do Município em ação de restituição/não incidência de ISSQN sobre cessão de direito de imagem (atleta, audiovisual, agenciamento esportivo) — mesmo sem pedido explícito de \"análise\", trate o upload de uma contestação nesse contexto como gatilho automático. Também use quando o usuário pedir \"analisa essa contestação\", \"verifica se cobrimos tudo\", \"faz uma auditoria da contestação\", \"separa os tópicos da contestação\" ou similar. Esta skill deve rodar SEMPRE antes de qualquer minuta de réplica ser montada (inclusive antes da skill replica-issqn) — não pule direto para a redação sem esse mapeamento de cobertura."
---


# Análise completa de contestação — ações de restituição de ISSQN (Suttile & Vaciski)

## Por que esta skill existe
Nasceu de um furo real: numa contestação do Município de Santos (caso
Calvelo), o argumento de que "a emissão de notas fiscais/o recolhimento
pelo regime de homologação (GISS ON LINE) configuraria confissão da
dívida" apareceu embutido no meio de um parágrafo sobre enquadramento
tributário, sem título ou seção própria, sem usar a palavra "PGDAS-D".
Uma leitura "por tópicos com título" da contestação passou direto por
esse argumento. O bloco de resposta padrão já existia no banco da skill
`replica-issqn` (Bloco C) — o problema não foi falta de bloco, foi falta
de uma varredura exaustiva e sistemática da contestação inteira, frase a
frase, contra a lista completa de gatilhos conhecidos.

Esta skill existe para that não se repita: ela obriga uma leitura
completa, parágrafo a parágrafo, e um cruzamento explícito contra **todos**
os gatilhos conhecidos antes de qualquer minuta ser escrita.

## Regra de ouro
Nunca leia a contestação "por tópicos que pulam aos olhos" (títulos,
negrito, capítulos numerados pelo próprio Município). Argumentos
relevantes frequentemente aparecem escondidos dentro de parágrafos sobre
outro assunto (regime tributário, histórico do contrato, etc.), sem
destaque visual. A única leitura segura é sequencial e completa, do
início ao fim do documento, sem pular nenhum parágrafo.

## Passo 1 — Leitura sequencial completa
Extraia o texto integral da contestação (PDF ou DOCX). Leia parágrafo por
parágrafo, na ordem em que aparecem, do início ao fim — inclusive
parágrafos de contexto/histórico que parecem só narrativos. Para cada
parágrafo, pergunte: "este parágrafo contém, mesmo que de forma
subordinada ou implícita, uma alegação de fato ou uma tese jurídica que
precisa de resposta na réplica?" Se sim, registre:
- número da fls. ou página;
- transcrição literal (ou paráfrase fiel) do trecho;
- classificação preliminar: preliminar processual ou mérito.

Não descarte um argumento por parecer secundário, redundante ou
"só uma observação de passagem" — é exatamente esse tipo de trecho que
já escapou uma vez.

## Passo 2 — Checklist obrigatório contra os gatilhos conhecidos
Depois da leitura livre do Passo 1, faça uma segunda varredura, desta vez
dirigida: percorra cada um dos gatilhos abaixo (banco de blocos da skill
`replica-issqn`) e responda explicitamente SIM/NÃO se a contestação toca
nesse ponto, mesmo que de forma indireta ou com terminologia diferente da
descrita aqui. Esta etapa existe justamente para pegar o que a leitura
livre pode ter deixado passar.

| Bloco | Gatilho (varie a terminologia — não procure só a palavra exata) |
|---|---|
| A — Obrigação de dar x fazer | Contrato é chamado de "misto"/"complexo"; alega-se que a prestação de serviço (fazer) é o elemento preponderante ou principal do negócio. |
| B — Atividade-fim x atividade-meio | Município cita cláusulas específicas (comparecimento a eventos, sessão de fotos, uso de uniforme, presença em ações promocionais) para caracterizar prestação de serviço. |
| C — Tese de "confissão" | Qualquer menção a: nota fiscal, recolhimento espontâneo, PGDAS-D, Supersimples, GISS ON LINE, DES, "regime de homologação", "autodeclaração", "autolançamento", guias geradas pelo próprio contribuinte — mesmo sem a palavra "confissão" aparecer explicitamente. Esse é o gatilho que já escapou uma vez — checar com atenção redobrada, inclusive em parágrafos que parecem só descrever o histórico do enquadramento tributário do contribuinte. |
| D — "Luvas"/prêmios | Tributação de bônus de contratação, "luvas", premiações, valores condicionados a resultado esportivo. |
| E — Legitimidade da PJ / agenciamento | Questionamento da estrutura via pessoa jurídica constituída pelo atleta; menção a "burlar o fisco"/planejamento tributário abusivo; tentativa de enquadrar como "agenciamento", "intermediação", "gerenciamento" (inclusive citação literal de cláusula do contrato social/objeto social/CNAE nesse sentido) — item 10.03 da LC 116/2003. |
| F — Lista da LC 116/2003 / propriedade intelectual | Enquadramento por interpretação extensiva em item da lista (3.02, 10.03, 17.06...); equiparação a propriedade intelectual, marca, obra artística/literária, "bem intangível". |
| H — Incompetência/complexidade em Juizado Especial | Alegação de que a causa é complexa demais para o juizado, necessidade de perícia, etc. |
| I — Tutela de urgência/fato superveniente | Pedido de revogação de tutela concedida; menção a fiscalização/autuação após a citação. |
| J — Revelia do Município | Alegação sobre tempestividade da contestação, ou ausência de efeitos da revelia contra a Fazenda Pública. |
| K — Ilegitimidade ativa | Questionamento de quem é a parte legítima para pleitear (atleta pessoa física x PJ), competência do juízo. |
| L — Art. 166 CTN | Condiciona a restituição à prova de que o encargo não foi repassado a terceiro. |
| M — Honorários (Juizado) | Pedido de condenação em honorários quando a via processual é Juizado Especial da Fazenda Pública (onde normalmente não cabe). |
| G — Repetição do indébito | Sempre presente de alguma forma — mapear o valor, período e fundamento que o Município usa para discutir a restituição (mesmo que só para negar). |

Se a contestação trouxer um argumento que não se encaixa em nenhum
gatilho acima, mesmo depois dessa checagem cuidadosa, ele é candidato a
**bloco novo**: não redija a resposta sozinho — sinalize ao usuário,
pergunte a linha de argumentação que o escritório quer adotar, e só
depois de validado sugira adicionar como bloco novo ao banco da skill
`replica-issqn`.

## Passo 3 — Entregar o quadro de cobertura antes de qualquer minuta
Ao final dos Passos 1 e 2, monte e apresente ao usuário uma tabela única,
nesta ordem (é a mesma lista, agora consolidada e cruzada):

| # | Fls./trecho | Tópico (preliminar ou mérito) | Bloco correspondente | Status |
|---|---|---|---|---|
| 1 | fls. XXX | descrição curta | A / B / C ... / SEM BLOCO | Coberto / Requer validação |

Regras para essa entrega:
- Liste TODOS os tópicos identificados nos Passos 1 e 2, mesmo os que
  pareçam menores ou repetitivos — a decisão de agrupar ou não é do
  usuário, não sua.
- Todo item "SEM BLOCO" precisa aparecer destacado no topo ou em negrito,
  como pendência que bloqueia a redação da réplica até validação.
- Não avance para redigir a minuta (skill `replica-issqn`) enquanto
  houver item "SEM BLOCO" sem posicionamento do usuário — pergunte
  explicitamente se ele quer validar a tese agora ou seguir sem cobrir
  aquele ponto (deixando registrado que foi uma decisão consciente, não
  um esquecimento).

## Passo 4 — Handoff para a redação
Só depois do quadro aprovado (ou com as pendências explicitamente
assumidas pelo usuário), prossiga para a skill `replica-issqn` para
montar a minuta, usando este quadro como o mapeamento tópico → bloco já
pronto (substitui a segmentação livre do Passo 1 daquela skill).

## Observação importante
Esta skill só analisa e mapeia — não redige a réplica. A redação e a
formatação final do `.docx` são responsabilidade da skill `replica-issqn`.
Se o usuário pedir a réplica direto (sem pedir "análise" explicitamente),
rode esta análise primeiro mesmo assim, de forma transparente ("primeiro
vou mapear todos os argumentos da contestação contra o banco de blocos,
depois monto a minuta"), e só então monte a minuta.

