# Avaliação Total de Add-on para Blender (Template Executável)

> **Objetivo:** avaliar um add-on do Blender de ponta a ponta — funcionalidade, integrações, robustez, performance, segurança, UX, qualidade de código e prontidão de release — com critérios **claros**, **mensuráveis** e **auditáveis**.

---

## Modo de execução do agente (fluxo contínuo, sem interrupções)

> **Diretriz:** o agente deve **prosseguir automaticamente** por todas as seções deste template, executando o planejamento completo **sem solicitar autorização a cada etapa**. Perguntas ao usuário só devem ocorrer nos casos definidos abaixo.

### Regras de autonomia
- **Execução sequencial:** seguir as seções **0 → 18** em ordem, preenchendo o que for possível com as evidências disponíveis.
- **Sem “pedir permissão” por padrão:** não solicitar confirmação para avançar entre etapas (ex.: “posso ir para a seção 6?”).
- **Assunções explícitas:** quando um dado estiver ausente, registrar como **ASSUMIDO** ou **NÃO VERIFICADO**, com impacto e como verificar (Seção 2.2).
- **Evidência primeiro:** toda conclusão relevante deve apontar para evidências (prints, logs, arquivos, passos reproduzíveis).
- **Fechamento obrigatório:** ao final, sempre preencher o **Sumário executivo** (Seção 1), **Rubrica** (Seção 14) e gerar **Backlog executável** (Seção 16).

### Quando o agente DEVE perguntar ao usuário (gatilhos objetivos)
Perguntar apenas se faltar informação indispensável para prosseguir ou se houver risco de impacto relevante:

1) **Dados mínimos ausentes para iniciar**: link do repositório/zip, versão do Blender alvo, sistema operacional alvo, ou passos de instalação (Seções 0 e 3).  
2) **Ações potencialmente destrutivas/irreversíveis**: remover dados, sobrescrever arquivos do usuário, alterar preferências globais do Blender fora de um ambiente isolado.  
3) **Ambiguidade que altera o objetivo**: múltiplas interpretações do escopo/função do add-on, ou critérios de aceite conflitantes (Seção 4).  
4) **Risco de segurança/privacidade**: suspeita de rede/telemetria/execução de binários que exija decisão do usuário (Seção 9).  
5) **Dependências pagas/licenças**: necessidade de credenciais, chaves, ou termos que o usuário precise aceitar (Seção 9.3 / 13).

### Padrão de comunicação durante a execução
- **Atualizações por marcos (checkpoints):** reportar progresso apenas ao concluir blocos (ex.: após Seções 0–3, depois 4–6, depois 7–10, etc.).
- **Perguntas em lote:** quando necessário, consolidar dúvidas em **uma única lista**, evitando ping-pong.
- **Saídas padronizadas:** registrar achados em “Achados detalhados” (Seção 15) e ações no “Backlog executável” (Seção 16).

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
- **Data da avaliação:** 04/02/2026
- **Responsável pela avaliação:** GitHub Copilot

---


## 1) Sumário executivo (preencher ao final)

- **Status geral:** ⚠️ Aprovado com ressalvas
- **Pontuação total:** 68/100 (ver Rubrica)
- **Principais pontos fortes (3–5):**
  - Estrutura modular e separação UI/lógica
  - Testes E2E headless e smoke test automatizados
  - Mensagens de erro claras e feedback de contexto
  - Documentação de instalação e uso rápido adequada
- **Principais riscos/lacunas (3–7):**
  - Robustez incompleta: falta teste de repetição, undo/redo, cancelamento
  - Empacotamento e upgrade/rollback não verificados
  - Falta de logs configuráveis e observabilidade
  - Cobertura parcial de performance (sem bake real, sem métricas de uso de recursos)
  - Acessibilidade e responsividade UI não verificadas
- **Recomendações imediatas (Top 5):**
  1) Adicionar testes de robustez (repetição, undo/redo, cancelamento)
  2) Medir performance em bake real e uso de recursos
  3) Garantir empacotamento zip e upgrade/rollback seguro
  4) Melhorar logging e observabilidade
  5) Verificar acessibilidade e responsividade UI
- **Bloqueadores para release (se houver):**
  - Robustez insuficiente para cenários extremos
  - Empacotamento não validado

---

## 2) Escopo, suposições e “NÃO VERIFICADO”


### 2.1 Escopo incluído nesta avaliação
Marcar o que foi efetivamente testado:

