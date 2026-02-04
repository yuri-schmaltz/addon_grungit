"""Teste de integridade dos arquivos gerados pelo bake Grungit."""
import sys
from pathlib import Path
import bpy  # type: ignore
import os

ADDON_MODULE = "grungit"

def ensure_addon_enabled():
    prefs = bpy.context.preferences
    if ADDON_MODULE in prefs.addons:
        return
    try:
        bpy.ops.preferences.addon_enable(module=ADDON_MODULE)
    except Exception:
        pass
    if ADDON_MODULE in prefs.addons:
        return
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    try:
        module = __import__(ADDON_MODULE)
        if hasattr(module, "register"):
            module.register()
    except Exception as exc:
        raise RuntimeError(f"Falha ao habilitar o add-on Grungit: {exc}") from exc
    if ADDON_MODULE in prefs.addons:
        return
    if not hasattr(bpy.types.Scene, "grungit"):
        raise RuntimeError("Falha ao habilitar o add-on Grungit.")

# Importa e registra o módulo grungit manualmente se não estiver ativado
try:
    import grungit
    if hasattr(grungit, "register"):
        grungit.register()
except Exception as exc:
    print(f"[WARN] Falha ao importar/registrar grungit: {exc}")

def main():
    ensure_addon_enabled()
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.name = "IntegrityObj"
    mat = bpy.data.materials.new(name="IntegrityMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    # Salva o arquivo .blend antes de executar o operador
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "integrity_test.blend"
    bpy.ops.wm.save_mainfile(filepath=str(blend_path))
    # Executa o bake
    result = bpy.ops.object.grungit()
    # Força o output_dir para um caminho absoluto e existente
    output_dir = tmp_dir / "integrity_output"
    output_dir.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.grungit.output_dir = str(output_dir)
    # Verifica se arquivos de textura foram gerados
    if not output_dir.is_absolute():
        output_dir = (repo_root / output_dir).resolve()
    found = False
    for ext in (".png", ".exr", ".jpg"):
        for file in output_dir.glob(f"*{ext}"):
            if file.stat().st_size > 0:
                print(f"PASS: Arquivo gerado: {file} ({file.stat().st_size} bytes)")
                found = True
    if not found:
        print("FAIL: Nenhum arquivo de textura gerado ou arquivo vazio.")
        sys.exit(1)

if __name__ == "__main__":
    main()
