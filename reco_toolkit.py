#Reco Toolkit - Automatización de reconocimiento OSINT 
#By: c4feina

import subprocess
import argparse
import json
import os
from datetime import datetime

class ReconToolkit:
    def __init__(self, target, output_dir=None):
        self.target = target
        self.output_dir = output_dir or f"recon_{target.replace('.', '_')}"
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'subdomains': [],
            'emails': [],
            'ports': [],
            'technologies': []
        }
        
        # Crea directorio de salida
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"\n[*] Target: {target}")
        print(f"[*] Output: {self.output_dir}\n")
    
    def ejecutar_comando(self, cmd, archivo_salida=None):
        #Ejecuta un comando y opcionalmente guarda la salida en un archivo
        try:
            resultado = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=300
            )
            
            if archivo_salida:
                with open(archivo_salida, 'w') as f:
                    f.write(resultado.stdout)
            
            return resultado.stdout, resultado.returncode
        except Exception as e:
            print(f"[!] Error ejecutando comando: {e}")
            return None, 1
    
    def harvester(self):
        # Ejecuta theHarvester para buscar emails y subdominios :3
        print("[*] Ejecutando Harvester...")
        
        archivo = os.path.join(self.output_dir, "harvester_results")
        cmd = f"theHarvester -d {self.target} -b all -f {archivo}"
        
        salida, codigo = self.ejecutar_comando(cmd)
        
        if codigo == 0:
            print("[✓] Harvester completado")
            # Parseo básico de resultados
            if salida and '@' in salida:
                emails = [l.strip() for l in salida.split('\n') 
                         if '@' in l and self.target in l]
                self.results['emails'] = emails[:10]
            
            if salida and 'Hosts found' in salida:
                lines = salida.split('Hosts found')[1].split('\n')
                hosts = [l.strip() for l in lines if self.target in l]
                self.results['subdomains'] = hosts[:20]
                print(f"[+] Encontrados {len(self.results['subdomains'])} subdominios")
        else:
            print("[!] Harvester falló (¿lo tenes instalado?)")
    
    def nmap(self, puertos="1-1000"):
        #Ejecuta Nmap para escanear puertos abiertos 
        print(f"[*] Ejecutando Nmap (puertos {puertos})...")
        
        archivo = os.path.join(self.output_dir, "nmap_scan.txt")
        cmd = f"nmap -sV -T4 -p {puertos} {self.target} -oN {archivo}"
        
        salida, codigo = self.ejecutar_comando(cmd)
        
        if codigo == 0:
            print("[✓] Nmap completado")
            # Extraer puertos abiertos
            if salida and 'open' in salida:
                puertos_abiertos = [l.strip() for l in salida.split('\n') 
                                   if 'open' in l and '/tcp' in l]
                self.results['ports'] = puertos_abiertos
                print(f"[+] Encontrados {len(puertos_abiertos)} puertos abiertos")
        else:
            print("[!] Nmap falló (¿está instalado?)")
    
    def whatweb(self):
        #Ejecuta WhatWeb para detectar tecnologías web
        print("[*] Ejecutando WhatWeb...")
        
        archivo = os.path.join(self.output_dir, "whatweb_results.json")
        cmd = f"whatweb {self.target} --log-json={archivo}"
        
        salida, codigo = self.ejecutar_comando(cmd)
        
        if codigo == 0:
            print("[✓] WhatWeb completado")
            # Parsear JSON de salida
            try:
                if os.path.exists(archivo):
                    with open(archivo, 'r') as f:
                        data = json.load(f)
                        if data and len(data) > 0:
                            plugins = data[0].get('plugins', {})
                            self.results['technologies'] = list(plugins.keys())[:15]
                            print(f"[+] Detectadas {len(self.results['technologies'])} tecnologías")
            except:
                pass
        else:
            print("[!] WhatWeb falló (¿está instalado?)")
    
    def recon_completo(self):
        #Ejecuta todas las herramientas de reconocimiento
        print("="*60)
        print(f"Iniciando reconocimiento completo en {self.target}")
        print("="*60 + "\n")
        
        self.harvester()
        self.nmap()
        self.whatweb()
        
        # Guarda resumen
        self.guardar_resumen()
        self.mostrar_resumen()
    
    def guardar_resumen(self):
        #Guarda el resumen consolidado en JSON
        archivo = os.path.join(self.output_dir, "summary.json")
        with open(archivo, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n[✓] Resumen guardado en: {archivo}")
    
    def mostrar_resumen(self):
        #Muestra un resumen de los resultados obtenidos
        print("\n" + "="*60)
        print("RESUMEN DE RESULTADOS")
        print("="*60)
        
        if self.results['subdomains']:
            print(f"\n[+] Subdominios ({len(self.results['subdomains'])}):")
            for s in self.results['subdomains'][:5]:
                print(f"    {s}")
            if len(self.results['subdomains']) > 5:
                print(f"    ... y {len(self.results['subdomains'])-5} más")
        
        if self.results['emails']:
            print(f"\n[+] Emails ({len(self.results['emails'])}):")
            for e in self.results['emails'][:5]:
                print(f"    {e}")
        
        if self.results['ports']:
            print(f"\n[+] Puertos abiertos ({len(self.results['ports'])}):")
            for p in self.results['ports']:
                print(f"    {p}")
        
        if self.results['technologies']:
            print(f"\n[+] Tecnologías ({len(self.results['technologies'])}):")
            for t in self.results['technologies'][:10]:
                print(f"    {t}")
        
        print("\n" + "="*60)
        print(f"[✓] Resultados guardados en: {self.output_dir}/")
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Reco Toolkit OSINT',
        epilog='''
Ejemplos:
  python reco.py -t ejemplo.com --full
  python reco.py -t target.com --harvester
  python reco.py -t target.com --nmap -p 1-65535
        '''
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='Dominio objetivo')
    parser.add_argument('--full', action='store_true', 
                       help='Reconocimiento completo')
    parser.add_argument('--harvester', action='store_true', 
                       help='Solo theHarvester')
    parser.add_argument('--nmap', action='store_true', 
                       help='Solo Nmap')
    parser.add_argument('--whatweb', action='store_true', 
                       help='Solo WhatWeb')
    parser.add_argument('-o', '--output', 
                       help='Directorio de salida personalizado')
    parser.add_argument('-p', '--ports', default='1-1000',
                       help='Rango de puertos (default: 1-1000)')
    
    args = parser.parse_args()
    
    # iniciar toolkit
    toolkit = ReconToolkit(args.target, args.output)
    
    try:
        if args.full:
            toolkit.recon_completo()
        elif args.harvester:
            toolkit.harvester()
            toolkit.guardar_resumen()
        elif args.nmap:
            toolkit.nmap(args.ports)
            toolkit.guardar_resumen()
        elif args.whatweb:
            toolkit.whatweb()
            toolkit.guardar_resumen()
        else:
            print("[!] Especificá --full o una herramienta")
            print("[!] Usá -h para ver la ayuda")
    
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por el usuario")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()