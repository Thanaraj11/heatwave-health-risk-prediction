"""
Data cleaning module for climate and health datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_and_clean_climate(input_path, output_path=None):
    """
    Load and clean climate dataset
    - Drop unnecessary columns
    - Handle missing values
    """
    print("Loading climate dataset...")
    climate_df = pd.read_csv(input_path)
    print(f"  Original shape: {climate_df.shape}")
    
    # Drop specified columns
    drop_cols = ['Climate_ID', 'District', 'Heat_Index']
    existing_drop = [col for col in drop_cols if col in climate_df.columns]
    if existing_drop:
        climate_df = climate_df.drop(existing_drop, axis=1)
        print(f"  Dropped columns: {existing_drop}")
    
    # Remove rows with null values
    climate_df.dropna(inplace=True)
    
    # Fill remaining numeric nulls with mean
    numeric_cols = climate_df.select_dtypes(include=['number']).columns
    climate_df[numeric_cols] = climate_df[numeric_cols].fillna(climate_df[numeric_cols].mean())
    
    print(f"  Cleaned shape: {climate_df.shape}")
    
    if output_path:
        climate_df.to_csv(output_path, index=False)
        print(f"  Saved to: {output_path}")
    
    return climate_df

def load_and_clean_health(input_path, output_path=None):
    """
    Load and clean health dataset
    - Handle missing values
    """
    print("Loading health dataset...")
    health_df = pd.read_csv(input_path)
    print(f"  Original shape: {health_df.shape}")
    
    # Remove rows with null values
    health_df.dropna(inplace=True)
    
    # Fill remaining nulls with 0
    health_df.fillna(0, inplace=True)
    
    print(f"  Cleaned shape: {health_df.shape}")
    
    if output_path:
        health_df.to_csv(output_path, index=False)
        print(f"  Saved to: {output_path}")
    
    return health_df

def main():
    # Set paths
    project_root = Path(__file__).parent.parent.parent
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    
    # Create processed directory if it doesn't exist
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean climate data
    climate_df = load_and_clean_climate(
        raw_dir / "climate_sri_lanka.csv",
        processed_dir / "cleaned_climate.csv"
    )
    
    # Clean health data
    health_df = load_and_clean_health(
        raw_dir / "health_sri_lanka.csv",
        processed_dir / "cleaned_health.csv"
    )
    
    print("\n✅ Data cleaning completed successfully!")
    return climate_df, health_df

if __name__ == "__main__":
    main()