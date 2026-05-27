"""
Merge cleaned climate and health datasets
"""

import pandas as pd
from pathlib import Path

def merge_datasets(climate_path, health_path, output_path):
    """
    Merge health and climate data on date columns
    Inner join on Admitted_Date (health) = Date (climate)
    """
    print("Loading cleaned datasets...")
    climate_df = pd.read_csv(climate_path)
    health_df = pd.read_csv(health_path)
    
    print(f"  Climate shape: {climate_df.shape}")
    print(f"  Health shape: {health_df.shape}")
    
    # Perform merge
    merged_df = pd.merge(
        health_df,
        climate_df,
        left_on='Admitted_Date',
        right_on='Date',
        how='inner'
    )
    
    print(f"  Merged shape: {merged_df.shape}")
    
    # Save merged data
    merged_df.to_csv(output_path, index=False)
    print(f"  Saved to: {output_path}")
    
    return merged_df

def main():
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    merged_df = merge_datasets(
        processed_dir / "cleaned_climate.csv",
        processed_dir / "cleaned_health.csv",
        processed_dir / "merged_cleaned.csv"
    )
    
    print(f"\n✅ Merge completed! Total records: {len(merged_df)}")
    return merged_df

if __name__ == "__main__":
    main()