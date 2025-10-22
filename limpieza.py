
import pandas as pd

# ----------------------------------------------------
# ETAPA 1: EXTRACCIÓN
# ----------------------------------------------------
print("=== ETAPA 1: EXTRACCIÓN ===")

# Ruta del dataset original
ruta = "ESTABLECIMIENTO_SALUD_202509.xlsx"

# Cargar las tres hojas principales
clues = pd.read_excel(ruta, sheet_name="CLUES_202509")
subclues = pd.read_excel(ruta, sheet_name="SUBCLUES_202509")
horarios = pd.read_excel(ruta, sheet_name="HORARIOS_202509")

print(f"Datos cargados:")
print(f"- CLUES: {len(clues)} registros")
print(f"- SUBCLUES: {len(subclues)} registros")
print(f"- HORARIOS: {len(horarios)} registros\n")

# ----------------------------------------------------
# ETAPA 2: TRANSFORMACIÓN
# ----------------------------------------------------
print("=== ETAPA 2: TRANSFORMACIÓN ===")

# ---------- CLUES ----------
print("Limpieza de CLUES...")

clues.columns = clues.columns.str.strip().str.upper()
clues = clues.drop_duplicates(subset=["CLUES"])

# Normalización de texto
for col in ["NOMBRE DE LA INSTITUCION", "ENTIDAD", "MUNICIPIO", "LOCALIDAD"]:
    clues[col] = clues[col].astype(str).str.strip().str.title()

# Normalización de fechas
clues["FECHA ULTIMO MOVIMIENTO"] = pd.to_datetime(
    clues["FECHA ULTIMO MOVIMIENTO"], errors="coerce", dayfirst=True
)

# Conversión de coordenadas
clues["LATITUD"] = pd.to_numeric(clues["LATITUD"], errors="coerce")
clues["LONGITUD"] = pd.to_numeric(clues["LONGITUD"], errors="coerce")

# Rellenar valores faltantes
clues.fillna("NO APLICA", inplace=True)

print(" CLUES limpiado correctamente.\n")

# ---------- SUBCLUES ----------
print("Limpieza de SUBCLUES...")

subclues.columns = subclues.columns.str.strip().str.upper()
subclues = subclues.drop_duplicates(subset=["SUBCLUES"])

# Normalización de campos
for col in ["SERVICIO", "AREA", "UBICACION FISICA"]:
    subclues[col] = subclues[col].astype(str).str.strip().str.title()
subclues.fillna("NO APLICA", inplace=True)

print(" SUBCLUES limpiado correctamente.\n")

# ---------- LIMPIEZA Y REESTRUCTURACIÓN DE HORARIOS ----------
print("Limpieza y normalización de HORARIOS...")

horarios.columns = horarios.columns.str.strip().str.upper()

# Normalizar formato de horas
for col in ["HORA INICIO", "HORA FIN"]:
    horarios[col] = horarios[col].astype(str).str.strip()

# Convertir los días (LUNES a DOMINGO) en filas (modelo largo)
dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]

horarios_long = horarios.melt(
    id_vars=["CLUES", "HORA INICIO", "HORA FIN"],
    value_vars=dias,
    var_name="DIA_SEMANA",
    value_name="ABIERTO"
)

# Quitar filas sin datos y normalizar texto
horarios_long = horarios_long[horarios_long["ABIERTO"].notna()]
horarios_long["DIA_SEMANA"] = horarios_long["DIA_SEMANA"].str.title()
horarios_long["ABIERTO"] = horarios_long["ABIERTO"].replace({"Si": "SI", "No": "NO"})

print(" HORARIOS transformado correctamente (formato largo).\n")

# ----------------------------------------------------
# ETAPA 3: VALIDACIÓN DE RELACIONES
# ----------------------------------------------------
print("=== ETAPA 3: VALIDACIÓN DE RELACIONES ===")

# Validar que todos los subclues y horarios correspondan a CLUES existentes
subclues = subclues[subclues["CLUES"].isin(clues["CLUES"])]
horarios_long = horarios_long[horarios_long["CLUES"].isin(clues["CLUES"])]

print(f"Subclues válidos: {len(subclues)}")
print(f"Horarios válidos: {len(horarios_long)}\n")

# ----------------------------------------------------
# ETAPA 4: CARGA DE DATOS
# ----------------------------------------------------
print("=== ETAPA 4: CARGA ===")

# Guardar los datos limpios en archivos Excel independientes
clues.to_excel("clean_dim_establecimientos.xlsx", index=False)
subclues.to_excel("clean_dim_servicios.xlsx", index=False)
horarios_long.to_excel("clean_dim_horarios.xlsx", index=False)

print(" Archivos generados correctamente:")
print("  - clean_dim_establecimientos.xlsx")
print("  - clean_dim_servicios.xlsx")
print("  - clean_dim_horarios.xlsx\n")

print("=== PROCESO ETL FINALIZADO CON ÉXITO ===")
