# Grungit (Blender Add-on)

Add-on para aplicar desgaste e sujeira (grunge/dirt) em materiais e gerar texturas via bake, com suporte a mapas PBR.

## Requisitos

- Blender 5.0+ (ajuste conforme sua versão)
- Cycles disponível para bake
- Arquivos de dados presentes em grungit/grungit_data

## Instalação

1. Empacote a pasta grungit em um .zip (ou use o repositório diretamente).
2. Blender → Preferences → Add-ons → Install… → selecione o .zip.
3. Ative o add-on “Grungit”.

## Uso rápido (Grungit)

1. Salve o arquivo .blend.
2. Selecione um ou mais objetos (malhas com materiais).
3. Abra o painel “Grungit” na barra lateral (N) da Viewport 3D.
4. Ajuste resolução, diretório de saída, qualidade e “Overall amount”.
5. Clique em “Apply Grungit”.

Dica: o Quick mode não faz bake e pode ser usado sem salvar o arquivo.

## Uso rápido (PBR Bake)

1. Salve o arquivo .blend.
2. Selecione os objetos.
3. Abra o painel “PBR Bake”.
4. Configure o diretório de saída e escolha canais/parâmetros (samples/margin).
5. Clique em “PBR Bake”.

Os arquivos são salvos em //Textures/ (pasta relativa ao .blend).

## Problemas comuns

- “Data files missing”: reinstale o add-on e verifique grungit/grungit_data.
- “Save the .blend file”: o bake precisa de um arquivo salvo.
- Sem materiais: o add-on ignora slots vazios ou não usados.
- Aviso “does not support blend relative // prefix”: mensagem do Blender ao usar caminhos relativos; o add-on normaliza o output.

## Teste headless (smoke test)

Requer Blender instalado localmente.

1. Defina a variável de ambiente `BLENDER_BIN` apontando para o executável do Blender (ex.: `C:\\Blender\\blender.exe`).
2. Execute o script:
	- `python scripts/run_smoke_test.py`

O teste cria um cubo, aplica Grungit em modo rápido e valida a presença do NodeGroup.

## Benchmark de performance (quick mode)

1. Defina `BLENDER_BIN` apontando para o executável do Blender.
2. Execute:
	- `python scripts/run_perf_benchmark.py`

O script imprime um JSON com tempo para cena pequena (1 objeto) e grande (25 objetos).

## E2E bake headless (Cycles)

1. Defina `BLENDER_BIN` apontando para o executável do Blender.
2. Execute:
	- `python scripts/run_e2e_bake_test.py`

O teste salva um .blend temporário, executa bake real e valida o arquivo *_Grungit.exr.

## Validação de output_dir (headless)

1. Defina `BLENDER_BIN` apontando para o executável do Blender.
2. Execute:
	- `python scripts/run_output_dir_validation_test.py`

O teste passa um caminho inválido e valida que o output é gravado no diretório padrão.

## E2E bake com cena complexa

1. Defina `BLENDER_BIN` apontando para o executável do Blender.
2. Execute:
	- `python scripts/run_e2e_complex_scene_test.py`

O teste cria materiais com nós de roughness/normal e objetos multi-user.

## E2E bake com cena realista

1. Defina `BLENDER_BIN` apontando para o executável do Blender.
2. Execute:
	- `python scripts/run_e2e_realistic_scene_test.py`

O teste cria objetos com modifiers, múltiplos materiais e texturas geradas.

## E2E bake com asset externo

1. Verifique se o arquivo assets/space_truck.blend existe.
2. Defina `BLENDER_BIN` apontando para o executável do Blender.
3. Execute:
	- `python scripts/run_e2e_external_asset_test.py`

O teste abre o .blend externo, seleciona todas as malhas e executa o bake.

## Assets de teste

- assets/space_truck.blend: usado nos testes E2E com asset externo.

## CI (GitHub Actions)

O workflow em .github/workflows/ci.yml executa smoke test e os E2E headless.

## Estrutura do projeto

- grungit/grungit.py: operador principal e bake de grunge
- grungit/grungit_ui.py: painel de UI do Grungit
- grungit/pbrbake.py: bake de mapas PBR
- grungit/pbrbake_ui.py: painel de UI do PBR Bake
- grungit/properties.py: propriedades do add-on

## Licença

Veja LICENSE.