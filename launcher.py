# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time

if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

print("\n")
print("ESCANEO")

python_exe = os.path.join("python_portable", "python.exe")
if not os.path.exists(python_exe):
    print("ERROR: Python portable no encontrado")
    input("\nPresiona ENTER para salir...")
    sys.exit(1)

for archivo in ["progreso_escaneo.txt", "progreso_encriptacion.txt"]:
    if os.path.exists(archivo):
        try:
            os.remove(archivo)
        except:
            pass

proceso = subprocess.Popen([python_exe, "index.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ultimo_escaneo = -1
ultimo_encriptacion = -1
fase = "escaneo"
archivos_count = "0"
encriptados_count = "0"

while proceso.poll() is None:
    if os.path.exists("progreso_escaneo.txt"):
        try:
            with open("progreso_escaneo.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()
                for linea in lineas:
                    if "Archivos:" in linea:
                        try:
                            archivos_count = linea.split(":")[1].strip()
                        except:
                            pass
                    elif "%" in linea and "[" in linea and "]" in linea:
                        try:
                            porcentaje = int(linea.split("]")[1].strip().split("%")[0])
                            if porcentaje != ultimo_escaneo:
                                barra = "█" * (porcentaje // 2) + "░" * (50 - porcentaje // 2)
                                print(f"\r[{barra}] {porcentaje}% | Archivos: {archivos_count}  ", end="", flush=True)
                                ultimo_escaneo = porcentaje
                        except:
                            pass
        except:
            pass
    
    if os.path.exists("progreso_encriptacion.txt"):
        if fase == "escaneo":
            print("\n\nENCRIPTACION")
            fase = "encriptacion"
        
        try:
            with open("progreso_encriptacion.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()
                for linea in lineas:
                    if "Encriptados:" in linea:
                        try:
                            encriptados_count = linea.split(":")[1].strip()
                        except:
                            pass
                    elif "%" in linea and "[" in linea and "]" in linea:
                        try:
                            porcentaje = int(linea.split("]")[1].strip().split("%")[0])
                            if porcentaje != ultimo_encriptacion:
                                barra = "█" * (porcentaje // 2) + "░" * (50 - porcentaje // 2)
                                print(f"\r[{barra}] {porcentaje}% | Encriptados: {encriptados_count}  ", end="", flush=True)
                                ultimo_encriptacion = porcentaje
                        except:
                            pass
        except:
            pass
    
    time.sleep(0.2)

proceso.wait()

print("\n\nTERMINADO")
input("\nPresiona ENTER para salir...")
