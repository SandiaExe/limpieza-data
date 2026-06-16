import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

def normalize_and_eda_2025():
    input_path = "data/raw/metsyn_2025.csv"
    output_data_path = "data/interim/metsyn_2025_normalizado.csv"
    output_plot_dir = "data/interim/plots_2025"
    
    os.makedirs(os.path.dirname(output_data_path), exist_ok=True)
    os.makedirs(output_plot_dir, exist_ok=True)
    
    df = pd.read_csv(input_path)
    print(f"Dataset 2025 cargado. Registros iniciales: {df.shape[0]}")
    
    # 1. NORMALIZACIÓN Y LIMPIEZA DE CAMPOS ANÓMALOS
    # Corregir la fila 196 donde presion_dia tenía un string corrupto "68/97"
    df['presion_dia'] = df['presion_dia'].astype(str).str.replace('68/97', '82', regex=False)
    
    cols_clinicas = ['perabd', 'glu', 'ct', 'trig', 'hdl', 'ldl', 'presion_sis', 'presion_dia', 'imc', 'hb', 'plaq', 'leuc']
    for col in cols_clinicas:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['-', '', ' ', 'None', 'NaN', 'nan'], np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    df['sexo'] = df['sexo'].astype(str).str.upper().str.strip()
    
    df['antHTa'] = df['antecedentes'].fillna('').str.lower().str.contains('hiperten|hta|presion alta').astype(int)
    df['antDM'] = df['antecedentes'].fillna('').str.lower().str.contains('diabete|dm').astype(int)
    
    df['period'] = "2025"
    
    df.to_csv(output_data_path, index=False)
    print(f"-> Data normalizada de 2025 guardada exitosamente en: {output_data_path}")
    
    # 2. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
    print("\nGenerando reportes gráficos de exploración 2025...")
    
    # Gráfico A: Gráfico de barras de nulos (Evidenciará el vacío total de perabd)
    plt.figure(figsize=(10, 5))
    missing_pct = df[cols_clinicas].isnull().mean() * 100
    missing_pct = missing_pct.sort_values(ascending=False)
    sns.barplot(x=missing_pct.values, y=missing_pct.index, palette="Dark2")
    plt.title("Ausencia Crítica de Variables Clínicas (Año 2025)")
    plt.xlabel("% de Valores Nulos (Evidencia de Pérdida de Variable 'perabd')")
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "missing_data_2025.png"))
    plt.close()
    
    # Gráfico B: Distribución del IMC por Género (Línea base pre-imputación)
    plt.figure(figsize=(8, 4))
    sns.kdeplot(data=df, x="imc", hue="sexo", fill=True, common_norm=False, palette="Set1", alpha=0.5)
    plt.title("Análisis de Densidad de IMC por Género (Año 2025)")
    plt.xlabel("Índice de Masa Corporal (imc)")
    plt.ylabel("Densidad")
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "densidad_imc_2025.png"))
    plt.close()

if __name__ == "__main__":
    normalize_and_eda_2025()