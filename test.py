import re

# Lista de ejemplos de cadenas a modificar
nombres = [
    "AGUNIMON - P-029 (Holo)",
    "LOBOMON - P-030 (Holo)",
    "GATOMON - P-031 (Holo)"
]

# Ciclo para procesar cada nombre en la lista
nombres_modificados = []
for nombre in nombres:
    # Verificar si "(Holo)" está en la cadena
    if "(Holo)" in nombre:
        # Reemplazar "(Holo)" por "(Foil)" y moverlo antes de "- P-XXX"
        nuevo_nombre = re.sub(r'(\s-\sP-\d{3})\s\(Holo\)', r' (Foil)\1', nombre)
        nombres_modificados.append(nuevo_nombre)
    else:
        nombres_modificados.append(nombre)

# Imprimir los nombres modificados
for nombre_modificado in nombres_modificados:
    print(nombre_modificado)