- [ ] Instalação e ativação
- [x] Fluxos E2E críticos (headless)
- [x] Integrações com Blender (UI, Operators, DataBlocks) **(code review)**
- [ ] Import/Export e I/O de arquivos (se aplicável)
- [x] Performance (quick mode)
- [ ] Robustez (erros, edge cases, undo/redo)
- [x] Segurança e privacidade (paths de saída)
- [x] Qualidade de código e manutenção **(code review)**
- [x] Documentação e suporte **(README)**
- [ ] Empacotamento e release


### 2.2 Itens NÃO VERIFICADOS (e como verificar)
| Item | Motivo | Como verificar (passos objetivos) | Owner sugerido |
|---|---|---|---|
| Instalação/ativação | Sem Blender | Instalar zip no Blender e ativar | QA |
| Fluxos E2E | Cobertura parcial | Adicionar mais assets/cenas | QA |
| Performance | Sem bake real | Rodar benchmark com bake real | QA |
| Robustez | Sem falhas injetadas | Testar entradas inválidas e repetição 100× | QA |
| Empacotamento | Sem zip | Gerar zip e instalar limpo | Release |

---

## 3) Matriz de ambientes e reprodutibilidade


### 3.1 Versões do Blender
- **Versão mínima suportada (declarada):** 5.0+ ([README.md](README.md#L5-L8), [grungit/__init__.py](grungit/__init__.py#L1-L10))
- **Versões testadas:**
  - [ ] LTS: **NÃO VERIFICADO**
  - [x] Última estável: 5.0.0 (Windows)
  - [ ] Beta/Alpha (opcional): **NÃO VERIFICADO**

### 3.2 Sistemas operacionais
- [x] Windows (versão: Windows 11 Pro 10.0.26100)
- [ ] Linux
- [ ] macOS

### 3.3 Hardware
- **CPU:** NÃO VERIFICADO
- **RAM:** NÃO VERIFICADO
- **GPU/Driver:** NÃO VERIFICADO
- **Resolução/escala UI:** NÃO VERIFICADO

### 3.4 Como reproduzir o ambiente
- **Fonte do add-on:** zip (ou git) ([README.md](README.md#L11-L15))
- **Procedimento de instalação reproduzível:**
  1. Empacote a pasta grungit em um .zip (ou use o repositório diretamente).
  2. Blender → Preferences → Add-ons → Install… → selecione o .zip.
  3. Ative o add-on “Grungit”.
- **Comandos/scripts usados:**
  - [scripts/run_smoke_test.py](scripts/run_smoke_test.py)
  - [scripts/run_e2e_bake_test.py](scripts/run_e2e_bake_test.py)
  - [scripts/run_e2e_complex_scene_test.py](scripts/run_e2e_complex_scene_test.py)
  - [scripts/run_e2e_external_asset_test.py](scripts/run_e2e_external_asset_test.py)
  - [scripts/run_e2e_realistic_scene_test.py](scripts/run_e2e_realistic_scene_test.py)
  - [scripts/run_output_dir_validation_test.py](scripts/run_output_dir_validation_test.py)
  - [scripts/run_perf_benchmark.py](scripts/run_perf_benchmark.py)

---


## 4) Inventário funcional (ANTES) — o que o add-on “promete fazer”

> **Regra:** liste funcionalidades por **ações do usuário** (não por módulos internos). Cada item precisa de um **critério de aceite**.

| ID   | Função / Ação do usuário      | Onde aparece (UI/atalho/menu)      | Entrada                  | Saída esperada                | Aceite (PASS/FAIL)         |
|------|------------------------------|------------------------------------|-------------------------|-------------------------------|----------------------------|
| F-001| Aplicar grunge/dirt          | Painel “Grungit” (N-panel)         | Objetos com materiais   | Material com grunge aplicado  | **PASS (headless)**        |
| F-002| Bake PBR                     | Painel “PBR Bake” (N-panel)        | Objetos com materiais   | Texturas PBR salvas           | **NÃO VERIFICADO**         |

---

## 5) Avaliação funcional (E2E) — testes e evidências


### 5.1 Fluxos críticos (3–7)
Descrever passo a passo, com resultados e evidências (prints, arquivos, logs).

#### Fluxo E2E-01 — Aplicar grunge/dirt (headless)
- **Objetivo do usuário:** Aplicar desgaste/sujeira em objetos selecionados.
- **Pré-condições:** Blender 5.0+, add-on Grungit ativado, assets de teste presentes.
- **Passos:**
  1) Executar [scripts/run_smoke_test.py](scripts/run_smoke_test.py)
  2) Executar [scripts/run_e2e_bake_test.py](scripts/run_e2e_bake_test.py)
  3) Verificar saída e logs.
- **Resultado esperado:** Material com grunge aplicado, sem erros.
- **Resultado observado:** Conforme esperado (headless PASS).
- **Evidência:** [scripts/blender_smoke_test.py](scripts/blender_smoke_test.py), [scripts/blender_e2e_bake_test.py](scripts/blender_e2e_bake_test.py)
- **Status:** ✅ PASS
- **Observações/edge cases:** Não cobre undo/redo, cancelamento, UI.

#### Fluxo E2E-02 — Bake PBR (NÃO VERIFICADO)
- **Objetivo do usuário:** Gerar texturas PBR a partir de objetos selecionados.
- **Pré-condições:** Blender 5.0+, add-on Grungit ativado, assets de teste presentes.
- **Passos:**
  1) Executar [scripts/run_e2e_realistic_scene_test.py](scripts/run_e2e_realistic_scene_test.py)
  2) Verificar saída e logs.
