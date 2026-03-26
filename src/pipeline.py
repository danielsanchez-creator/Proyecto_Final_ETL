from extract import ejecutar_extraccion
from transform import ejecutar_transformacion

def disparar_pipeline():
    print("--- PIPELINE ETL INICIADO ---")
    
    # Paso 1: Extraccion
    estado, datos = ejecutar_extraccion()
    
    if estado:
        # Paso 2: Transformacion
        df_final = ejecutar_transformacion(datos)
        
        if df_final is not None:
            print("--- FASE DE TRANSFORMACION FINALIZADA ---")
            print("Estructura de columnas final:")
            print(df_final.columns.tolist())
            print(f"Total de registros procesados: {len(df_final)}")
            
            # Opcional: Guardar resultado
            # df_final.to_csv("datos_ecommerce_transformados.csv", index=False)
    else:
        print("Error: El pipeline se detuvo en la fase de extraccion.")

if __name__ == "__main__":
    disparar_pipeline()