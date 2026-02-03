"""Validação de output_dir para Grungit e PBR Bake."""

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


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def create_test_mesh():
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    mat = bpy.data.materials.new(name="PathMat")
    mat.use_nodes = True
    obj.data.materials.append(mat)
    return obj


def save_temp_blend():
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "path_validation.blend"
    bpy.ops.wm.save_mainfile(filepath=str(blend_path))
    return blend_path


def run_grungit_invalid_path():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.grungit.quick_mode = False
    scene.grungit.output_dir = "//../Invalid/"
    result = bpy.ops.object.grungit()
    if "FINISHED" not in result:
        raise RuntimeError(f"Grungit bake falhou: {result}")


def assert_output_in_default_dir():
    default_dir = Path(bpy.path.abspath("//Textures/Grungit/")).resolve()
    if not default_dir.exists():
        raise RuntimeError("Diretório padrão não foi criado.")
    exr_files = list(default_dir.glob("*_Grungit.exr"))
    if not exr_files:
        raise RuntimeError("Nenhum arquivo de bake encontrado no diretório padrão.")
    for exr in exr_files:
        if default_dir not in exr.resolve().parents:
            raise RuntimeError("Arquivo fora do diretório padrão.")


def main():
    ensure_addon_enabled()
    reset_scene()
    create_test_mesh()
    save_temp_blend()
    run_grungit_invalid_path()
    assert_output_in_default_dir()
    print("output_dir validation OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"output_dir validation FAIL: {exc}")
        sys.exit(1)
