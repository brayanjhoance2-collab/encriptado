import os
import sys
import subprocess
import time
import ctypes
import base64
from datetime import datetime


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_YELLOW = '\033[43m'


cancelado = False


def habilitar_colores_cmd():
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def print_banner():
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║  {Colors.BOLD}███████╗██╗███████╗████████╗███████╗███╗   ███╗ █████╗{Colors.END}{Colors.CYAN}               ║
║  {Colors.BOLD}██╔════╝██║██╔════╝╚══██╔══╝██╔════╝████╗ ████║██╔══██╗{Colors.END}{Colors.CYAN}              ║
║  {Colors.BOLD}███████╗██║███████╗   ██║   █████╗  ██╔████╔██║███████║{Colors.END}{Colors.CYAN}              ║
║  {Colors.BOLD}╚════██║██║╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║██╔══██║{Colors.END}{Colors.CYAN}              ║
║  {Colors.BOLD}███████║██║███████║   ██║   ███████╗██║ ╚═╝ ██║██║  ██║{Colors.END}{Colors.CYAN}              ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.END}
"""
    print(banner)


def print_info_sistema():
    admin_status = f"{Colors.GREEN}[✓] ADMINISTRADOR{Colors.END}" if es_admin() else f"{Colors.YELLOW}[•] USUARIO NORMAL{Colors.END}"
    
    info = f"""
{Colors.BOLD}INFORMACIÓN:{Colors.END}
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}

  {Colors.WHITE}Modo:{Colors.END} {admin_status}
  {Colors.WHITE}Fecha:{Colors.END} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
    print(info)


def verificar_python_portable():
    python_exe = os.path.join("python_portable", "python.exe")
    return os.path.exists(python_exe)


def monitorear_proceso(proceso):
    global cancelado
    
    ultimo_progreso = -1
    
    while proceso.poll() is None:
        try:
            if os.path.exists("progreso_escaneo.txt"):
                with open("progreso_escaneo.txt", "r", encoding="utf-8") as f:
                    contenido = f.read()
                    lineas = contenido.split("\\n")
                    for linea in lineas:
                        if "%" in linea:
                            try:
                                porcentaje = int(linea.split("]")[1].strip().replace("%", ""))
                                if porcentaje != ultimo_progreso:
                                    print(f"\r{Colors.CYAN}Escaneo: {porcentaje}%{Colors.END}", end="", flush=True)
                                    ultimo_progreso = porcentaje
                            except:
                                pass
            
            if os.path.exists("progreso_encriptacion.txt"):
                with open("progreso_encriptacion.txt", "r", encoding="utf-8") as f:
                    contenido = f.read()
                    lineas = contenido.split("\\n")
                    for linea in lineas:
                        if "%" in linea:
                            try:
                                porcentaje = int(linea.split("]")[1].strip().replace("%", ""))
                                if porcentaje != ultimo_progreso:
                                    print(f"\r{Colors.GREEN}Encriptacion: {porcentaje}%{Colors.END}", end="", flush=True)
                                    ultimo_progreso = porcentaje
                            except:
                                pass
            
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            cancelado = True
            proceso.terminate()
            print(f"\n\n{Colors.RED}PROCESO CANCELADO{Colors.END}")
            return False
    
    print()
    return True


