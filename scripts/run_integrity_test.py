import subprocess
import os

def main():
    blender_bin = os.environ.get("BLENDER_BIN", r"C:\Blender\blender.exe")
    script = os.path.join(os.path.dirname(__file__), "blender_integrity_test.py")
    # Remove o argumento -b para rodar em modo interativo
    cmd = [blender_bin, "-P", script]
    print(f"Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if "PASS" in result.stdout:
        print("[OK] Teste de integridade dos arquivos passou.")
    else:
        print("[FAIL] Teste de integridade dos arquivos falhou.")
        exit(1)

if __name__ == "__main__":
    main()
