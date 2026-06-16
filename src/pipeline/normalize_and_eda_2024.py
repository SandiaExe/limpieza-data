import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

def normalize_and_eda_2024():
    input_path = "data/raw/metsyn_2024.csv"
    output_data_path = "data/interim/metsyn_2024_normalizado.csv"
    output_plot_dir = "data/interim/plots_2024"
    
    os.makedirs(os.path.dirname(output_data_path), exist_ok=True)
    os.makedirs(output_plot_dir, exist_ok=True)
    
    df = pd.read_csv(input_path)
    print(f"Dataset 2024 cargado. Registros iniciales: {df.shape[0]}")
    
    # 1. NORMALIZACIÓN DE PRESIÓN COMPUESTA (RESCATE DE DATOS)
    def extract_bp(row):
        text = str(row['presionarterial'])
        nums = re.findall(r'\d+', text)
        if len(nums) >= 2:
            return float(nums[0]), float(nums[1])
        return row['presion_sis'], row['presion_dia']

    bp_extracted = df.apply(extract_bp, axis=1, result_type='expand')
    df['presion_sis'] = bp_extracted[0]
    df['presion_dia'] = bp_extracted[1]
    
    # Normalización estándar de columnas
    cols_clinicas = ['perabd', 'glu', 'ct', 'trig', 'hdl', 'ldl', 'presion_sis', 'presion_dia', 'imc', 'hb', 'plaq', 'leuc']
    for col in cols_clinicas:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['-', '', ' ', 'None', 'NaN', 'nan'], np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Estandarizar las variaciones de género encontradas en 2024
    df['sexo'] = df['sexo'].astype(str).str.upper().str.strip()
    df['sexo'] = df['sexo'].map({'MASCULINO': 'M', 'FEMENINO': 'F', 'M': 'M', 'F': 'F'})
    
    # Convertir antecedentes mapeados como "SI"/"NO" texto a binario numérico
    df['antHTa'] = df['antHTa'].str.strip().str.upper().map({'SI': 1, 'NO': 0}).fillna(0).astype(int)
    df['antDM'] = df['antDM'].str.strip().str.upper().map({'SI': 1, 'NO': 0}).fillna(0).astype(int)
    
    df['period'] = "2024"
    
    df.to_csv(output_data_path, index=False)
    print(f"-> Data normalizada de 2024 guardada exitosamente en: {output_data_path}")
    
    # 2. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
    print("\nGenerando reportes gráficos de exploración 2024...")
    
    # Gráfico A: Reporte de Datos Faltantes
    plt.figure(figsize=(10, 5))
    missing_pct = df[cols_clinicas].isnull().mean() * 100
    missing_pct = missing_pct.sort_values(ascending=False)
    sns.barplot(x=missing_pct.values, y=missing_pct.index, palette="Reds_r")
    plt.title("Porcentaje de Datos Faltantes por Variable Clínica (Año 2024)")
    plt.xlabel("% de Valores Nulos")
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "missing_data_2024.png"))
    plt.close()
    
    # Gráfico B: Scatter Plot Presión Arterial Rescatada
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df.dropna(subset=['presion_sis', 'presion_dia']), x='presion_dia', y='presion_sis', alpha=0.6, color="purple")
    plt.axhline(130, color="crimson", linestyle="--", label="Umbral Sistólica (≥130 mmHg)") [cite: 23]
    plt.axvline(85, color="crimson", linestyle=":", label="Umbral Diastólica (≥85 mmHg)") [cite: 23]
    plt.title("Presión Arterial Clínicamente Rescatada (Año 2024)")
    plt.xlabel("Presión Diastólica (mmHg)")
    plt.ylabel("Presión Sistólica (mmHg)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "presion_arterial_rescatada_2024.png"))
    plt.close()

if __name__ == "__main__":
    normalize_and_eda_2024()