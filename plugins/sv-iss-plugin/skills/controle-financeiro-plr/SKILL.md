---
name: "controle-financeiro-plr"
description: "Mantém e evolui o artefato ao vivo do Cowork \"Controle Financeiro 2026 + Rateio PLR\" (artifact id `controle-financeiro-2026-trello`), que lê/escreve no quadro Trello \"Controle Financeiro 2026\" e guarda comprovantes, envolvimento por processo e config do rateio PLR trimestral dos CLT em window.storage. Use sempre que o usuário pedir para editar, corrigir, adicionar funcionalidade, ajustar a fórmula do rateio PLR, ou mudar o CÓDIGO/COMPORTAMENTO desse artefato — mesmo sem citar o nome exato, só descrevendo \"o painel financeiro\", \"o rateio dos advogados CLT\" ou similar. NÃO use (explique que não precisa) quando o pedido for só lançar um dado do dia a dia — colaborador, salário, envolvimento, trimestre, comprovante — isso é feito na tela do artefato, não editando código."
---

# Sistema: Controle Financeiro 2026 + Rateio PLR (Suttile & Vaciski)

Este artefato ao vivo do Cowork (id `controle-financeiro-2026-trello`) tem duas partes: (1) um painel de lançamentos financeiros que lê e escreve cartões num quadro Trello, e (2) uma calculadora de rateio de PLR trimestral para os colaboradores CLT do escritório. Comprovantes, envolvimento por processo e a configuração do rateio ficam salvos no `window.storage` do próprio artefato (não no Trello).

## Regra mais importante: dado vs código

Antes de tocar em qualquer coisa, decida qual é o pedido:

- **É um DADO do dia a dia?** ("adiciona a Fulana como colaboradora", "lança o envolvimento do Pedro nesse processo", "muda o salário da Isabela", "seleciona o trimestre X", "anexa esse comprovante") — isso mora em `window.storage`, **dentro do navegador do usuário**. Você não tem acesso a esse storage fora da sessão do navegador dele. A ação certa é orientar o usuário a fazer isso na própria tela do artefato (botão "+ Adicionar colaborador", campo de salário, seletor "Processo", etc.) — não editar o HTML nem chamar `update_artifact`.
- **É uma mudança de COMPORTAMENTO/CÓDIGO?** ("muda a fórmula do rateio", "adiciona uma coluna", "corrige esse texto", "cria uma aba nova", "o botão X não está funcionando") — aí sim siga o fluxo de edição abaixo.

Isso importa porque o array `DEFAULT_COLABORADORES` no código só é usado como valor inicial quando `window.storage.get('plr-colaboradores')` vem vazio (artefato nunca configurado). Num artefato que já está em uso — como este está, desde agosto/2026 — editar esse array e republicar **não muda nada para o usuário**, porque o storage já tem dados salvos que sobrescrevem o default. Já vi isso acontecer num teste: pareceu um edit válido, mas era um no-op. Se o pedido for de dado, é só explicar isso e apontar pro campo certo na tela.

## Como localizar e editar o artefato (mudanças de código)

1. Chame `mcp__cowork__list_artifacts` e ache a entrada com id `controle-financeiro-2026-trello`. Ela traz um `path`.
2. Leia esse `path` com Read para ver o HTML completo atual — **edite o que já existe, não recrie do zero**. O arquivo pode ter uma tag extra `<script type="application/json" id="cowork-artifact-meta">` injetada pelo Cowork (metadados) — ignore-a, o código do app está na tag `<script>` sem atributos.
3. Copie o conteúdo pra um arquivo de trabalho no seu diretório de outputs/scratch (ex: `controle-financeiro-2026-trello-workcopy.html`) e aplique as mudanças ali com Edit.
4. Valide antes de publicar:
   - Sintaxe JS — extraia só a tag `<script>` sem atributos (não a de metadados) e rode `node --check`:
     ```python
     import re
     html = open('workcopy.html', encoding='utf-8').read()
     m = re.search(r'<script>(.*)</script>', html, re.S)
     open('/tmp/script.js', 'w', encoding='utf-8').write(m.group(1))
     ```
     depois `node --check /tmp/script.js`.
   - IDs — confira que todo `document.getElementById('X')` tem um `id="X"` correspondente no HTML. Um grep simples encontra a maioria, mas ids montados dinamicamente (ex: `'tab-' + variavel`) não batem por string — não trate isso como erro, seria falso positivo.
   - Para mudanças que alteram comportamento de verdade (fórmula, filtros, sincronização entre tabelas), vale simular a execução com jsdom antes de publicar: carregue o HTML com `runScripts:'dangerously'`, forneça mocks de `window.cowork.callMcpTool` (retornando `{content:[{text: JSON.stringify(...)}], isError:false}` no formato de cada ferramenta do Trello) e `window.storage` (um objeto em memória com get/set/delete/list assíncronos), dispare os eventos que o usuário dispararia, e leia o DOM resultante. Isso pegou bugs reais durante o desenvolvimento deste artefato que `node --check` sozinho não pegaria.
