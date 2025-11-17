import os
import sys
import subprocess
import time

# Configurar UTF-8
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

print("\n" + "="*70)
print("SISTEMA DE ENCRIPTACION INICIANDO...".center(70))
print("="*70 + "\n")

# Verificar Python portable
python_exe = os.path.join("python_portable", "python.exe")
if not os.path.exists(python_exe):
    print("ERROR: Python portable no encontrado")
    input("\nPresiona ENTER para salir...")
    sys.exit(1)

# Ejecutar encriptación directa
print("Iniciando proceso de encriptacion...\n")
proceso = subprocess.Popen([python_exe, "index.py"])

# Monitorear progreso
ultimo_progreso = -1

while proceso.poll() is None:
    try:
        # Mostrar progreso de escaneo
        if os.path.exists("progreso_escaneo.txt"):
            with open("progreso_escaneo.txt", "r", encoding="utf-8") as f:
                contenido = f.read()
                lineas = contenido.split("\n")
                for linea in lineas:
                    if "%" in linea:
                        try:
                            porcentaje = int(linea.split("]")[1].strip().replace("%", ""))
                            if porcentaje != ultimo_progreso:
                                print(f"\rEscaneo: {porcentaje}%", end="", flush=True)
                                ultimo_progreso = porcentaje
                        except:
                            pass
        
        # Mostrar progreso de encriptación
        if os.path.exists("progreso_encriptacion.txt"):
            with open("progreso_encriptacion.txt", "r", encoding="utf-8") as f:
                contenido = f.read()
                lineas = contenido.split("\n")
                for linea in lineas:
                    if "%" in linea:
                        try:
                            porcentaje = int(linea.split("]")[1].strip().replace("%", ""))
                            if porcentaje != ultimo_progreso:
                                print(f"\rEncriptacion: {porcentaje}%", end="", flush=True)
                                ultimo_progreso = porcentaje
                        except:
                            pass
        
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        proceso.terminate()
        print("\n\nPROCESO CANCELADO")
        input("\nPresiona ENTER para salir...")
        sys.exit(0)

print("\n\n" + "="*70)
print("PROCESO COMPLETADO".center(70))
print("="*70)

# Mostrar reportes generados
if os.path.exists("reporte_encriptacion.txt"):
    print("\nReporte generado: reporte_encriptacion.txt")

input("\nPresiona ENTER para salir...")
