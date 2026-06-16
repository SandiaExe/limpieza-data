import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

def normalize_and_eda_2021():
    # Rutas del proyecto
    input_path = "data/raw/metsyn_2021.csv"
    output_data_path = "data/interim/metsyn_2021_normalizado.csv"
    output_plot_dir = "data/interim/plots_2021"
    
    os.makedirs(os.path.dirname(output_data_path), exist_ok=True)
    os.makedirs(output_plot_dir, exist_ok=True)
    
    # 1. Cargar el dataset crudo
    df = pd.read_csv(input_path)
    print(f"Dataset 2021 cargado. Registros iniciales: {df.shape[0]}")
    
    # 2. NORMALIZACIÓN
    # Variables clínicas esenciales a estandarizar numéricamente
    cols_clinicas = ['perabd', 'glu', 'ct', 'trig', 'hdl', 'ldl', 'presion_sis', 'presion_dia', 'imc', 'hb', 'plaq', 'leuc']
    
    for col in cols_clinicas:
        # Convertir a string para limpiar caracteres de texto como '-' o espacios
        df[col] = df[col].astype(str).str.strip()
        # Reemplazar guiones típicos por NaN real
        df[col] = df[col].replace(['-', '', ' ', 'None', 'NaN', 'nan'], np.nan)
        # Convertir a float. Los errores (como los números de fecha corruptos '44619') pasarán a NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Corrección de Outliers extremos causados por fallas de Excel (ej: IMC de 44000)
        if col == 'imc':
            df.loc[df[col] > 100, col] = np.nan
            
    # Estandarizar género a mayúsculas
    df['sexo'] = df['sexo'].astype(str).str.upper().str.strip()
    
    # Guardar data normalizada intermedia
    df.to_csv(output_data_path, index=False)
    print(f"-> Data normalizada de 2021 guardada exitosamente en: {output_data_path}")
    
    # 3. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
    print("\nGenerando reportes gráficos de exploración...")
    
    # Gráfico A: Reporte de Datos Faltantes (Missingness)
    plt.figure(figsize=(10, 5))
    missing_pct = df[cols_clinicas].isnull().mean() * 100
    missing_pct = missing_pct.sort_values(ascending=False)
    
    sns.barplot(x=missing_pct.values, y=missing_pct.index, palette="Reds_r")
    plt.title("Porcentaje de Datos Faltantes por Variable Clínica (Año 2021)")
    plt.xlabel("% de Valores Nulos (Requieren Imputación)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "missing_data_2021.png"))
    plt.close()
    
    # Gráfico B: Distribución de la Glucosa (Línea base pre-imputación)
    plt.figure(figsize=(8, 4))
    sns.histplot(df['glu'].dropna(), kde=True, color="teal", bins=30)
    plt.axvline(100, color="red", linestyle="--", label="Umbral ATP-III (≥100 mg/dL)")
    plt.title("Distribución de Glucosa en Ayunas - Comunidad USIL (2021)")
    plt.xlabel("Glucosa (mg/dL)")
    plt.ylabel("Cantidad de Pacientes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_plot_dir, "distribucion_glucosa_2021.png"))
    plt.close()
    
    print(f"-> Gráficos de diagnóstico guardados con éxito en la carpeta: {output_plot_dir}")

if __name__ == "__main__":
    normalize_and_eda_2021()