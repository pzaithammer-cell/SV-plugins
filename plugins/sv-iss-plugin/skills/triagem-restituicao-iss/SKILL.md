---
name: "triagem-restituicao-iss"
description: "Use ao triar documentação de ações de restituição de ISS para clientes de esporte (atletas, direito de imagem) ou audiovisual (produtoras), a partir de notas fiscais dos últimos anos. Identifica perfil do cliente e regime tributário (Simples Nacional ou não), extrai dados das NFs, cruza com o comprovante do regime aplicável, consolida em planilha e — nas etapas seguintes do pipeline — organiza a documentação para protocolo, apoia a montagem da petição inicial e monta a planilha de cálculo de atualização monetária (IPCA-E) para instruir o valor atualizado."
---


# Triagem de Restituição de ISS — Esporte e Audiovisual

## Papel
Assistente jurídico especializado em apoiar o fluxo completo de ações tributárias de
**restituição de ISS**, do início (triagem documental) até o fim (petição inicial
pronta para protocolo). Aplica-se a escritórios que atuam com clientes de esporte e
entretenimento. Cada ação se baseia em notas fiscais de serviços emitidas pelo cliente
(tipicamente nos últimos 5 anos).

## Como esta skill deve evoluir entre sessões — LEIA ANTES DE COMEÇAR
Esta skill é um documento vivo. Ela nasceu só com a etapa de triagem, mas o escritório
está expandindo o pipeline (organização de documentos para protocolo, elaboração da
petição inicial, e o que vier depois). **Toda sessão que usar esta skill deve deixá-la
melhor do que encontrou**, seguindo o padrão abaixo:

1. **Enquanto trabalha**, anote (mentalmente ou num arquivo de rascunho) qualquer
   coisa que não estava documentada aqui e que você teve que descobrir por tentativa e
   erro: um layout de documento novo, uma armadilha de extração, uma preferência de
   formatação do Pedro, um passo novo do fluxo (ex.: como montar a petição inicial),
   uma correção de um erro anterior.
2. **Ao final da sessão** (ou assim que a descoberta for validada com o Pedro), chame
   `mcp__cowork__save_skill` com `name: "triagem-restituicao-iss"`, `overwrite: true`
   e o **conteúdo completo desta skill** (leia o atual primeiro) mais a sua adição —
   nunca substitua o todo por só a parte nova, e nunca dependa de editar o arquivo em
   disco (`skills/triagem-restituicao-iss/SKILL.md`), porque isso é só um cache
   somente-leitura da sessão — só `save_skill` persiste de verdade. **Se você tentar
   editar o arquivo em disco (`Edit`), vai receber o erro "is read-only in this
   session" — isso é esperado, não é bug: use `save_skill` diretamente.**
3. **Formato de cada aprendizado novo**: adicione na seção mais próxima do assunto (não
   crie uma seção solta de "changelog"), e sempre explique o quê, o porquê (**Why**) e
   como aplicar da próxima vez (**How to apply**) — segue o mesmo padrão já usado nas
   seções de regime tributário e nos exemplos de correção abaixo.
4. **Se a mudança for específica de um caso** (não generalizável, ex.: um detalhe só do
   caso 8 Milímetros), ela pertence à memória do projeto daquele caso
   (`memory/project_caso_<nome>.md`), não a esta skill. Esta skill deve conter só
   conhecimento reutilizável entre casos. **Nota:** a ferramenta de memória de projeto
   (arquivos em `memory/`) pode não estar acessível em toda sessão — se as tentativas de
   `Read`/`Edit` nesse caminho falharem com "outside this session's connected folders",
   não insista; guarde o aprendizado reutilizável aqui mesmo na skill (que sempre
   funciona via `save_skill`) em vez de perder a informação.
5. **Se descobrir uma etapa nova do pipeline** (ex.: como organizar os documentos para
   protocolo, como montar a petição inicial a partir do quadro de restituição), adicione
   uma seção nova ao final desta skill, no mesmo nível das seções "Passo a passo da
   triagem" e "Quadro de restituição" — não crie uma skill separada para isso, a menos
   que o Pedro peça explicitamente. O objetivo é ter um único playbook por perfil de
   caso, cobrindo do início ao fim.

## Roadmap do pipeline (etapas já cobertas vs. a expandir)
1. ✅ **Triagem documental** — perfil do cliente, regime tributário, extração de NFs,
   cruzamento com o comprovante, planilha de triagem. Coberto em detalhe abaixo.
2. ✅ **Quadro de restituição para a petição** — por nota e consolidado por mês.
   Coberto em detalhe abaixo.
3. ✅ **Organização da documentação para protocolo** — testada em caso de 1 município
   (8 Milímetros, 05/08/2026; e Benassi Sports, 07/08/2026) e em caso de múltiplos
   municípios/réus ao longo do tempo (Ganso, 06/08/2026). Ver seção própria abaixo com
   a numeração padrão do escritório, o método de consolidação por ano/categoria
   (incluindo divisão em partes para respeitar limite de tamanho por arquivo, inclusive
   o caso-limite de um único arquivo-fonte grande demais, e a ordenação cronológica
   correta das notas dentro de cada bloco) e a lista de pendências típicas.
4. ✅ **Elaboração da petição inicial** — primeira petição real montada com sucesso
   (caso 8 Milímetros, 05/08/2026); método expandido e testado em caso multi-município
   com 3 petições reais (Ganso, 06/08/2026, usando modelos-precedente reais em vez do
   modelo genérico "MARCELO" — ver seção própria abaixo).
5. ✅ **Cálculo de atualização monetária (IPCA-E)** — primeira planilha de cálculo
   montada com sucesso (caso RW Sports, 05/08/2026), para instruir a inicial com o
   valor atualizado. Ver seção própria abaixo com a metodologia, a fonte de dados do
   índice e o tratamento dos juros de mora (SELIC) ainda não computáveis nesta fase.
6. ⬜ **Etapas futuras** (protocolo em si — envio no PJe/e-SAJ, acompanhamento
   processual, procuração/assinatura eletrônica, etc.) — adicionar conforme forem sendo
   feitas.

## Perfis de cliente atendidos
O mesmo processo se aplica a dois perfis, que diferem no documento que
antecede/justifica a nota fiscal e no volume esperado de notas por mês:

| Perfil | Documento que antecede a NF | Volume típico de notas/mês |
|---|---|---|
| **Atletas** | Contrato de Cessão de Direito de Imagem | Baixo — geralmente até 3-4 notas/mês |
| **Produtores de audiovisual** | Contrato de prestação de serviço ou proposta comercial por cliente | Alto — pode haver dezenas de notas em um único mês |

Identifique o perfil do caso logo no início da triagem: isso muda o documento de
suporte esperado para cada nota e a expectativa de volume. Um mês com poucas notas é
normal para atleta, mas pode sinalizar lacuna para produtor audiovisual — e vice-versa,
um mês com muitas notas seria incomum para um atleta.

**Caso Ganso (Paulo Henrique Chagas de Lima Costi, 06/08/2026):** perfil atleta, com uma
particularidade nova em relação ao 8 Milímetros/RW Sports — a empresa do atleta mudou de
**domicílio fiscal 3 vezes** ao longo do período do caso (Praia Grande/SP → São
Paulo/SP → Barueri/SP), sempre com o mesmo CNPJ e o mesmo tomador único (o clube de
futebol). Isso gera notas em 3 municípios diferentes dentro da mesma ação/triagem, cada
um com layout de NF próprio e regime de comprovante próprio. **Nesse tipo de caso, a
planilha de triagem deve ter a cidade como dimensão de primeira classe** (coluna própria
em toda aba, cores por cidade) e a recomendação de ajuizamento deve ser de **uma ação por
Município réu** (cada um é o ente tributante daquele período), não uma ação só — deixar
isso explícito na aba de pendências/observações da planilha. **Além da planilha
consolidada, o Pedro pediu abas extras "Cidade - X" (uma por município), cada uma
autocontida: tabela de notas daquela cidade + duas seções de texto "O QUE TEMOS" / "O
QUE ESTÁ FALTANDO" específicas daquele município** — isso deixou cada ação mais fácil de
revisar isoladamente sem precisar filtrar a aba grande. Vale oferecer esse formato (abas
por cidade, com seções de "temos/falta") sempre que um caso tiver mais de um
município/réu, mesmo sem o Pedro pedir explicitamente — foi um pedido natural depois de
ver a planilha consolidada. **As 3 petições iniciais do caso Ganso foram concluídas em
06/08/2026** (ver seção "Elaboração da petição inicial" abaixo, subseção "Casos
multi-município") — esse caso é agora a referência completa de ponta a ponta (triagem →
protocolo → 3 petições) para o padrão "empresa que mudou de domicílio fiscal".

**Caso Benassi Sports LTDA (João Victor Silva Benassi, 07/08/2026):** perfil atleta,
domicílio fiscal único (Américo Brasiliense/SP) durante todo o período (09/2023 a
05/2026) — caso "simples" de 1 município, mas com dois tomadores diferentes ao longo do
tempo (Ferroviária S.A.F. em 2023, depois Coritiba SAF de 2024 em diante), o que por si
só não muda o réu (é sempre o Município do domicílio do prestador) mas é relevante para
saber quais contratos de imagem pedir à contabilidade (um por tomador/período). Município
migrou de layout de NF em 2026 (do layout próprio da prefeitura para o padrão nacional
NFS-e) — mesma situação já registrada para o Ganso em Américo Brasiliense/Barueri,
tratar como já documentado na seção de observações técnicas de extração.

## Documentos que compõem cada caso
Normalmente solicitados à contabilidade do cliente:
1. Contrato Social da empresa
2. Documento pessoal do representante da empresa
3. Registros das notas fiscais dos serviços prestados (NF)
4. Documentos que comprovem o pagamento do ISS (comprovante/declaração)
5. Documento de origem da prestação de serviço — varia por perfil (Contrato de Cessão
   de Direito de Imagem para atletas; contrato/proposta comercial para audiovisual)

Ao iniciar um caso novo, faça um inventário rápido de quais desses 5 itens existem no
dossiê recebido e quais faltam — isso já é um achado a reportar, não apenas um
pré-requisito. **Nota:** o Contrato Social muitas vezes já traz o RG/CPF/endereço
completo de cada sócio (na parte de qualificação dos sócios) — antes de tratar o
"documento pessoal do representante" como definitivamente faltante, ler o Contrato
Social inteiro; ele pode suprir boa parte da qualificação necessária para a petição
mesmo sem uma cópia escaneada do RG/CPF em separado. **O mesmo vale para o próprio
Contrato de Cessão/Sublicenciamento de Direitos de Imagem** (caso Ganso, 06/08/2026;
confirmado de novo no caso Benassi, 07/08/2026): a cláusula de qualificação das partes
desse contrato também costuma trazer CPF e RG completos do atleta/sócio — ler esse
contrato antes de marcar o documento pessoal como "totalmente faltante"; registrar como
"parcialmente suprido" quando só falta a cópia digitalizada do documento em si (não o
dado de qualificação).

**Quando o dossiê tem mais de um tomador ao longo do tempo (ex.: Benassi: Ferroviária em
2023, depois Coritiba de 2024 em diante), o item 5 (documento de origem/Contrato de
Imagem) deve ser cobrado por tomador e por período de vigência, não só "um contrato
qualquer"** — um único contrato no dossiê cobrindo só um dos tomadores/períodos não
supre os demais. Verificar se o contrato presente no dossiê cobre exatamente o período
em que as notas daquele tomador foram emitidas (ex.: contrato vigente até 30/11/2024,
mas notas ao mesmo tomador seguem sendo emitidas depois disso — sinalizar a falta de
aditivo/renovação como pendência).

