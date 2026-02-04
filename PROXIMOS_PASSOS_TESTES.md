# Próximos Passos para Execução Completa dos Testes Automatizados do Add-on Grungit

## 1. Instalação e Ativação do Add-on no Blender

1. Abra o Blender na interface gráfica.
2. Vá em **Edit > Preferences > Add-ons**.
3. Clique em **Install...** e selecione a pasta ou arquivo ZIP do add-on `grungit`.
4. Marque a caixa para ativar o add-on "Grungit".
5. Feche as preferências e salve as configurações.

## 2. Garantir Diretório de Saída para Texturas

- Certifique-se de que o diretório configurado em `output_dir` nas propriedades do Grungit seja absoluto e com permissão de escrita.
- Recomenda-se usar um caminho como `C:/Users/SEU_USUARIO/Documents/addon-grungit/tmp/integrity_output`.

## 3. Execução dos Testes Automatizados

- Execute os scripts de teste via terminal ou prompt de comando, por exemplo:
  - `python scripts/run_robustness_100x_test.py`
  - `python scripts/run_undo_redo_test.py`
  - `python scripts/run_cancel_test.py`
  - `python scripts/run_no_selection_test.py`
  - `python scripts/run_no_material_test.py`
  - `python scripts/run_no_uv_test.py`
  - `python scripts/run_perf_test.py`
  - `python scripts/run_integrity_test.py`

> **Nota:** Para testes que envolvem geração de arquivos (ex: integridade), rode o Blender em modo interativo (sem `-b`) se necessário.

## 4. Diagnóstico de Falhas

- Se algum teste falhar com erro "No module named 'grungit'":
  - Confirme que o add-on está instalado e ativado no Blender.
  - Se necessário, copie a pasta `grungit` para a pasta de add-ons do Blender:  
    `[BLENDER_PATH]/[VERSION]/scripts/addons/`
- Se não gerar arquivos de textura:
  - Verifique o caminho de saída e permissões.
  - Certifique-se de que o operador está configurado para salvar externamente.

## 5. Recomendações Finais

- Sempre valide se o operador está disponível no menu de objetos do Blender.
- Para integração contínua (CI), automatize a instalação do add-on e configure o PYTHONPATH conforme necessário.
- Documente evidências de cada execução de teste (prints, logs, arquivos gerados).

---

**Responsável:** [Seu Nome]
**Data:** 04/02/2026
