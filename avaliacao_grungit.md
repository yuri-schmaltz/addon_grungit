# Avaliação Total de Add-on para Blender (Template Executável)

> **Objetivo:** avaliar um add-on do Blender de ponta a ponta — funcionalidade, integrações, robustez, performance, segurança, UX, qualidade de código e prontidão de release — com critérios **claros**, **mensuráveis** e **auditáveis**.

---

## 0) Metadados do add-on

- **Nome do add-on:** Grungit
- **Versão do add-on:** 1.9.2 ([grungit/__init__.py](grungit/__init__.py#L1-L10))
- **Autor / Organização:** Abdou Bouam ([grungit/__init__.py](grungit/__init__.py#L1-L10))
- **Repositório / Página:** yuri-schmaltz/addon-grungit
- **Licença:** GPL-3.0 ([LICENSE](LICENSE#L1))
- **Tipo:** Material / Shading / Bake
- **Escopo declarado pelo autor:** aplicar desgaste/sujeira e gerar texturas via bake, com suporte PBR ([README.md](README.md#L1-L35))
- **Dependências externas:** Blender 5.0+, Cycles, arquivos de dados em grungit_data ([README.md](README.md#L5-L9))
- **Recursos do Blender usados:** Operators, Panels, PropertyGroup, NodeGroups, bake (Cycles), bpy.ops.wm.append ([grungit/__init__.py](grungit/__init__.py#L17-L54), [grungit/grungit.py](grungit/grungit.py#L22-L732), [grungit/grungit_ui.py](grungit/grungit_ui.py#L10-L95), [grungit/pbrbake.py](grungit/pbrbake.py#L13-L120), [grungit/pbrbake_ui.py](grungit/pbrbake_ui.py#L11-L65), [grungit/properties.py](grungit/properties.py#L11-L199))
- **Nível de maturidade (autor):** não declarado
- **Data da avaliação:** 03/02/2026
- **Responsável pela avaliação:** GitHub Copilot

---

## 1) Sumário executivo (preencher ao final)

- **Status geral:** ❌ Reprovado (por falta de evidências E2E/robustez/performance)
- **Pontuação total:** 42/100 (ver Rubrica)
- **Principais pontos fortes (3–5):**
  - Registro/desregistro e properties configurados corretamente ([grungit/__init__.py](grungit/__init__.py#L38-L54))
  - Validações básicas de contexto para bake ([grungit/grungit.py](grungit/grungit.py#L44-L52), [grungit/pbrbake.py](grungit/pbrbake.py#L22-L37))
  - UI clara no painel N e fluxo de uso no README ([grungit/grungit_ui.py](grungit/grungit_ui.py#L10-L95), [grungit/pbrbake_ui.py](grungit/pbrbake_ui.py#L11-L65), [README.md](README.md#L17-L35))
- **Principais riscos/lacunas (3–7):**
  - Ausência de evidências E2E completas (bake real)
  - Sem documentação de compatibilidade real por versão/OS
  - Sem política de logs/diagnóstico
- **Recomendações imediatas (Top 5):**
  1) Completar E2E com bake real (Cycles)
  2) Registrar métricas p50/p95 com cenas reais
  3) Validar compatibilidade em versões do Blender
  4) Documentar versões testadas do Blender e OS
  5) Adicionar modo de diagnóstico/logs configurável
- **Bloqueadores para release (se houver):** ausência de evidências E2E/performance

---

## 2) Escopo, suposições e “NÃO VERIFICADO”

### 2.1 Escopo incluído nesta avaliação
Marcar o que foi efetivamente testado:

- [ ] Instalação e ativação
- [ ] Fluxos E2E críticos
- [x] Integrações com Blender (UI, Operators, DataBlocks) **(code review)**
- [ ] Import/Export e I/O de arquivos (se aplicável)
- [ ] Performance
- [ ] Robustez (erros, edge cases, undo/redo)
- [ ] Segurança e privacidade (se aplicável)
- [x] Qualidade de código e manutenção **(code review)**
- [x] Documentação e suporte **(README)**
- [ ] Empacotamento e release

### 2.2 Itens NÃO VERIFICADOS (e como verificar)
| Item | Motivo | Como verificar (passos objetivos) | Owner sugerido |
|---|---|---|---|
| Instalação/ativação | Sem Blender | Instalar zip no Blender e ativar | QA |
| Fluxos E2E | Sem Blender | Executar E2E-01/02 | QA |
| Performance | Sem medição real | Rodar benchmark e registrar resultados | QA |
| Robustez | Sem falhas injetadas | Testar entradas inválidas e repetição 100× | QA |
| Empacotamento | Sem zip | Gerar zip e instalar limpo | Release |

---

## 3) Matriz de ambientes e reprodutibilidade

### 3.1 Versões do Blender
- **Versão mínima suportada (declarada):** 5.0+ ([README.md](README.md#L5-L8), [grungit/__init__.py](grungit/__init__.py#L1-L10))
- **Versões testadas:**
  - [ ] LTS: **NÃO VERIFICADO**
  - [ ] Última estável: **NÃO VERIFICADO**
  - [ ] Beta/Alpha (opcional): **NÃO VERIFICADO**

### 3.2 Sistemas operacionais
- [x] Windows (versão: **não informada**)
- [ ] Linux
- [ ] macOS

### 3.3 Hardware
- **CPU:** **NÃO VERIFICADO**
- **RAM:** **NÃO VERIFICADO**
- **GPU/Driver:** **NÃO VERIFICADO**
- **Resolução/escala UI:** **NÃO VERIFICADO**

### 3.4 Como reproduzir o ambiente
- **Fonte do add-on:** repositório local / zip
- **Procedimento de instalação reproduzível:** descrito no README ([README.md](README.md#L11-L15))
- **Comandos/scripts usados:** **NÃO VERIFICADO**

---

## 4) Inventário funcional (ANTES) — o que o add-on “promete fazer”

| ID | Função / Ação do usuário | Onde aparece (UI/atalho/menu) | Entrada | Saída esperada | Aceite (PASS/FAIL) |
|---|---|---|---|---|---|
| F-001 | Aplicar grunge/dirt | Painel “Grungit” (N-panel) | Objetos com materiais | Material com grunge aplicado | **NÃO VERIFICADO** |
| F-002 | Bake PBR | Painel “PBR Bake” (N-panel) | Objetos com materiais | Texturas PBR salvas | **NÃO VERIFICADO** |

---

## 5) Avaliação funcional (E2E) — testes e evidências

### 5.1 Fluxos críticos (3–7)
**PARCIAL:** smoke test e E2E bake headless executados (Cycles). Ainda faltam cenários adicionais.

### 5.2 Regressões e compatibilidade
- **O add-on altera configurações globais do Blender?** não observado no código.
- **O add-on interfere em outros add-ons?** não observado no código.

---

## 6) Integrações com o Blender (profundidade técnica)

### 6.1 Registro e ciclo de vida
- [x] `register()`/`unregister()` corretos e idempotentes ([grungit/__init__.py](grungit/__init__.py#L38-L54))
- [x] Sem resíduos após desinstalar (classes, keymaps, handlers, timers) ([grungit/__init__.py](grungit/__init__.py#L47-L54))
- [ ] Suporte a “Reload Scripts” / recarregar add-ons sem duplicar registro — **NÃO VERIFICADO**

**Evidência:** revisão de código.

### 6.2 UI (Panels, Menus, UIList, Popovers)
- **Localização e consistência:** N-panel, categoria “Grungit”.
- **Estados:** feedback para dados ausentes, Cycles indisponível, arquivo não salvo, seleção inválida ([grungit/grungit_ui.py](grungit/grungit_ui.py#L43-L70), [grungit/pbrbake_ui.py](grungit/pbrbake_ui.py#L28-L41))
- **Responsividade:** **NÃO VERIFICADO**
- **Acessibilidade mínima:** **NÃO VERIFICADO**

### 6.3 Operators e UX operacional
- [x] `bl_options` adequado (`REGISTER`, `UNDO`) ([grungit/grungit.py](grungit/grungit.py#L22-L26), [grungit/pbrbake.py](grungit/pbrbake.py#L13-L20))
- [ ] Compatibilidade com Undo/Redo — **NÃO VERIFICADO**
- [x] Mensagens de erro legíveis ([grungit/grungit.py](grungit/grungit.py#L44-L52), [grungit/pbrbake.py](grungit/pbrbake.py#L22-L37))
- [ ] Cancelamento funciona — **NÃO VERIFICADO**

### 6.4 Dados e DataBlocks
- [x] Uso correto de `bpy.data` / `context` ([grungit/grungit.py](grungit/grungit.py#L80-L260))
- [ ] Evita corromper cenas/arquivos — **NÃO VERIFICADO**
- [x] Custom properties com namespace ([grungit/properties.py](grungit/properties.py#L11-L199))
- [ ] Operações em batch e depsgraph — **NÃO VERIFICADO**

### 6.5 Dependência do contexto e modo
- [x] Tratamento de seleção e tipo de objeto ([grungit/grungit.py](grungit/grungit.py#L796-L816), [grungit/pbrbake.py](grungit/pbrbake.py#L22-L37))
- [ ] Tratamento de multi-object e multi-user data — **NÃO VERIFICADO**

### 6.6 Handlers, Timers, Modal Operators
- [x] Não cria handlers/timers.

### 6.7 Integrações específicas
- [x] Shader Nodes / Material Pipeline
- [ ] Geometry Nodes
- [ ] Animation/Drivers/NLA
- [ ] Render (Cycles/Eevee), Compositor
- [ ] Grease Pencil
- [ ] Asset Browser
- [ ] File Browser / IO (import/export)
- [ ] Python deps via pip / site-packages
- [ ] Integrações externas

---

## 7) Robustez e confiabilidade

### 7.1 Testes de falha (fault injection)
**NÃO VERIFICADO.**

### 7.2 Gestão de erros
- [x] Erros tratados com `report` em validações básicas ([grungit/grungit.py](grungit/grungit.py#L44-L52), [grungit/pbrbake.py](grungit/pbrbake.py#L22-L37))
- [ ] Logs úteis para diagnóstico — **NÃO VERIFICADO**

### 7.3 Estabilidade
- **Crash/hang observado?** **NÃO VERIFICADO**

---

## 8) Performance (métrica antes/depois)

**PARCIAL:** benchmark headless executado (quick mode). Valores registrados abaixo.

| Cenário | Medida | Antes | Depois | Delta | Status |
|---|---:|---:|---:|---:|---|
| Pequeno | Tempo (s) |  | 0.0359 |  |  |
| Grande | Tempo (s) |  | 0.0078 |  |  |

---

## 9) Segurança, privacidade e cadeia de suprimentos (quando aplicável)

### 9.1 Superfícies
- [ ] Acesso a rede (HTTP, sockets)
- [ ] Execução de binários/`subprocess`
- [x] Leitura/escrita fora do projeto (paths configuráveis) ([grungit/grungit.py](grungit/grungit.py#L703-L732), [grungit/pbrbake.py](grungit/pbrbake.py#L41-L90))
- [ ] Download de modelos/assets/deps
- [ ] Telemetria / envio de dados

### 9.2 Checklist essencial
- [x] Sem `shell=True` e sem concatenação de comandos
- [ ] Validação de caminhos — **NÃO VERIFICADO**
- [ ] Limites de tamanho e tempo para I/O — **NÃO VERIFICADO**
- [ ] Dependências “pinned” — N/A
- [ ] Arquivos temporários seguros — **NÃO VERIFICADO**
- [ ] Política de logs sem dados sensíveis — **NÃO VERIFICADO**

### 9.3 Licenças e compliance
- Licença do add-on: GPL-3.0 ([LICENSE](LICENSE#L1))

---

## 10) UX, consistência e acessibilidade (prático e objetivo)

### 10.1 Heurísticas (PASS/FAIL)
- [ ] Descoberta: usuário encontra a função em ≤ 10s sem ler manual — **NÃO VERIFICADO**
- [x] Feedback: pré-condições exibidas na UI ([grungit/grungit_ui.py](grungit/grungit_ui.py#L43-L70), [grungit/pbrbake_ui.py](grungit/pbrbake_ui.py#L28-L41))
- [ ] Erros: texto acionável — **NÃO VERIFICADO**
- [ ] Consistência: nomes/ícones/agrupamento alinhados ao Blender — **NÃO VERIFICADO**
- [ ] Sem “poluição” de UI — **NÃO VERIFICADO**

### 10.2 Acessibilidade mínima (quando aplicável)
- [ ] Labels claros e não ambíguos — **NÃO VERIFICADO**
- [ ] Navegação por teclado — **NÃO VERIFICADO**
- [ ] Suporte a escala UI 125%/150% sem clipping — **NÃO VERIFICADO**

---

## 11) Qualidade do código e manutenção

### 11.1 Estrutura e padrões
- [x] Organização modular (UI vs lógica) ([README.md](README.md#L43-L49))
- [ ] Tipagem/documentação interna — limitada
- [ ] Evita estados globais perigosos — usa estado em classe `Grungit`

### 11.2 Compatibilidade de API do Blender
- [ ] Sem uso de API depreciada sem fallback — **NÃO VERIFICADO**
- [ ] Tratamento de diferenças entre versões — **NÃO VERIFICADO**

### 11.3 Testabilidade e automação
- [ ] Testes automatizados (E2E completo)
- [x] Smoke E2E scriptável (quick mode)
- [x] CI com smoke test

### 11.4 Observabilidade
- [ ] Logging configurável

---

## 12) Documentação, suporte e onboarding

### 12.1 Documentação mínima
- [x] Instalação ([README.md](README.md#L11-L15))
- [x] Quickstart ([README.md](README.md#L17-L35))
- [x] Troubleshooting ([README.md](README.md#L37-L41))
- [ ] Compatibilidade (versões do Blender, OS)
- [ ] Desinstalação/limpeza
- [ ] Exemplos

### 12.2 Qualidade da documentação (PASS/FAIL)
- [x] Executável por alguém novo em ≤ 15 min (provável)
- [ ] Prints ou GIFs
- [ ] Links funcionando e atualizados — **NÃO VERIFICADO**

---

## 13) Empacotamento e release

### 13.1 Estrutura do pacote
- [ ] Zip instalável padrão Blender — **NÃO VERIFICADO**
- [x] `bl_info` completo ([grungit/__init__.py](grungit/__init__.py#L1-L10))
- [ ] Sem arquivos desnecessários — **NÃO VERIFICADO**
- [ ] Dependências inclusas ou instruções claras — **NÃO VERIFICADO**

### 13.2 Upgrade/rollback
- [ ] Atualizar versão não quebra preferências/salvos — **NÃO VERIFICADO**
- [ ] Migração de dados — **NÃO VERIFICADO**
- [ ] Rollback funciona — **NÃO VERIFICADO**

---

## 14) Rubrica de pontuação (0–5) e pesos

| Área | Peso | Nota (0–5) | Subtotal |
|---|---:|---:|---:|
| Funcionalidade E2E | 25 | 2 | 10 |
| Integrações com Blender | 15 | 3 | 9 |
| Robustez/Confiabilidade | 15 | 2 | 6 |
| Performance | 10 | 1 | 2 |
| Segurança/Privacidade (se aplicável) | 10 | 2 | 4 |
| UX/Acessibilidade | 10 | 2 | 4 |
| Qualidade de código/manutenção | 10 | 2 | 4 |
| Documentação/Onboarding | 5 | 3 | 3 |
| **TOTAL** | **100** |  | **42** |

### 14.1 Critérios de decisão (sugestão)
- ✅ **Aprovado:** ≥ 80 e **sem bloqueadores**
- ⚠️ **Aprovado com ressalvas:** 65–79 ou com riscos mitigáveis em curto prazo
- ❌ **Reprovado:** < 65 ou com bloqueadores (crash, corrupção, insegurança crítica)

---

## 15) Achados detalhados (formato obrigatório)

**A-001**
- **Categoria:** Código / Testabilidade
- **Severidade:** Média
- **Descrição objetiva:** E2E bake básico executado, mas falta ampliar cobertura (cenários e assets).
- **Evidência:** scripts em [scripts/blender_e2e_bake_test.py](scripts/blender_e2e_bake_test.py) e [scripts/run_e2e_bake_test.py](scripts/run_e2e_bake_test.py).
- **Impacto:** risco de regressões em casos não cobertos.
- **Causa provável:** testes iniciais limitados.
- **Recomendação (ação):** adicionar cenários com múltiplos materiais/objetos.
- **Validação PASS/FAIL:** geração de texturas válidas em todos os cenários.
- **Risco de regressão + mitigação:** médio; mitigar com expansão de testes.
- **Owner sugerido:** Dev/QA
- **Status:** Em progresso

**A-002**
- **Categoria:** Performance
- **Severidade:** Média
- **Descrição objetiva:** benchmark executado, mas sem p50/p95 e sem bake real.
- **Evidência:** scripts em [scripts/blender_perf_benchmark.py](scripts/blender_perf_benchmark.py) e [scripts/run_perf_benchmark.py](scripts/run_perf_benchmark.py); resultados na Seção 8.
- **Impacto:** incerteza de tempo de bake real.
- **Causa provável:** medições ainda não executadas em cenários reais.
- **Recomendação (ação):** rodar benchmark com amostras (p50/p95) e cena de bake real.
- **Validação PASS/FAIL:** tabela completa com p50/p95.
- **Risco de regressão + mitigação:** médio; mitigar com execução periódica.
- **Owner sugerido:** QA
- **Status:** Em progresso

**A-003**
- **Categoria:** Segurança
- **Severidade:** Baixa
- **Descrição objetiva:** saída de arquivos usa path fornecido sem validação.
- **Evidência:** uso direto de `output_dir` ([grungit/grungit.py](grungit/grungit.py#L703-L732), [grungit/pbrbake.py](grungit/pbrbake.py#L41-L90)).
- **Impacto:** gravação em paths inválidos/inseguros.
- **Causa provável:** ausência de sanitização.
- **Recomendação (ação):** normalizar e validar path.
- **Validação PASS/FAIL:** testar paths inválidos/relativos.
- **Risco de regressão + mitigação:** baixo; unit test de path.
- **Owner sugerido:** Dev
- **Status:** Aberto

---

## 16) Backlog executável (priorizado)

| Prioridade | Tarefa | Objetivo | Passos | Aceite | Esforço | Risco |
|---:|---|---|---|---|---|---|
| P0 | E2E completo com bake | Provar bake real | Script Blender headless | Texturas válidas | M | M |
| P1 | Rodar benchmark | Definir SLO | Executar e registrar | Tabela p50/p95 | S | L |
| P1 | Validar compatibilidade | Reduzir risco | Testar versões | Matriz preenchida | M | M |
| P2 | Validação de paths | Reduzir erros | Sanitizar output_dir | Sem crashes | S | L |

---

## 17) Apêndice — roteiro rápido de teste (checklist)

### Instalação/ativação
- [ ] Instalar via Preferences > Add-ons > Install…
- [ ] Ativar; fechar/reabrir Blender; confirmar persistência
- [ ] Desativar/reativar; confirmar ausência de duplicação

### Funcionalidade
- [x] Fluxo principal (E2E-01) PASS (bake headless)
- [ ] Fluxos secundários PASS
- [ ] Undo/Redo PASS
- [ ] Cancelamento PASS

### Robustez
- [ ] Entradas inválidas não crasham
- [ ] Execução repetida 100× sem degradar
- [ ] Cena grande não trava permanentemente

### Performance
- [x] Medições coletadas e registradas (quick mode)

### Segurança (se aplicável)
- [ ] Sem execução insegura / downloads sem validação

### Documentação
- [ ] Quickstart executável do zero

---

## 18) Registro de evidências

| Evidência | Tipo | Local (arquivo/URL/caminho) | Observação |
|---|---|---|---|
| E-001 | Código | [grungit/__init__.py](grungit/__init__.py#L1-L54) | `bl_info`, register/unregister |
| E-002 | Código | [grungit/grungit.py](grungit/grungit.py#L44-L816) | validações e execução do `Grungit` |
| E-003 | Código | [grungit/pbrbake.py](grungit/pbrbake.py#L13-L120) | validações e bake PBR |
| E-004 | README | [README.md](README.md#L5-L59) | requisitos, smoke test e benchmark |
| E-005 | CI | [.github/workflows/ci.yml](.github/workflows/ci.yml) | smoke test e E2E bake no GitHub Actions |
| E-006 | Log | scripts/run_smoke_test.py (execução local) | Smoke test OK (Blender 5.0.0) |
| E-007 | Log | scripts/run_perf_benchmark.py (execução local) | JSON: small=0.0359s, large=0.0078s |
| E-008 | Log | scripts/run_e2e_bake_test.py (execução local) | E2E bake OK (BakeMat_Grungit.exr) |