**Um e-mail de solicitação de notas fiscais do próprio tomador (ex.: um clube pedindo
as NFs para a contabilidade) pode revelar período contratual anterior ao que consta no
dossiê de NFs enviado** (caso Ganso: um e-mail de dez/2021 listava parcelas com
vencimento desde 15/03/2019, mas as NFs enviadas só cobriam a partir de 12/2021). Tratar
isso como um achado a registrar na pendência, mas **cruzar sempre com a prescrição
quinquenal da repetição de indébito tributário (art. 168, CTN)** antes de tratar como
pendência bloqueante — se a data provável de ajuizamento já deixaria aquele período fora
da janela de 5 anos, a lacuna de documentação provavelmente não afeta o valor a pleitear,
e isso deve ser dito explicitamente na planilha (evita alarme falso de "faltam 2 anos de
notas" quando na prática já estariam prescritas).

**Lacunas na sequência de numeração das notas (números que "pulam") não são
necessariamente um problema — sempre perguntar ao cliente antes de tratar como
pendência bloqueante.** No caso Ganso, o Pedro confirmou que os números 6, 10, 66 e 67
(São Paulo) "não existem mesmo" — ou seja, a lacuna era esperada (nota cancelada, número
pulado no emissor, etc.), não uma nota faltante no dossiê. **How to apply:** reportar a
lacuna normalmente na triagem inicial (é a postura correta antes de confirmar), mas
assim que o cliente/advogado confirmar que a lacuna é normal, atualizar a planilha (e
qualquer pasta de protocolo já montada) trocando o alerta "✗ pendente" por um "✓
confirmado" — não deixar o alerta antigo se ele já foi resolvido em conversa, porque um
alerta desatualizado é pior que não ter alerta (o usuário para de confiar na lista de
pendências). **No caso Benassi (07/08/2026), as lacunas de numeração (32, 35, 36, 44,
53, 54, 56, 57, 58, 72, 74-80) ainda não foram confirmadas pelo cliente/contabilidade no
momento da triagem — foram incluídas no e-mail de pendências enviado à contabilidade
(ver seção "Envio de pendências à contabilidade por e-mail" abaixo) em vez de aguardar
uma sessão futura para perguntar; assim que a resposta chegar, atualizar a planilha e a
pasta de protocolo (PENDENCIAS.txt) da mesma forma que no Ganso.**

## Envio de pendências à contabilidade por e-mail
**Testado no caso Benassi (07/08/2026):** depois de fechar a lista de pendências da
triagem (documentos ausentes, lacunas de numeração, divergências mês a mês, notas com
ISS = 0,00 suspeito), formalizar tudo em um único e-mail à contabilidade do cliente, em
vez de deixar as pendências só registradas na planilha aguardando uma conversa futura.

- **Como achar o e-mail da contabilidade quando não há contato explícito no dossiê**: as
  próprias NFs de prefeitura costumam trazer, no bloco "PRESTADOR DE SERVIÇOS", um campo
  de e-mail que não é do cliente final, e sim do escritório de contabilidade que emite as
  notas em nome dele (ex.: `fiscal@castroassessoria.com.br` no caso Benassi — domínio
  "castroassessoria" bate com uma assessoria contábil, não com o nome do cliente/atleta).
  Confirmar esse padrão abrindo 2-3 notas de anos diferentes antes de assumir que é
  realmente o contato certo (no caso Benassi, o mesmo e-mail apareceu em notas de 2023 e
  2025 — consistente ao longo do tempo).
- **Formato do e-mail**: uma lista numerada, cada item com o suficiente de contexto para
  a contabilidade agir sem precisar abrir a planilha de triagem (ex.: "nota nº X emitida
  em [competência], mas o comprovante não traz essa competência — poderiam confirmar
  declaração/pagamento por outra via?"), cobrindo na ordem: (1) documentos do dossiê
  ausentes/incompletos (Contrato Social, documento pessoal, contratos de origem por
  tomador/período), (2) competências inteiras sem nenhuma nota no dossiê apesar de
  constarem no comprovante, (3) lacunas de numeração a confirmar, (4) divergências
  pontuais de quantidade/valor por competência, (5) notas com alíquota/ISS = 0,00
  suspeitas, (6) pedido de guias individuais de pagamento (se só houver um resumo anual
  agregado, sem data de pagamento por competência).
- **Criar como rascunho (draft), nunca enviar diretamente** — usar a ferramenta de
  criação de rascunho do Gmail (`create_draft`) e deixar para o Pedro revisar/enviar. Ele
  pode querer ajustar tom, adicionar destinatários em cópia, ou confirmar o e-mail do
  destinatário antes do envio efetivo.

**Why:** transforma a lista de pendências (que só existia dentro da planilha/PENDENCIAS)
em uma ação concreta que já sai da sessão — reduz o atraso entre "identificar a lacuna" e
"cobrar quem pode resolvê-la", sem depender do Pedro lembrar de fazer isso manualmente
depois de ler a planilha.

**How to apply:** ao final de uma triagem (ou de uma atualização de pendências), oferecer
proativamente montar esse e-mail de cobrança à contabilidade, usando a lista de
pendências já consolidada na aba "Pendências" da planilha como roteiro — não é preciso
esperar o Pedro pedir explicitamente, mas a criação do rascunho em si (não o envio) pode
ser feita direto quando ele pedir "manda um e-mail" ou similar.

## ATENÇÃO: acesso ao dossiê via Google Drive
O dossiê normalmente chega como um Google Doc índice, com links para pastas do Google
Drive por categoria/ano. Ao acessar essas pastas:

- **Não confiar apenas em um conector MCP de Drive para listar/contar arquivos.**
  Conectores MCP podem estar autenticados numa conta diferente da conta que realmente
  tem acesso completo às pastas compartilhadas, e retornar uma lista parcial sem
  nenhum erro visível (ex.: mostrar 2 arquivos numa pasta que na verdade tem 40+). Isso
  gera falsos positivos de "lacuna de documentação".
- **Sempre conferir a contagem real abrindo a pasta pelo navegador** (Claude in Chrome,
  com a conta que o usuário efetivamente usa), antes de reportar qualquer pasta como
  vazia ou incompleta. Comparar o número de arquivos visto no navegador com o que o
  conector MCP retornou.
- Se houver divergência, priorizar o que o navegador mostra, e usar o navegador
  (selecionar tudo → Baixar, que o Drive compacta em .zip) para baixar os arquivos reais
  para uma pasta de trabalho local antes de processá-los — isso também facilita
  rasterizar/OCR os PDFs que forem imagem. Ao baixar uma pasta inteira pelo menu do
  nome da pasta (não Ctrl+A), aguardar a notificação "Download pronto" antes de navegar
  para a próxima pasta — navegar cedo demais cancela o zip em preparação.
- Só depois de confirmar a contagem real é que faz sentido calcular volumes esperados
  por competência (tabela de perfis acima) ou apontar lacunas para a contabilidade.
- **Quando o dossiê chega como uma pasta local já sincronizada (ex.: OneDrive) em vez de
  Google Drive**, o mesmo cuidado se aplica na direção oposta: **sempre rodar
  `unzip -l` (listar sem extrair) em cada .zip do dossiê antes de assumir que o conteúdo
  bate com o nome do arquivo.** Já aconteceu (caso Ganso, 06/08/2026) de um zip chamado
  "Notas fiscais Fluminense 2023, 2024 e 2025.zip" conter, na prática, só uma imagem de
  assinatura de e-mail (`GráficoColado-1.tiff`, ~14KB) — zero notas fiscais de verdade,
  apesar do nome prometer 3 anos de documentos. **Why:** provavelmente um erro de quem
  organizou o e-mail/anexo do lado do cliente, mas só aparece se você checar o tamanho
  total do zip (poucos KB é suspeito) e o `unzip -l` antes de extrair. **How to apply:**
  ao mapear os arquivos de um dossiê novo, rodar `ls -la *.zip` e `unzip -l` em cada um
  logo no início, e tratar qualquer zip nomeado como "notas/documentos de período X" mas
  com conteúdo vazio/mínimo como pendência de reenvio a reportar — mesmo que o mesmo
  período pareça já coberto por outra pasta do dossiê (confirmar, não presumir que é
  redundante).
- **Quando a pasta do caso já contém arquivos "*_merged.pdf" soltos na raiz** (lotes de
  upload originais do cliente, antes de serem separados em arquivos individuais por
  nota), **não usar esses arquivos como fonte para os blocos de protocolo** — eles
  costumam ser reagrupamentos arbitrários (por lote de upload, não por ano/categoria) e
  ficam redundantes assim que a pasta `NF/<ano>/` com um arquivo por nota já existe
  (caso Benassi, 07/08/2026: 6 arquivos `_merged.pdf` na raiz somavam exatamente as
  mesmas 66 páginas já presentes, individualizadas, em `NF/2023` a `NF/2026`). Confirmar
  a redundância somando páginas antes de ignorá-los, mas o merge para a pasta de
  protocolo deve sempre partir dos arquivos individuais (permite escolher exatamente
  quais notas entram em cada bloco/competência, o que um lote de upload bruto não
  permite).

## Salvando entregáveis em pasta do usuário
Antes de sobrescrever um arquivo de entrega (planilha, quadro) na pasta do caso,
verificar se ele está aberto no Excel/Word do usuário (erro "Permission denied" no
`cp`/`rm`, ou presença de um arquivo de lock `~$nome.xlsx` na mesma pasta). Se estiver
aberto, **avisar o usuário e pedir para fechar antes de salvar** — não criar
automaticamente uma cópia com sufixo `_v2`. Isso evita várias versões soltas na pasta.
**Isso pode acontecer mais de uma vez na mesma sessão** (caso Ganso: o usuário reabriu o
arquivo entre uma correção e outra) — cada nova tentativa de `cp`/salvar deve refazer a
mesma checagem de lock (`~$nome.xlsx`), não presumir que já está fechado só porque foi
fechado uma vez antes na conversa.

**A pasta do caso (workspace do usuário) não permite `rm`/renomear arquivos já
escritos** (`Operation not permitted`, caso Benassi, 07/08/2026 — ao corrigir a ordem
das notas dentro de um PDF já entregue, o `rm` do arquivo antigo falhou). **Isso não
bloqueia a correção**: `cp` sobrescrevendo o mesmo nome de arquivo funciona normalmente
(é escrita de conteúdo, não deleção/renomeação) — quando precisar substituir um
entregável já copiado para a pasta do caso, gerar a nova versão com **o mesmo nome de
arquivo** em `/tmp` e sobrescrever via `cp` direto, em vez de tentar apagar o antigo
primeiro. Se o nome do arquivo precisar mudar (ex.: uma divisão em partes que resultou
em uma quantidade diferente de arquivos), os arquivos com nomes antigos que não têm mais
correspondência ficam órfãos na pasta — usar `mcp__cowork__allow_cowork_file_delete`
para pedir permissão de remover esses órfãos, ou avisar o Pedro para removê-los
manualmente, em vez de tentar `rm` direto.

**Os arquivos de trabalho em `/tmp` não sobrevivem entre sessões/dias** — se numa nova
sessão os scripts/JSONs intermediários não estiverem mais lá, não é preciso refazer tudo
do zero: os dados finais já estão nas planilhas entregues na pasta do caso (ex.: aba
"Extratos - PAs Completos" do arquivo de triagem), que podem ser lidas de volta com
`openpyxl` (`data_only=True`) para recuperar os valores já apurados.

**Arquivos "cloud-only" (OneDrive) que ainda não sincronizaram no sandbox**: se um
comando de shell (`cp`, `open`, leitura via Python) falhar com `[Errno 22] Invalid
argument` (não `[Errno 2] No such file`) num arquivo dentro da pasta do caso montada via
OneDrive, o arquivo provavelmente é só um placeholder na nuvem, ainda não baixado para o
disco do sandbox — não é bug de encoding de nome de arquivo (já testado: normalizar
Unicode NFC/NFD não resolve, e o mesmo erro acontece até em nomes sem acento).
**Solução: chamar a ferramenta `Read` nesse arquivo específico** — isso força o
download/materialização, e depois o mesmo caminho passa a funcionar normalmente em
bash/Python. Ao fazer merge em lote de muitos PDFs (ex.: consolidar um ano inteiro de
notas fiscais), rodar primeiro um loop de teste (`PdfReader(f)` em cada arquivo, sem
fazer nada com o resultado) para detectar todos os arquivos com esse problema de uma vez
só, chamar `Read` em cada um deles, e só depois rodar o merge de verdade — evita ter que
descobrir as falhas uma a uma no meio de um merge grande. **Nem sempre há arquivos
cloud-only**: no caso Benassi (07/08/2026), o mesmo loop de teste não encontrou nenhum
arquivo problemático — todos os 66 PDFs de NF, os 4 comprovantes e os demais documentos
já estavam sincronizados no disco, então o merge pôde ser feito direto sem nenhuma
chamada a `Read` prévia. Rodar o loop de teste sempre, mas não assumir que ele vai
necessariamente encontrar problemas.
**A ferramenta `Read` também
serve para casos pontuais (2-3 arquivos) fora de um merge em lote** — ela devolve o
conteúdo do PDF já renderizado visualmente na conversa (uma "imagem" por página), então
para um punhado de notas fiscais isoladas que precisariam de OCR, às vezes é mais rápido
simplesmente ler o valor direto da renderização do que rodar o pipeline de OCR completo
(caso Ganso: usado para 3 notas de Barueri que eram as únicas ainda não sincronizadas;
caso Benassi: usado para spot-check de verificação de 2 notas e 1 comprovante já
sincronizados, só para conferir a fidelidade da extração anterior — não é só para
destravar arquivos cloud-only).
**Nota adicional (caso Ganso, petições, 06/08/2026):** a ferramenta `Read` (arquivos) e o
sandbox de `bash` enxergam **filesystems diferentes** — um arquivo criado via `bash` em
`/tmp/work/algo.jpg` não aparece para `Read` mesmo com o caminho "traduzido" certo. Para
inspecionar visualmente um arquivo gerado no sandbox de bash (ex.: página de PDF
renderizada em `.jpg` para QA), **copiar primeiro para dentro da pasta de outputs
montada** (`cp arquivo.jpg /sessions/<sessão>/mnt/outputs/`) e só então chamar `Read`
com o caminho Windows correspondente — não adianta ajustar o caminho de `/tmp/work` na
tentativa de `Read`, ele sempre vai falhar com "outside this session's connected
folders". **A mesma restrição vale ao entregar arquivos finais**: qualquer PDF/planilha
montado em `/tmp` (bash) precisa ser copiado (`cp`) para o caminho da pasta do caso
montada via bash (`/sessions/<sessão>/mnt/<PastaDoCaso>/...`) antes de considerar a
entrega concluída — escrever em `/tmp` sozinho não é visível nem para o usuário nem para
o `Write`/`Read` do lado Windows.

## Os dois regimes tributários — trate como fluxos diferentes
O cliente pode estar **fora do Simples Nacional** ou ser **optante do Simples
Nacional**. Identifique o regime antes de aplicar as regras de cruzamento — a própria
NF do optante do Simples costuma trazer o aviso impresso: *"Documento emitido por ME ou
EPP optante pelo SIMPLES NACIONAL..."*.

### A) Fora do Simples Nacional
- **NF:** layout varia por município; traz Prestador, Tomador, discriminação do
  serviço, base de cálculo, ISS retido/devido e competência. Nesse regime o **valor do
  ISS aparece diretamente na própria NF** (não precisa de rateio) — cada nota já traz
  seu ISS individual e, normalmente, uma guia de recolhimento própria. **Nem toda
  prefeitura imprime o "Valor do ISS" como campo isolado**: São Paulo, Praia Grande e
  Américo Brasiliense imprimem (campo "Valor do ISS (R$)" / "Total do ISSQN"), mas
  Barueri só imprime a **alíquota** na linha do item de serviço (ex.: "2,00" na coluna
  Alíquota) sem uma linha de valor de ISS separada — nesse caso, calcular `ISS = Valor
  Total da Nota × Alíquota / 100` e documentar na planilha que foi calculado a partir da
  alíquota impressa, não copiado de um campo pronto (caso Ganso, Barueri, 06/08/2026).
- **Comprovante:** o formato do comprovante varia por prefeitura, não é sempre um único
  "Resumo das Declarações" anual — pode ser: (a) um relatório anual consolidado
  ("Resumo das Declarações") com número de documentos declarados por competência
  (Américo Brasiliense, caso Benassi: um PDF por ano — 2023, 2024, 2025, 2026 — cada um
  com uma linha por competência, quantidade de documentos e valor pago), ou (b) uma
  **guia de recolhimento individual por competência** (ex.: São Paulo emite um
  "DAMSP — Documento de Arrecadação do Município de São Paulo" por mês/competência, com
  status "GUIA QUITADA" ou "GUIA QUITADA POR RDT" quando paga). Identificar qual dos dois
  formatos o dossiê trouxe antes de montar o cruzamento — a lógica de "uma linha por
  competência" funciona para os dois, só muda a granularidade da fonte.
- **Cruzamento:** comparar quantidade de notas da competência (na pasta) com número de
  documentos declarados no comprovante daquela competência (ou, no formato de guia
  individual, o valor do ISS somado das notas da competência contra o valor de receita
  da guia daquele mês); checar se toda competência com nota emitida tem uma linha
  "Pago"/guia quitada correspondente.
- **Ausência de guia/comprovante NÃO significa que o ISS não foi pago** — nesse regime
  (diferente do Simples Nacional, onde "não pago" é um status literal do Extrato, ver
  seção B), a nota fiscal em si já é presunção de recolhimento; a falta de guia no
  dossiê é só uma falta de comprovação documental, não um indício de inadimplência.
  **Por isso, ao montar a pasta de protocolo, o critério de "só as competências pagas"
  (usado no regime Simples Nacional, ver seção de organização de documentos abaixo) não
  se aplica da mesma forma aqui** — confirmar com o Pedro se todas as notas emitidas
  entram no pedido/anexos mesmo sem guia (caso Ganso: sim, confirmado em 06/08/2026;
  caso Benassi: sim, confirmado em 07/08/2026 via `AskUserQuestion` — "todas as notas
  emitidas" foi a escolha nos dois casos até agora neste regime), em vez de aplicar por
  padrão a mesma regra do caso Simples Nacional.

**Achado de portal de prefeitura — São Paulo gera dois tipos de PDF que parecem
duplicados mas são complementares (caso Ganso, 06/08/2026):** o portal
`nfe.prefeitura.sp.gov.br` tem duas rotas de impressão diferentes —
`notaprint.aspx` (a própria nota fiscal, com discriminação do serviço e ISS) e
`guiaprint.aspx` (a guia de recolhimento DAM-SP, o comprovante de pagamento). Se o
dossiê trouxer duas pastas com nomes parecidos cobrindo o mesmo período (ex.: "NOTAS SÃO
PAULO" e "São Paulo"), **não presumir que é duplicidade/redundância** — abrir um PDF de
cada pasta e checar a URL no rodapé da página (visível mesmo sem OCR, já que o cabeçalho
do print-to-PDF normalmente tem texto real): se uma bate com `notaprint` e a outra com
`guiaprint`, são as notas e os comprovantes de pagamento, respectivamente — exatamente o
par nota+comprovante que a triagem precisa, só que cada um numerado com sua própria
sequência (nota numerada 1-75; guia numerada por competência, não por número de nota).
**How to apply:** ao encontrar duas pastas com nomes semelhantes no mesmo dossiê, abrir
um arquivo de cada uma primeiro (via `pdftotext` no cabeçalho, sem precisar OCR completo
ainda) para classificar o papel de cada pasta antes de decidir se são duplicatas ou
complementares.

**PDFs de "print to PDF" de portal de prefeitura frequentemente só têm texto real no
cabeçalho (URL, data/hora de impressão), com o corpo do documento como imagem** — isso
já era conhecido para o caso genérico, mas vale reforçar o teste rápido: rodar
`pdftotext -layout` e contar não só o total de caracteres, mas se aparecem **marcadores
de conteúdo real** (`CNPJ`, `Tomador`, `Prestador`, `Valor Total`) — um PDF de cabeçalho
apenas costuma ter 200-300 caracteres (a URL sozinha já passa de 200), o que engana um
filtro só por contagem de caracteres. Usar presença desses marcadores, não só o tamanho
do texto, para decidir se o arquivo precisa de OCR. **O layout de Américo Brasiliense
(caso Benassi) tem fonte customizada e `pdftotext` retorna texto ilegível/embaralhado
mesmo tendo milhares de caracteres** — nesse caso o teste de "marcadores de conteúdo
real" não pega o problema (o texto existe, só está corrompido); a checagem mais
confiável acaba sendo visual (`Read` da própria ferramenta, que renderiza o PDF) em vez
de só `pdftotext`. As notas do novo layout nacional NFS-e (2026 em diante) já têm texto
limpo/extraível normalmente.

### B) Optante do Simples Nacional
- **NF:** layout da prefeitura do município do prestador; costuma ter texto extraível
  normalmente. Traz Prestador, Tomador, descrição do serviço e, no campo de
  discriminação, texto livre identificando o cliente/atleta e o mês/proposta de
  referência. **O campo "Valor do ISS" impresso na própria NF normalmente vem 0,00** —
  o ISS não é calculado nota a nota, é uma fatia do DAS mensal consolidado.
- **Comprovante:** **Extrato do Simples Nacional (PGDAS-D/DAS)** — relatório mensal que
  consolida vários tributos (IRPJ, CSLL, COFINS, PIS, INSS/CPP, ISS) a partir da
  receita bruta total do período de apuração (PA).
  - Cada Extrato de um PA específico também traz, na seção "Receitas Brutas
    Anteriores" (item 2.2.1), um histórico de ~23-24 meses de receita bruta mensal
    anterior. Isso permite reconstruir a receita bruta declarada mês a mês combinando
    2-3 Extratos de datas diferentes, mesmo sem o DAS completo de cada mês — mas o
    detalhamento de ISS por tributo só existe no Extrato cuja competência (PA) é
    exatamente aquele mês. **Sempre pedir ao cliente/contabilidade os DAS mensais
    completos de todo o período do caso** (não só 2-3 extratos) assim que possível —
    isso é o que permite preencher "Valor do ISS Pago" e "Data do ISS Pago" por
    competência no quadro final, em vez de deixar só a receita reconstruída.
  - O Extrato tem três seções relevantes para o ISS, e **cada uma serve para uma coisa
    diferente — não são intercambiáveis**:
    - **Item "3) Valor do Débito por Tributo para a Atividade" / "4) Total Geral da
      Empresa"**: NUNCA usar. É só o cálculo base do tributo, sem multa/juros — o Total
      fica subestimado sempre que há atraso na apuração/pagamento.
    - **Item "6) Informações sobre DAS Gerado"**: é a guia realmente gerada. Seu campo
      "Total" (Principal + Multa + Juros) é a fonte correta do **"Total DAS"** da
      competência. Mas a linha "ISS" que aparece *dentro* do item 6 é só o valor base
      (antes de ratear multa/juros entre os tributos) — **não usar essa linha como
      "Valor do ISS"**.
    - **Item "6.1) Discriminação dos Valores Calculados no DAS Gerado"**: é a fonte
      correta do **"Valor do ISS"** da competência. Traz o mesmo total do item 6, mas já
      com a multa/juros rateada proporcionalmente entre os tributos (some as 6 linhas
      de 6.1 e bate exatamente com o Total do item 6). Quando não há multa/juros no mês,
      o valor de 6.1 coincide com a linha ISS do item 6 — a diferença só aparece em
      meses com atraso.
    - **Item "6.2) Informações da Arrecadação do DAS gerado nesta apuração"**: única
      fonte de data e valor efetivamente pago. Se disser "Não foi reconhecido pagamento
      até a presente data", ver nota abaixo antes de presumir que é erro de extração.
  - Exemplo real (competência 01/2023, caso 8 Milímetros): item 3/4 = R$2.415,85; linha
    ISS dentro do item 6 = R$2.415,85 (igual ao 3/4, porque ambos ignoram multa/juros);
    item 6.1 = R$3.103,40 (correto — Total do DAS naquele mês foi R$9.263,88, com
    R$1.442,30 de multa e R$610,09 de juros rateados entre os 6 tributos). Usar
    R$2.415,85 como "Valor do ISS" nesse caso subestimaria a restituição.
  - **Se o item 6.2 disser "Não foi reconhecido pagamento até a presente data", trate
    isso como um fato do documento, não como falha de extração.** Confirme sempre
    reabrindo o texto bruto do PDF daquela competência antes de suspeitar de bug —
    esse texto costuma aparecer igual em extratos "Apuração Original" e
    "Retificadora" (ou seja, não é a retificadora que causa o "não pago"). Se o
    número de meses "não pago" parecer alto demais ao cliente/advogado, a causa mais
    provável não é erro de regex, e sim que o pagamento daquela competência aconteceu
    por uma via que não aparece neste Extrato específico (ex.: parcelamento à parte,
    DAS avulso reemitido, GNRE). **Nunca reclassificar como "pago" sem prova
    documental** — isso vira alegação fática numa petição. Reporte a lista de
    competências "não pago" como pendência a confirmar com o cliente/contabilidade
    (pedir comprovante de pagamento por outra via, se houver), em vez de presumir uma
    das duas hipóteses. **E, ao montar a petição inicial, exclua essas competências do
    pedido de restituição** — só cabe repetição de indébito sobre valores efetivamente
    pagos (confirmado com o Pedro no caso 8 Milímetros: 22 meses pagos entraram no
    pedido, 19 meses "não pago" ficaram de fora).
- **Cruzamento:** comparar a soma do valor das notas emitidas na competência (por texto
  de discriminação ou data de emissão) com a "Receita Bruta do PA" (ou reconstruída via
  histórico) daquele mês. Divergência pode indicar nota não declarada, nota lançada no
  mês errado, ou erro de digitação na descrição da nota — mas confira primeiro se não é
  apenas mais um caso de listagem incompleta (ver seção acima) antes de reportar como
  divergência real.

## Passo a passo da triagem
1. **Identificar o regime tributário** do cliente.
2. **Ler cada NF** e extrair: prestador, tomador (razão social e CNPJ), competência
   (preferir nome do arquivo ou campo "Competência" da NF a inferir só do texto livre),
   natureza do serviço, base de cálculo, valor do ISS, valor total.
3. **Validar se a nota pertence à ação**, sinalizando para revisão manual quando:
   - o texto não menciona claramente a natureza esperada do serviço para aquele perfil
     (ex.: "direito de imagem" para atletas; objeto compatível com contrato/proposta
     para audiovisual) — pode ser variação de redação, mas precisa confirmação;
   - para atletas, o tomador não parece clube de futebol/entidade esportiva; para
     audiovisual, o tomador não bate com nenhum contrato/proposta conhecido do cliente;
   - a competência mencionada no texto livre diverge da data de emissão de forma
     suspeita (nota emitida em mês N mencionando mês N-1 quando já existe outra nota
     para N-1 — pode ser erro de digitação recorrente).
4. **Checar completude por competência** ao longo do período do caso: para cada mês,
   deve existir nota emitida E documento correspondente no comprovante do regime
   aplicável. Reportar meses sem nenhum registro. Calibrar expectativa de volume pelo
   perfil (ver tabela acima) — e, de novo, confirmar via navegador que a pasta
   realmente está incompleta antes de reportar. **Quando o caso tem mais de uma cidade
   (empresa que mudou de domicílio fiscal), fazer essa checagem de completude por
   competência considerando a união de todas as cidades** — um mês pode estar "vazio"
   olhando só para uma cidade mas coberto por outra (ou genuinamente vazio nas três,
   o que é o achado relevante a reportar).
5. **Cruzar com o comprovante** conforme a lógica do regime (A ou B acima).
6. **Consolidar em planilha de triagem**, com uma aba de notas extraídas, uma de
   cruzamento com o comprovante (achados sinalizados) e uma com os dados brutos do
   comprovante.
7. **Montar o quadro de restituição para o corpo da petição** (ver seção abaixo) — só
   depois que as etapas 1-6 estiverem razoavelmente estáveis, porque esse quadro é o
   que o advogado cola direto na peça.

## Quadro de restituição para o corpo da petição
Esse é o quadro que efetivamente entra no texto da petição (diferente da planilha de
triagem interna). Formato padrão do escritório, uma linha por nota fiscal:

| Número da Nota | Mês de Referência | Descrição da Nota | Valor da Nota Fiscal (R$) | Valor do ISS (R$) | Valor do ISS Pago (R$) | Data do ISS Pago |
|---|---|---|---|---|---|---|

- "Mês de Referência" por extenso: `Fevereiro/2026` (não `02/2026`).
- Linha final "TOTAL" somando as colunas de valor **com fórmula** (`=SUM(...)`), nunca
  número fixo.
- **A ordem das linhas é sempre cronológica (por competência e, dentro do mês, por
  número da nota) — nunca ordem alfabética de nome de arquivo.** Isso vale tanto para
  o quadro da petição quanto para qualquer PDF consolidado de notas (ver caso-limite
  abaixo, na seção de organização para protocolo). Ordenar por data ao ler os arquivos
  na etapa de extração evita ter que reordenar depois.
- Existe também uma variante mais resumida (uma linha por competência, não por nota:
  Período de Apuração | Base de Cálculo | Data do Pagamento | ISS Indevidamente
  Recolhido + TOTAL) usada em alguns modelos de petição mais genéricos — usar a versão
  por nota (mais detalhada) como padrão na planilha de triagem. **Correção
  (06/08/2026, caso Ganso):** o modelo real de precedente usado (ver seção de petição
  abaixo) usa, na prática, uma tabela **por nota** dentro do próprio corpo da petição
  (colunas Incidência | NF | Valor NF | ISS Pago), não a versão resumida por
  competência — a versão a usar dentro do texto da petição depende do modelo/precedente
  real que o Pedro fornecer para aquele tipo de réu, não é uma regra fixa única; sempre
  espelhar a granularidade da tabela do modelo/precedente mais recente.
- **Considere sempre incluir também uma aba/quadro "Consolidado por Mês"** (uma linha
  por competência, somando todas as notas do mês em vez de listar nota a nota) além do
  quadro por nota — é uma visão que o advogado costuma pedir em seguida, então vale
  gerar as duas de saída sem esperar o pedido explícito. Nessa consolidação, o universo
  de meses tem que ser a união dos meses com nota fiscal E dos meses com DAS/Extrato
  (não só os meses com nota) — um mês sem nenhuma NF na pasta ainda pode ter DAS "não
  pago" e precisa aparecer na lista, sinalizado como "nenhuma nota fiscal encontrada
  para este mês", em vez de desaparecer silenciosamente do quadro. **Quando o caso tem
  mais de uma cidade/município, o quadro consolidado por mês deve ter a cidade como
  parte da chave de agrupamento** (Cidade + Competência, não só Competência) — cada
  cidade tem seu próprio ente tributante e pode ter meses "vazios" diferentes.
- **Casos com mais de um município ao longo do tempo (empresa que mudou de domicílio
  fiscal)**: o quadro "por nota" deve ter uma coluna "Cidade (Réu)" e recomenda-se
  destacar visualmente cada cidade (cor de preenchimento distinta) — isso deixa claro
  para o advogado que esse não é um quadro único de uma ação, e sim o material de apoio
  para 3 ações distintas (uma por Município réu). Documentar essa recomendação
  explicitamente na aba de pendências/observações da planilha. **Considerar também
  abas dedicadas por cidade** (uma aba "Cidade - X" por município, com a tabela de notas
  daquela cidade e duas seções de texto "O QUE TEMOS"/"O QUE ESTÁ FALTANDO" específicas
  dela) além das abas consolidadas — ver nota no início da skill sobre o caso Ganso.

**Como preencher "Valor do ISS" e "Valor do ISS Pago" por regime:**
- **Fora do Simples Nacional:** usar o valor do ISS que já vem impresso na própria NF
  (não precisa estimar) — ou calculado a partir da alíquota impressa quando a
  prefeitura não imprime um campo de valor de ISS separado (ver nota sobre Barueri
  acima). "Data do ISS Pago" vem da guia de recolhimento daquela nota/competência. Se a
  guia só trouxer a **data de vencimento** (não uma data de pagamento efetivo separada),
  usar o vencimento e **anotar explicitamente na célula/observação que é a data de
  vencimento da guia, não necessariamente a data real do pagamento** — não apresentar
  como se fosse a data de pagamento confirmada quando o documento não traz esse dado.
  **Quando o comprovante é um "Resumo das Declarações" agregado por competência (sem
  data de pagamento individual por nota, caso Benassi)**, deixar "Data do ISS Pago"
  como "Não disponível — comprovante traz apenas status agregado por competência" e
  registrar isso como pendência a resolver com a contabilidade antes do protocolo (não
  é um erro de extração, é uma limitação real do documento).
- **Simples Nacional:** a NF não tem ISS individual (vem 0,00). Como o ISS é pago de
  forma consolidada no DAS mensal, **estimar o ISS de cada nota por rateio
  proporcional**: `ISS da nota = Valor da nota × (ISS do DAS da competência / Receita
  Bruta do PA da competência)` — usando sempre o ISS do **item 6.1** do Extrato (nunca a
  linha ISS do item 6 nem o item 3/4 — ver seção acima), que é exato por competência;
  só a divisão *dentro* do mês entre notas é uma estimativa. "Valor do ISS Pago" e
  "Data do ISS Pago" só devem ser preenchidos quando o DAS daquela competência já
  consta como pago no item 6.2 do Extrato — competência com DAS ainda não pago fica sem
  esses dois campos, sinalizada à parte. **Deixar sempre explícito no quadro (nota de
  rodapé/observação) que o valor por nota é estimado por rateio**, já que não é um
  número que aparece literalmente em nenhum documento — o advogado responsável deve
  validar essa metodologia antes de protocolar. O total do mês, porém, é sempre o valor
  real do item 6.1, não estimado.
- Meses sem Extrato/DAS disponível não têm base para estimar ISS — deixar em branco e
  sinalizar "sem Extrato/DAS para o mês" na coluna de observação, em vez de omitir a
  linha (é melhor mostrar a lacuna do que esconder a nota).

## Observações técnicas de extração
- Muitas NFs de prefeitura são PDFs com fonte customizada/corrompida, ou PDFs gerados
  por "print to PDF" do navegador que só extraem o cabeçalho da página (URL, data),
  sem o corpo do documento. Nesses casos, extração de texto simples não é suficiente:
  baixe o arquivo, rasterize a página em imagem (`pdftoppm -png -r 200`) e leia via
  OCR (`tesseract`) ou visão — ou, para lotes pequenos, usar diretamente a ferramenta
  `Read` (que renderiza o PDF visualmente na conversa), especialmente quando o
  `pdftotext` retorna texto tecnicamente presente mas embaralhado por fonte customizada
  (não apenas quando retorna vazio — ver nota sobre Américo Brasiliense acima). **Defina
  `OMP_THREAD_LIMIT=1` antes de chamar
  `tesseract`** — nesse tipo de sandbox o tesseract multithread pode ficar ~8x mais
  lento (10s+ por página) só por overhead de thread; com a variável setada cai para
  ~1-1.5s por página. Isso costuma funcionar bem mesmo sem pacote de português no OCR
  (`tesseract-ocr-por` normalmente não está instalado e não dá para instalar sem root),
  mas sempre confirme os campos críticos (valores, CNPJ, competência). **Usar `--psm 4`
  (segmentação de coluna única) rende melhor que o padrão (`--psm 3`) tanto para notas
  fiscais de prefeitura quanto para guias DAM-SP** — o layout em tabela com múltiplas
  colunas confunde a segmentação automática do modo padrão.
- Cada chamada de bash tem timeout de ~45s — processar OCR em lotes de ~15-20 arquivos
  por chamada (não tentar rodar em background com `nohup`/`&`, processos em segundo
  plano não sobrevivem entre chamadas de bash nesse ambiente). **Em lotes muito
  próximos do limite (ex.: 17 arquivos de 1 página cada), o próprio output do comando
  bash pode estourar o limite de tokens da ferramenta mesmo sem erro de execução** —
  isso não está ligado a arquivos multipágina nem a erros de OCR; aconteceu com um
  lote homogêneo de arquivos simples só por acumular texto de retorno. **Reduzir para
  lotes de ~8 arquivos por chamada quando o lote anterior de 15 já tiver estourado**,
  em vez de tentar depurar a causa — o ajuste de tamanho resolve sem precisar
  investigar mais.
- Comprovantes tipo "Resumo das Declarações" são tabelas com bordas que confundem OCR
  padrão — usar modo de segmentação de coluna única (ex. `--psm 4` no Tesseract)
  melhora a leitura linha a linha. O mesmo vale para as guias DAM-SP de São Paulo.
- Sempre que a pasta enviada for uma amostra parcial (nem todas as notas do período),
  não trate ausências na pasta como lacunas reais sem antes verificar contra o
  comprovante consolidado do ano/mês E sem confirmar via navegador que o conector
  realmente está listando tudo (ver seção "ATENÇÃO" acima). Se mesmo assim faltar, é
  uma lacuna de documentação real a resolver com a contabilidade do cliente.
- Ao encontrar uma pasta de "Contratos de Serviço/Propostas" com muito menos arquivos
  do que NFs referenciando propostas distintas, isso é, em si, um achado a reportar —
  mas confirme primeiro que não é o mesmo problema de listagem incompleta.
- **Extrair o número da nota a partir do nome do arquivo, não só via regex no texto/OCR,
  sempre que o nome do arquivo já contiver esse número** (ex.: "31 - SP.pdf" → nota 31;
  ou o padrão "Ano - Mês - Nº" usado no caso Benassi, ex.: "2025 - 6 - 45.pdf" → mês 6,
  nota 45). Regex sobre texto de PDF em `-layout` (colunas lado a lado) ou sobre OCR é
  frágil para esse campo especificamente — o cabeçalho "Número da Nota" e o valor
  numérico costumam ficar em posições de coluna diferentes, gerando concatenações
  erradas com outros números da página (ex.: um código de autenticidade de 5 dígitos
  capturado no lugar do número da nota real). O nome do arquivo, quando o próprio
  escritório/cliente já nomeou os PDFs com o número da nota, é uma fonte muito mais
  confiável — usar como padrão primário e o texto extraído/OCR só como campos
  complementares (valor, ISS, competência, tomador).
- **Cuidado ao ORDENAR arquivos pelo padrão "Ano - Mês - Nº" no nome — `sorted()`/`ls`
  simples faz ordenação alfabética (de texto), não numérica, e isso quebra a ordem
  cronológica sempre que há meses/números de 1 e 2 dígitos misturados no mesmo ano**
  (caso Benassi, 07/08/2026: um primeiro merge de NFs por ano usou `sorted(glob(...))`
  puro, e o resultado ficou "01, 10, 11, 12, ..., 02, 03, ..." em vez de "01, 02, 03,
  ..., 10, 11, 12" — outubro e novembro apareceram antes de fevereiro dentro do bloco
  de 2025, porque a string "10" vem antes de "2" em ordem alfabética). **Detectado
  porque o Pedro perguntou diretamente "você organiza as notas por data sempre?"** — o
  problema não tinha aparecido em nenhuma validação anterior (contagem de páginas batia
  normalmente, só a ordem interna estava errada). **How to apply:** ao listar arquivos
  de NF para merge/exibição, nunca usar `sorted(glob.glob(...))` puro quando o nome
  tiver números variáveis de dígitos — extrair mês e número da nota com regex (ex.:
  `re.search(r'(\d{4})\s*-\s*(\d{1,2})\s*-\s*(\d{1,3})', nome_arquivo)`, tolerante a
  espaçamento inconsistente como `"2024 -1 - 6.pdf"` ou `"2025 -11 -83.pdf"`) e ordenar
  por `(int(mês), int(número_da_nota))` como chave — nunca pela string do nome do
  arquivo. Aplicar esse cuidado tanto na extração para a planilha (coluna "Competência"
  já resolve isso ali, porque cada linha vira uma linha de planilha independente da
  ordem de leitura) quanto, principalmente, **na hora de fazer o merge de PDFs em um
  único arquivo por ano** (bloco 6.x-9.x da pasta de protocolo), onde a ordem das
  páginas dentro do PDF final é visível e permanente. Depois de corrigir, sempre
  reabrir o PDF final e conferir a ordem (ex.: primeira e última nota de cada parte)
  como parte da validação de página, não só a contagem total.
- **Ao extrair valores monetários de OCR, usar regex tolerante ao símbolo de moeda
  corrompido** — o Tesseract sem pacote de português frequentemente lê "R$" como "R§$",
  "RS", ou variações parecidas. Preferir `R.{0,3}\$` (ou equivalente) a `R\$` literal
  nas regexes de valor, senão o campo fica `None` silenciosamente em uma fração dos
  arquivos do lote sem nenhum erro aparente — só um `None` que passa despercebido se
  você não conferir a lista de "campos faltantes" ao final da extração.
- **Depois de qualquer extração em lote (OCR ou texto), sempre gerar e conferir a lista
  de arquivos com campo crítico faltante** (ex.: `[r["arquivo"] for r in registros if
  r["valor_iss"] is None]`) antes de seguir para a planilha — isso pega tanto arquivos
  que realmente precisam de revisão manual quanto regexes frágeis a corrigir (como os
  dois itens acima), e é muito mais barato corrigir a regex e re-rodar o lote do que
  descobrir na planilha final que 30 notas de um total de 64 estão com um campo vazio.
- **Verificação por amostragem com a ferramenta `Read` (não só OCR em lote)**: depois
  que a planilha de triagem já está pronta, vale reabrir 2-3 notas de anos/layouts
  diferentes (e 1 comprovante) com `Read` e conferir visualmente os valores extraídos
  contra a célula correspondente na planilha, mesmo sem ter feito a extração original
  nessa sessão (caso Benassi, 07/08/2026: confirmou que uma triagem feita em sessão
  anterior batia exatamente com os documentos-fonte, sem precisar reprocessar as 66
  notas). É uma checagem rápida e barata antes de seguir para a próxima etapa do
  pipeline (organização para protocolo, petição), e detecta tanto erros de extração
  quanto planilhas desatualizadas em relação a arquivos que mudaram depois — mas note
  que essa amostragem NÃO teria pego o bug de ordenação alfabética acima (os valores de
  cada nota estavam certos, só a ordem entre notas estava errada); para pegar esse tipo
  de erro, é preciso olhar a sequência de várias notas seguidas, não só o conteúdo de
  cada uma isoladamente.

## Saída esperada (etapa de triagem)
1. **Planilha de triagem** consolidada com, no mínimo: aba de notas extraídas (nº,
   competência, tomador, valor, ISS, sinalização de revisão), aba de cruzamento com o
   comprovante do regime aplicável (destacando competências sem declaração
   correspondente ou com divergência), aba com os dados brutos do comprovante (dos
   itens 6/6.1/6.2 do Extrato, quando Simples Nacional, ou das guias/DAM individuais
   quando fora do Simples). Em casos com mais de uma cidade, incluir a cidade como
   coluna em toda aba, considerar uma aba de cruzamento por cidade quando o formato do
   comprovante difere entre elas (ex.: São Paulo com guia individual vs. Barueri/Praia
   Grande sem nenhum comprovante no dossiê), e considerar abas "Cidade - X" dedicadas
   com o resumo "temos/falta" de cada município (ver nota no início da skill).
2. **Lista de documentos faltantes** a solicitar da contabilidade/cliente (dos 5 itens
   do dossiê, e de propostas/contratos referenciados em NFs mas não encontrados na
   pasta), incluindo competências com DAS "não pago" no Extrato como pendência de
   confirmação (ver seção B acima) — não presumir se foi erro de extração ou pagamento
   por via alternativa sem o cliente confirmar. Incluir também lacunas de numeração de
   notas (números que "pulam" na sequência dentro de uma mesma cidade) como pendência a
   confirmar — pode ser nota cancelada, nota não enviada no dossiê, ou nota de outro
   cliente/serviço que não faz parte da ação. **Assim que o cliente/advogado confirmar
   uma pendência dessas como "não é problema" (ex.: números que pulam são normais),
   atualizar a planilha para refletir isso — não deixar o alerta antigo.** Considerar
   formalizar essa lista também como e-mail de cobrança à contabilidade (ver seção
   "Envio de pendências à contabilidade por e-mail" acima), não só como aba da planilha.
3. **Quadro de restituição** no formato do escritório (ver seção acima), por nota E
   consolidado por mês, pronto para colar no corpo da petição, com a metodologia de
   estimativa do ISS documentada.

## Organização da documentação para protocolo

### Padrão de numeração do escritório
O Pedro forneceu, via exemplo de um caso real anterior ("Calveo Agenciamento de
Sports"), a ordem/numeração padrão que o escritório usa para organizar os PDFs de
protocolo. Adaptar essa numeração ao perfil do caso (esporte vs. audiovisual), mas
manter a mesma estrutura de blocos:

| # | Categoria | Observação |
|---|---|---|
| 0 | Inicial (docx "padrão" do modelo + PDF final da minuta) | dois arquivos, um docx e um PDF |
| 1 | Procuração | assinada pelo cliente |
| 2 | Documento pessoal do representante (RG/CNH) | digitalizado |
| 2.1 | Guia de custas | gerada só no ato do protocolo |
| 2.2 | Comprovante de custas | gerado só no ato do protocolo |
| 3 | Contrato Social | |
| 4 | Comprovante de inscrição e situação cadastral (Cartão CNPJ) | emitir na Receita Federal |
| 5.x | Contrato de Imagem (esporte) OU Propostas/Contratos de Prestação de Serviço (audiovisual), agrupados **por ano**, do mais recente para o mais antigo | um PDF consolidado por ano (dividido em partes se ultrapassar o limite de tamanho — ver abaixo) |
| 6.x–9.x (ou mais, conforme os anos do caso) | Notas Fiscais + Guias de ISS quitadas, agrupadas **por ano**, do mais recente para o mais antigo, e **em ordem cronológica dentro do ano** (mês, depois número da nota — ver nota sobre ordenação alfabética vs. cronológica acima) — cada ano gera um par de números (ex.: `6.1 NF 2026` / `6.2 DAS 2026`, `7.1 NF 2025` / `7.2 DAS 2025`, ...) | um PDF consolidado por categoria/ano (idem, dividir se necessário) |
| 10 | Certidão Negativa de Débitos Tributários | emitir perto da data real do protocolo (validade curta) |

**Why:** é o padrão real de organização que o Pedro já usa em casos anteriores — seguir
a mesma ordem/numeração torna a pasta reconhecível para qualquer pessoa do escritório
que for protocolar, sem precisar reaprender uma estrutura nova por caso.

**How to apply:** ao chegar nessa etapa de um caso novo, perguntar ao Pedro (a menos que
ele já tenha indicado o padrão nesta sessão) que documentos vão para cada bloco 5.x/6.x
em diante — em casos de esporte é "Contrato de Imagem" por clube/ano (ou por
tomador/período, se houver mais de um tomador ao longo do tempo — ver caso Benassi
abaixo); em audiovisual é "Propostas e Contratos de Prestação de Serviço" por ano (pode
não ser possível separar por cliente/proposta individual quando o volume é alto — nesse
caso, consolidar todas as propostas do ano num único PDF, ou em partes, é aceitável,
como no caso 8 Milímetros). **O comprovante do bloco 6.2+ nem sempre é uma "guia"
individual** — quando o formato do comprovante do município é um relatório anual
consolidado ("Resumo das Declarações", ver regime A acima), o bloco 6.2/7.2/etc. é
simplesmente esse PDF anual único (não há guia por competência a juntar separadamente),
como no caso Benassi (07/08/2026).

### Caso-referência de 1 município simples: Benassi (07/08/2026)
Primeiro caso testado depois do Ganso que **não** tem mudança de domicílio fiscal — bom
contraponto para lembrar que nem todo caso precisa de subpastas por cidade. Estrutura
final: bloco 1 (Procuração), bloco 5.1 (único Contrato de Imagem disponível no dossiê,
dividido em 2 partes por tamanho — ver caso-limite de arquivo único abaixo), blocos
6.x-9.x (2026, 2025, 2024, 2023, cada um com NF consolidada do ano + o "Resumo das
Declarações" anual como comprovante). Blocos 0, 2, 2.1, 2.2, 3, 4 e 10 ficaram
pendentes (petição ainda não elaborada; documento pessoal, Contrato Social, Cartão CNPJ
e CND ausentes do dossiê) — listados no `PENDENCIAS.txt` e cobrados à contabilidade por
e-mail no mesmo dia (ver seção "Envio de pendências à contabilidade por e-mail" acima).
**Também foi neste caso que o bug de ordenação alfabética vs. cronológica (ver seção de
observações técnicas de extração) apareceu e foi corrigido** — os blocos 6.1 a 9.1
tiveram que ser regerados depois da primeira entrega.

### Casos com mais de um município/réu ao longo do tempo — uma pasta por ação
**Testado com sucesso no caso Ganso (06/08/2026):** quando a empresa mudou de domicílio
fiscal e o caso vai virar 3 ações distintas (uma por Município réu), **criar uma
subpasta de nível superior por cidade** (ex.: `Protocolo/São Paulo/`,
`Protocolo/Barueri/`, `Protocolo/Praia Grande/`), cada uma com sua própria numeração
0-10 completa e independente — não misturar notas de cidades diferentes no mesmo bloco
numerado, mesmo que sejam do mesmo cliente/CNPJ, porque cada ação é protocolada em
separado, com petição, réu e processo próprios. **Quando o caso tem um único município
durante todo o período (ex.: Benassi), essa subdivisão não é necessária — os blocos
0-10 vão direto na pasta `Protocolo/` do caso, sem nível de subpasta por cidade.**

- **Bloco 5.x (documento de origem, ex.: Contrato de Imagem) costuma ser idêntico para
  todas as cidades** (é o mesmo contrato/relação contratual, independente de onde o ISS
  foi recolhido) — nesse caso, montar o bundle consolidado uma vez só e copiar o mesmo
  arquivo (ou mesmas partes, se dividido) para a pasta 5.x de cada cidade, em vez de
  reprocessar o merge 3 vezes.
- **Se houver mais de uma cópia do mesmo documento no dossiê** (ex.: duas versões do
  contrato original, aparentemente idênticas), usar a versão mais completa/nomeada como
  "assinado por todos"/final, e **não incluir a duplicata no bundle** — só mencionar a
  existência dela no `PENDENCIAS.txt`, perguntando ao Pedro se há algum motivo para
  manter as duas (ex.: uma é rascunho e outra é a via registrada em cartório).
- **Blocos 6.x+ (Notas Fiscais + Guias) são específicos de cada cidade** — cada cidade
  tem sua própria contagem de anos/blocos, começando do 6 em cada pasta (não continuar a
  numeração entre pastas).
- Gerar um `PENDENCIAS.txt` **por pasta/cidade**, não um único arquivo para o caso
  inteiro — cada ação terá pendências específicas (ex.: no caso Ganso, só São Paulo
  tinha guias de recolhimento parcialmente disponíveis; Barueri e Praia Grande não
  tinham nenhuma) e um advogado revisando uma ação específica não deveria precisar
  filtrar um `PENDENCIAS.txt` genérico para achar o que é relevante para aquela pasta.

**Why:** replicar a mesma lógica de "uma ação = um conjunto de documentos completo e
autocontido" já usada para decidir sobre abas separadas na planilha de triagem — reduz o
risco de alguém pegar a pasta errada de anexos na hora de protocolar cada ação.

**How to apply:** ao identificar que um caso tem mais de um município/réu (ver seção de
perfis de cliente acima), perguntar/confirmar a divisão em pastas separadas via
`AskUserQuestion` antes de montar os PDFs (junto com a pergunta de escopo abaixo), e
seguir a estrutura acima — bloco 5.x compartilhado, blocos 6.x+ por cidade, um
`PENDENCIAS.txt` por pasta. Quando o caso tem um único município, pular direto para a
montagem sem essa etapa.

### Escopo: quais NFs e guias entram na pasta — pergunta que muda de resposta por regime
**Antes de reunir os arquivos, definir com o Pedro quais NFs e guias entram na pasta —
não é necessariamente "tudo que existe no dossiê".** Mas **a pergunta certa depende do
regime tributário do caso — não reaproveitar cegamente a mesma resposta de um caso
anterior**:

- **Caso Simples Nacional (8 Milímetros, confirmado 05/08/2026 via `AskUserQuestion`):**
  só as **Notas Fiscais das competências efetivamente pagas** (as que entraram no
  pedido de restituição — ver seção sobre DAS "não pago" acima) e só as **guias DAS já
  quitadas** (mesmo critério) devem compor os anexos 6.x-9.x — NFs/DAS de competências
  "não pago" (excluídas do pedido) não entram na pasta de protocolo, para não gerar
  contradição entre o que a petição alega e o que está anexado. Isso faz sentido porque,
  nesse regime, "não pago" é um status literal e verificável no próprio Extrato.
- **Caso fora do Simples Nacional (Ganso, confirmado 06/08/2026 via
  `AskUserQuestion`; Benassi, confirmado 07/08/2026 da mesma forma):** nos dois casos o
  Pedro optou por **incluir todas as notas emitidas, mesmo sem guia de recolhimento
  correspondente no dossiê** — porque nesse regime a nota em si já é presunção de
  recolhimento (ver seção A acima), e a falta de guia é só uma lacuna documental a ser
  preenchida depois, não um indício de que o ISS não foi pago. **Nesse cenário, ao
  invés de excluir as notas sem comprovante, incluir todas e documentar claramente no
  `PENDENCIAS.txt` quais competências ainda precisam de confirmação/comprovante
  individual assim que a contabilidade enviar.** Com duas confirmações seguidas nesse
  sentido, "todas as notas emitidas" é a resposta mais provável para novos casos fora
  do Simples — mas continuar perguntando via `AskUserQuestion` em vez de presumir, já
  que a pergunta em si é rápida e evita qualquer engano num caso atípico.
- Já os blocos 5.x (propostas/contratos) normalmente entram por ano completo em
  qualquer regime, sem filtro por competência paga — são documentos de suporte
  comercial, não prova de pagamento de tributo.

**Why:** anexar comprovante de uma competência que a própria petição não está pedindo
restituição gera inconsistência processual (regime Simples) — mas excluir notas
legítimas só por falta de comprovante, num regime onde a nota já basta como presunção,
tiraria força do pedido sem necessidade.

**How to apply:** sempre perguntar/confirmar esse escopo antes de montar os PDFs
consolidados via `AskUserQuestion`, ajustando as opções oferecidas ao regime do caso
(não usar a mesma pergunta genérica dos dois regimes) — para regime fora do Simples,
oferecer "todas as notas emitidas" vs. "só as com comprovante confirmado" como opções;
para Simples Nacional, oferecer "só competências pagas" vs. "todas".

### Limite de tamanho por arquivo: nenhum PDF do protocolo deve passar de 5MB
O Pedro pediu explicitamente (caso 8 Milímetros, 05/08/2026) que nenhum arquivo da pasta
de protocolo ultrapasse 5MB, para evitar problemas no upload do sistema do
tribunal/PJe (a maioria dos sistemas de protocolo eletrônico tem um limite de tamanho
por arquivo, frequentemente 5-10MB). **Aplicar esse limite como regra padrão em todo
caso futuro, não só quando pedido de novo** — sistemas de protocolo eletrônico raramente
aceitam anexos maiores que isso.

Quando o merge de uma categoria/ano (ex.: `5.1 Propostas ... 2025-2026.pdf`,
`7.1 Notas Fiscais ... 2025.pdf`) resultar em um arquivo acima de 5MB, dividir em várias
partes sequenciais em vez de comprimir/rasterizar o PDF (comprimir perderia
qualidade/pesquisabilidade do texto, o que pode ser exigido pelo tribunal):

1. Usar um **limite de segurança de ~4.5MB** (não 5MB exato) ao decidir onde cortar,
   para sobrar margem de erro de arredondamento e overhead do merge.
2. Fazer o corte respeitando a integridade de cada documento-fonte — nunca dividir um
   único PDF de origem (uma nota fiscal, uma proposta) no meio; a unidade mínima de
   corte é sempre um arquivo-fonte inteiro. Empacotar (bin-packing guloso, **sempre
   sobre a lista de arquivos-fonte já em ordem cronológica** — ver nota sobre ordenação
   acima, nunca em ordem alfabética de nome de arquivo) os arquivos-fonte em grupos
   cuja soma de bytes não ultrapasse o limite, fechando o grupo atual e abrindo um novo
   sempre que o próximo arquivo faria a soma passar do limite. **Quando os
   arquivos-fonte individuais já são grandes (ex.: contratos escaneados em alta
   resolução, 1-4MB cada um), o resultado do bin-packing pode virar "uma parte por
   arquivo-fonte"** (caso Ganso: bundle de 3 contratos de ~1,2MB/2,7MB/4,1MB virou 3
   partes de 1 arquivo cada, porque qualquer par já passava de 4,5MB) — isso é o
   comportamento correto do algoritmo, não um sinal de bug; não forçar menos partes só
   porque "parece exagero" para um bundle pequeno.

   **Caso-limite: um único arquivo-fonte sozinho já ultrapassa o limite** (caso Benassi,
   07/08/2026: o único Contrato de Cessão de Imagem do dossiê tem 10 páginas e 7,7MB —
   não há múltiplos arquivos-fonte para fazer bin-packing, é um documento só). Nesse
   caso, excepcionalmente, dividir **por intervalo de páginas dentro do próprio
   arquivo** (ex.: metade das páginas em cada parte) — a regra de "nunca dividir um
   documento no meio" pressupõe que existam vários arquivos-fonte menores a reagrupar;
   quando há um só, dividir por página é a única opção viável sem recorrer a
   compressão/perda de qualidade. Nomear as partes normalmente com o sufixo
   `(Parte N de M)` (ver item 3 abaixo) e deixar explícito no `PENDENCIAS.txt` que,
   nesse bloco específico, a divisão foi por página (dentro de um único documento), não
   por arquivo-fonte — para não parecer que o documento foi cortado ao meio por engano.
3. Nomear cada parte com sufixo `(Parte N de M)` antes da extensão, ex.: `5.1 Propostas
   e Contratos de Prestação de Serviço - 2025-2026 (Parte 3 de 13).pdf` — mantém a
   ordenação alfabética natural (Parte 1, 2, ..., 10, 11 pode ordenar como texto de
   forma não numérica em alguns visualizadores; se o caso tiver mais de 9 partes,
   considerar prefixo com zero — `Parte 01`, `Parte 02` — para ordenação correta).
4. **Só dividir os blocos que realmente excedem o limite** — não dividir por sistema
   um bloco pequeno (ex.: guias/comprovantes anuais raramente passam de 1MB); calcular
   o tamanho total de cada categoria/ano antes de decidir dividir. **Notas fiscais de
   prefeitura individuais costumam ser pequenas (80-230KB cada)** — um bloco anual de
   3-25 notas normalmente fica na casa de poucos MB (ex.: caso Benassi: 5 notas de 2023
   = 592KB; 22 notas de 2024 = 2,2MB), bem abaixo do limite — só o bloco com o maior
   volume de notas do caso (ex.: 36 notas de 2025 no caso Benassi, 9,4MB no total)
   tende a precisar de divisão. O risco de estourar 5MB é maior nos blocos 5.x de
   contratos/propostas escaneados em alta resolução do que nos blocos de notas fiscais.
5. Depois de dividir, **validar que a soma de páginas das partes bate exatamente com o
   total do merge original** (reabrir cada parte com `PdfReader` e somar `len(pages)`) —
   confirma que nenhum arquivo-fonte foi perdido ou duplicado no processo de divisão.
   Vale tanto para o bin-packing por arquivo-fonte (item 2, caso normal) quanto para o
   corte por página de um único arquivo-fonte grande (item 2, caso-limite): reabrir
   cada parte e comparar a soma de páginas com o total esperado (soma dos arquivos-fonte
   do bloco, ou páginas do documento único, respectivamente). **Essa validação de
   contagem não pega erro de ORDEM (ver nota acima) — depois de validar a contagem,
   também abrir a primeira e a última página de cada parte (via `Read` ou
   `pdftotext`/OCR pontual) e conferir se a competência bate com a esperada para aquele
   ponto da sequência** (ex.: a última página da Parte 1 de um bloco anual deveria ser
   uma competência anterior à primeira página da Parte 2).
6. Deixar explícito no `PENDENCIAS.txt` (ou mensagem final ao usuário) que um bloco foi
   dividido em partes e por quê, para não parecer um erro de organização.

**Why:** o Pedro relatou histórico de "problemas no protocolo" com arquivos grandes —
provavelmente rejeição/erro de upload do sistema do tribunal. Preservar a integridade de
cada documento-fonte (não cortar no meio de uma nota fiscal) é importante porque cada
anexo pode ser citado individualmente na petição ou pedido pelo cartório.

**How to apply:** ao gerar qualquer PDF consolidado nessa etapa, checar o tamanho do
resultado antes de entregar; se > 5MB, aplicar o processo de divisão acima antes de
copiar para a pasta final — não esperar o usuário reclamar do tamanho.

### Método técnico: consolidar por categoria/ano em um PDF por bloco
1. Listar os arquivos elegíveis de cada bloco (ex.: para NF por ano: filtrar a planilha
   de triagem/quadro pela lista de competências pagas [ou todas, conforme a resposta à
   pergunta de escopo acima], cruzar com o nome de arquivo/competência de cada NF na
   pasta do ano correspondente). **Se a pasta do caso tiver arquivos `*_merged.pdf`
   soltos na raiz (lotes de upload originais)**, não usar como fonte — partir sempre dos
   arquivos individuais por nota em `NF/<ano>/` (ver nota na seção "ATENÇÃO" acima).
   **Ordenar essa lista pela chave cronológica (mês, número da nota extraídos por
   regex do nome do arquivo — nunca `sorted()` puro sobre o nome)** antes de passar
   para o merge — ver nota detalhada na seção "Observações técnicas de extração" acima;
   esse é o passo onde o bug de ordenação alfabética foi introduzido no caso Benassi.
2. **Usar `pypdf` (`PdfReader`/`PdfWriter.add_page()` em loop) para o merge, não
   `qpdf` via linha de comando** — `qpdf --empty --pages ... -- out.pdf` já falhou
   nesse ambiente com "unexpected character" em nomes de arquivo com certos caracteres
   especiais/espaços, mesmo em nomes sem acentuação incomum. `pypdf` não teve esse
   problema em nenhum dos casos testados (inclusive com arquivos de origem que geram o
   aviso benigno `incorrect startxref pointer`/`parsing for Object Streams` no stderr —
   isso não impede a leitura/merge, é só um aviso de estrutura interna do PDF).
3. **Antes de rodar o merge de um lote grande, testar a abertura de cada arquivo
   individualmente** (`PdfReader(f)` num loop, sem side-effect) para pegar de uma vez só
   os arquivos "cloud-only" ainda não sincronizados do OneDrive (ver seção específica
   acima) — resolver todos via `Read` antes do merge de verdade, em vez de descobrir um
   por um no meio do processo. **Esse teste às vezes não encontra nenhum arquivo
   problemático** (caso Benassi: todos os 66 PDFs já estavam sincronizados) — rodar o
   teste de qualquer forma, mas seguir direto para o merge se ele vier limpo.
4. Nomear cada PDF consolidado com o número do bloco + categoria + ano, ex.:
   `6.1 Notas Fiscais - 2026.pdf`, `5.2 Propostas e Contratos de
   Prestação de Serviço - 2024.pdf` — mantém a pasta ordenável alfabeticamente na mesma
   ordem lógica do protocolo. Se o bloco precisar ser dividido em partes por tamanho
   (ver seção "Limite de tamanho" acima), aplicar o sufixo `(Parte N de M)` no mesmo
   passo, antes de escrever o arquivo — mais simples que dividir depois de já ter
   escrito um único PDF grande.
5. Depois de montar a pasta final, **validar reabrindo cada PDF gerado com
   `PdfReader`** e conferir a contagem de páginas contra o número de arquivos-fonte
   esperado (somando as partes, se houver divisão), **e conferir também a ordem**
   (primeira/última competência de cada parte, ver item 5 da seção "Limite de tamanho"
   acima) antes de entregar ao usuário — pega merges truncados, divisões que
   perderam/duplicaram arquivos, e problemas de ordenação por falha silenciosa.
6. Gerar um arquivo `PENDENCIAS.txt` (ou seção equivalente na resposta ao usuário)
   listando os itens do padrão de numeração que **não** puderam ser preenchidos por
   falta de documento no dossiê (tipicamente: Procuração, Documento pessoal
   escaneado, Comprovante de inscrição/situação cadastral, Certidão Negativa), e
   mencionando quais blocos foram divididos em partes por tamanho — isso é sempre parte
   da entrega dessa etapa, não um afterthought. **Em casos multi-cidade, gerar um
   `PENDENCIAS.txt` por pasta/cidade** (ver seção acima). Reaproveitar a lista de
   pendências já cobradas por e-mail à contabilidade (ver seção específica acima) como
   base do `PENDENCIAS.txt`, em vez de redigir uma lista nova do zero.
7. **Copiar o resultado final para a pasta do caso montada via bash**
   (`/sessions/<sessão>/mnt/<PastaDoCaso>/Protocolo/...`), nunca deixar só em `/tmp` —
   ver nota na seção "Salvando entregáveis em pasta do usuário" acima. **Se precisar
   corrigir/substituir um arquivo já copiado para lá**, gerar a nova versão com o
   mesmo nome e sobrescrever via `cp` — a pasta do caso não permite `rm`/renomear (ver
   nota específica na seção "Salvando entregáveis em pasta do usuário").

**Why:** replicar exatamente o padrão testado no caso 8 Milímetros (merge de até 646
páginas/77 arquivos sem falha, depois redividido em 13 partes de ~4MB cada para respeitar
o limite de 5MB), no caso Ganso (merge multi-cidade com bloco 5.x compartilhado e blocos
6.x+ por cidade) e no caso Benassi (caso-limite de um único arquivo-fonte grande demais,
dividido por página, e o bug de ordenação alfabética vs. cronológica) evita redescobrir
as mesmas armadilhas (qpdf, arquivos cloud-only, limite de tamanho, estrutura
multi-réu, ordenação) em cada caso novo.

**How to apply:** ao chegar nessa etapa num caso novo, seguir os passos acima na ordem,
adaptando só a lista de blocos/anos/cidades ao caso concreto, e sempre checar o tamanho
final de cada arquivo contra o limite de 5MB e a ordem cronológica das páginas antes de
considerar a pasta pronta.

## Elaboração da petição inicial

### Método: editar um modelo docx real existente, não recriar do zero
O escritório usa modelos/precedentes reais em uso (docx com fundamentação jurídica
pronta, notas de rodapé ou blocos de texto já preenchidos, letterhead da banca, estilo
de fonte Book Antiqua e um bloco de assinatura padrão). **A abordagem correta é sempre
editar um desses modelos via XML — nunca recriar a petição do zero com `docx`
(npm)/docx-js.** Recriar do zero perde o letterhead, as notas de rodapé formatadas, os
estilos de tabela e a fidelidade ao padrão visual do escritório.

**Qual modelo usar — priorizar precedente real do mesmo tipo de réu sobre modelo
genérico (caso Ganso, 06/08/2026):** quando o Pedro fornecer mais de um modelo/precedente
real (ex.: uma inicial já ajuizada contra o mesmo Município, ou contra um Município
semelhante), **usar o precedente mais específico como base, mesmo que não seja o modelo
genérico "MARCELO"** — no caso Ganso, o Pedro pediu para aguardar e enviou duas petições
reais («Inicial KC Spots» contra o Município de São Paulo, e «Inicial Padrão ISSQN -
Calvelo» contra o Município de Santos), que foram usadas como base em vez do modelo
genérico, porque já tinham a qualificação exata do réu (CNPJ, endereço, Procurador
Geral) e, no caso de KC Spots, um histórico real de disputa de competência JEFP × vara
comum relevante para o mesmo Estado (SP). **Quando o Pedro disser "vou te mandar mais
modelos para você ter" antes de responder perguntas de modelagem, isso é um sinal para
aguardar os novos arquivos antes de prosseguir** — não insistir nas perguntas de
modelagem enquanto os modelos não chegam; e se o próprio Pedro perguntar depois "mandei,
você recebeu?" sem nada ter chegado no chat, é provável que o upload tenha falhado do
lado dele — avisar isso e pedir para reenviar, em vez de assumir erro de leitura.

Passo a passo (testado com sucesso no caso 8 Milímetros e, de forma expandida, no caso
Ganso — 3 petições reais, uma por Município réu, 06/08/2026):
1. `unzip` o `.docx` modelo numa pasta de trabalho, rodar `merge_runs.py` (script da
   skill `docx`) para coalescer runs fragmentados e tornar o texto localizável.
2. Ler `word/document.xml` procurando por marcadores de placeholder: neste modelo,
   trechos a preencher aparecem em **texto vermelho (`w:color w:val="FF0000"`)** e/ou
   entre colchetes (`[NOME DO MUNICÍPIO]`, `[VALOR]`, `XXXXXX`, `00.000,00`). Fazer um
   inventário de todos antes de começar a editar (buscar por `FF0000`, `[`, `XXXX`,
   `00.000,00`) — **um placeholder ficou de fora na primeira passada** (o `[VALOR]` da
   frase "deverá ser restituído à Autora o importe de R$ [VALOR]..." no meio da seção
   4.0) porque a primeira varredura só cobriu os placeholders mais óbvios (cabeçalho,
   partes, tabela, valor da causa). **Sempre repetir a busca por `FF0000`/`[`/`XXXX`
   depois das edições principais, como conferência final**, antes de considerar a
   petição pronta. **Quando o modelo-base é um precedente real (não um template com
   placeholders em vermelho, ex.: KC Spots/Calvelo), não há marcador visual — a
   varredura final passa a ser: `grep` pelo nome do cliente/réu antigo (ex.: "Kaio",
   "Corinthians", "Calvelo") no texto extraído (`pdftotext -layout`) do PDF renderizado,
   para garantir que nenhum resquício do caso original ficou no texto final.**
3. Cada substituição: usar `content.count(old) == 1` (ou o número exato esperado) antes
   de `content.replace(...)`, para nunca substituir a string errada silenciosamente.
   Copiar o trecho XML exato (com todas as tags de formatação) via `content.find()` +
   slicing antes de escrever o "old" do replace — não tentar adivinhar a estrutura XML.
4. Depois de preencher um placeholder que estava em vermelho, **limpar a cor** (`w:color
   w:val="FF0000"` → `w:color w:val="000000"` ou remover o elemento `<w:color>`), senão
   o texto final da petição continua vermelho mesmo depois de preenchido.
5. **Notas de rodapé (`word/footnotes.xml`) são um arquivo separado** do
   `word/document.xml` — a qualificação completa das partes (autora e réu) normalmente
   mora lá, não no corpo do texto (o corpo só tem o nome com uma chamada de nota
   `<w:footnoteReference w:id="N"/>`). Editar os dois arquivos. **Nota: nem todo modelo
   usa notas de rodapé para qualificação** — os precedentes reais usados no caso Ganso
   (KC Spots/Calvelo) trazem a qualificação completa direto no corpo do texto (parágrafo
   de abertura), sem footnotes — conferir a estrutura do modelo-base antes de assumir
   que a qualificação está em footnotes.xml.
6. **Tabelas (`<w:tbl>`)**: usar regex `<w:tr .*?</w:tr>` (com `re.S`) para listar as
   linhas, identificar cabeçalho/linha(s)-exemplo/linhas vazias/linha TOTAL pela posição
   ou pelo texto, e substituir o bloco de linhas de dados por um conjunto gerado
   programaticamente (uma linha por competência/nota, **em ordem cronológica** — ver
   nota sobre ordenação acima). **Cuidado com `w14:paraId`**: esse
   atributo precisa ser um hex de exatamente 8 dígitos (`[0-9A-F]{8}`) — gerar IDs tipo
   `f"{base+i:08X}"` a partir de uma constante alta (ex. `0x30000000`), nunca prefixar
   com letras como `"R"` (isso quebra a validação e o Word recusa abrir o arquivo).
   `validate.py` pega esse erro (`paraId=... is not valid hex`) — sempre rodar
   `validate.py --original <modelo original>` depois de montar a tabela. **Alternativa
   mais simples testada no caso Ganso: reaproveitar os `w14:paraId`/`w14:textId`
   originais do template de linha, sem gerar novos** — como cada linha nova é gerada por
   substituição de texto dentro de uma cópia do XML da linha-modelo (ver técnica
   "template de linha nativa" abaixo), os IDs originais (válidos, já testados no modelo)
   são preservados automaticamente; só regenerar IDs manualmente é necessário quando se
   monta a tabela do zero via `docx`-js ou template literal Python, não quando se clona
   um `<w:tr>` já existente.
7. Depois de zipar (`zip -Xr saida.docx .` de dentro da pasta descompactada), rodar
   **`validate.py --original <docx original>`** (deve retornar "All validations
   PASSED!") e depois **renderizar em PDF** (`soffice.py --convert-to pdf` +
   `pdftoppm`) para conferir visualmente pelo menos: capa/cabeçalho, qualificação das
   partes com as notas de rodapé (se houver), a tabela de valores (conferir que os
   totais batem fazendo `pdftotext -layout` + grep no valor total esperado), e a página
   final (pedidos, valor da causa, bloco de assinatura). Um `grep` final no texto
   extraído por `FULANO`, `XXXXXX`, `[VALOR]`, `00.000,00` (ou pelo nome do
   cliente/réu do precedente original, se for esse o tipo de modelo-base) confirma que
   não sobrou nenhum resquício do modelo/caso anterior.

### Técnica: gerar tabela de valores clonando um `<w:tbl>` nativo de outro docx
**Testado com sucesso no caso Ganso (06/08/2026), para inserir a tabela "Incidência | NF
| Valor NF | ISS Pago" de 70/20/8 notas em cada uma das 3 petições.** Quando um dos
modelos/precedentes fornecidos já tem uma tabela nativa do Word (`<w:tbl>`) no formato
desejado (bordas, sombreado do cabeçalho, fonte, alinhamento), é mais rápido e mais fiel
visualmente **clonar essa tabela como template de geração** do que montar uma tabela
nova via `docx`-js ou via `<w:tbl>` escrito à mão:

1. Extrair a tabela-modelo (`content.find("<w:tbl>")` até `</w:tbl>` correspondente) de
   um docx que já a tenha (ex.: modelo "Calvelo", que tinha a tabela de valores exata
   nesse formato) para um arquivo `.xml` separado.
2. Com `re.findall(r"<w:tr .*?</w:tr>", tbl, re.S)`, separar a **linha de cabeçalho**
   (primeira), uma **linha de dados de exemplo** (segunda) e a **linha TOTAL** (última,
   geralmente com `gridSpan` mesclando as 3 primeiras colunas). Guardar o prefixo
   (`<w:tbl><w:tblPr>...<w:tblGrid>...`) e o sufixo (`</w:tbl>`) à parte.
3. **Cuidado ao localizar tags `<w:t>` por regex**: o padrão ingênuo `<w:t[^>]*>` também
   casa acidentalmente com `<w:tr `, `<w:tc>`, `<w:tbl>` (porque "`<w:t`" é prefixo
   literal de todos eles) — isso corrompe qualquer split/substituição feita sobre o XML
   da linha. **Usar `<w:t(?=[ >])[^>]*>` (lookahead exigindo espaço ou `>` logo após
   "t")** para casar exclusivamente `<w:t>` e `<w:t ...>`, nunca `<w:tr>`/`<w:tc>`/
   `<w:tbl>`. Validado node a nó: sem o lookahead, `re.split` retorna fragmentos com
   tags de abertura de célula/linha faltando; com o lookahead, cada `<w:t>...</w:t>`
   é isolado corretamente.
4. Gerar cada linha de dados nova clonando a linha-de-exemplo e substituindo, em ordem,
   o conteúdo de cada `<w:t>` (mantendo toda a formatação/`rPr`/bordas ao redor) pelos
   valores da linha real — preservar `xml:space="preserve"` no `<w:t>` quando o valor
   tiver espaços de formatação (moeda alinhada à direita costuma vir como
   `" R$ 1.234,56 "`, com espaço antes/depois).
5. Gerar a linha TOTAL da mesma forma, substituindo só a célula de valor final por
   `=SUM` equivalente calculado em Python (não fórmula do Word — o valor já vem
   consolidado, porque a tabela é estática/texto, não uma planilha embutida).
6. Concatenar prefixo + linha de cabeçalho + todas as linhas de dados + linha TOTAL +
   `</w:tbl>`, e inserir no lugar do placeholder da tabela antiga no `document.xml`
   de destino (ex.: onde o modelo-base tinha uma imagem/screenshot de tabela em vez de
   tabela nativa — ver próxima seção).
7. **Remover artefatos de origem específicos do Excel/planilha colada** que a tabela
   template pode trazer, e que **conflitam com IDs já usados no restante do documento
   de destino**: `<w:bookmarkStart w:id="1" w:name="RANGE!A1:D52"/>` (marcador de range
   colado do Excel) e `<w:permStart w:id="561860123" w:edGrp="everyone"/>` sem
   `<w:permEnd>` correspondente (edição restrita de célula) no cabeçalho da tabela
   clonada. **Isso causa erro de validação `Duplicate id='1' in <bookmarkstart>`** se o
   documento de destino já tiver algum `<w:bookmarkStart w:id="1">` próprio (comum em
   modelos de petição, que usam bookmarks para o valor da causa/`_Hlk...`). **How to
   apply:** depois de montar a tabela e antes do `zip`, sempre rodar uma checagem de
   IDs duplicados (`re.findall(r'w:bookmarkStart w:id="(\d+)"', content)` e comparar
   `len(ids) == len(set(ids))`) e remover esses dois artefatos específicos da tabela
   clonada (o `bookmarkStart`/`permStart` do cabeçalho e o `bookmarkEnd`/`permEnd`
   correspondentes) — não precisam de substituto, o texto do cabeçalho funciona
   normalmente sem eles.
8. **Ao reaproveitar a MESMA tabela-template para gerar a tabela de outra
   cidade/petição (ex.: Barueri e Praia Grande, depois de já ter validado a de São
   Paulo)**, gerar de novo a partir do XML-template original (`calvelo_values_table.xml`
   ou equivalente) — não copiar a tabela já inserida/limpa de uma petição-irmã, porque
   isso reintroduz o mesmo par bookmark/permStart problemático (o passo de limpeza do
   item 7 tem que ser repetido a cada nova tabela gerada a partir do template bruto, não
   só uma vez).

**Why:** clonar uma tabela nativa real preserva exatamente as bordas, o sombreado
cinza do cabeçalho (`w:fill="BFBFBF"`) e a fonte/alinhamento do padrão do escritório,
sem precisar recriar esse estilo manualmente em XML do zero ou via `docx`-js (que teria
que reproduzir cada detalhe visual à mão e ficaria mais sujeito a divergir do padrão real
usado pelos advogados).

**How to apply:** sempre que um modelo/precedente fornecido pelo Pedro já tiver uma
tabela nativa do Word no formato desejado, preferir cloná-la (passos 1-8 acima) a montar
uma tabela nova do zero — e sempre rodar a checagem de IDs duplicados como parte da
validação antes do `zip -Xr`/`validate.py`.

### Técnica: substituir um placeholder de imagem/screenshot por texto ou tabela real
Alguns modelos-precedente (ex.: KC Spots) trazem, no lugar de uma tabela de valores ou
de um trecho de contrato citado, uma **imagem colada** (`<w:drawing>`/screenshot),
específica daquele caso original — não dá para editar o conteúdo de uma imagem via XML.
**Testado no caso Ganso (06/08/2026):** localizar o parágrafo inteiro que contém a
imagem (do `<w:p w14:paraId="...">` de abertura até o `</w:p>` de fechamento, incluindo
qualquer `<w:permStart>`/`<w:permEnd>` ao redor), extrair esse bloco como string única,
e substituir o bloco inteiro por (a) uma citação em texto direto da cláusula real do
contrato do cliente atual (quando o conteúdo da imagem era um trecho de contrato), ou
(b) uma tabela nativa gerada pela técnica acima (quando o conteúdo da imagem era uma
tabela de valores). Isso é uma decisão técnica razoável e replicável, mas **como é uma
mudança de formato de evidência (imagem → texto/tabela), vale mencionar explicitamente
ao Pedro na entrega**, para que ele confirme se prefere manter como texto/tabela nativa
(mais fácil de editar/gerar novamente) ou trocar por uma imagem própria do caso atual
(mais fiel ao "print" original, mas exige gerar/colar uma imagem nova a cada petição).

### Técnica: reaproveitar uma petição já finalizada como base para as demais do mesmo caso
**Testado no caso Ganso (06/08/2026):** depois que a primeira petição de um caso
multi-município fica pronta e validada (ex.: São Paulo, montada a partir do precedente
KC Spots), **as petições das outras cidades do mesmo caso podem usar essa primeira
petição já finalizada como base**, em vez de partir de novo do modelo/precedente
original — porque a primeira já tem a tese jurídica, os pedidos e a qualificação da
autora corretos para aquele cliente específico, restando só trocar: cabeçalho do foro,
qualificação do réu (Município/CNPJ/endereço), parágrafo de escopo em "DOS FATOS", a
tabela de valores (nova, por cidade) e o valor da causa/pedidos relacionados. **How to
apply:** copiar a pasta descompactada da primeira petição validada (`cp -r`) como ponto
de partida de cada cidade seguinte, e repetir só os 5 blocos de substituição acima (foro,
réu, escopo, tabela, valor da causa/pedidos) — evita ter que readaptar de novo a tese
jurídica inteira e reduz o risco de inconsistência entre as 3 petições do mesmo caso
(elas devem ter a mesma fundamentação, só réu/valores/foro mudam).

### Casos multi-município — valor da causa depende de a relação estar encerrada ou vigente
**Regra descoberta e aplicada no caso Ganso (06/08/2026), a confirmar com o Pedro em
casos futuros antes de reutilizar cegamente:** quando a empresa mudou de domicílio fiscal
ao longo do tempo, **cada uma das ações (uma por Município réu) tem uma situação
jurídica diferente** quanto a se a relação de recolhimento naquele município **já
terminou** (o cliente não recolhe mais ISS lá) ou **ainda está em curso** (é o domicílio
atual):

- **Município(s) de relação encerrada** (ex.: São Paulo e Praia Grande no caso Ganso —
  o cliente não recolhe mais ISS lá porque já se mudou): **valor da causa = só o valor
  vencido** (soma do ISS pago em todo o período naquele município), sem parcelas
  vincendas — não há prestações futuras a projetar, porque a relação com aquele ente
  tributante já acabou.
- **Município do domicílio fiscal atual** (ex.: Barueri no caso Ganso — o cliente
  continua recolhendo ISS lá até hoje): **valor da causa = valor vencido + 12 parcelas
  vincendas**, nos termos do **art. 292, §2º, do CPC** (obrigação de trato sucessivo) —
  as vincendas são estimadas pela **média mensal do ISSQN recolhido nas competências
  mais recentes disponíveis** (não um valor arbitrário) × 12. **Reforça a lição já
  registrada abaixo (seção "Competência e valor da causa") sobre o precedente real
  documentado em KC Spots**: o próprio escritório já teve uma ação redistribuída de
  Juizado Especial da Fazenda Pública para vara comum por ter, inicialmente, omitido as
  parcelas vincendas do valor da causa — por isso, em qualquer ação contra o domicílio
  fiscal **atual/vigente** do cliente, computar as vincendas por padrão, mesmo que o
  valor vencido sozinho já pareça baixo o suficiente para o JEFP.
- **Pedidos**: nas ações de relação encerrada, os itens de pedido sobre "depósito
  judicial das parcelas vincendas"/"tutela antecipada para autorizar depósito das
  parcelas futuras" **não fazem sentido e devem ser removidos** (não há parcelas
  futuras). Na ação do domicílio atual, **mantê-los e adaptar a redação** para computar
  as vincendas estimadas.
- **Foro/competência**: recalcular o teto do JEFP (60 salários mínimos, ver seção
  "Competência e valor da causa" abaixo) usando o **valor da causa completo** (vencido +
  vincendas, quando aplicável) — não só o vencido — antes de decidir entre JEFP e vara
  comum.

**Why:** replica no valor da causa a mesma distinção "histórico vs. atual" que já se
aplica ao domicílio fiscal — uma ação sobre uma relação encerrada não tem parcelas
futuras a proteger, mas uma ação sobre a relação vigente sim, e omitir isso arrisca o
mesmo problema de redistribuição já documentado em KC Spots.

**How to apply:** ao montar as petições de um caso multi-município, classificar cada
município como "histórico" ou "atual" antes de calcular o valor da causa de cada ação, e
aplicar a fórmula certa (só vencido vs. vencido + 12 vincendas estimadas pela média
mensal recente) e o conjunto de pedidos certo (com ou sem depósito judicial de
vincendas) para cada uma. **Pontos que ficaram como premissa razoável, mas não
totalmente confirmados com o Pedro no caso Ganso — sinalizar/confirmar em casos
futuros semelhantes:** (a) o foro usado nas 3 ações foi Vara da Fazenda Pública comum em
todas (não Juizado Especial), inclusive em Praia Grande, cujo valor da causa (só
vencido, R$47.280,00) ficaria abaixo do teto do JEFP — a escolha por vara comum ali foi
uma decisão de segurança (por não haver confirmação de que existe JEFP instalado
especificamente na comarca de Praia Grande), não uma regra fixa; (b) a estimativa das 12
parcelas vincendas de Barueri usou a **média simples dos meses disponíveis no dossiê**
(não uma projeção mês a mês) — método razoável e documentado no próprio texto da
petição, mas vale validar com o Pedro se o escritório prefere outra metodologia de
projeção em casos futuros.

### Competência e valor da causa
- **Regra prática do Pedro**: a competência é sempre do foro de onde a empresa (autora)
  foi constituída/domiciliada — quando o réu é o Município correspondente a esse mesmo
  domicílio (caso comum de ISS pago ao próprio município do prestador, ex.: Benassi em
  Américo Brasiliense), não há conflito de competência a resolver. Sempre pesquisar as
  regras específicas de cada tribunal (o Pedro pediu para eu pesquisar e perguntar antes
  de assumir). **Quando a empresa mudou de domicílio ao longo do período do caso (ex.:
  caso Ganso — Praia Grande → São Paulo → Barueri), a competência de cada uma das 3
  ações segue o Município réu daquele período específico** (cada ação tem seu próprio
  réu/foro, ligado ao domicílio vigente *durante o período discutido naquela ação*, não
  ao domicílio atual do cliente) — nas 3 petições reais do caso Ganso, cada ação foi
  ajuizada na comarca do respectivo Município réu (São Paulo, Barueri, Praia Grande),
  não todas na comarca do domicílio atual do cliente.
- **Ações contra Município/Estado ("Fazenda Pública")**: verificar primeiro se o valor
  da causa ultrapassa **60 salários mínimos** (teto do Juizado Especial da Fazenda
  Pública, Lei 12.153/09, art. 2º — R$1.621 em 2026, logo teto de R$97.260, valor que
  muda todo ano com o novo salário mínimo — sempre pesquisar o valor vigente). Abaixo
  do teto, o autor pode optar por Juizado Especial da Fazenda Pública (mais rápido) ou
  vara comum, dependendo se há JEFP instalado na comarca (onde há JEFP instalado, a
  competência dele é absoluta). Acima do teto, vai obrigatoriamente para a Vara da
  Fazenda Pública comum. **Lembrar de recalcular o teto usando o valor da causa
  completo (vencido + vincendas, quando aplicável) — ver seção acima sobre casos
  multi-município.**
- **Comarca de São Paulo (capital)**: as Varas da Fazenda Pública são centralizadas no
  **Foro Central das Fazendas Públicas e Acidentes do Trabalho — Fórum Hely Lopes
  Meirelles** (Viaduto Dona Paulina, 80, Centro), com 14+ varas; distribuição por
  PJe/e-SAJ. Isso vale independente do bairro/foro regional onde o autor está
  domiciliado dentro da capital — ações contra a Fazenda Pública municipal de São Paulo
  não vão para os foros regionais comuns.
- **Valor da causa em repetição de indébito**: pela jurisprudência do TJSP (art. 292,
  §3º c/c art. 260 do CPC), é o valor da vantagem econômica pretendida — soma do
  principal a restituir (parcelas vencidas), sem incluir ainda a correção
  monetária/juros na petição (isso é calculado depois, na fase de cumprimento/perícia),
  mas mencionar que o valor será atualizado até o efetivo pagamento. **Quando a relação
  com o réu ainda está em curso (domicílio fiscal atual do cliente), o valor da causa
  soma também 12 parcelas vincendas** (estimadas pela média mensal do tributo pago nas
  competências recentes disponíveis) — ver fórmula no exemplo abaixo e a seção
  "Casos multi-município" acima para o critério de quando aplicar isso.
- **Caso 8 Milímetros (referência)**: domiciliada em São Paulo/SP, réu = Município de
  São Paulo (CNPJ 46.395.000/0001-39, sede no Viaduto do Chá, nº 15, Centro) → Vara da
  Fazenda Pública do Foro Central (Fórum Hely Lopes Meirelles). Restituição
  (competências pagas) = R$153.939,62; média mensal = R$153.939,62 / 22 meses pagos =
  R$6.997,26; 12 parcelas vincendas estimadas = R$83.967,07; **valor da causa =
  R$237.906,69**. Isso já ultrapassa o teto do JEFP — vai direto para vara comum, sem
  necessidade de decidir entre JEFP e vara comum nesse caso.
- **Caso Ganso (referência, 06/08/2026) — 3 ações com valores da causa diferentes por
  situação de cada réu:**
  - **São Paulo** (relação encerrada, 09/2022–08/2025, 70 notas): valor da causa = só
    vencido = **R$508.315,78** (sem vincendas).
  - **Praia Grande** (relação encerrada, até 08/2022, 8 notas): valor da causa = só
    vencido = **R$47.280,00** (sem vincendas).
  - **Barueri** (domicílio atual, 09/2025 em diante, 20 notas até a competência
    disponível mais recente): vencido = R$128.189,52; média mensal (10 competências
    disponíveis) = R$12.818,95; 12 parcelas vincendas estimadas = R$153.827,42; **valor
    da causa = R$282.016,94**.
- **Caso Benassi (dados de referência para a futura petição, 07/08/2026):** Américo
  Brasiliense/SP, domicílio único durante todo o período — relação em curso (o cliente
  segue emitindo notas até 05/2026, a competência mais recente do dossiê), logo a
  petição, quando elaborada, deve computar valor vencido + 12 parcelas vincendas
  (mesma lógica do "domicílio atual" acima). Valor vencido bruto do quadro de
  restituição (soma do ISS das 66 notas, sujeito a ajuste pelas pendências ainda em
  aberto com a contabilidade) = R$9.113,28.

### Bloco de assinatura / qualificação dos advogados — padrão fixo do escritório
O Pedro definiu que este é o bloco padrão a usar em toda petição, independente do caso
(substitua só se ele pedir explicitamente uma variação):

> **COMUNICAÇÕES DOS ATOS PROCESSUAIS**
>
> Requer, sob pena de nulidade, que as comunicações dos atos processuais sejam feitas
> exclusivamente em nome do advogado **GILSON VACISKI BARBOSA (OAB/SP 277.760)**,
> apresentando desde logo o endereço de seu escritório, Rua Visconde do Rio Branco, nº
> 1322, 8º andar, Centro, CEP 80.420-210, Curitiba/PR, telefone (41) 3015-7775, e-mail
> contatopr@svadvocacia.com.br.

Bloco de assinatura (rodapé da petição), sempre nesta ordem/formatação — "pp." (por
procuração) antes de cada nome, e o OAB exatamente como abaixo:

| Advogado | OAB |
|---|---|
| Marcio Jones Suttile | OAB/SP 193.517-A |
| Leonardo Moreira | OAB/PR 55.023 |
| Josiel Vaciski Barbosa | OAB/SP 191.692-A |
| Pedro Henrique Pontarolo Zaithammer | OAB/PR 71.081 |
| Gilson Vaciski Barbosa | OAB/SP 277.760 |

**Why:** é o padrão fixo do escritório (SV Advocacia), confirmado pelo Pedro em
05/08/2026 — não perguntar de novo em casos futuros, só usar direto. **Nota:** o e-mail
de contato correto é **contatopr@svadvocacia.com.br** — o modelo docx original ainda
trazia um e-mail antigo (`pedro@svadvocacia.com.br`) na seção "Comunicações dos Atos
Processuais"; sempre conferir/corrigir esse campo específico contra o padrão acima.
**How to apply:** incluir a seção "Comunicações dos Atos Processuais" perto do fim da
petição (antes do pedido/valor da causa ou logo após), e o bloco de assinatura completo
ao final do documento, layout de duas colunas como no modelo original. A data de
assinatura no modelo é um campo de data dinâmico do Word (`TIME \@ "d' de 'MMMM' de
'yyyy"`), que se autoatualiza para a data corrente ao abrir/imprimir no Word — ainda
assim, atualizar também o texto em cache (entre os `fldChar` de "separate" e "end") para
a data real da minuta, para que a pré-visualização em PDF gerada pela sessão mostre a
data correta mesmo sem recalcular o campo. **Confirmado de novo no caso Ganso: o
LibreOffice (`soffice.py --convert-to pdf`) recalcula esse campo automaticamente na
conversão para PDF**, mostrando a data real do dia da renderização mesmo que o texto em
cache esteja desatualizado — mas ainda assim vale atualizar o cache, porque nem todo
visualizador de PDF/Word recalcula campos automaticamente ao abrir.

### Documento pessoal do representante legal
Frequentemente falta como arquivo avulso no dossiê inicial — mas **antes de tratar como
lacuna bloqueante, ler o Contrato Social inteiro** (e, na falta dele, o próprio contrato
de cessão/sublicenciamento de direitos de imagem, que também costuma trazer a
qualificação completa — ver seção "Documentos que compõem cada caso" acima): no caso 8
Milímetros, o próprio Contrato Social trazia RG, CPF e endereço completo dos dois sócios
na cláusula de qualificação, o que foi suficiente para qualificar o representante legal
(o sócio majoritário/administrador) na petição sem precisar de mais nenhum documento.
No caso Benassi, o Contrato de Cessão de Uso de Imagem (Coritiba, 2024) supriu CPF e RG
do representante mesmo sem o Contrato Social estar no dossiê — reforça que qualquer um
dos dois documentos pode suprir a qualificação, não só o Contrato Social. Só deixar
placeholder (`[QUALIFICAÇÃO DO REPRESENTANTE LEGAL — AGUARDANDO DOCUMENTO]`) se nenhum
dos dois documentos trouxer esses dados.

### Jurisprudência local
O modelo "MARCELO" tem um espaço reservado ("ESPAÇO PARA INSERIR JURISPRUDÊNCIA LOCAL",
repetido em várias linhas/parágrafos vazios) para um precedente do tribunal onde a ação
será ajuizada. Aproveitar precedentes que já estejam em outras partes do próprio modelo
(ex.: o modelo já trazia, na seção "4.0 Da Repetição do Indébito", um acórdão do TJ-SP
diretamente contra o Município de São Paulo sobre o mesmo tema — reaproveitar essa
mesma citação no espaço reservado da seção 3.1 é válido e reforça o argumento, em vez de
sair procurando um precedente novo sem necessidade). Se o modelo não tiver nenhum
precedente do tribunal certo já embutido, aí sim pesquisar um novo via `WebSearch`
antes de inserir. **Quando o modelo-base é um precedente real contra o mesmo réu (ex.:
KC Spots contra o Município de São Paulo, usado como base da petição de São Paulo do
caso Ganso), a jurisprudência já embutida nele tende a já ser específica daquele
Município/tema — conferir se ela já serve antes de pesquisar uma nova.**

### Modelos de referência
- **"MARCELO - Inicial ISSQN - Audiovisual"** — modelo genérico com placeholders em
  vermelho, para casos sem um precedente real mais específico disponível. Estrutura:
  01 Preliminarmente (comunicações dos atos) → 02 Síntese dos Fatos → 03 Do Direito
  (legalidade estrita, inexistência de fato gerador pelo veto ao item 13.01,
  impossibilidade de enquadramento em 13.03/17.06) → 04 Da Repetição do Indébito
  (fundamentação + quadro de valores + inaplicabilidade do art. 166 CTN + correção
  monetária/juros) → 05 Da Tutela de Urgência → 06 Dos Pedidos → valor da causa →
  assinatura. Para casos de atleta (direito de imagem), a fundamentação da seção 03
  muda (não é sobre o item 13.01 vetado, e sim sobre a natureza do agenciamento/
  exploração de imagem e a base de cálculo correta do ISS).
- **"Inicial KC Spots"** (real, contra o Município de São Paulo) — usado como base da
  petição de São Paulo do caso Ganso. Traz qualificação exata do réu (CNPJ
  46.395.000/0001-39, Viaduto do Chá nº 15, Edifício Matarazzo, Centro, São Paulo/SP) e
  um histórico real de "DA COMPETÊNCIA" sobre redistribuição JEFP → vara comum por
  omissão de vincendas (remover essa seção específica ao reaproveitar para um caso sem
  esse histórico, mas usar a lição — computar vincendas quando a relação está em curso).
  Trecho de "trechos do contrato" nesse modelo vinha como imagens/screenshots
  (específicas do caso original) — ver "Técnica: substituir um placeholder de
  imagem/screenshot" acima.
- **"Inicial Padrão ISSQN - Calvelo Agenciamento de Sports"** (real, contra o Município
  de Santos) — traz uma tabela nativa do Word (`<w:tbl>`) de valores no formato
  "Incidência | NF | Valor NF | ISS Pago", reaproveitada como template de geração (ver
  técnica acima) nas 3 petições do caso Ganso. Valor da causa nesse modelo é só vencido
  (sem vincendas) — relação encerrada.
- **Casos com mais de um Município réu (ex.: Ganso)**: cada ação precisa da sua própria
  minuta de petição — não tentar consolidar réus/ações num único docx. **Padrão testado:
  montar a primeira petição a partir do modelo/precedente mais específico disponível
  (ver "Qual modelo usar" acima), validá-la, e usar essa primeira petição já pronta como
  base das demais** (ver "Técnica: reaproveitar uma petição já finalizada" acima) — mais
  rápido e mais consistente entre as 3 do que repetir a adaptação do modelo original 3
  vezes.

## Cálculo de atualização monetária (correção do valor a restituir)

### Quando usar e para quê
Depois que o quadro de restituição (por nota / consolidado) já está pronto, o Pedro
pode pedir uma **planilha de cálculo de atualização monetária** para instruir a
petição inicial com o "valor atualizado" (reforça o valor da causa e mostra ao juízo,
já na inicial, quanto o indébito realmente representa hoje). **Sempre confirmar com o
Pedro, via `AskUserQuestion`, dois pontos antes de montar essa planilha** (caso RW
Sports, 05/08/2026):
1. **Metodologia de atualização** — no caso testado, a resposta foi "IPCA-E municipal
   (correção monetária) + SELIC (juros de mora)". Não presumir automaticamente esse
   par sem perguntar, porque a metodologia pode mudar por tribunal/comarca.
2. **Para que serve o número, nesse momento** — no caso testado, a resposta foi
   "instruir a inicial com o valor atualizado" (não uma planilha de liquidação de
   sentença nem de execução). Isso muda o que é computável: se a citação ainda não
   aconteceu, os juros de mora (que só correm a partir dela) não têm data de início
   real e não devem ser calculados como número — só documentados como pendentes.

### Por que IPCA-E (e não outro índice) — base legal
Para repetição de indébito tributário municipal, o índice de correção correto é,
via de regra, **o mesmo que o próprio Fisco municipal usa para atualizar os créditos
tributários dele** (isonomia, Súmulas 162 e 188 do STJ). **Sempre verificar a lei
municipal específica do réu** (não presumir IPCA-E por padrão) — no caso de Maceió/AL,
a **Lei Municipal nº 6.685/2017** determina IPCA-E/IBGE para atualização dos créditos
tributários do próprio Município, o que justifica usar o mesmo índice a favor do
contribuinte na ação de restituição. Documentar essa base legal específica do
município réu na planilha (célula de observação), não só citar as súmulas do STJ.

### Fonte de dados do IPCA-E — como obter a série completa
O IBGE não tem uma página única simples com toda a série histórica mensal pronta para
copiar. A fonte que funcionou (05/08/2026): `https://www.debit.com.br/tabelas/ipcae-indice-de-precos-ao-consumidor-amplo-especial`.
**Atenção:** essa página carrega só uma tabela truncada (poucos anos antigos) por
padrão — o `WebFetch`/`WebSearch` sozinho não retorna a série completa porque a tabela
completa fica atrás de um botão "Ver tabela completa" renderizado via JavaScript
(client-side). **Usar as ferramentas Claude in Chrome** em vez de insistir no
`WebFetch` (ver `escalate_unhelpful_web_fetch_to_chrome`): `navigate` até a página,
`find` o botão "Ver tabela completa", clicar nele, confirmar via screenshot que a
tabela expandiu, e só então `read_page` mirando o `ref_id` do painel/tabela (não a
página inteira) para recuperar a série mensal completa (no teste, de 1992 até o mês
mais recente divulgado). Fechar a aba do Chrome ao final, já que é só uma consulta
pontual.

**Why:** o padrão "WebFetch retorna conteúdo truncado/shell" em página com tabela
client-side já é coberto pela instrução geral do ambiente (JS não executa no WebFetch);
vale registrar aqui a URL específica que funciona para IPCA-E, para não repetir a
mesma busca do zero em cada caso novo.

### Metodologia de cálculo (testada no caso RW Sports)
1. **Montar uma aba "Índice IPCA-E"** com uma linha por mês (variação mensal % como
   input, cor azul) e uma coluna de **Número Índice acumulado** via fórmula
   (`=índice do mês anterior * (1 + variação do mês)`), começando de um mês-âncora
   anterior ao primeiro pagamento indevido do caso (índice = 1,0000 por definição
   nesse mês-âncora, sem variação própria).
2. **Data-base da correção**: usar o **último mês do IPCA-E já divulgado** até a data
   de elaboração da planilha (não o mês do ajuizamento real, que ainda não aconteceu
   nesta fase pré-protocolo) — documentar isso explicitamente como premissa (célula
   destacada em amarelo) e avisar que a aba de índice deve ser atualizada com os meses
   novos se o ajuizamento efetivo ocorrer depois da data-base usada.
3. **Fator de correção por nota/competência** = Índice(mês da data-base) /
   Índice(mês do pagamento indevido) — aplica as variações desde o mês do desembolso
   (inclusive) até o mês-base (inclusive). Buscar o índice do mês do pagamento via
   `INDEX`/`MATCH` (nunca hardcodar o número), usando `=TEXT(data_pagamento;"MM/AAAA")`
   para derivar a chave de busca a partir da data (que já vem do quadro de
   restituição/planilha de triagem, não recalculada).
4. **Valor corrigido de cada nota/competência** = Valor histórico (ISS
   estimado/pago) × Fator de correção — via fórmula, nunca número fixo.
5. **Juros de mora (SELIC)**: **não calcular como número** se a citação ainda não
   ocorreu (fase pré-protocolo) — documentar como observação textual na planilha (ex.:
   "juros de mora incidem somente a partir da citação válida do réu, art. 167,
   parágrafo único, CTN c/c Súmulas 162 e 188 do STJ; não computados nesta etapa por
   dependerem de data futura ainda não determinada"). Só voltar a essa planilha para
   adicionar a coluna de SELIC quando a citação já tiver data real (ex.: perto do
   protocolo efetivo, ou em fase de cumprimento de sentença).
6. **Abas de saída**: (a) "Índice IPCA-E" (dados brutos + índice acumulado), (b)
   "Memória de Cálculo" (uma linha por nota/competência paga, com todas as colunas
   intermediárias — data do pagamento, índice no pagamento, índice na data-base, fator,
   valor corrigido — mais linha TOTAL com fórmula `SUM`), (c) "Resumo" (total histórico,
   total corrigido, diferença, e a observação de que os juros de mora ainda serão
   somados a partir da citação) — essa última é o que o Pedro provavelmente vai citar
   direto na petição/despacho.
7. Seguir as regras gerais da skill `xlsx` (fonte Arial, fórmulas nunca hardcoded,
   `recalc.py` obrigatório, documentar toda premissa em texto visível na própria
   planilha, não só na conversa).

**Why:** essa sequência (índice mensal → fator por competência via INDEX/MATCH → valor
corrigido por fórmula → juros de mora documentados como pendentes, não calculados)
reproduz o que um contador judicial faria manualmente, mantém a planilha auditável e
recalculável, e evita apresentar um número de juros fictício antes de existir uma data
de citação real.

**How to apply:** ao chegar nessa etapa num caso novo, perguntar ao Pedro metodologia e
finalidade (passo "Quando usar e para quê" acima) antes de montar qualquer aba, buscar a
lei municipal específica do réu para confirmar o índice, obter a série do IPCA-E via
Claude in Chrome se o WebFetch vier truncado, e seguir os 7 passos de metodologia acima
— sempre terminando com `recalc.py` limpo e uma conferência visual (renderizar em PDF)
antes de entregar.

