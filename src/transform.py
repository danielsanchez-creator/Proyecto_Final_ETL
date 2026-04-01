import pandas as pd
from deep_translator import GoogleTranslator
import unidecode

def transformar_datos(datasets):
    print("--- Iniciando Fase de Transformación ---")
    
    # 1. UNIÓN DE TABLAS
    df = pd.merge(datasets['orders'], datasets['items'], on='order_id')
    df = pd.merge(df, datasets['products'], on='product_id')
    df = pd.merge(df, datasets['customers'], on='customer_id')
    df = pd.merge(df, datasets['category_translation'], on='product_category_name', how='left')
    df = pd.merge(df, datasets['reviews'][['order_id', 'review_score', 'review_comment_message']], 
                  on='order_id', how='left')

    # 2. LIMPIEZA
    df['review_comment_message'] = df['review_comment_message'].fillna("")
    df['customer_city'] = df['customer_city'].apply(
        lambda x: unidecode.unidecode(str(x)).upper() if pd.notnull(x) else x
    )

    # 3. FINANZAS Y LOGÍSTICA
    df['price_usd'] = df['price'] / 3.9
    cols_fecha = ['order_purchase_timestamp', 'order_estimated_delivery_date', 'order_delivered_customer_date']
    for col in cols_fecha:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    df['delivery_delta_days'] = (df['order_estimated_delivery_date'] - df['order_delivered_customer_date']).dt.days

    # 4. NLP Y SENTIMIENTO
    def categorizar_sentimiento(score):
        if score >= 4: return 'Satisfecho (Positivo)'
        elif score == 3: return 'Neutral'
        else: return 'Crítico (Negativo)'
    
    df['sentiment_es'] = df['review_score'].apply(categorizar_sentimiento)

    try:
        translator = GoogleTranslator(source='pt', target='es')
        mask_quejas = (df['review_score'] <= 2) & (df['review_comment_message'].str.len() > 10)
        indices_quejas = df[mask_quejas].head(15).index
        df['review_espanol'] = ""
        
        print("Traduciendo muestra de feedback crítico...")
        for idx in indices_quejas:
            texto_original = df.at[idx, 'review_comment_message']
            df.at[idx, 'review_espanol'] = translator.translate(texto_original)
    except Exception as e:
        print(f"Aviso: La traducción falló: {e}")

    # 5. SELECCIÓN DE COLUMNAS
    # --- CAMBIO EN TRANSFORM.PY ---
    columnas_reporte = [
        'order_id', 'customer_id', 'customer_city', 'customer_state',
        'product_category_name_english', 'price_usd', 'review_score',
        'sentiment_es', 'review_comment_message', 'review_espanol',
        'delivery_delta_days', 'order_purchase_timestamp'
    ]
    
    # Esta línea asegura que solo se seleccionen las que realmente existen
    df_final = df[[c for c in columnas_reporte if c in df.columns]].copy() 
    print(f"Transformación completada: {len(df_final)} registros.") [cite: 223]
    return df_final