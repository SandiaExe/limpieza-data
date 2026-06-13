import pandas as pd
import os

def split_original_excel():
    excel_path = "metsyn_dataset.xlsx"
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    # Definir las hojas y sus nombres de destino
    sheets = {
        "2021": "metsyn_2021.csv",
        "2023": "metsyn_2023.csv",
        "2024": "metsyn_2024.csv",
        "2025": "metsyn_2025.csv"
    }
    
    for sheet_name, csv_name in sheets.items():
        print(f"Procesando hoja {sheet_name}...")
        
        # Leer la hoja del Excel
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # --- LIMPIEZA ESPECÍFICA PARA 2021 ---
        # Si la tabla de conteo de hombres/mujeres genera filas vacías seguidas de texto al final,
        # eliminamos las filas donde los datos clínicos clave estén completamente vacíos.
        if sheet_name == "2021":
            # Eliminamos filas que sean completamente nulas o descartamos el resumen del final
            # Ajusta 'patient_id' o la primera columna si tiene otro nombre en tu Excel
            df = df.dropna(subset=[df.columns[0]]) 
        
        # Ruta de destino en data/raw/
        output_path = os.path.join(output_dir, csv_name)
        df.to_csv(output_path, index=False)
        
        # Validación de filas extraídas
        # df.shape[0] cuenta las filas sin el encabezado. Sumamos 1 para contrastar con tu conteo.
        print(f"  -> Guardado en {output_path} | Filas totales (con encabezado): {df.shape[0] + 1}")

if __name__ == "__main__":
    if os.path.exists("metsyn_dataset.xlsx"):
        split_original_excel()
    else:
        print("Error: No se encontró 'metsyn_dataset.xlsx' en la raíz del proyecto.")