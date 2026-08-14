# SV-plugins

Marketplace privado de plugins de Claude da **SV Advocacia**.

> ⚠️ Repositório privado. Não torne público sem antes sanitizar dados reais de clientes/colaboradores presentes nas skills.

## Plugins disponíveis

| Plugin | Descrição |
|---|---|
| [`sv-iss-plugin`](./plugins/sv-iss-plugin) | Skills do fluxo de restituição de ISSQN (atleta/audiovisual), procuração/honorários, réplica a contestações, atualização jurídica diária e controle financeiro/PLR. |

## Instalar (Claude Code)

```
/plugin marketplace add pzaithammer-cell/SV-plugins
/plugin install sv-iss-plugin@sv-plugins
```

## Manter atualizado

Qualquer alteração nas skills deve ser commitada e enviada (`git push`) para este repositório. Pedro é responsável por manter o marketplace atualizado; colaboradores têm acesso de leitura.
