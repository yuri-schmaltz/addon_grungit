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

## Estrutura do projeto

- grungit/grungit.py: operador principal e bake de grunge
- grungit/grungit_ui.py: painel de UI do Grungit
- grungit/pbrbake.py: bake de mapas PBR
- grungit/pbrbake_ui.py: painel de UI do PBR Bake
- grungit/properties.py: propriedades do add-on

## Licença

Veja LICENSE.