def ejecutar_modo_normal():
    global cancelado
    cancelado = False
    
    clear()
    print_banner()
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}MODO NORMAL ACTIVADO{Colors.END}\n")
    
    if not verificar_python_portable():
        print(f"{Colors.RED}Error: Python portable no encontrado{Colors.END}")
        input(f"\n{Colors.CYAN}ENTER para volver...{Colors.END}")
        return
    
    try:
        python_exe = os.path.join("python_portable", "python.exe")
        proceso = subprocess.Popen([python_exe, "index.py"])
        
        completado = monitorear_proceso(proceso)
        
        if completado and not cancelado:
            print(f"\n{Colors.GREEN}COMPLETADO{Colors.END}")
        
    except KeyboardInterrupt:
        cancelado = True
        print(f"\n\n{Colors.RED}PROCESO CANCELADO{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
    
    input(f"\n{Colors.CYAN}ENTER para volver...{Colors.END}")


def ejecutar_modo_admin():
    global cancelado
    cancelado = False
    
    clear()
    print_banner()
    
    print(f"\n{Colors.BOLD}{Colors.RED}MODO ADMINISTRADOR ACTIVADO{Colors.END}\n")
    
    if not es_admin():
        print(f"{Colors.YELLOW}Requiere permisos de administrador{Colors.END}\n")
        print(f"  {Colors.CYAN}1.{Colors.END} Reiniciar como admin")
        print(f"  {Colors.CYAN}0.{Colors.END} Volver")
        
        opcion = input(f"\n{Colors.BOLD}Opción: {Colors.END}").strip()
        
        if opcion == "1":
            try:
                if os.name == 'nt':
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, f'"{os.path.abspath(__file__)}" --admin', None, 1
                    )
                sys.exit(0)
            except:
                return
        else:
            return
    
    if not verificar_python_portable():
        print(f"{Colors.RED}Error: Python portable no encontrado{Colors.END}")
        input(f"\n{Colors.CYAN}ENTER para volver...{Colors.END}")
        return
    
    try:
        python_exe = os.path.join("python_portable", "python.exe")
        proceso = subprocess.Popen([python_exe, "index.py"])
        
        completado = monitorear_proceso(proceso)
        
        if completado and not cancelado:
            print(f"\n{Colors.GREEN}COMPLETADO{Colors.END}")
        
    except KeyboardInterrupt:
        cancelado = True
        print(f"\n\n{Colors.RED}PROCESO CANCELADO{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
    
    input(f"\n{Colors.CYAN}ENTER para volver...{Colors.END}")


def mostrar_claves():
    clear()
    print_banner()
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}CLAVES DE ENCRIPTACION{Colors.END}\n")
    print(f"{Colors.CYAN}{'═'*70}{Colors.END}\n")
    
    if not os.path.exists("llave.key"):
        print(f"{Colors.RED}No se encontró llave.key{Colors.END}")
        print(f"{Colors.YELLOW}Ejecuta primero el modo de encriptación{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓ llave.key encontrada{Colors.END}")
        print(f"{Colors.WHITE}Ubicación: {os.path.abspath('llave.key')}{Colors.END}\n")
    
    if not os.path.exists("MASTER_PASSWORD.txt"):
        print(f"{Colors.RED}No se encontró MASTER_PASSWORD.txt{Colors.END}")
        print(f"{Colors.YELLOW}Ejecuta primero el modo de encriptación{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓ MASTER_PASSWORD.txt encontrada{Colors.END}")
        print(f"{Colors.WHITE}Ubicación: {os.path.abspath('MASTER_PASSWORD.txt')}{Colors.END}\n")
        
        try:
            with open("MASTER_PASSWORD.txt", "rb") as f:
                password_encoded = f.read()
                password_decoded = base64.b85decode(password_encoded)
                
            print(f"{Colors.BOLD}PASSWORD (Base85):{Colors.END}")
            print(f"{Colors.CYAN}{password_encoded.decode()[:100]}...{Colors.END}\n")
            
            print(f"{Colors.BOLD}PASSWORD (HEX):{Colors.END}")
            print(f"{Colors.CYAN}{password_decoded.hex()[:100]}...{Colors.END}\n")
            
            print(f"{Colors.RED}⚠ GUARDA ESTAS CLAVES EN LUGAR SEGURO{Colors.END}")
            print(f"{Colors.YELLOW}Sin ellas NO se pueden recuperar los archivos{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}Error al leer password: {e}{Colors.END}")
    
    print(f"\n{Colors.CYAN}{'═'*70}{Colors.END}")
    input(f"\n{Colors.CYAN}ENTER para volver...{Colors.END}")


def menu_principal():
    while True:
        clear()
        print_banner()
        print_info_sistema()
        
        print(f"{Colors.BOLD}OPCIONES:{Colors.END}\n")
        print(f"  {Colors.BG_BLUE}{Colors.WHITE} 1 {Colors.END} {Colors.CYAN}MODO NORMAL{Colors.END}")
        print(f"  {Colors.BG_RED}{Colors.WHITE} 2 {Colors.END} {Colors.RED}MODO ADMINISTRADOR{Colors.END}")
        print(f"  {Colors.BG_YELLOW}{Colors.WHITE} 5 {Colors.END} {Colors.YELLOW}MOSTRAR CLAVES{Colors.END}")
        print(f"  {Colors.WHITE} 0 {Colors.END} {Colors.WHITE}Salir{Colors.END}")
        
        print(f"\n{Colors.YELLOW}{'─'*70}{Colors.END}")
        opcion = input(f"{Colors.BOLD}Selecciona: {Colors.END}").strip()
        
        if opcion == "1":
            ejecutar_modo_normal()
        elif opcion == "2":
            ejecutar_modo_admin()
        elif opcion == "5":
            mostrar_claves()
        elif opcion == "0":
            clear()
            sys.exit(0)
        else:
            time.sleep(0.5)


def main():
    habilitar_colores_cmd()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--admin":
        ejecutar_modo_admin()
        sys.exit(0)
    
    try:
        menu_principal()
    except KeyboardInterrupt:
        clear()
        print(f"\n{Colors.RED}Programa cerrado{Colors.END}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
