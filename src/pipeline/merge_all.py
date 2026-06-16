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
        
    # Unificar todas las matrices anuales respetando las columnas compartidas
    consolidated_df = pd.concat(datasets, ignore_index=True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    consolidated_df.to_csv(output_path, index=False)
    
    print("\n==============================================")
    print(f"¡PROCESO TOTAL DE CONSOLIDACIÓN EXITOSO!")
    print(f"Dataset guardado en: {output_path}")
    print(f"Dimensiones finales del dataset: {consolidated_df.shape[0]} filas, {consolidated_df.shape[1]} columnas")
    print("==============================================")

if __name__ == "__main__":
    merge_all_periods()