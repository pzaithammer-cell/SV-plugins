---
name: "procuracao-honorarios"
description: "Gera procuração, contrato de honorários advocatícios e (quando trabalhista) declaração de hipossuficiência para novos clientes do escritório Suttile & Vaciski, a partir de documentos de identificação do cliente (RG, CNH, contrato social, cartão CNPJ etc.) e de três informações rápidas — segmento/tipo de ação, percentual de honorários e réu. Cobre os cinco tipos de ação do escritório: ISS de Atleta/Jogador, ISS de Audiovisual, Ação Trabalhista, Ação da SEGA (uso indevido de imagem) e CNRD. Depois de gerados e aprovados pelo usuário, converte os documentos finais em PDF e os envia para assinatura na plataforma ZapSign. Use sempre que o usuário mandar documentos de um cliente e pedir para gerar procuração, contrato de honorários, ou declaração de hipossuficiência/insuficiência de rendimentos — mesmo que ele não use a palavra \"skill\" ou não cite o nome do arquivo. Também dispare este fluxo quando o usuário mencionar \"novo cliente\", \"gerar os documentos padrão\", ou similar, no contexto do escritório."
---

---
name: procuracao-honorarios
description: >-
  Gera procuração, contrato de honorários advocatícios e (quando trabalhista) declaração de
  hipossuficiência para novos clientes do escritório Suttile & Vaciski, a partir de documentos de
  identificação do cliente (RG, CNH, contrato social, cartão CNPJ etc.) e de três informações
  rápidas — segmento/tipo de ação, percentual de honorários e réu. Cobre os cinco tipos de ação
  do escritório: ISS de Atleta/Jogador, ISS de Audiovisual, Ação Trabalhista, Ação da SEGA (uso
  indevido de imagem) e CNRD. Depois de gerados e aprovados pelo usuário, converte os documentos
  finais em PDF e os envia para assinatura na plataforma ZapSign. Use sempre que o usuário mandar
  documentos de um cliente e pedir para gerar procuração, contrato de honorários, ou declaração
  de hipossuficiência/insuficiência de rendimentos — mesmo que ele não use a palavra "skill" ou
  não cite o nome do arquivo. Também dispare este fluxo quando o usuário mencionar "novo
  cliente", "gerar os documentos padrão", ou similar, no contexto do escritório.
---

# Procuração e Contrato de Honorários

Este escritório abre um novo caso da mesma forma sempre: recebe os documentos de identificação
do cliente, e alguém preenche à mão uma procuração, um contrato de honorários e (se trabalhista)
uma declaração de hipossuficiência. Esta skill automatiza esse preenchimento — e, depois de
aprovado pelo usuário, também gera o PDF final e sobe para assinatura no ZapSign.

## Fluxo

1. **Receba os documentos do cliente** (upload no chat ou arquivos na pasta): RG, CNH, contrato
   social, cartão CNPJ, o que tiver. Leia-os (são imagens/PDFs — use a leitura nativa, não precisa
   de OCR externo).

2. **Confirme com o usuário, se ele não tiver mandado junto**:
   - Segmento/tipo de ação (ISS Atleta/Jogador, ISS Audiovisual, Trabalhista, SEGA ou CNRD)
   - Percentual de honorários (se não informado, use o padrão do segmento — ver
     `references/campos-por-segmento.md` — mas avise qual padrão está usando)
   - Réu (contra quem é a ação)

3. **Extraia os dados do cliente** dos documentos e monte os cinco campos do template:
   `OUTORGANTE_NOME`, `OUTORGANTE_QUALIFICACAO`, `REU`, `PERCENTUAL`, `DATA` (data de hoje, por
   extenso, em português — ex. "07 de agosto de 2026"). Leia
   `references/campos-por-segmento.md` para o formato exato de cada campo, especialmente
   `OUTORGANTE_QUALIFICACAO`, que muda bastante entre pessoa física e jurídica.

   Se o cliente for pessoa jurídica com mais de um sócio, verifique no contrato social quem tem
   poder de administração isolada — é essa pessoa que assina como representante. Se a
   administração for conjunta ou não estiver clara, pergunte ao Pedro antes de prosseguir.

4. **Mostre os dados extraídos ao usuário antes de gerar os arquivos finais.** Isso é importante:
   são documentos com efeito jurídico, e erro de CPF, RG ou grafia de nome não é algo que se
   corrige depois de assinado. Um resumo curto dos campos já serve — não precisa reproduzir o
   texto inteiro da qualificação.

