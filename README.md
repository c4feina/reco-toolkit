# Reco-Toolkit

Script de Python que automatiza el reconocimiento inicial. Ejecuta varias herramientas OSINT y organiza los resultados en un solo lugar, la idea salio de mis tareas en bug bounty.

Usa herramientas de recon en un solo comando (proximamente quiero incluir otras):
- **theHarvester** - Busca emails y subdominios
- **Nmap** - Escanea puertos abiertos
- **WhatWeb** - Detecta tecnologías web

En vez de correr cada herramienta, el script las ejecuta todas y genera un reporte.

## Instalación

```bash
# Clonar el repo
git clone https://github.com/c4feina/reco-toolkit.git
cd reco-toolkit

# Instalar dependencias
pip install -r requirements.txt

# Instalar herramientas (Ubuntu/Debian)
sudo apt install nmap whatweb -y
pip3 install theHarvester
```

## Uso

```bash
# Reconocimiento completo
python recon.py -t ejemplo.com --full

# Solo subdominios
python recon.py -t ejemplo.com --harvester

# Solo escaneo de puertos
python recon.py -t ejemplo.com --nmap
```

## Salida

Todo se guarda en `recon_ejemplo_com/`:
```
recon_ejemplo_com/
├── harvester_results.json    # Emails y subdominios
├── nmap_scan.txt             # Puertos abiertos
├── whatweb_results.json      # Tecnologías detectadas
└── summary.json              # Resumen consolidado
```

## Ejemplo de uso

```bash
$ python recotoolkit.py -t target.com --full

[*] Running theHarvester...
[✓] Found 15 subdomains
[*] Running Nmap...
[✓] Found 3 open ports
[*] Running WhatWeb...
[✓] Detected 8 technologies

[✓] Results saved to: recon_target_com/
```

## Roadmap

- [ ] Agregar Subfinder
- [ ] Integrar Nuclei para escaneo de vulnerabilidades
- [ ] Dashboard web para visualizar resultados
- [ ] Soporte para múltiples targets

## Disclaimer

Herramienta para uso en bug bounty autorizado y pentesting con permiso. Usá solo en sistemas propios o con autorización explícita.
