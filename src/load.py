import sqlite3
import pandas as pd
import os

def cargar_datos(df, nombre_tabla="ventas_enriquecidas", ruta_db="data/processed/olist_final.db"):
    print(f"--- Iniciando Carga en SQL (Tabla: {nombre_tabla}) ---")
    ruta_real_db = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ruta_db))
    os.makedirs(os.path.dirname(ruta_real_db), exist_ok=True)
    
    try:
        with sqlite3.connect(ruta_real_db) as conn:
            df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
            print(f"Éxito: Se cargaron {len(df)} filas.")
    except Exception as e:
        print(f"Error crítico en carga: {e}")