5. **Gere os documentos** com `scripts/fill_template.py`, usando os templates de
   `assets/templates/<segmento>/`:

   ```bash
   python3 scripts/fill_template.py \
     --template assets/templates/iss-jogador/procuracao.docx \
     --output "Procuração - <Nome do Cliente>.docx" \
     --field 'OUTORGANTE_NOME=RW SPORTS E EVENTOS LTDA' \
     --field 'OUTORGANTE_QUALIFICACAO=pessoa jurídica de direito privado, inscrita no CNPJ/MF sob o nº 37.219.346/0001-95, com sede na Rua Maria Ramos de Lima, nº 45, Aptº 1507, Torre B, Antares, CEP 57.048-360, Maceió/AL, neste ato representada por seu administrador, JOSE RENATO DA SILVA JUNIOR, brasileiro, nascido em 19/01/1990, casado, jogador, CPF nº 089.066.144-89, RG nº 32.877.471 SSP/AL, residente e domiciliado na Rua Doutora Rosa Cabús, nº 142, Aptº 302, Edifício Sangiovese, Jatiuca, CEP 57.035-825, Maceió/AL.' \
     --field 'REU=Natal/RN' \
     --field 'DATA=07 de agosto de 2026'
   ```

   Repita para o contrato de honorários (mesmos campos, mais `PERCENTUAL`), e para a declaração
   de hipossuficiência se for caso trabalhista (só precisa de `OUTORGANTE_NOME`,
   `OUTORGANTE_QUALIFICACAO` e `DATA`).

   O script falha se sobrar algum `{{TOKEN}}` sem preencher no resultado — isso é intencional,
   é o jeito de pegar campo esquecido antes de entregar o documento errado. Se aparecer esse
   erro, volte ao passo 3 e complete o dado que faltou.

6. **Verifique visualmente antes de entregar.** Converta para PDF e leia (ou abra o .docx) —
   confirme que os dados batem com os documentos originais do cliente. Nunca pule esta etapa:
   é a rede de segurança contra erro de extração.

   ```bash
   python <caminho-do-skill-docx>/scripts/office/soffice.py --headless --convert-to pdf final.docx
   ```

7. **Salve os arquivos finais (.docx)** em uma subpasta com o nome do cliente dentro da pasta
   "Procuração e Contrato de Honorários" (ex.: `RW Sports e Eventos - ISS Natal/`), e
   apresente ao usuário para conferência final. Não avance para os passos 8 e 9 sem o "ok"
   explícito do usuário — são documentos com efeito jurídico.

8. **Depois do "ok" do usuário, gere o PDF final de cada documento** (mesmo conversor do passo
   6, mas salvando o resultado desta vez) e coloque na mesma subpasta ao lado dos `.docx`:

   ```bash
   python <caminho-do-skill-docx>/scripts/office/soffice.py --headless --convert-to pdf \
     --outdir "Procuração e Contrato de Honorários/<Nome do Cliente>/" \
     "Procuração e Contrato de Honorários/<Nome do Cliente>/<arquivo>.docx"
   ```

9. **Suba os PDFs no ZapSign para assinatura.** O ZapSign não tem conector MCP dedicado — faça
   isso pela extensão Claude in Chrome, navegando até app.zapsign.com.br, autenticado com a
   conta do escritório, e usando o fluxo de upload/criação de documento para assinatura. Se a
   extensão não estiver conectada, avise o usuário e peça para conectar antes de prosseguir. Não
   defina signatários nem envie para assinatura sem confirmar com o usuário o(s) destinatário(s)
   corretos — a skill só cobre a preparação e o upload do documento, não decide quem assina.

## Onde salvar os arquivos gerados (e o que nunca vai para o GitHub)

Os documentos finais desta skill (procuração, contrato, declaração de hipossuficiência, PDFs)
ficam sempre na pasta local do caso do cliente, dentro do projeto — nunca só na conversa.
**Nunca commitar ou enviar esses arquivos para o repositório GitHub `SV-plugins`**: esse
repositório é só para o código desta skill (`SKILL.md`, `scripts/`, `assets/templates/` com
tokens vazios), sem nenhum dado real de cliente. Quando o Pedro tiver uma nuvem privada
conectada (ex.: OneDrive/Microsoft 365 com escrita habilitada), sincronizar os arquivos também
para lá, além da pasta local — nunca em vez da pasta local.

## Estrutura desta skill

```
procuracao-honorarios/
├── SKILL.md
├── scripts/
│   └── fill_template.py       — preenche um template com os dados de um cliente
├── assets/templates/
│   ├── cnrd/
│   ├── iss-jogador/
│   ├── iss-audiovisual/
│   ├── sega/
│   └── trabalhista/            — o único com declaracao-hipossuficiencia.docx
└── references/
    └── campos-por-segmento.md  — o que cada token significa e o percentual padrão por segmento
```

## Por que os templates usam tokens `{{CAMPO}}`

Os modelos originais do escritório eram documentos já preenchidos do último cliente usado como
rascunho. Isso funciona uma vez, mas quebra fácil (basta o texto mudar um pouco e a substituição
por busca-e-troca falha). Os templates desta skill foram convertidos para usar marcadores
explícitos — isso é o que torna o preenchimento confiável e repetível. Se algum modelo do
escritório mudar no futuro (nova cláusula, novo segmento), repita esse processo: abra o `.docx`,
troque os dados variáveis do cliente-exemplo por `{{TOKEN}}` correspondente, e valide com
`scripts/office/validate.py` da skill `docx` antes de salvar.

