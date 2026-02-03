"""E2E bake usando asset externo (.blend)."""

# pyright: reportMissingImports=false

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


def open_asset():
    repo_root = Path(__file__).resolve().parents[1]
    asset_path = repo_root / "assets" / "space_truck.blend"
    if not asset_path.exists():
        raise RuntimeError("Asset space_truck.blend não encontrado em assets/.")
    bpy.ops.wm.open_mainfile(filepath=str(asset_path))


def select_all_meshes():
    bpy.ops.object.select_all(action="DESELECT")
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not meshes:
        raise RuntimeError("Nenhuma malha encontrada no asset.")
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]


def run_grungit_bake():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.grungit.quick_mode = False
    scene.grungit.overall_amount = 0.5
    scene.grungit.output_dir = "//Textures/Grungit/"
    result = bpy.ops.object.grungit()
    if "FINISHED" not in result:
        raise RuntimeError(f"Grungit bake falhou: {result}")


def find_bake_output():
    output_dir = bpy.path.abspath("//Textures/Grungit/")
    output_path = Path(output_dir)
    if not output_path.exists():
        raise RuntimeError("Diretório de saída não foi criado.")
    exr_files = list(output_path.glob("*_Grungit.exr"))
    if len(exr_files) < 1:
        raise RuntimeError("Arquivo de bake não encontrado.")
    return exr_files


def main():
    ensure_addon_enabled()
    open_asset()
    select_all_meshes()
    run_grungit_bake()
    outputs = find_bake_output()
    print(f"E2E asset OK: {len(outputs)} arquivos")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"E2E asset FAIL: {exc}")
        sys.exit(1)
