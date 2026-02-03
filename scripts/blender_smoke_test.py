"""Smoke test headless para o Grungit."""

# pyright: reportMissingImports=false

import sys
from pathlib import Path

import bpy  # type: ignore

ADDON_MODULE = "grungit"
NODEGROUPS = {"Grungit v1.9.1", "Grungit Dirt v1.9.1"}


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
    mat = bpy.data.materials.new(name="SmokeMat")
    mat.use_nodes = True
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
    return obj, mat


def run_grungit():
    scene = bpy.context.scene
    scene.grungit.quick_mode = True
    scene.grungit.overall_amount = 0.5
    result = bpy.ops.object.grungit()
    if "FINISHED" not in result:
        raise RuntimeError(f"Grungit falhou: {result}")


def assert_nodes(material):
    nodes = material.node_tree.nodes
    for node in nodes:
        if node.type == "GROUP" and node.node_tree and node.node_tree.name in NODEGROUPS:
            return
    raise RuntimeError("NodeGroup do Grungit não foi aplicado ao material.")


def main():
    ensure_addon_enabled()
    reset_scene()
    _, material = create_test_mesh()
    run_grungit()
    assert_nodes(material)
    print("Smoke test OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Smoke test FAIL: {exc}")
        sys.exit(1)
