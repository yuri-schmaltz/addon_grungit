import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "blender_e2e_realistic_scene_test.py"


def get_blender_bin():
    blender_bin = os.environ.get("BLENDER_BIN")
    if blender_bin:
        return blender_bin
    raise RuntimeError(
        "Defina a variável de ambiente BLENDER_BIN apontando para o executável do Blender."
    )


def main():
    blender_bin = get_blender_bin()
    cmd = [
        blender_bin,
        "-b",
        "-P",
        str(SCRIPT),
    ]
    print("Executando:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(ROOT))
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
