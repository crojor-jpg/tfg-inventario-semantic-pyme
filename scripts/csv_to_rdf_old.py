"""Script base para convertir un CSV de inventario a RDF/Turtle.

Este es un esqueleto inicial. Deberás adaptarlo a las columnas reales de tu CSV
y a la ontología definitiva (clases y propiedades).
"""

import csv
from pathlib import Path

BASE_URI = "http://example.org/inventario#"

def csv_a_rdf(ruta_csv: str, ruta_salida_ttl: str):
    ruta = Path(ruta_csv)
    salida = Path(ruta_salida_ttl)

    with ruta.open(encoding="utf-8") as f_in, salida.open("w", encoding="utf-8") as f_out:
        lector = csv.DictReader(f_in, delimiter=",")
        f_out.write("""@prefix inv: <http://example.org/inventario#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

""")
        for i, fila in enumerate(lector, start=1):
            prod_id = fila.get("id_producto", f"prod{i}")
            uri_prod = f"<{BASE_URI}{prod_id}>"
            nombre = fila.get("nombre", "").replace('"', '\\"')
            categoria = fila.get("categoria", "").replace('"', '\\"')
            caducidad = fila.get("caducidad", "")

            if nombre:
                f_out.write(f"{uri_prod} inv:nombre \"{nombre}\"^^xsd:string .\n")
            if categoria:
                f_out.write(f"{uri_prod} inv:categoria \"{categoria}\"^^xsd:string .\n")
            if caducidad:
                f_out.write(f"{uri_prod} inv:fechaCaducidad \"{caducidad}\"^^xsd:date .\n")

if __name__ == "__main__":
    csv_a_rdf("data/inventario_ejemplo.csv", "rdf/datos.ttl")
