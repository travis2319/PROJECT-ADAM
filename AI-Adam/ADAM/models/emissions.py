# models/emission.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score

class EnhancedCarEmissionsMLModel:
    def __init__(self, data: pd.DataFrame):
        self.df = data
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
        try:
            for feature in self.features:
                self.df[feature] = pd.to_numeric(self.df[feature], errors='coerce')

            preprocessor = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', RobustScaler())
            ])

            missing_features = [feature for feature in self.features if feature not in self.df.columns]
            if missing_features:
                raise KeyError(f"Missing features: {missing_features}")

            self.X = preprocessor.fit_transform(self.df[self.features])
            self.y = self._create_compliance_labels()

        except Exception as e:
            raise Exception(f"Error during preprocessing: {e}")

    def _create_compliance_labels(self):
        compliance_labels = np.ones(len(self.df), dtype=int)
        for sensor, threshold in self.indian_emission_norms.items():
            sensor_compliance = (
                (self.df[sensor] >= threshold['min']) &
                (self.df[sensor] <= threshold['max'])
            )
            compliance_labels[~sensor_compliance] = 0
        return compliance_labels

    def train_optimized_model(self):
        try:
            # Split data into training and test sets
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
            )

            # Check if both classes are present in the training set
            if len(np.unique(y_train)) < 2:
                raise ValueError("Training data must contain at least two classes.")

            models = {
                'RandomForest': RandomForestClassifier(
                    n_estimators=200, max_depth=10, min_samples_split=5, random_state=42
                ),
                'GradientBoosting': GradientBoostingClassifier(
                    n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42
                )
            }

            best_model = None
            best_score = 0

            for name, model in models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # Ensure predict_proba is called correctly
                if hasattr(model, "predict_proba"):
                    roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
                else:
                    raise RuntimeError(f"{name} does not support probability predictions.")

                if roc_auc > best_score:
                    best_model = model
                    best_score = roc_auc

            if best_model is None:
                raise Exception("No model was trained successfully.")

            self.model = best_model
            return best_model

        except Exception as e:
            raise Exception(f"Error during model training: {e}")
    
    def predict(self, data):
        if self.model is None:
            raise Exception("Model has not been trained yet.")
        
        try:
            return self.model.predict(data)
        except Exception as e:
            raise Exception(f"Prediction error: {e}")
