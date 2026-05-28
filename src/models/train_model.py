"""
Train Random Forest model for risk prediction with NaN handling
"""

import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_model(features_path, model_path, save_plots=True):
    """
    Train Random Forest classifier and save model
    """
    print(f"Loading features from: {features_path}")
    df = pd.read_csv(features_path)
    
    # Split features and target
    X = df.drop(columns=['Risk_Level'])
    y = df['Risk_Level']
    
    print(f"Original shape: {X.shape}")
    print(f"Missing values in X: {X.isnull().sum().sum()}")
    
    # Handle missing values
    if X.isnull().sum().sum() > 0:
        print("\n⚠️ Found missing values! Dropping rows with NaN...")
        valid_mask = ~X.isnull().any(axis=1)
        X = X[valid_mask]
        y = y[valid_mask]
        print(f"New shape after dropping NaN: {X.shape}")
    
    print(f"Features shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    # Get unique classes
    unique_classes = sorted(y.unique())
    print(f"Unique classes in target: {unique_classes}")
    
    # Define class names based on actual classes
    class_names = []
    for cls in unique_classes:
        if cls == 0:
            class_names.append('Low')
        elif cls == 1:
            class_names.append('Medium')
        elif cls == 2:
            class_names.append('High')
    
    print(f"Class names: {class_names}")
    print(f"Features: {list(X.columns)}")
    
    # Train-test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTrain size: {X_train.shape}")
    print(f"Test size: {X_test.shape}")
    
    # Train model
    print("\nTraining Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Predict and evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*50}")
    print(f"Model Accuracy: {accuracy:.4f}")
    print(f"{'='*50}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    if save_plots:
        # Plot confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=class_names,
                    yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        
        # Save plot
        plots_dir = Path(__file__).parent.parent.parent / "plots"
        plots_dir.mkdir(exist_ok=True)
        plt.savefig(plots_dir / "confusion_matrix.png", dpi=150, bbox_inches='tight')
        plt.show()
        
        # Feature importance
        importance_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("\nFeature Importance:")
        print(importance_df)
        
        # Plot feature importance
        plt.figure(figsize=(10, 6))
        sns.barplot(data=importance_df.head(10), x='Importance', y='Feature')
        plt.title('Top 10 Feature Importances')
        plt.tight_layout()
        plt.savefig(plots_dir / "feature_importance.png", dpi=150, bbox_inches='tight')
        plt.show()
    
    # Save model
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n✅ Model saved to: {model_path}")
    
    return model, accuracy

def main():
    project_root = Path(__file__).parent.parent.parent
    
    features_path = project_root / "data" / "processed" / "features_ready.csv"
    model_path = project_root / "models" / "risk_model.pkl"
    
    if not features_path.exists():
        print(f"❌ Error: {features_path} not found!")
        print("Please run build_features.py first.")
        return
    
    train_model(features_path, model_path)

if __name__ == "__main__":
    main()