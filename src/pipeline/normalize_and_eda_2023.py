import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

def normalize_and_eda_2023():
    input_path = "data/raw/metsyn_2023.csv"
    output_data_path = "data/interim/metsyn_2023_normalizado.csv"
    output_plot_dir = "data/interim/plots_2023"
    
    os.makedirs(os.path.dirname(output_data_path), exist_ok=True)
    os.makedirs(output_plot_dir, exist_ok=True)
    
    df = pd.read_csv(input_path)
    print(f"Dataset 2023 cargado. Registros iniciales: {df.shape[0]}")
    
    # 1. NORMALIZACIÓN
    cols_clinicas = ['perabd', 'glu', 'ct', 'trig', 'hdl', 'ldl', 'presion_sis', 'presion_dia', 'imc', 'hb', 'plaq', 'leuc']
    
    for col in cols_clinicas:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['-', '', ' ', 'None', 'NaN', 'nan', '_'], np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Estandarizar género de palabra completa a letra ('MASCULINO' -> 'M')
    df['sexo'] = df['sexo'].astype(str).str.upper().str.strip()
    df['sexo'] = df['sexo'].map({'MASCULINO': 'M', 'FEMENINO': 'F', 'M': 'M', 'F': 'F'})
    
    # Extracción analítica de antecedentes desde el texto libre
    df['antHTa'] = df['antecedentes'].fillna('').str.lower().str.contains('hiperten|hta|presion alta').astype(int)
    df['antDM'] = df['antecedentes'].fillna('').str.lower().str.contains('diabete|dm').astype(int)
    
    df['period'] = "2023"
    
    df.to_csv(output_data_path, index=False)
    print(f"-> Data normalizada de 2023 guardada exitosamente en: {output_data_path}")
    
    # 2. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
    print("\nGenerando reportes gráficos de exploración 2023...")
    
    # Gráfico A: Reporte de Datos Faltantes
    plt.figure(figsize=(10, 5))
    missing_pct = df[cols_clinicas].isnull().mean() * 100
    missing_pct = missing_pct.sort_values(ascending=False)
    sns.barplot(x=missing_pct.values, y=missing_pct.index, palette="Reds_r")
    plt.title("Porcentaje de Datos Faltantes por Variable Clínica (Año 2023)")
    plt.xlabel("% de Valores Nulos")
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "missing_data_2023.png"))
    plt.close()
    
    # Gráfico B: Distribución de Triglicéridos (Línea base pre-imputación)
    plt.figure(figsize=(8, 4))
    sns.histplot(df['trig'].dropna(), kde=True, color="orangered", bins=30)
    plt.axvline(150, color="darkred", linestyle="--", label="Umbral ATP-III (≥150 mg/dL)")
    plt.title("Distribución de Triglicéridos - Comunidad USIL (2023)")
    plt.xlabel("Triglicéridos (mg/dL)")
    plt.ylabel("Cantidad de Pacientes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "distribucion_trigliceridos_2023.png"))
    plt.close()
    
    print(f"-> Gráficos guardados en: {output_plot_dir}")

if __name__ == "__main__":
    normalize_and_eda_2023()