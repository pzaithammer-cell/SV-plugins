---
name: atualizacao-juridica-diaria
description: Gera um resumo diário com até 10 acontecimentos jurídicos relevantes (decisões judiciais, notícias de imprensa, fatos do dia) nas áreas Cível, Trabalhista, Desportivo e Previdenciário, com foco em conteúdo para redes sociais de escritório de advocacia. Use sempre que o usuário pedir "atualização jurídica", "resumo do dia", "notícias jurídicas de hoje", "pauta para redes sociais", "bom dia jurídico", ou variações do tipo "traz as novidades de hoje" no contexto do escritório. Também use como instrução de tarefa agendada (Cowork Scheduled Tasks) para rodar automaticamente toda manhã.
---

# Atualização Jurídica Diária

Skill para compilar acontecimentos jurídicos relevantes do dia, voltados à produção de conteúdo para redes sociais de um escritório de advocacia que atua nas áreas Cível, Trabalhista, Desportivo e Previdenciário.

## Objetivo

Entregar 10 acontecimentos por dia — decisões de tribunais superiores (STF, STJ, TST, STJD), movimentações legislativas relevantes, ou notícias de imprensa jurídica — distribuídos de forma equilibrada entre as 4 áreas (referência: 2-3 itens por área), cada um com um ângulo de conteúdo sugerido.

## Perfil do escritório (critério de seleção)

O escritório atua com viés voltado a **pessoas físicas**, principalmente trabalhadores. Isso deve guiar a escolha dos itens, não só a redação:

- **Trabalhista e Previdenciário**: priorizar decisões e temas que impactem positivamente o trabalhador/segurado — direitos ganhos, teses favoráveis, mudanças que ampliam proteção ou benefício. Evitar dar destaque a decisões que só interessam ao empregador/à União do ponto de vista de redução de custo, a menos que sejam relevantes o suficiente para o trabalhador entender o que perdeu ou como se proteger.
- **Cível**: pode ser mais diverso — inclui temas de consumidor, família, sucessões, contratos do dia a dia, responsabilidade civil, direito digital etc. Não precisa ter viés trabalhador, mas evitar temas puramente empresariais/societários que não dialogam com pessoa física.
- **Desportivo**: também pode ser mais diverso (não precisa focar em trabalhador) — inclui disciplina, contratos de atletas, direitos de imagem, decisões de tribunais desportivos em geral.

Na dúvida entre dois itens de peso parecido na mesma área, priorizar o que tem lado humano mais evidente (impacto real e imediato na vida de uma pessoa) sobre o que é só de interesse técnico-corporativo.

## Processo

1. **Buscar por área, não de forma combinada, e priorizando imprensa geral sobre sites institucionais.** Faça buscas separadas para cada uma das 4 áreas. Prefira queries que retornem cobertura de portais generalistas (G1, UOL, CNN Brasil, Metrópoles, R7) e não apenas sites institucionais de tribunal — esses costumam trazer temas técnicos sem apelo popular. Sugestões de query por área:
   - Cível: "decisão STF STJ direito civil [mês/ano atual]", "golpe fraude consumidor notícia viral [mês/ano atual]"
   - Trabalhista: "TST STF decisão trabalhista [mês/ano atual]", "direito do trabalhador decisão favorável notícia", "pejotização vínculo empregatício notícia"
   - Desportivo: "STJD notícia [mês/ano atual]", "CAS TAS decisão futebol", "[clube grande] STJD punição notícia"
   - Previdenciário: "INSS aposentadoria STF STJ notícia [mês/ano atual]", "segurado INSS direito benefício decisão favorável"

2. **Priorizar o que é recente e tem repercussão popular — isso vem antes de relevância técnica.** O critério principal de seleção é "essa notícia já está sendo comentada/tem potencial de viralizar", não "essa é a decisão juridicamente mais importante do dia". Concretamente:
   - Prefira um tema que já é assunto no Twitter/X, grupos de WhatsApp, portais de notícia generalistas (G1, UOL, CNN Brasil) ou trending no momento, mesmo que a fonte não seja STF/STJ/TST — uma decisão de primeira instância ou TRT regional bem comentada na imprensa vale mais, para fins de rede social, do que uma tese técnica inédita de tribunal superior que só interessa a advogados.
   - Evite decisões de repercussão puramente jurídica/técnica (ex.: fixação de tese processual, mudança de entendimento sobre ônus da prova) que não têm gancho popular óbvio, mesmo vindas de tribunal superior — a menos que o tema em si (não a decisão) já seja popular (ex.: revisão da vida toda, pejotização, motorista de app, bets).
   - Casos de tribunais regionais (TRT, TJ estadual) só entram se tiverem alcance de imprensa nacional/viral (ou seja, se você já encontrou eles noticiados fora do próprio site do tribunal) — não usar apenas porque saíram no portal institucional do tribunal.
   - Temas com nome de clube grande, atleta, personalidade pública, golpe/fraude comum, ou situação do dia a dia de qualquer pessoa (aluguel, salário atrasado, golpe no PIX, demissão, herança) tendem a funcionar melhor do que teses processuais.

