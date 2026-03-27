import pandas as pd
import os

def ejecutar_extraccion(ruta_base="data/raw/"):
    print("Iniciando Extracción...")
    archivos = {
        'orders': 'olist_orders_dataset.csv',
        'items': 'olist_order_items_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'reviews': 'olist_order_reviews_dataset.csv',
        'customers': 'olist_customers_dataset.csv',
        'category_translation': 'product_category_name_translation.csv'
    }
    
    datasets = {}
    ruta_real = os.path.join(os.path.dirname(__file__), "..", ruta_base)
    
    for clave, archivo in archivos.items():
        ruta_completa = os.path.normpath(os.path.join(ruta_real, archivo))
        if os.path.exists(ruta_completa):
            datasets[clave] = pd.read_csv(ruta_completa)
        else:
            print(f"Error: No se encontró {archivo} en {ruta_completa}")
            
    return datasets