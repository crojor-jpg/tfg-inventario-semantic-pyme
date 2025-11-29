import csv
from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD, URIRef
import requests

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
CSV_FILE = "inventario.csv"
TTL_FILE = "inventario_generado.ttl"
FUSEKI_ENDPOINT = "http://localhost:3030/inventario_sostenible/data"  # dataset en Fuseki

# Namespace base de la ontología
BASE = Namespace("http://www.ejemplo.org/inventario#")

# -----------------------------
# CREAR GRAFO RDF
# -----------------------------
g = Graph()
g.bind("inv", BASE)

# Clases
Producto = BASE.Producto
Proveedor = BASE.Proveedor
CriterioSostenibilidad = BASE.CriterioSostenibilidad

# Propiedades de objeto
proveedorDe = BASE.proveedorDe
cumpleCriterio = BASE.cumpleCriterio

# Propiedades de datos
cantidadStock = BASE.cantidadStock
fechaCaducidad = BASE.fechaCaducidad
precio = BASE.precio

# -----------------------------
# LECTURA DEL CSV Y CONVERSIÓN
# -----------------------------
with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Normalizamos nombres de recursos
        prod_id = row["Producto"].replace(" ", "_")
        prov_id = row["Proveedor"].replace(" ", "_")

        # URIs
        prod_uri = BASE[prod_id]
        prov_uri = BASE[prov_id]
        crit_uri = BASE[row["CriterioSostenibilidad"]]

        # Declaraciones
        g.add((prod_uri, RDF.type, Producto))
        g.add((prov_uri, RDF.type, Proveedor))
        g.add((crit_uri, RDF.type, CriterioSostenibilidad))

        # Relación proveedor-producto
        g.add((prov_uri, proveedorDe, prod_uri))

        # Relación producto-criterio
        g.add((prod_uri, cumpleCriterio, crit_uri))

        # Atributos
        g.add((prod_uri, cantidadStock, Literal(int(row["Cantidad"]), datatype=XSD.integer)))
        g.add((prod_uri, fechaCaducidad, Literal(row["FechaCaducidad"], datatype=XSD.date)))
        g.add((prod_uri, precio, Literal(float(row["Precio"]), datatype=XSD.decimal)))

# -----------------------------
# GUARDAR A ARCHIVO TTL
# -----------------------------
g.serialize(destination=TTL_FILE, format="turtle")
print(f"✅ RDF generado en {TTL_FILE}")

# -----------------------------
# OPCIONAL: SUBIR A FUSEKI
# -----------------------------
try:
    headers = {"Content-Type": "text/turtle"}
    data = g.serialize(format="turtle")
    response = requests.post(FUSEKI_ENDPOINT, data=data, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        print("✅ RDF cargado correctamente en Fuseki")
    else:
        print(f"⚠️ Error al subir a Fuseki: {response.status_code} {response.text}")
except Exception as e:
    print(f"⚠️ No se pudo conectar con Fuseki: {e}")
