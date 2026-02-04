"""Teste automatizado: bake sem objeto selecionado deve falhar com erro claro."""

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

def main():
    ensure_addon_enabled()
    bpy.ops.object.select_all(action="DESELECT")
    # Salva o arquivo .blend antes de executar o operador
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "no_selection_test.blend"
    bpy.ops.wm.save_mainfile(filepath=str(blend_path))
    try:
        result = bpy.ops.object.grungit()
        if "CANCELLED" in result:
            print("PASS: Operador corretamente cancelado sem seleção.")
        else:
            print(f"FAIL: Operador não deveria executar sem seleção. Resultado: {result}")
            sys.exit(1)
    except Exception as exc:
        print(f"PASS: Exceção esperada ao tentar bake sem seleção: {exc}")

if __name__ == "__main__":
    main()
