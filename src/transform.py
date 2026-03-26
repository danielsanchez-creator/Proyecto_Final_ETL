import pandas as pd
import matplotlib.pyplot as plt

def ejecutar_transformacion(datasets):
    print("--- Iniciando Transformacion ---")
    
    try:
        # Extraer dataframes del diccionario enviado por extract.py
        df_cust = datasets["customers"]
        df_ord = datasets["orders"]
        df_items = datasets["items"]
        df_rev = datasets["reviews"]

        # 1. Uniones (Merge)
        # Unimos Clientes con Ordenes
        df_m = pd.merge(df_ord, df_cust[['customer_id', 'customer_city']], on="customer_id")
        # Unimos con Items (Precio)
        df_m = pd.merge(df_m, df_items[['order_id', 'price']], on="order_id")
        # Unimos con Reviews (Score)
        df_m = pd.merge(df_m, df_rev[['order_id', 'review_score']], on="order_id")

        # 2. Transformaciones de Moneda y Fechas
        print("Transformando precios a USD y formateando fechas...")
        tasa_usd = 0.18
        df_m['price_usd'] = df_m['price'] * tasa_usd
        
        columnas_fecha = ["order_purchase_timestamp", "order_approved_at", "order_delivered_customer_date"]
        for col in columnas_fecha:
            df_m[col] = pd.to_datetime(df_m[col], errors='coerce')

        # 3. Limpieza de Ciudades
        df_m['customer_city'] = df_m['customer_city'].str.upper().str.strip()

        # --- GRAFICO 1: TOP 10 CIUDADES ---
        print("Mostrando grafico de ciudades...")
        plt.figure(figsize=(10, 6))
        df_m['customer_city'].value_counts().head(10).plot(kind='bar', color='skyblue')
        plt.title("Top 10 Ciudades por Volumen de Compras")
        plt.xlabel("Ciudad")
        plt.ylabel("Total de Ordenes")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # --- GRAFICO 2: REVIEW SCORE VS PRICE ---
        print("Mostrando grafico Score vs Precio...")
        plt.figure(figsize=(10, 6))
        df_agrupado = df_m.groupby('review_score')['price_usd'].mean()
        df_agrupado.plot(kind='line', marker='s', color='darkred', linewidth=2)
        plt.title("Precio Promedio (USD) segun Calificacion de Usuario")
        plt.xlabel("Review Score (1-5)")
        plt.ylabel("Precio Promedio en USD")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

        return df_m

    except KeyError as e:
        print(f"Error: No se encontro la tabla o columna {e}. Revisa el diccionario en extract.py")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None