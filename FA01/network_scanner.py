import nmap
import socket
from scapy.all import ARP, Ether, srp
import platform
import subprocess
import re

class NetworkScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        
    def get_local_ip(self):
        """Obtiene la IP local de la máquina"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_network_range(self):
        """Obtiene el rango de la red local"""
        ip = self.get_local_ip()
        ip_parts = ip.split('.')
        return f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"

    def scan_network(self):
        """Escanea la red y obtiene información de los dispositivos"""
        network = self.get_network_range()
        devices = []

        # Escaneo básico con nmap
        self.nm.scan(hosts=network, arguments='-sn')
        
        for host in self.nm.all_hosts():
            # Escaneo detallado para cada host
            self.nm.scan(hosts=host, arguments='-sV -O --version-intensity 5')
            
            device_info = {
                'ip': host,
                'hostname': self.get_hostname(host),
                'mac': self.get_mac_address(host),
                'vendor': self.get_vendor_info(host),
                'type': self.detect_device_type(host),
                'os': self.get_os_info(host),
                'services': self.get_services(host),
                'model': self.get_device_model(host),
                'status': 'Activo'
            }
            devices.append(device_info)

        return devices

    def get_hostname(self, ip):
        """Obtiene el nombre del host"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def get_mac_address(self, ip):
        """Obtiene la dirección MAC"""
        try:
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            return answered_list[0][1].hwsrc
        except:
            return "Unknown"

    def get_vendor_info(self, ip):
        """Obtiene información del fabricante"""
        try:
            mac = self.get_mac_address(ip)
            if mac != "Unknown":
                return self.nm[ip]['vendor'].get(mac, "Unknown")
            return "Unknown"
        except:
            return "Unknown"

    def get_os_info(self, ip):
        """Obtiene información del sistema operativo"""
        try:
            if 'osmatch' in self.nm[ip]:
                return self.nm[ip]['osmatch'][0]['name']
            return "Unknown"
        except:
            return "Unknown"

    def get_services(self, ip):
        """Obtiene los servicios activos"""
        services = []
        try:
            for port in self.nm[ip].all_ports():
                if 'name' in self.nm[ip]['tcp'][port]:
                    services.append({
                        'port': port,
                        'name': self.nm[ip]['tcp'][port]['name'],
                        'product': self.nm[ip]['tcp'][port].get('product', 'Unknown'),
                        'version': self.nm[ip]['tcp'][port].get('version', 'Unknown')
                    })
        except:
            pass
        return services

    def get_device_model(self, ip):
        """Intenta obtener el modelo del dispositivo"""
        try:
            services = self.get_services(ip)
            for service in services:
                if service['product'] != 'Unknown':
                    return service['product']
            return "Unknown"
        except:
            return "Unknown"

    def detect_device_type(self, ip):
        """Detecta el tipo de dispositivo"""
        try:
            services = self.get_services(ip)
            ports = [service['port'] for service in services]
            
            # Detectar impresoras
            if any(port in [515, 631, 9100] for port in ports):
                return "Impresora"
            
            # Detectar routers
            if any(port in [80, 443, 8080] for port in ports) and any(service['name'] in ['http', 'https'] for service in services):
                return "Router"
            
            # Detectar cámaras IP
            if any(port in [554, 8000, 37777] for port in ports):
                return "Cámara IP"
            
            # Detectar computadoras
            if any(service['name'] in ['microsoft-ds', 'netbios-ssn', 'ssh', 'rdp'] for service in services):
                return "Computadora"
            
            # Detectar servidores
            if any(service['name'] in ['http', 'https', 'mysql', 'postgresql', 'mssql'] for service in services):
                return "Servidor"
            
            return "Dispositivo de Red"
        except:
            return "Unknown" 