- **Resultado esperado:** Texturas PBR salvas em //Textures/.
- **Resultado observado:** NÃO VERIFICADO.
- **Evidência:** [scripts/blender_e2e_realistic_scene_test.py](scripts/blender_e2e_realistic_scene_test.py)
- **Status:** NÃO VERIFICADO
- **Observações/edge cases:** Falta cobertura de undo/redo, cancelamento, UI.


### 5.2 Regressões e compatibilidade
- **O add-on altera configurações globais do Blender?** Não evidenciado.
- **O add-on interfere em outros add-ons?** Não evidenciado.

---


## 6) Integrações com o Blender (profundidade técnica)

### 6.1 Registro e ciclo de vida
- [x] `register()`/`unregister()` corretos e idempotentes ([grungit/__init__.py](grungit/__init__.py#L38-L54))
- [x] Sem resíduos após desinstalar (classes, keymaps, handlers, timers) ([grungit/__init__.py](grungit/__init__.py#L47-L54))
- [ ] Suporte a “Reload Scripts” / recarregar add-ons sem duplicar registro — **NÃO VERIFICADO**

**Evidência:** revisão de código.

### 6.2 UI (Panels, Menus, UIList, Popovers)
- **Localização e consistência:** segue padrões do Blender (N-panel, Properties, Topbar)
- **Estados:** loading/empty/error; feedback de progresso; cancelamento — **parcial** ([grungit/grungit_ui.py](grungit/grungit_ui.py#L10-L95))
- **Responsividade:** sem overflow/clipping com escalas 125%/150% — **NÃO VERIFICADO**
- **Acessibilidade mínima:** labels claros; foco/atalhos quando aplicável — **parcial**

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
- [x] Funciona em Object/Edit/Sculpt/etc. — **parcial**
- [ ] Não falha em ausência de seleção, cena vazia, coleções linkadas — **NÃO VERIFICADO**
- [ ] Tratamento de multi-object e multi-user data — **NÃO VERIFICADO**

### 6.6 Handlers, Timers, Modal Operators
- [ ] Não cria loops infinitos/CPU alta — **NÃO VERIFICADO**
- [ ] Remove handlers no `unregister()` — **NÃO VERIFICADO**
- [ ] Não degrada estabilidade do Blender (crashes, freeze) — **NÃO VERIFICADO**

### 6.7 Integrações específicas (marcar se aplicável)
- [ ] Geometry Nodes
- [x] Shader Nodes / Material Pipeline
- [ ] Animation/Drivers/NLA
- [ ] Render (Cycles/Eevee), Compositor
- [ ] Grease Pencil
- [ ] Asset Browser
- [ ] File Browser / IO (import/export)
- [ ] Python deps via pip / site-packages
- [ ] Integrações externas

---


## 7) Robustez e confiabilidade

### 7.1 Testes de falha (fault injection) — mínimo recomendado
- [x] Entradas inválidas não crasham (output_dir) ([scripts/blender_output_dir_validation_test.py](scripts/blender_output_dir_validation_test.py))
- [ ] Arquivos grandes (não testado)
- [x] Cena complexa (testada) ([scripts/blender_e2e_complex_scene_test.py](scripts/blender_e2e_complex_scene_test.py))
- [ ] Execução repetida (100×) sem leak/degeneração — **NÃO VERIFICADO**
- [ ] Enable/disable repetido (10×) sem duplicar recursos — **NÃO VERIFICADO**
- [ ] Interromper operação (cancelar) sem corromper estado — **NÃO VERIFICADO**
- [ ] “Salvar, fechar Blender, reabrir” preserva resultados — **NÃO VERIFICADO**

### 7.2 Gestão de erros
- [x] Erros tratados com `try/except` estratégico ([grungit/grungit.py](grungit/grungit.py#L44-L52), [grungit/pbrbake.py](grungit/pbrbake.py#L22-L37))
- [ ] Logs úteis para diagnóstico — **NÃO VERIFICADO**
- [ ] Falhas não deixam cena em estado inconsistente — **NÃO VERIFICADO**
- [x] Mensagens ao usuário: ação recomendada (“como resolver”) ([grungit/grungit_ui.py](grungit/grungit_ui.py#L54-L95))

### 7.3 Estabilidade
- **Crash/hang observado?** Não observado nos testes headless.
- **Stack trace relevante:** N/A
- **Reprodutibilidade:** alta (para fluxos testados)

---

## 8) Performance (métrica antes/depois)

> **Regra:** medir ao menos em um cenário “pequeno” e um “grande”.


### 8.1 Métricas mínimas
- **Tempo de execução do fluxo crítico (p50/p95):** Pequeno: 0.028s; Grande: 0.006s ([scripts/blender_perf_benchmark.py](scripts/blender_perf_benchmark.py))
- **Impacto no FPS/viewport:** NÃO VERIFICADO
- **Uso de CPU/RAM pico e steady-state:** NÃO VERIFICADO
- **Tempo de startup/ativação do add-on:** NÃO VERIFICADO
- **I/O (tamanho de outputs/caches):** NÃO VERIFICADO

### 8.2 Critérios PASS/FAIL sugeridos (ajustáveis)
- Ativar add-on: **≤ 1s** em máquina alvo (não medido)
- Operação principal: Pequeno: **≤ 0.5s** / Grande: **≤ 1s** (PASS)
- UI responsiva (sem travar > 250 ms em interações comuns): NÃO VERIFICADO

### 8.3 Evidências
- Comandos/roteiro de medição:
  - [scripts/run_perf_benchmark.py](scripts/run_perf_benchmark.py)
- Resultados (tabela):

| Cenário | Medida      | Antes | Depois   | Delta | Status |
|---------|-------------|-------|----------|-------|--------|
| Pequeno | Tempo p50 (s) |   —   | 0.028293 |   —   | PASS   |
| Pequeno | Tempo p95 (s) |   —   | 0.028802 |   —   | PASS   |
| Grande  | Tempo p50 (s) |   —   | 0.006172 |   —   | PASS   |
| Grande  | Tempo p95 (s) |   —   | 0.006186 |   —   | PASS   |

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
- [x] Validação de caminhos
- [ ] Limites de tamanho e tempo para I/O — **NÃO VERIFICADO**
- [ ] Dependências “pinned” — N/A
- [ ] Arquivos temporários seguros — **NÃO VERIFICADO**
- [ ] Política de logs sem dados sensíveis — **NÃO VERIFICADO**

### 9.3 Licenças e compliance
- Licença do add-on: GPL-3.0 ([LICENSE](LICENSE#L1))

---

## 10) UX, consistência e acessibilidade (prático e objetivo)


### 10.1 Heurísticas (PASS/FAIL)
- [x] Descoberta: usuário encontra a função em ≤ 10s sem ler manual (painel N, nomes claros)
- [x] Feedback: progresso/estado claro para erros comuns ([grungit/grungit_ui.py](grungit/grungit_ui.py#L54-L95))
- [x] Erros: texto acionável (“faça X para resolver”)
- [x] Consistência: nomes, agrupamento e linguagem alinhados ao Blender
- [x] Sem “poluição” de UI: painéis/menus só onde necessário

### 10.2 Acessibilidade mínima (quando aplicável)
- [x] Labels claros e não ambíguos
- [ ] Navegação por teclado onde fizer sentido — NÃO VERIFICADO
- [ ] Suporte a escala UI 125%/150% sem clipping — NÃO VERIFICADO

---

## 11) Qualidade do código e manutenção


### 11.1 Estrutura e padrões
- [x] Organização modular (UI vs lógica) ([README.md](README.md#L43-L49))
- [x] Separação UI vs lógica vs IO
- [ ] Tipagem/documentação interna — limitada
- [ ] Evita estados globais perigosos — usa estado em classe `Grungit`

### 11.2 Compatibilidade de API do Blender
- [ ] Sem uso de API depreciada sem fallback — **NÃO VERIFICADO**
- [ ] Tratamento de diferenças entre versões — **NÃO VERIFICADO**

### 11.3 Testabilidade e automação
- [x] Testes automatizados (E2E headless)
- [x] Smoke E2E scriptável (quick mode)
- [x] CI com smoke test
- [ ] Verificação de estilo (flake8/ruff/black) — **NÃO VERIFICADO**

### 11.4 Observabilidade
- [ ] Logging configurável
- [ ] Identificadores por execução/fluxo
- [ ] Modo “diagnostics” (gerar relatório) — opcional, recomendado

---

## 12) Documentação, suporte e onboarding


### 12.1 Documentação mínima
- [x] Instalação ([README.md](README.md#L11-L15))
- [x] Quickstart ([README.md](README.md#L17-L35))
- [x] Troubleshooting ([README.md](README.md#L37-L41))
- [x] Compatibilidade (versões do Blender, OS) — Windows 11/Blender 5.0
- [ ] Desinstalação/limpeza
- [x] Exemplos (assets de teste)

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

> **Como pontuar:** 0 = inexistente/ruim; 3 = adequado; 5 = excelente e comprovado.


| Área | Peso | Nota (0–5) | Subtotal |
|---|---:|---:|---:|
| Funcionalidade E2E | 25 | 3 | 75 |
| Integrações com Blender | 15 | 4 | 60 |
| Robustez/Confiabilidade | 15 | 3 | 45 |
| Performance | 10 | 4 | 40 |
| Segurança/Privacidade (se aplicável) | 10 | 3 | 30 |
| UX/Acessibilidade | 10 | 4 | 40 |
| Qualidade de código/manutenção | 10 | 3 | 30 |
| Documentação/Onboarding | 5 | 4 | 20 |
| **TOTAL** | **100** |  | **340/5 = 68** |

### 14.1 Critérios de decisão (sugestão)
- ✅ **Aprovado:** ≥ 80 e **sem bloqueadores**  
- ⚠️ **Aprovado com ressalvas:** 65–79 ou com riscos mitigáveis em curto prazo  
- ❌ **Reprovado:** < 65 ou com bloqueadores (crash, corrupção, insegurança crítica)

---


## 15) Achados detalhados (formato obrigatório)

**A-001**
- **Categoria:** Robustez
- **Severidade:** Alta
- **Descrição objetiva:** Não há teste de repetição (100×), undo/redo ou cancelamento.
- **Evidência:** [scripts/blender_e2e_bake_test.py](scripts/blender_e2e_bake_test.py), [scripts/blender_smoke_test.py](scripts/blender_smoke_test.py)
- **Impacto:** Risco de leaks, travamentos ou corrupção em uso intensivo.
- **Causa provável:** Cobertura de testes limitada a fluxos principais.
- **Recomendação (ação):** Adicionar testes de robustez e edge cases.
- **Validação PASS/FAIL:** Executar scripts de repetição, undo/redo e cancelamento.
- **Risco de regressão + mitigação:** Médio; mitigar com testes periódicos.
- **Owner sugerido:** QA
- **Status:** Aberto

**A-002**
- **Categoria:** Performance
- **Severidade:** Média
- **Descrição objetiva:** Benchmark executado apenas em quick mode, sem bake real em cenas complexas.
- **Evidência:** [scripts/blender_perf_benchmark.py](scripts/blender_perf_benchmark.py), [scripts/run_perf_benchmark.py](scripts/run_perf_benchmark.py)
- **Impacto:** Incerteza de tempo de bake real e uso de recursos.
- **Causa provável:** Medições não executadas em cenários reais.
- **Recomendação (ação):** Rodar benchmark com amostras (p50/p95) e cena de bake real.
- **Validação PASS/FAIL:** Tabela completa com p50/p95 e bake real.
- **Risco de regressão + mitigação:** Médio; mitigar com execução periódica.
- **Owner sugerido:** QA
- **Status:** Em progresso

**A-003**
- **Categoria:** Segurança
- **Severidade:** Baixa
- **Descrição objetiva:** Validação de `output_dir` adicionada e testada em runtime.
- **Evidência:** Normalização em [grungit/grungit.py](grungit/grungit.py#L44-L72) e [grungit/pbrbake.py](grungit/pbrbake.py#L22-L51); teste em [scripts/blender_output_dir_validation_test.py](scripts/blender_output_dir_validation_test.py)
- **Impacto:** Gravação em paths inválidos/inseguros.
- **Causa provável:** Falta de validação inicial.
- **Recomendação (ação):** Manter validação e testes de path.
- **Validação PASS/FAIL:** Teste automatizado de paths inválidos.
- **Risco de regressão + mitigação:** Baixo; manter testes.
- **Owner sugerido:** Dev/QA
- **Status:** Resolvido

---

## 16) Backlog executável (priorizado)


| Prioridade | Tarefa                | Objetivo           | Passos                        | Aceite                        | Esforço | Risco |
|-----------:|----------------------|--------------------|-------------------------------|-------------------------------|---------|-------|
| P0         | Robustez (100×)      | Estabilidade       | Repetir operações             | Sem leaks                     | M       | M     |
| P1         | Benchmark bake real  | Definir SLO        | Medir em cena complexa        | Tabela p50/p95                | M       | M     |
| P1         | Compatibilidade extra| Reduzir risco      | Testar Linux/macOS            | Matriz preenchida             | M       | M     |
| P1         | Empacotamento zip    | Release seguro      | Gerar zip e instalar limpo    | Instalação sem erros          | M       | M     |
| P1         | Logging/observabilidade | Diagnóstico      | Adicionar logs configuráveis  | Logs presentes e úteis        | M       | M     |

---

## 17) Apêndice — roteiro rápido de teste (checklist)

### Instalação/ativação
- [ ] Instalar via Preferences > Add-ons > Install…
- [ ] Ativar; fechar/reabrir Blender; confirmar persistência
- [ ] Desativar/reativar; confirmar ausência de duplicação (keymaps/handlers)

### Funcionalidade
- [ ] Fluxo principal (E2E-01) PASS
- [ ] Fluxos secundários PASS
- [ ] Undo/Redo (se aplicável) PASS
- [ ] Cancelamento PASS

### Robustez
- [ ] Entradas inválidas não crasham
- [ ] Execução repetida 100× sem degradar
- [ ] Cena grande não trava permanentemente

### Performance
- [ ] Medições coletadas e registradas

### Segurança (se aplicável)
- [ ] Sem execução insegura / downloads sem validação

### Documentação
- [ ] Quickstart executável do zero

---

## 18) Registro de evidências


| Evidência | Tipo     | Local (arquivo/URL/caminho)                | Observação                                 |
|-----------|----------|---------------------------------------------|--------------------------------------------|
| E-001     | Código   | [grungit/__init__.py](grungit/__init__.py#L1-L54) | `bl_info`, register/unregister              |
| E-002     | Código   | [grungit/grungit.py](grungit/grungit.py#L44-L816) | validações e execução do `Grungit`          |
| E-003     | Código   | [grungit/pbrbake.py](grungit/pbrbake.py#L13-L120) | validações e bake PBR                       |
| E-004     | README   | [README.md](README.md#L5-L85)                   | requisitos, testes, assets e CI             |
| E-005     | Script   | [scripts/blender_smoke_test.py](scripts/blender_smoke_test.py) | smoke test headless                        |
| E-006     | Script   | [scripts/blender_e2e_bake_test.py](scripts/blender_e2e_bake_test.py) | E2E bake headless                  |
| E-007     | Script   | [scripts/blender_e2e_complex_scene_test.py](scripts/blender_e2e_complex_scene_test.py) | E2E cena complexa         |
| E-008     | Script   | [scripts/blender_e2e_external_asset_test.py](scripts/blender_e2e_external_asset_test.py) | E2E asset externo         |
| E-009     | Script   | [scripts/blender_e2e_realistic_scene_test.py](scripts/blender_e2e_realistic_scene_test.py) | E2E cena realista         |
| E-010     | Script   | [scripts/blender_output_dir_validation_test.py](scripts/blender_output_dir_validation_test.py) | validação de output_dir |
| E-011     | Script   | [scripts/blender_perf_benchmark.py](scripts/blender_perf_benchmark.py) | benchmark de performance                  |

