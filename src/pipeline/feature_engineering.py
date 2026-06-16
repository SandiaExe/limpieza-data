import pandas as pd
import numpy as np
import os

def calculate_atp3_criteria(df):
    """
    Evalúa vectorialmente los 5 criterios clínicos del ATP-III adaptados a Latinoamérica.
    """
    # 1. Obesidad Abdominal (Población local: Hombres >= 90 cm, Mujeres >= 80 cm)
    cond_perabd_m = (df['sexo'] == 'M') & (df['perabd'] >= 90)
    cond_perabd_f = (df['sexo'] == 'F') & (df['perabd'] >= 80)
    df['criterio_perabd'] = (cond_perabd_m | cond_perabd_f).astype(int)
    
    # 2. Triglicéridos Altos (>= 150 mg/dL)
    df['criterio_trig'] = (df['trig'] >= 150).astype(int)
    
    # 3. HDL Colesterol Bajo (< 40 mg/dL en varones / < 50 mg/dL en damas)
    cond_hdl_m = (df['sexo'] == 'M') & (df['hdl'] < 40)
    cond_hdl_f = (df['sexo'] == 'F') & (df['hdl'] < 50)
    df['criterio_hdl'] = (cond_hdl_m | cond_hdl_f).astype(int)
    
    # 4. Presión Arterial Elevada (Sistólica >= 130 ó Diastólica >= 85 ó Antecedente Médico de HTA)
    cond_presion = (df['presion_sis'] >= 130) | (df['presion_dia'] >= 85) | (df['antHTa'] == 1)
    df['criterio_presion'] = cond_presion.astype(int)
    
    # 5. Glucosa Alterada (Glucosa >= 100 mg/dL ó Antecedente Médico de Diabetes)
    cond_glucosa = (df['glu'] >= 100) | (df['antDM'] == 1)
    df['criterio_glu'] = cond_glucosa.astype(int)
    
    # ---- EVALUACIÓN DIAGNÓSTICA ----
    # Conteo de factores positivos por paciente (Rango de 0 a 5)
    df['criterios_acumulados'] = (
        df['criterio_perabd'] + 
        df['criterio_trig'] + 
        df['criterio_hdl'] + 
        df['criterio_presion'] + 
        df['criterio_glu']
    )
    
    # Diagnóstico Positivo (metsyn_flag = 1) si acumula 3 o más factores mínimos de riesgo
    df['metsyn_flag'] = (df['criterios_acumulados'] >= 3).astype(int)
    
    return df

def process_all_versions():
    input_dir = "data/processed/imputed_versions"
    output_dir = "data/processed/final_datasets"
    os.makedirs(output_dir, exist_ok=True)
    
    versiones = ['mice', 'knn', 'missforest']
    print("=== Iniciando Ingeniería de Características Clínicas (ATP-III) ===")
    
    for version in versiones:
        file_path = os.path.join(input_dir, f"dataset_clean_{version}.csv")
        if not os.path.exists(file_path):
            print(f"Saltando {version}: No se encontró el archivo.")
            continue
            
        df = pd.read_csv(file_path)
        df_processed = calculate_atp3_criteria(df)
        
        out_path = os.path.join(output_dir, f"dataset_final_{version}.csv")
        df_processed.to_csv(out_path, index=False)
        
        # Muestra analítica para evaluar el impacto del método de imputación en la tasa diagnóstica
        prevalencia = df_processed['metsyn_flag'].mean() * 100
        print(f"Versión [{version.upper()}] calculada con éxito:")
        print(f"  -> Prevalencia de Síndrome Metabólico detectada: {prevalencia:.2f}%")
        print(f"  -> Archivo final guardado en: {out_path}\n")

if __name__ == "__main__":
    process_all_versions()