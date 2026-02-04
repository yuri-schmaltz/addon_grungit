"""Teste de robustez: repete o bake 100 vezes para detectar leaks, crashes ou degradação."""

import sys
from pathlib import Path
import bpy  # type: ignore

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
    obj.name = "RobustObj"
    mat = bpy.data.materials.new(name="RobustMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj

def run_grungit_bake():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.grungit.quick_mode = False
    scene.grungit.overall_amount = 0.5
    scene.grungit.output_dir = "//Textures/Grungit/"
    result = bpy.ops.object.grungit()
    if "FINISHED" not in result:
        raise RuntimeError(f"Grungit bake falhou: {result}")

def main():
    ensure_addon_enabled()
    reset_scene()
    create_test_mesh()
    # Salva o arquivo .blend antes de iniciar as repetições
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "robustness_100x_test.blend"
    bpy.ops.wm.save_mainfile(filepath=str(blend_path))
    for i in range(100):
        # Garante que o objeto está selecionado e ativo
        obj = bpy.data.objects.get("RobustObj")
        if obj is not None:
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        try:
            run_grungit_bake()
            print(f"Iteração {i+1}/100: OK")
        except Exception as exc:
            print(f"Iteração {i+1}/100: FAIL: {exc}")
            sys.exit(1)
    print("Robustez 100× OK")

if __name__ == "__main__":
    main()
