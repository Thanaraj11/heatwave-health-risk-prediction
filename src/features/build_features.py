"""
Feature engineering for risk prediction with proper NaN handling
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.impute import SimpleImputer

def add_hypertension(df):
    """Create hypertension feature from BP readings"""
    df['Hypertension'] = (
        (df['Systolic_BP'] >= 140) | (df['Diastolic_BP'] >= 90)
    ).astype(int)
    return df

def add_heat_index(df):
    """Calculate heat index using simplified formula"""
    df['Heat_Index'] = df['Temperature_C'] + (0.12 * df['Humidity_%'])
    return df

def assign_risk(row):
    """
    Assign risk level based on rules
    Returns: 0=Low, 1=Medium, 2=High
    """
    disease_score = (
        row['Heart_Disease'] +
        row['Diabetes'] +
        row['Respiratory_Issue'] +
        row['Hypertension']
    )
    
    # HIGH RISK - Loosened conditions for demonstration
    # Original: Heat_Index > 42 AND (Age > 60 OR disease_score >= 2 OR Outdoor_Worker == 1)
    if (row['Heat_Index'] > 40 and 
        (row['Age'] > 55 or disease_score >= 1 or row['Outdoor_Worker'] == 1)):
        return 2  # High
    
    # MEDIUM RISK
    elif (row['Heat_Index'] >= 35 or 
          disease_score >= 1 or 
          row['Outdoor_Worker'] == 1):
        return 1  # Medium
    
    # LOW RISK
    return 0  # Low

def encode_categorical(df):
    """Convert categorical columns to numeric"""
    # Encode Gender
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].map({'M': 1, 'F': 0})
    
    # Encode Hydration Level
    if 'Hydration_Level' in df.columns:
        hydration_map = {'Low': 0, 'Moderate': 1, 'Good': 2}
        df['Hydration_Level'] = df['Hydration_Level'].map(hydration_map)
    
    return df

def drop_unused_columns(df):
    """Remove columns not needed for modeling"""
    cols_to_drop = ['Person_ID', 'Date', 'Admitted_Date', 'Climate_ID', 'District']
    existing_cols = [col for col in cols_to_drop if col in df.columns]
    
    if existing_cols:
        df = df.drop(columns=existing_cols)
        print(f"  Dropped columns: {existing_cols}")
    
    return df

def handle_missing_values(df):
    """
    Comprehensive missing value handling
    """
    print("\n" + "="*50)
    print("MISSING VALUE HANDLING")
    print("="*50)
    
    # Check for missing values
    missing_before = df.isnull().sum()
    missing_cols = missing_before[missing_before > 0]
    
    if len(missing_cols) > 0:
        print(f"\nFound missing values in {len(missing_cols)} columns:")
        print(missing_cols)
        
        # Option 1: Drop rows with missing target (Risk_Level)
        if 'Risk_Level' in df.columns:
            target_missing = df['Risk_Level'].isnull().sum()
            if target_missing > 0:
                print(f"\n  Dropping {target_missing} rows with missing Risk_Level")
                df = df.dropna(subset=['Risk_Level'])
        
        # Option 2: For numeric columns, fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        imputer = SimpleImputer(strategy='median')
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
        print(f"\n  Imputed numeric columns with median values")
        
        # Option 3: For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                df[col] = df[col].fillna(mode_val)
                print(f"  Imputed '{col}' with mode: '{mode_val}'")
    else:
        print("\n✓ No missing values found!")
    
    # Verify no missing values remain
    missing_after = df.isnull().sum().sum()
    print(f"\nTotal missing values after handling: {missing_after}")
    
    return df

def build_features(input_path, output_path):
    """
    Complete feature engineering pipeline with NaN handling
    """
    print(f"\nLoading data from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"  Original shape: {df.shape}")
    
    # Drop unused columns
    df = drop_unused_columns(df)
    
    # Handle missing values FIRST (before feature engineering)
    df = handle_missing_values(df)
    
    # Feature engineering
    df = add_hypertension(df)
    df = add_heat_index(df)
    print(f"\n  Added features: Hypertension, Heat_Index")
    
    # Check Heat Index distribution
    print(f"\n  Heat Index Statistics:")
    print(f"    Min: {df['Heat_Index'].min():.2f}")
    print(f"    Max: {df['Heat_Index'].max():.2f}")
    print(f"    Mean: {df['Heat_Index'].mean():.2f}")
    print(f"    >40 count: {(df['Heat_Index'] > 40).sum()}")
    print(f"    >42 count: {(df['Heat_Index'] > 42).sum()}")
    
    # Encode categorical
    df = encode_categorical(df)
    
    # Assign risk levels (returns 0,1,2 directly)
    df['Risk_Level'] = df.apply(assign_risk, axis=1)
    
    # Final check for any NaN in features
    print("\n" + "="*50)
    print("FINAL VALIDATION")
    print("="*50)
    
    X = df.drop(columns=['Risk_Level'])
    y = df['Risk_Level']
    
    # Check for NaN in features
    nan_in_features = X.isnull().sum().sum()
    if nan_in_features > 0:
        print(f"⚠️ WARNING: {nan_in_features} NaN values remain in features!")
        print("Dropping rows with any NaN...")
        df = df.dropna()
        print(f"  New shape: {df.shape}")
    else:
        print("✓ No NaN values in features - ready for training!")
    
    print(f"\nFinal shape: {df.shape}")
    print(f"\nRisk Level Distribution:")
    risk_counts = df['Risk_Level'].value_counts().sort_index()
    risk_names = {0: 'Low', 1: 'Medium', 2: 'High'}
    for risk_code, count in risk_counts.items():
        print(f"  {risk_names[risk_code]}: {count} ({count/len(df)*100:.1f}%)")
    
    # Save
    df.to_csv(output_path, index=False)
    print(f"\n✅ Features saved to: {output_path}")
    
    return df

def main():
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    input_file = processed_dir / "merged_cleaned.csv"
    output_file = processed_dir / "features_ready.csv"
    
    if not input_file.exists():
        print(f"❌ Error: {input_file} not found!")
        print("Please run merge_data.py first.")
        return
    
    build_features(input_file, output_file)

if __name__ == "__main__":
    main()