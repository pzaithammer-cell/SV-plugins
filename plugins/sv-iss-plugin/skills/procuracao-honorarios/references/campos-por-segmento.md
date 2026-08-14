# Campos por segmento

Cada template em `assets/templates/<segmento>/` usa os mesmos cinco tokens. O que muda de
segmento para segmento é o texto fixo ao redor deles (objeto da ação, cláusulas) e o percentual
padrão de honorários — não os nomes dos tokens.

## Os cinco tokens

| Token | O que é | Aparece em |
|---|---|---|
| `{{OUTORGANTE_NOME}}` | Nome do cliente (PF) ou razão social (PJ), exatamente como consta no documento de identificação | Procuração, Contrato, Declaração |
| `{{OUTORGANTE_QUALIFICACAO}}` | Bloco de qualificação completo — ver formatos abaixo | Procuração, Contrato, Declaração |
| `{{REU}}` | Contra quem é a ação (réu/parte adversa) — cidade, clube, empresa, conforme o segmento | Procuração, Contrato |
| `{{PERCENTUAL}}` | Percentual de honorários por extenso, ex: `25% (vinte e cinco por cento)` | Contrato |
| `{{DATA}}` | Data do documento por extenso, ex: `07 de agosto de 2026` | Procuração, Contrato, Declaração |

Nunca invente ou pule um token — se o dado não estiver nos documentos que o cliente mandou,
pergunte ao Pedro antes de gerar o arquivo final. O `fill_template.py` já falha (por padrão)
se sobrar algum `{{...}}` sem preencher, exatamente para evitar isso.

## Formato de `{{OUTORGANTE_QUALIFICACAO}}`

Este token carrega o parágrafo inteiro de qualificação, sem quebras internas — é mais robusto
tentar tokenizar cada CPF/RG/endereço separadamente, porque o formato varia muito entre pessoa
física e jurídica, e nem todo cliente tem todos os dados (nem todo mundo informa e-mail, nem todo
atleta tem inscrição CBF, etc.). Monte o texto seguindo o padrão observado nos modelos:

**Pessoa física** (ex.: atleta):
```
brasileiro, [estado civil,] [profissão,] [filho(a) de X,] [nascido em DD/MM/AAAA,]
CPF nº XXX.XXX.XXX-XX, RG nº XXXXXXXXX SSP/UF, [inscrição CBF nº XXXXX,]
[com endereço eletrônico email@exemplo.com,] residente e domiciliado na Rua X, nº X,
[complemento,] Bairro, Cidade/UF, CEP XXXXX-XXX.
```

**Pessoa jurídica** (ex.: empresa/produtora):
```
pessoa jurídica de direito privado, inscrita no CNPJ/MF sob o nº XX.XXX.XXX/0001-XX,
com sede na Rua X, nº X, [complemento,] Bairro, CEP XXXXX-XXX, Cidade/UF, neste ato
representada por seu(sua) [administrador(a)/sócio(a)], NOME DO REPRESENTANTE, brasileiro(a),
[estado civil,] [profissão,] CPF nº XXX.XXX.XXX-XX, RG nº XXXXXXXXX SSP/UF, residente e
domiciliado(a) na Rua X, nº X, Bairro, Cidade/UF, CEP XXXXX-XXX.
```

Se o contrato social não deixar claro quem administra isoladamente (mais de um administrador,
ou administração conjunta), pare e pergunte ao Pedro quem deve assinar — não presuma.

**Atenção à pontuação final:** na Procuração e no Contrato, o texto fixo do modelo não coloca
nada depois do token — então `OUTORGANTE_QUALIFICACAO` deve terminar com ponto final
(ex.: `..., CEP 57.035-825, Maceió/AL.`). Já na Declaração de Hipossuficiência (Trabalhista), o
modelo já tem uma vírgula fixa logo depois do token, continuando a frase com "declaro não ter
condições..." — nesse caso `OUTORGANTE_QUALIFICACAO` **não deve** terminar com ponto (termine
apenas no último dado, sem pontuação), senão sai ".," duplicado.

## Por segmento

### ISS Atleta/Jogador e ISS Audiovisual (`iss-jogador/`, `iss-audiovisual/`)
Mesmo texto de cláusulas nos dois — a única diferença de fato é qual pasta/nome usar (o Pedro
trata os dois como o mesmo tipo de ação: Ação Declaratória de Não Incidência de ISSQN c/c
Repetição de Indébito Tributário).
- `{{REU}}`: cidade/UF do Município réu, ex. `Natal/RN`. O texto fixo em volta já diz
  "Município de {{REU}}" — não repita "Município de" dentro do token.
- `{{PERCENTUAL}}` padrão: `25% (vinte e cinco por cento)` — confirme com o Pedro se for diferente.
- Cláusula de autorização de uso de imagem do sócio está fixa no contrato — normal, não precisa tocar.

### Trabalhista (`trabalhista/`)
- `{{REU}}`: nome do empregador/clube, ex. `Operário Futebol Clube`.
- `{{PERCENTUAL}}` padrão: `20% (vinte por cento)`.
- Único segmento com declaração de hipossuficiência — gerar sempre os três documentos
  (procuração, contrato, declaração) juntos.

### SEGA (`sega/`)
- `{{REU}}`: em geral a produtora/empresa de jogo (histórico: SEGA Games C. LTD), mas o
  template está parametrizado caso outro caso similar apareça.
- `{{PERCENTUAL}}` padrão: `25% (vinte e cinco por cento)`.
- Casos de indenização por uso indevido de imagem — cliente é sempre pessoa física (atleta).

### CNRD (`cnrd/`)
- `{{REU}}`: clube réu, ex. `Club Athletico Paranaense`.
- `{{PERCENTUAL}}` padrão: `20% (vinte por cento)`.
- Objeto: notificação extrajudicial + CNRD (Câmara Nacional de Resolução de Disputas da CBF).

## O que NUNCA muda (não precisa de token)
- Qualificação dos outorgados/contratados (os 5 sócios do escritório, OABs, CPFs, endereço).
- Cláusula de poderes "ad judicia et extra" da procuração.
- Foro de eleição (Curitiba/PR ou Curitiba – Paraná, conforme o modelo original de cada segmento).
- Estrutura das cláusulas de honorários (dedução, sucumbência, rescisão, foro).
