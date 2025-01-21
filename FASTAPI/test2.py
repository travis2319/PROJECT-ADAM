import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import os

class EnhancedCarEmissionsMLModel:
    def __init__(self, dataframe):
        self.df = dataframe
        self.model = None
        self.features = [
            'o2_s1_wr_current',
            'o2_b1s2',
            'short_fuel_trim_1',
            'long_fuel_trim_1',
            'engine_load',
            'coolant_temp',
            'throttle_pos',
            'rpm'
        ]
        self.indian_emission_norms = {
            'o2_s1_wr_current': {'min': 0.1, 'max': 0.9},
            'o2_b1s2': {'min': 0.1, 'max': 0.9},
            'short_fuel_trim_1': {'min': -10, 'max': 10},
            'long_fuel_trim_1': {'min': -10, 'max': 10},
            'engine_load': {'min': 20, 'max': 80},
            'coolant_temp': {'min': 80, 'max': 110},
            'throttle_pos': {'min': 0, 'max': 100},
            'rpm': {'min': 600, 'max': 4000}
        }

    def advanced_preprocessing(self):
        for feature in self.features:
            # Convert to numeric and handle non-numeric values
            self.df[feature] = pd.to_numeric(self.df[feature], errors='coerce')

        # Check for missing values
        print("Missing values per feature:")
        print(self.df[self.features].isnull().sum())

        # Replace missing values with median and scale
        preprocessor = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', RobustScaler())
        ])

        self.X = preprocessor.fit_transform(self.df[self.features])
        self.y = self._create_compliance_labels()

    def _create_compliance_labels(self):
        compliance = np.ones(len(self.df), dtype=int)
        for sensor, norm in self.indian_emission_norms.items():
            compliance[(self.df[sensor] < norm['min']) | (self.df[sensor] > norm['max'])] = 0
        return compliance

    def train_optimized_model(self):
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        models = {
            'RandomForest': RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
            'GradientBoosting': GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
        }

        best_model = None
        best_score = 0

        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

            print(f"{name} ROC AUC Score: {roc_auc:.4f}")

            if roc_auc > best_score:
                best_model = model
                best_score = roc_auc

        self.model = best_model

    def visualize_comprehensive_report(self):
        if self.model is None:
            print("Model needs to be trained before visualization.")
            return

        plt.figure(figsize=(20, 10))
        importance = self.model.feature_importances_
        plt.barh(self.features, importance)
        plt.title("Feature Importance")
        plt.show()

def main():
    # Fetch your data accordingly
    # This assumes you have a DataFrame `emissions_data`
    emissions_data = pd.DataFrame()  # Replace with actual data fetching function

    emissions_analysis = EnhancedCarEmissionsMLModel(emissions_data)
    emissions_analysis.advanced_preprocessing()
    emissions_analysis.train_optimized_model()
    emissions_analysis.visualize_comprehensive_report()

if __name__ == "__main__":
    main()