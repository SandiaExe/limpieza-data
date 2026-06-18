import pandas as pd
import os

def merge_all_periods():
    interim_dir = "data/interim"
    output_path = "data/processed/consolidated_dataset.csv"
    
    files = [
        os.path.join(interim_dir, "metsyn_2021_normalizado.csv"),
        os.path.join(interim_dir, "metsyn_2023_normalizado.csv"),
        os.path.join(interim_dir, "metsyn_2024_normalizado.csv"),
        os.path.join(interim_dir, "metsyn_2025_normalizado.csv")
    ]
    
    datasets = []
    for f in files:
        if os.path.exists(f):
            print(f"Concatenando: {f}")
            datasets.append(pd.read_csv(f))
            
    if not datasets:
        print("Error: No se encontraron archivos intermedios normalizados.")
        return
        
    consolidated_df = pd.concat(datasets, ignore_index=True)
    
    # 1. Eliminar filas duplicadas
    consolidated_df = consolidated_df.drop_duplicates()
    
    # 2. Rellenar nulos de antecedentes con 0
    if 'antHTa' in consolidated_df.columns and 'antDM' in consolidated_df.columns:
        consolidated_df['antHTa'] = consolidated_df['antHTa'].fillna(0).astype(int)
        consolidated_df['antDM'] = consolidated_df['antDM'].fillna(0).astype(int)

    # -----------------------------------------------------------------
    # NUEVOS AJUSTES: Optimización de tipos de datos y eliminación de redundancia
    # -----------------------------------------------------------------
    # Eliminar 'period' si existe en la matriz
    if 'period' in consolidated_df.columns:
        consolidated_df = consolidated_df.drop(columns=['period'])
        print("-> ¡Éxito! Columna redundante 'period' eliminada.")
        
    # Asegurar que 'anho' sea un entero estricto
    if 'anho' in consolidated_df.columns:
        consolidated_df['anho'] = consolidated_df['anho'].astype(int)
        print("-> ¡Éxito! Tipo de dato de 'anho' corregido a entero (int64).")
    # -----------------------------------------------------------------
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    consolidated_df.to_csv(output_path, index=False)
    
    print("\n==============================================")
    print(f"¡PROCESO TOTAL DE CONSOLIDACIÓN EXITOSO!")
    print(f"Dataset guardado en: {output_path}")
    print(f"Dimensiones finales: {consolidated_df.shape[0]} filas, {consolidated_df.shape[1]} columnas")
    print("==============================================")

if __name__ == "__main__":
    merge_all_periods()