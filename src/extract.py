import kagglehub
import os
import pandas as pd

def ejecutar_extraccion():
    ruta_proyecto = r"C:\Users\dsanchez\OneDrive - CXC Colombia\Escritorio\Estudio\proyecto_Final_ETL"
    
    try:
        print("--- Descargando y cargando datos de Kaggle ---")
        path_cache = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
        
        # IMPORTANTE: Los nombres de las llaves (ej. "customers") 
        # deben coincidir exactamente con lo que pide el transform.py
        datasets = {
            "customers": pd.read_csv(os.path.join(path_cache, "olist_customers_dataset.csv")),
            "orders": pd.read_csv(os.path.join(path_cache, "olist_orders_dataset.csv")),
            "items": pd.read_csv(os.path.join(path_cache, "olist_order_items_dataset.csv")),
            "reviews": pd.read_csv(os.path.join(path_cache, "olist_order_reviews_dataset.csv"))
        }
        
        print("Tablas cargadas: customers, orders, items, reviews.")
        return True, datasets

    except Exception as e:
        print(f"Error en extraccion: {e}")
        return False, None