3. **Selecionar 10 itens no total**, buscando equilíbrio entre as 4 áreas (não é necessário ser exatamente 2,5 por área — pode variar conforme o que há de mais relevante no dia).

4. **Para cada item, entregar:**
   - Título curto e chamativo (o "gancho")
   - 1-2 frases explicando o que aconteceu, em linguagem clara (evitar juridiquês pesado — o público de redes sociais não é só advogado)
   - **Fonte**: nome do veículo/tribunal e link da matéria ou decisão original. Nunca omitir — é o que permite ao escritório verificar antes de postar.
   - **Pertinência**: por que esse fato interessa ao público do escritório (cliente pessoa física, empresário, atleta, aposentado etc.) e por que vale a pena postar sobre ele agora
   - **Como usar nas redes**: formato sugerido (reels explicativo, carrossel, post estático, story de enquete/pergunta), mais uma observação de tom quando o tema for sensível ou exigir cautela (ex.: "tema polêmico, evitar tomar partido explícito")
   - **Legenda pronta**: um rascunho curto de legenda (2-4 frases, tom acessível, pode terminar com uma pergunta para engajamento) + 4-6 hashtags relevantes (misturando termos jurídicos e termos mais populares/de nicho da área, ex. #DireitoTrabalhista #PejotizaçãoNão #AdvogadaExplica)

5. **Seguir as regras de direito autoral padrão**: nunca reproduzir trechos longos de notícias ou decisões; parafrasear; no máximo uma citação curta (menos de 15 palavras) por fonte.

6. **Não inventar decisões ou notícias.** Se uma área não tiver nada relevante no dia, é preferível trazer 1-2 itens a menos nela e compensar em outra do que forçar um fato inexistente ou desatualizado.

## Formato de saída

Organizar por área (Cível, Trabalhista, Desportivo, Previdenciário), numerando os itens de 1 a 10 dentro do conjunto total. Cada item já sai completo com pertinência, sugestão de formato e legenda com hashtags — não é necessário perguntar antes, isso já é parte padrão da entrega. Ao final, perguntar apenas se o usuário quer aprofundar algum item específico (ex.: versão mais longa da legenda, roteiro de reels, etc.).

## Formato de e-mail (para tarefa agendada / rascunho no Gmail)

Quando o pedido for para gerar o e-mail diário para a equipe do escritório (ou quando estiver rodando como tarefa agendada que cria rascunho no Gmail), gerar também um e-mail pronto, junto com o resumo padrão acima:

- **Destinatários padrão**:
  - leonardo@svadvocacia.com.br
  - isabela.casagrande@svadvocacia.com.br
- **Assunto**: "Atualização Jurídica — [dia da semana], [data]" (ex.: "Atualização Jurídica — Quarta, 05/08/2026")
- **Corpo do e-mail**, em texto simples (sem formatação markdown pesada, já que vai virar e-mail de verdade):
  - Saudação curta ("Bom dia, time!")
  - Uma frase de abertura dizendo quantos itens vieram hoje e de quais áreas
  - Os itens listados por área, cada um com: título, resumo de 1-2 frases, fonte (link), pertinência resumida em 1 frase, e a legenda pronta (sem repetir a seção "como usar nas redes" e hashtags no e-mail — isso é auxiliar interno, pode ficar mais enxuto que a versão de chat)
  - Fechamento curto convidando a equipe a escolher quais itens virarão posts e avisando que os rascunhos de legenda já estão prontos para uso

Este e-mail é gerado como **rascunho** no Gmail conectado, nunca enviado diretamente — quem for responsável no escritório revisa e envia manualmente. Se estiver rodando como tarefa agendada, apenas criar o rascunho e não pedir confirmação (já que não há humano respondendo em tempo real), mas sob nenhuma hipótese enviar o e-mail automaticamente sem revisão humana.

## Uso como tarefa agendada

Se esta skill for usada como instrução de uma tarefa agendada (Cowork Scheduled Tasks) para rodar automaticamente toda manhã, o resultado deve ser autocontido: não faça perguntas de esclarecimento, apenas entregue o resumo do dia diretamente, já que não haverá um humano respondendo em tempo real.
