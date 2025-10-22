import pandas as pd

# Cargar los tres archivos limpios del ETL
dim_establecimientos = pd.read_excel("clean_dim_establecimientos.xlsx")
dim_servicios = pd.read_excel("clean_dim_servicios.xlsx")
dim_horarios = pd.read_excel("clean_dim_horarios.xlsx")

# Unir tablas con clave CLUES
merged = dim_establecimientos.merge(dim_servicios, on="CLUES", how="left") \
                             .merge(dim_horarios, on="CLUES", how="left")

# Filtrar columnas relevantes para análisis
dataset_final = merged[[
    "CLUES",
    "NOMBRE DE LA INSTITUCION",
    "ENTIDAD",
    "MUNICIPIO",
    "LOCALIDAD",
    "SERVICIO",
    "AREA",
    "DIA_SEMANA",
    "HORA INICIO",
    "HORA FIN",
    "ULTIMO MOVIMIENTO",
    "FECHA ULTIMO MOVIMIENTO",
    "LATITUD",
    "LONGITUD"
]]

# Exportar dataset consolidado
dataset_final.to_csv("dataset_final_salud.csv", index=False)
print("Dataset consolidado generado: dataset_final_salud.csv")
