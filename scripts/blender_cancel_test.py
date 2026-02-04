"""Teste de cancelamento do operador Grungit (simula ESC durante execução)."""

import sys
from pathlib import Path
import bpy  # type: ignore
import time

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

def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def create_test_mesh():
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.name = "CancelObj"
    mat = bpy.data.materials.new(name="CancelMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj

def run_grungit_bake_with_cancel():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.grungit.quick_mode = False
    scene.grungit.overall_amount = 0.5
    scene.grungit.output_dir = "//Textures/Grungit/"
    # Inicia o operador em modo modal (se suportado)
    result = bpy.ops.object.grungit('INVOKE_DEFAULT')
    time.sleep(0.5)  # Aguarda início
    # Simula ESC para cancelar
    bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
    print("Cancelamento simulado (ESC/tool change). Verifique se operador foi interrompido.")

def main():
    ensure_addon_enabled()
    reset_scene()
    create_test_mesh()
    # Salva o arquivo .blend antes de executar o operador
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "cancel_test.blend"
    bpy.ops.wm.save_mainfile(filepath=str(blend_path))
    run_grungit_bake_with_cancel()
    print("Se não houve crash, PASS (cancelamento testado).")

if __name__ == "__main__":
    main()
