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
        
    # 1. Unificar todas las matrices anuales
    consolidated_df = pd.concat(datasets, ignore_index=True)
    
    # 2. CORRECCIÓN: Eliminar filas completamente duplicadas si existen (eran, pero queria eliminarlas)
    initial_rows = consolidated_df.shape[0]
    consolidated_df = consolidated_df.drop_duplicates()
    final_rows = consolidated_df.shape[0]

    # -----------------------------------------------------------------
    # NUEVA CORRECCIÓN: Rellenar nulos de antecedentes con 0 (Ausencia de enfermedad) (Esto es un problema de la data de 2021)
    # -----------------------------------------------------------------
    if 'antHTa' in consolidated_df.columns and 'antDM' in consolidated_df.columns:
        consolidated_df['antHTa'] = consolidated_df['antHTa'].fillna(0).astype(int)
        consolidated_df['antDM'] = consolidated_df['antDM'].fillna(0).astype(int)
        print("-> ¡Éxito! Nulos en antecedentes médicos de 2021 rellenados con 0 (Sano).")
    # -----------------------------------------------------------------
    
    if initial_rows != final_rows:
        print(f"-> ¡Limpieza exitosa! Se eliminaron {initial_rows - final_rows} filas duplicadas.")
    
    # 3. Guardar el archivo limpio en la zona procesada
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    consolidated_df.to_csv(output_path, index=False)
    
    print("\n==============================================")
    print(f"¡PROCESO TOTAL DE CONSOLIDACIÓN EXITOSO!")
    print(f"Dataset guardado en: {output_path}")
    print(f"Dimensiones finales del dataset: {consolidated_df.shape[0]} filas, {consolidated_df.shape[1]} columnas")
    print("==============================================")

if __name__ == "__main__":
    merge_all_periods()