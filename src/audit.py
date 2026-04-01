import pandas as pd
import sqlite3
import os

def ejecutar_auditoria(df_final, datasets_crudos, ruta_db):
    print("\n" + "="*50)
    print("📊 REPORTE DE KPIs DE INGENIERÍA (ETL)")
    print("="*50)
    
    # KPI 1: Tasa de Vinculación (Basado en las 113k filas)
    total_ordenes = len(datasets_crudos['orders'])
    procesadas = df_final['order_id'].nunique()
    join_rate = (procesadas / total_ordenes) * 100
    print(f"1. Tasa de Vinculación: {join_rate:.2f}%") # [cite: 72, 73]
    
    # KPI 2: Completitud NLP
    con_texto = df_final[df_final['review_comment_message'] != ""].shape[0]
    completitud = (con_texto / len(df_final)) * 100
    print(f"2. Completitud de Reseñas (NLP): {completitud:.2f}%") # [cite: 80, 81]

    # KPI 3: Consistencia SQL (Debe coincidir con tus 113,314 filas)
    try:
        if os.path.exists(ruta_db):
            with sqlite3.connect(ruta_db) as conn:
                # IMPORTANTE: El nombre de la tabla debe ser 'reporte_ventas'
                filas_sql = pd.read_sql("SELECT COUNT(*) FROM reporte_ventas", conn).iloc[0, 0]
            print(f"3. Consistencia SQL: {'EXITOSA' if filas_sql == len(df_final) else 'DISCREPANCIA'}")
            print(f"   (Filas: {filas_sql})")
        else:
            print("3. Consistencia SQL: Base de datos no encontrada.")
    except Exception as e:
        print(f"3. Consistencia SQL: Error ({e})")
    print("="*50 + "\n")