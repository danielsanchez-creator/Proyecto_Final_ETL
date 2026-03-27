import os
import sys

# Asegurar que Python vea los archivos en /src
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from extract import ejecutar_extraccion
from transform import transformar_datos
from load import cargar_datos
from visualize import generar_reporte_visual

def ejecutar_pipeline():
    print("=== PIPELINE ETL OLIST INICIADO ===")
    
    # 1. EXTRACT
    data_cruda = ejecutar_extraccion()
    
    # 2. TRANSFORM
    df_enriquecido = transformar_datos(data_cruda)
    
    # 3. LOAD
    cargar_datos(df_enriquecido)
    
    # 4. VISUALIZE
    generar_reporte_visual(df_enriquecido)
    
    print("=== PIPELINE FINALIZADO EXITOSAMENTE ===")

if __name__ == "__main__":
    ejecutar_pipeline()