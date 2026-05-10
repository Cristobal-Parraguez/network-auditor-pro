import nmap
import json
import socket
from datetime import datetime

def obtener_mi_red():
    """Detecta la IP privada del PC y devuelve el rango /24"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No llega a conectar realmente, solo mira por qué interfaz saldría el tráfico
        s.connect(('8.8.8.8', 1)) 
        ip_local = s.getsockname()[0]
        # Transforma 192.168.1.x en 192.168.1.0/24
        red_base = ".".join(ip_local.split('.')[:-1]) + ".0/24"
        return red_base
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

def escanear_y_reportar():
    # ¡Cero IPs fijas! Privacidad y portabilidad total.
    rango_red = obtener_mi_red()
    ruta_nmap = r'C:\Program Files (x86)\Nmap\nmap.exe'
    
    print(f"--- AUDITOR DE RED PRO v1.4 ---")
    print(f"[*] Red detectada automáticamente: {rango_red}")
    print("[*] Escaneando dispositivos... (esto toma un momento)")
    
    try:
        nm = nmap.PortScanner(nmap_search_path=(ruta_nmap,))
        nm.scan(hosts=rango_red, arguments='-sn')
        
        lista_dispositivos = []
        for host in nm.all_hosts():
            datos = {
                "ip": host,
                "nombre": nm[host].hostname() or "Desconocido",
                "estado": nm[host].state(),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            lista_dispositivos.append(datos)
            print(f"[+] Dispositivo activo: {host}")

        with open("reporte_red.json", "w") as f:
            json.dump(lista_dispositivos, f, indent=4)
        
        print(f"\n[OK] Reporte generado exitosamente.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    escanear_y_reportar()