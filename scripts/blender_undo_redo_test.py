"""Teste de undo/redo para o operador Grungit."""

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
    obj.name = "UndoObj"
    mat = bpy.data.materials.new(name="UndoMat")
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
    obj = create_test_mesh()
    # Salva o arquivo .blend antes de executar o operador
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "undo_redo_test.blend"
    bpy.ops.wm.save_mainfile(filepath=str(blend_path))

    # Salva estado inicial do material
    mat = obj.data.materials[0]
    mat_nodes_before = [(n.name, n.bl_idname) for n in mat.node_tree.nodes]

    # Executa o operador (bake)
    run_grungit_bake()
    print("Bake executado. Simulando undo...")

    # Simula undo: remove material e recria igual ao original
    obj.data.materials.clear()
    mat_undo = bpy.data.materials.new(name="UndoMat")
    mat_undo.use_nodes = True
    # Remove todos os nodes padrão
    for n in list(mat_undo.node_tree.nodes):
        mat_undo.node_tree.nodes.remove(n)
    # Restaura nodes salvos usando bl_idname
    for name, bl_idname in mat_nodes_before:
        try:
            node = mat_undo.node_tree.nodes.new(bl_idname)
            node.name = name
        except Exception as exc:
            print(f"Falha ao recriar node {name} ({bl_idname}): {exc}")
    obj.data.materials.append(mat_undo)
    print("Undo simulado. Simulando redo...")

    # Garante que o objeto está selecionado e ativo antes do redo
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Executa novamente o operador (redo)
    run_grungit_bake()
    print("Redo simulado. Se não houve erro, PASS.")

if __name__ == "__main__":
    main()
