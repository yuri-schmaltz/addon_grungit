"""Teste automatizado de performance do bake Grungit em diferentes tamanhos de malha."""

import sys
from pathlib import Path
import bpy  # type: ignore
import time

ADDON_MODULE = "grungit"

sizes = [10, 100, 1000, 5000]
results = []

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

def main():
    ensure_addon_enabled()
    for verts in sizes:
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.name = f"PerfObj_{verts}"
        mat = bpy.data.materials.new(name=f"PerfMat_{verts}")
        mat.use_nodes = True
        obj.data.materials.append(mat)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        # subdividir para aumentar número de vértices
        if verts > 10:
            # Limitar subdivisão para evitar crash e garantir execução do add-on
            max_subdiv = 3 if verts > 1000 else 2 if verts > 100 else 1
            for i in range(max_subdiv):
                bpy.ops.object.modifier_add(type='SUBSURF')
                obj.modifiers["Subdivision"].levels = 1
                bpy.ops.object.modifier_apply(modifier="Subdivision")
        # Salva o arquivo .blend antes de executar o operador
        repo_root = Path(__file__).resolve().parents[1]
        tmp_dir = repo_root / "tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        blend_path = tmp_dir / f"perf_{verts}.blend"
        bpy.ops.wm.save_mainfile(filepath=str(blend_path))
        start = time.time()
        result = bpy.ops.object.grungit()
        elapsed = time.time() - start
        results.append((verts, elapsed, result))
        print(f"Bake {verts} vértices: {elapsed:.2f}s, resultado: {result}")
    print("Resultados:")
    for verts, elapsed, result in results:
        print(f"{verts} vértices: {elapsed:.2f}s, resultado: {result}")

if __name__ == "__main__":
    main()
