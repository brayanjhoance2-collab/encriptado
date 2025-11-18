import time


def actualizar_progreso_encriptacion(mensaje, archivos, porcentaje):
    try:
        with open("progreso_encriptacion.txt", "w", encoding="utf-8") as f:
            f.write("="*60 + "\\n")
            f.write("ENCRIPTACION EN PROGRESO\\n")
            f.write("="*60 + "\\n\\n")
            f.write(f"Hora: {time.strftime('%H:%M:%S')}\\n")
            f.write(f"Encriptados: {archivos:,}\\n")
            f.write(f"Estado: {mensaje}\\n\\n")
            barra = int(porcentaje / 2)
            f.write(f"[{'#'*barra}{'-'*(50-barra)}] {porcentaje}%\\n\\n")
            f.write("="*60 + "\\n")
    except:
        pass


def generar_reporte_escaneo(contador, total):
    lineas = []
    lineas.append("="*80)
    lineas.append("REPORTE DE ESCANEO".center(80))
    lineas.append("="*80)
    lineas.append("")
    lineas.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lineas.append(f"Archivos objetivo: {total:,}")
    lineas.append("")
    lineas.append("="*80)
    
    ordenado = sorted(contador.items(), key=lambda x: x[1], reverse=True)
    
    for ext, cantidad in ordenado:
        lineas.append(f"{ext:<15} {cantidad:>10,} archivos")
    
    lineas.append("")
    lineas.append("="*80)
    
    return "\\n".join(lineas)


def generar_reporte_encriptacion(encriptados, errores, tiempo, stats=None):
    reporte = f"""
REPORTE - SISTEMA ADAPTATIVO 12 CAPAS

Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}
Tiempo: {tiempo:.1f} segundos

ARCHIVOS ENCRIPTADOS: {encriptados:,}
ARCHIVOS CON ERROR: {errores:,}

===============================================================
                   SISTEMA ADAPTATIVO
===============================================================
"""
    
    if stats:
        reporte += f"""
DISTRIBUCION POR TAMANO:

< 1 MB   (12 capas): {stats['12_capas']:,} archivos
1-10 MB  (8 capas):  {stats['8_capas']:,} archivos
10-50 MB (5 capas):  {stats['5_capas']:,} archivos
> 50 MB  (3 capas):  {stats['3_capas']:,} archivos

"""
    
    reporte += """===============================================================
                   CAPAS DE SEGURIDAD
===============================================================
son 12
===============================================================
"""
    
    return reporte