5. Só depois de validar, chame `mcp__cowork__update_artifact` com `id: "controle-financeiro-2026-trello"`, o caminho do HTML atualizado, e um `update_summary` curto e específico (o usuário vê esse texto).

## O quadro Trello

- Board "Controle Financeiro 2026": `https://trello.com/b/c4YT62GE/controle-financeiro-2026`
- Board ARI: `ari:cloud:trello::board/workspace/6724d1ea41ac10d20d916a36/69446f2e44e37d0068c083d2`
- Workspace ARI: `ari:cloud:trello::workspace/6724d1ea41ac10d20d916a36`
- Listas = meses do ano (capitalização inconsistente: "Janeiro", "FEVEREIRO", "MARÇO"...; há uma lista híbrida "Janeiro/Fevereiro"), mais uma lista "Valores para Liberar" que não é mês — não assuma que toda lista é um mês.
- Cada cartão = um lançamento (recebimento de um caso/cliente). `dueComplete` do cartão: `true` = Recebido, `false` = Pendente.
- Prefixo das ferramentas Trello nesta conexão: `mcp__9c7c3235-79b1-4718-ba0c-21a7f7b10c83__` (ex: `trelloReadCard`, `trelloReadList`, `trelloWriteCard`, `trelloWriteList`). Esse prefixo é o ID do conector MCP e pode mudar se o usuário reconectar o Trello — se as chamadas falharem com "tool not found", procure (`ToolSearch` ou liste ferramentas disponíveis) o nome atual antes de editar o artefato, e atualize as constantes no início do `<script>` (`READ_CARD_TOOL`, `READ_LIST_TOOL`, `WRITE_CARD_TOOL`, `WRITE_LIST_TOOL`) e a lista `mcp_tools` passada em `update_artifact`.
- Ao ler cartões (`trelloReadCard`, `action: "list_by_board"`), a resposta real observada é `{"cards":{"nodes":[...], "pageInfo":{"hasNextPage":bool,"endCursor":str}}}` — não a forma agrupada por lista que a descrição da ferramenta sugere.
- Ao criar lista (`trelloWriteList`, `action: "create"`), a resposta é achatada: `{"listId":..., "name":..., "boardId":..., "position":...}` (diferente da forma de card, que é `{"cards":{"nodes":[...]}}`).

## Onde fica o que (e o que nunca vai para o GitHub)

O código deste artefato (a versão publicada via `update_artifact`) é o que sincroniza com o
repositório GitHub `SV-plugins`, junto com o `SKILL.md`. **Dados financeiros/pessoais nunca vão
para esse repositório**: comprovantes, envolvimento por processo, salários e configuração do
rateio ficam só no `window.storage` do navegador do usuário (não são arquivos, não saem daí) e
os lançamentos ficam só no Trello — nenhum dos dois é commitado em lugar nenhum.

## Convenção de nome dos cartões (lançamentos)

Texto livre, mas majoritariamente: `Cliente - [Tipo/observação -] R$ Valor [(parcela X/Y)] [- Ficha NNN]`. A ordem de "Ficha" e "R$" pode inverter em alguns cartões antigos. Exemplos reais: `"Reinaldo - Criminal - R$ 1.500,00"`, `"Austin - R$ 1.750,00 - Ficha 31758"`, `"LCT - FICHA 10576 - R$ 29.536,00"`, `"Max Alves - R$ 5.000,00 (parcela 1/4) - Ficha 32943.01"`. Alguns cartões não têm valor nenhum (ex: `"Welt Sports"`, `"ALC"`) — trate como "sem valor" na UI, nunca invente um número. A função `parseCardName` no artefato já implementa esse parser; se for alterar a lógica de nomes, mexa ali (é best-effort, não tente deixar 100% robusto para todo caso possível).

## Dados em window.storage (não estão no Trello, e não são visíveis para você fora do navegador do usuário)

