"""Benchmark headless para o Grungit (quick mode)."""

# pyright: reportMissingImports=false

import json
import sys
import time
from pathlib import Path

import bpy

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


def create_cube():
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    mat = bpy.data.materials.new(name="PerfMat")
    mat.use_nodes = True
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
    return obj


def create_scene(count):
    objs = []
    for i in range(count):
        obj = create_cube()
        obj.location.x = i * 2.0
        objs.append(obj)
    return objs


def run_grungit_quick():
    scene = bpy.context.scene
    scene.grungit.quick_mode = True
    scene.grungit.overall_amount = 0.5
    result = bpy.ops.object.grungit()
    if "FINISHED" not in result:
        raise RuntimeError(f"Grungit falhou: {result}")


def time_run(count):
    reset_scene()
    create_scene(count)
    start = time.perf_counter()
    run_grungit_quick()
    end = time.perf_counter()
    return end - start


def main():
    ensure_addon_enabled()
    small = time_run(1)
    large = time_run(25)
    output = {
        "small_objects": 1,
        "large_objects": 25,
        "small_seconds": small,
        "large_seconds": large,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Perf benchmark FAIL: {exc}")
        sys.exit(1)
