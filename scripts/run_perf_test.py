import subprocess
import os

def main():
    blender_bin = os.environ.get("BLENDER_BIN", r"C:\Blender\blender.exe")
    script = os.path.join(os.path.dirname(__file__), "blender_perf_test.py")
    cmd = [blender_bin, "-b", "-P", script]
    print(f"Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    print("[OK] Teste de performance finalizado.")

if __name__ == "__main__":
    main()
