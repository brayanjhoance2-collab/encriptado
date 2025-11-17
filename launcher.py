import os
import sys
import subprocess
import time
import ctypes


def habilitar_utf8_powershell():
    try:
        if os.name == 'nt':
            os.system('chcp 65001 > nul 2>&1')
            
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)
            kernel32.SetConsoleCP(65001)
            
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass


def verificar_python_portable():
    python_exe = os.path.join("python_portable", "python.exe")
    return os.path.exists(python_exe)


def mostrar_barra_progreso(tipo, porcentaje):
    barra_len = 50
    lleno = int(barra_len * porcentaje / 100)
    vacio = barra_len - lleno
    
    barra = '█' * lleno + '░' * vacio
    print(f"\\r{tipo}: [{barra}] {porcentaje}%", end='', flush=True)


def monitorear_proceso(proceso):
    ultimo_porcentaje = -1
    tipo_actual = "Escaneo"
    
    while proceso.poll() is None:
        try:
            if os.path.exists("progreso_escaneo.txt"):
                with open("progreso_escaneo.txt", "r", encoding="utf-8") as f:
                    contenido = f.read()
                    for linea in contenido.split("\\n"):
                        if "%" in linea:
                            try:
                                porcentaje = int(linea.split("]")[1].strip().replace("%", ""))
                                if porcentaje != ultimo_porcentaje:
                                    mostrar_barra_progreso("Escaneo", porcentaje)
                                    ultimo_porcentaje = porcentaje
                                    tipo_actual = "Escaneo"
                            except:
                                pass
            
            if os.path.exists("progreso_encriptacion.txt"):
                with open("progreso_encriptacion.txt", "r", encoding="utf-8") as f:
                    contenido = f.read()
                    for linea in contenido.split("\\n"):
                        if "%" in linea:
                            try:
                                porcentaje = int(linea.split("]")[1].strip().replace("%", ""))
                                if porcentaje != ultimo_porcentaje or tipo_actual != "Encriptacion":
                                    mostrar_barra_progreso("Encriptacion", porcentaje)
                                    ultimo_porcentaje = porcentaje
                                    tipo_actual = "Encriptacion"
                            except:
                                pass
            
            time.sleep(0.3)
            
        except KeyboardInterrupt:
            proceso.terminate()
            print("\\n\\nPROCESO CANCELADO")
            return False
    
    print()
    return True


def ejecutar_encriptacion():
    habilitar_utf8_powershell()
    
    print("="*70)
    print("SISTEMA DE ENCRIPTACION AUTOMATICO".center(70))
    print("="*70)
    print()
    
    if not verificar_python_portable():
        print("ERROR: Python portable no encontrado")
        input("\\nPresiona ENTER para salir...")
        return
    
    print("Iniciando proceso...")
    print()
    
    try:
        python_exe = os.path.join("python_portable", "python.exe")
        
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        proceso = subprocess.Popen(
            [python_exe, "index.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        completado = monitorear_proceso(proceso)
        
        if completado:
            print("\\nPROCESO COMPLETADO")
            print("="*70)
        
    except KeyboardInterrupt:
        print("\\n\\nPROCESO CANCELADO")
    except Exception as e:
        print(f"\\nERROR: {e}")
    
    print()
    input("Presiona ENTER para salir...")


def main():
    habilitar_utf8_powershell()
    
    try:
        ejecutar_encriptacion()
    except KeyboardInterrupt:
        print("\\n\\nPrograma cerrado")
        sys.exit(0)


if __name__ == "__main__":
    main()
