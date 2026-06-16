import pandas as pd
import numpy as np
import os
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer  # Requerido de forma global
from sklearn.impute import IterativeImputer                # Requerido de forma global
from sklearn.ensemble import RandomForestRegressor         # Requerido de forma global para MissForest

def apply_scientific_imputation(method="knn"):
    input_path = "data/processed/consolidated_dataset.csv"
    output_dir = "data/processed/imputed_versions"
    output_path = os.path.join(output_dir, f"dataset_clean_{method}.csv")
    
    if not os.path.exists(input_path):
        print(f"Error: No se encontró el dataset consolidado en {input_path}")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_path)
    print(f"Dataset consolidado cargado. Filas: {df.shape[0]} | Aplicando {method.upper()}...")
    
    # Variables clínicas esenciales propensas a nulos
    cols_clinicas = ['perabd', 'glu', 'ct', 'trig', 'hdl', 'ldl', 'presion_sis', 'presion_dia', 'imc', 'hb', 'plaq', 'leuc']
    
    X_incomplete = df[cols_clinicas].values
    
    # --- PROCESAMIENTO DE PROPUESTAS ---
    if method == "mice":
        # Propuesta 1: MICE Lineal
        imputer = IterativeImputer(max_iter=15, random_state=42)
        X_imputed = imputer.fit_transform(X_incomplete)
        
    elif method == "knn":
        # Propuesta 2: KNN Optimizado Base
        imputer = KNNImputer(n_neighbors=5, weights="distance")
        X_imputed = imputer.fit_transform(X_incomplete)
        
    elif method == "missforest":
        # Propuesta 3: Emulación de MissForest no paramétrica vía Random Forest Iterativo
        imputer = IterativeImputer(
            estimator=RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
            max_iter=10,
            random_state=42
        )
        X_imputed = imputer.fit_transform(X_incomplete)
        
    else:
        print("Error: Método no reconocido.")
        return

    df[cols_clinicas] = X_imputed
    df.to_csv(output_path, index=False)
    print(f"-> Versión de dataset limpia guardada con éxito en: {output_path}")
    print(f"-> Cantidad de nulos remanentes en variables clínicas: {df[cols_clinicas].isnull().sum().sum()}")

if __name__ == "__main__":
    import sys
    # Permitir capturar el argumento enviado por dvc.yaml (mice, knn o missforest)
    if len(sys.argv) > 1:
        chosen_method = sys.argv[1].lower()
    else:
        chosen_method = "mice"
        
    apply_scientific_imputation(method=chosen_method)