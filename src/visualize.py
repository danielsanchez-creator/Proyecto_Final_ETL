import matplotlib.pyplot as plt
import seaborn as sns
import os

def generar_reporte_visual(df):
    """
    Genera visualizaciones estratégicas basadas en el DataFrame enriquecido.
    Muestra el rendimiento financiero por categoría y la distribución de satisfacción.
    """
    print("--- Generando Visualizaciones de Negocio ---")
    
    # Configuración estética global
    sns.set_theme(style="whitegrid")
    
    # 1. ANÁLISIS DE CATEGORÍAS (VALOR ECONÓMICO)
    plt.figure(figsize=(12, 6))
    col_cat = 'product_category_name_english'
    
    if col_cat in df.columns:
        # Agrupación por ingresos totales en USD
        ingresos_cat = df.groupby(col_cat)['price_usd'].sum().sort_values(ascending=False).head(10)
        
        sns.barplot(
            x=ingresos_cat.values, 
            y=ingresos_cat.index, 
            hue=ingresos_cat.index, 
            palette='magma', 
            legend=False
        )
        plt.title('Top 10 Categorías por Ingreso Total (USD)', fontsize=14)
        plt.xlabel('Total USD ($)')
        plt.ylabel('Categoría')
        plt.tight_layout()
        plt.show()

    # 2. HISTOGRAMA: DISTRIBUCIÓN DE PRECIOS POR SCORE
    plt.figure(figsize=(12, 6))
    # Filtramos outliers de precio para mejorar la visualización (productos < 300 USD)
    df_hist = df[df['price_usd'] < 300].dropna(subset=['review_score'])
    
    sns.histplot(
        data=df_hist,
        x='price_usd',
        hue='review_score',
        multiple="stack",
        palette="viridis",
        bins=30,
        edgecolor=".3"
    )
    plt.title('Distribución de Ventas: Rangos de Precio y Calificación', fontsize=14)
    plt.xlabel('Precio del Producto ($ USD)')
    plt.ylabel('Cantidad de Ventas')
    plt.tight_layout()
    plt.show()

    # 3. RESUMEN DE SENTIMIENTO (NLP)
    plt.figure(figsize=(10, 6))
    if 'sentiment_es' in df.columns:
        sns.countplot(
            data=df, 
            x='sentiment_es', 
            palette='viridis',
            order=['Satisfecho (Positivo)', 'Neutral', 'Crítico (Negativo)']
        )
        plt.title('Resumen General de Sentimiento del Cliente', fontsize=14)
        plt.xlabel('Categoría de Sentimiento')
        plt.ylabel('Número de Reseñas')
        plt.tight_layout()
        plt.show()

    print("Visualizaciones finalizadas exitosamente.")