| Chave | Conteúdo |
|---|---|
| `anexo-<chave>` | JSON `{name, type, dataUrl}` — comprovante de um lançamento |
| `atuacao-<chave>` | JSON `{ [colaboradorId]: envolvimento }` — envolvimento (0 a 5) de cada colaborador CLT naquele processo específico |
| `plr-colaboradores` | array `{id, nome, salario, admissao (YYYY-MM-DD), envolvimento}` — o campo `envolvimento` do objeto é legado/não lido pela fórmula atual, ignore-o |
| `plr-pesos` | `{salario, tempo, envolvimento}` — pesos da fórmula (padrão 10, 1000, 10000) |
| `plr-trimestre` | texto do trimestre selecionado (ex: "3º Trimestre 2026") |
| `plr-historico` | array de trimestres salvos: `{trimestre, savedAt, resultados:[{nome, percentual}]}` |

`<chave>` = id do cartão Trello com todo caractere não-alfanumérico trocado por `_` (função `safeKey`).

Colaboradores padrão (usados só se `plr-colaboradores` vier vazio — artefato nunca configurado): Pedro Fraro (salário 4000, admissão 2023-08-01), Larissa (4590, 2025-02-01), Isabela (5882.5, 2022-11-01), Pedro Poli (3500, 2023-09-01), Marcelo Paz (4000, 2026-02-01).

## Fórmula do Rateio PLR

Para cada colaborador, no trimestre selecionado no campo "Trimestre":

1. `EnvolvimentoTotal` = soma de `atuacao-<cartão>[colaboradorId]` de todos os cartões cujo mês pertence ao trimestre (Q1=Jan/Fev/Mar, Q2=Abr/Mai/Jun, Q3=Jul/Ago/Set, Q4=Out/Nov/Dez; listas híbridas tipo "Janeiro/Fevereiro" contam se qualquer um dos meses do nome bater com o trimestre — função `entryMatchesQuarter`).
2. `TempoDeCasa` (anos) = (hoje − data de admissão) / 365.
3. `Pontuação` = 0 se `EnvolvimentoTotal` for 0; senão `Salário × pesoSalario + TempoDeCasa × pesoTempo + EnvolvimentoTotal × pesoEnvolvimento`.
4. `Percentual` = `Pontuação` da pessoa ÷ soma da `Pontuação` de todos. **Esse é o número que o usuário repassa ao financeiro do escritório para o pagamento.**

O envolvimento é lançado **processo a processo**, não como um número agregado manual — o usuário escolhe um "Processo" no seletor da aba PLR e informa o envolvimento (0-5) de cada colaborador naquele processo específico; a soma automática por colaborador/trimestre é o que entra na fórmula. A tabela "Detalhamento por processo" é só leitura (mostra o Percentual final repetido por linha, para exportar/demonstrar ao financeiro) — não tem mais campos de envolvimento editáveis nela; se o usuário quiser lançar envolvimento, é no seletor "Processo" da tabela de Rateio PLR, não ali.

Se o usuário pedir para mudar a fórmula (ex: usar média em vez de soma, ou pesos diferentes), implemente exatamente o que ele descrever — não assuma que "soma" é definitivo, foi uma escolha feita sob incerteza e pode mudar.

## Convenções de estilo já em uso (mantenha ao adicionar coisas novas)

- Paleta: `--paper` (fundo), `--navy` (título/destaque), `--gold`/`--gold-soft` (destaque de percentual/CTA), `--received`/`--pending` (verde/terracota para status).
- `:root { color-scheme: light }` é obrigatório (regra do `create_artifact`/`update_artifact` do Cowork).
- Tabelas grandes ficam dentro de `<div class="table-scroll">` (overflow-x) porque o número de colunas de colaboradores é dinâmico.
- Toda alteração que grava em `window.storage` deve re-renderizar as views que dependem daquele dado (ex: mudar um envolvimento precisa atualizar a tabela de Rateio PLR, o Detalhamento por processo, e a aba Lançamentos, já que compartilham o mesmo `atuacaoData`). Procure as funções `render()`, `plrRenderTable()`, `plrRenderDetalhamento()`, `plrRenderProcessoFields()` e chame as que forem afetadas — é fácil esquecer uma e deixar uma view desatualizada.
- Nunca use `localStorage`/`sessionStorage` — use `window.storage` (API própria do Cowork, assíncrona: `get(key, false)`, `set(key, value, false)`, `delete(key, false)`, `list(prefixo, false)`).

