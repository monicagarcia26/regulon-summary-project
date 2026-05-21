# =========================================
# Responsabilidad: Leer el archivo de interacciones y construir una estructura de datos que contenga la información relevante para cada TF.
# Entrada: Archivo TSV con interacciones entre reguladores y genes.
# Salida: lista de interacciones (TF, gen, efecto).
# =========================================
def load_interactions(filename):
    """
    Carga las interacciones desde un archivo TSV.

    Args:
        filename (str): Ruta del archivo de interacciones.

    Returns:
        list[tuple[str, str, str]]: Lista de interacciones (TF, gen, efecto).
    """
    interactions = []

    if not filename:
        raise ValueError("filename vacío")

    with open(filename) as f:
        for line in f:
            line = line.strip()

            # Ignorar líneas vacías
            if not line:
                continue

            # Ignorar comentarios
            if line.startswith("#"):
                continue

            # Ignorar encabezado
            if line.startswith("1)regulatorId"):
                continue

            fields = line.split("\t")

            # Validar número mínimo de columnas
            if len(fields) <= 6:
                continue

            TF = fields[1]
            gene = fields[4]
            effect = fields[5]

            # Validar effect
            if effect not in ["+", "-", "+-"]:
                continue

            interactions.append((TF, gene, effect))

    return interactions
