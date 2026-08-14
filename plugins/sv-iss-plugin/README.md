# sv-iss-plugin

Plugin interno da **SV Advocacia** com as skills de Claude usadas no dia a dia do escritório, principalmente no fluxo de restituição de ISSQN (atleta/audiovisual).

> ⚠️ **Repositório privado.** Estes arquivos contêm dados reais de casos e clientes do escritório (nomes, CPF/CNPJ, valores de causa, salários de colaboradores). Não torne este repositório público sem antes sanitizar os arquivos.

## Skills incluídas

| Skill | O que faz |
|---|---|
| `triagem-restituicao-iss` | Triagem de documentação de ações de restituição de ISS (esporte/audiovisual): identifica perfil e regime tributário, extrai dados de notas fiscais, consolida planilha, apoia montagem da petição inicial e cálculo de atualização monetária (IPCA-E). |
| `procuracao-honorarios` | Gera procuração, contrato de honorários e (quando trabalhista) declaração de hipossuficiência a partir dos documentos do cliente, para os 5 tipos de ação do escritório. Envia para assinatura via ZapSign. |
| `analise-contestacao-issqn` | Mapeia todos os tópicos de uma contestação do Município contra o banco de blocos argumentativos do escritório, antes de qualquer réplica. |
| `replica-issqn` | Monta a minuta de réplica no padrão do escritório, usando o mapeamento da skill de análise de contestação. |
| `atualizacao-juridica-diaria` | Gera resumo diário com até 10 acontecimentos jurídicos relevantes (Cível, Trabalhista, Desportivo, Previdenciário) para redes sociais do escritório. |
| `controle-financeiro-plr` | Mantém o artefato "Controle Financeiro 2026 + Rateio PLR" (lê/escreve no Trello, calcula rateio trimestral de PLR dos colaboradores CLT). |

## Instalação

No Claude Code ou Cowork, adicione este repositório como plugin (via marketplace local ou apontando para esta pasta) e habilite as skills desejadas.

## Estrutura

```
sv-iss-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── triagem-restituicao-iss/
│   ├── procuracao-honorarios/
│   ├── analise-contestacao-issqn/
│   ├── replica-issqn/
│   ├── atualizacao-juridica-diaria/
│   └── controle-financeiro-plr/
└── README.md
```
