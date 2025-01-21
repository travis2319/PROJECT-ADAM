from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

class EnhancedCarEmissionsMLModel:
    def __init__(self, dataframe):
        self.df = dataframe
        self.features = [
            'o2_s1_wr_current', 'o2_b1s2', 'short_fuel_trim_1',
            'long_fuel_trim_1', 'engine_load', 'coolant_temp',
            'throttle_pos', 'rpm'
        ]
        self.indian_emission_norms = {  # Define acceptable emission norms
            'o2_s1_wr_current': {'min': 0.1, 'max': 0.9},
            'o2_b1s2': {'min': 0.1, 'max': 0.9},
            'short_fuel_trim_1': {'min': -10, 'max': 10},
            'long_fuel_trim_1': {'min': -10, 'max': 10},
            'engine_load': {'min': 20, 'max': 80},
            'coolant_temp': {'min': 80, 'max': 110},
            'throttle_pos': {'min': 0, 'max': 100},
            'rpm': {'min': 600, 'max': 4000}
        }
        self.model = None
        self.X_test = None
        self.y_test = None

    def advanced_preprocessing(self):
        try:
            for feature in self.features:
                self.df[feature] = pd.to_numeric(self.df[feature], errors='coerce')

            print("Missing values per feature:")
            print(self.df[self.features].isnull().sum())

            preprocessor = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', RobustScaler())
            ])
            self.X = preprocessor.fit_transform(self.df[self.features])
            self.y = self._create_compliance_labels()

        except Exception as e:
            raise Exception(f"Error during preprocessing: {e}")

    def _create_compliance_labels(self):
        try:
            compliance = np.zeros(len(self.df), dtype=int)  # Start with all vehicles as non-compliant
            for sensor, norm in self.indian_emission_norms.items():
                compliance[(self.df[sensor] >= norm['min']) & (self.df[sensor] <= norm['max'])] = 1  # Mark as compliant

            unique, counts = np.unique(compliance, return_counts=True)
            print(f"Compliance label distribution: {dict(zip(unique, counts))}")

            if len(unique) < 2:
                raise ValueError("Target variable contains only a single class after preprocessing.")

            return compliance
        except Exception as e:
            raise Exception(f"Error creating compliance labels: {e}")

    def train_optimized_model(self):
        try:
            X_train, self.X_test, y_train, self.y_test = train_test_split(
                self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
            )

            print("Training set class distribution:")
            print(pd.Series(y_train).value_counts())

            model = RandomForestClassifier(n_estimators=200, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(self.X_test)
            roc_auc = roc_auc_score(self.y_test, model.predict_proba(self.X_test)[:, 1])
            print(f"Model Accuracy: {accuracy_score(self.y_test, y_pred):.4f}")
            print(f"ROC AUC: {roc_auc:.4f}")

            self.model = model

        except Exception as e:
            raise Exception(f"Error training emissions model: {e}")

    def generate_visualization(self):
        """
        Generate a confusion matrix visualization.
        """
        if self.model is None or self.X_test is None:
            raise Exception("Model is not trained or no test data is available.")

        # Predict the test data
        predictions = self.model.predict(self.X_test)
        cm = confusion_matrix(self.y_test, predictions, labels=[0, 1])

        # Create confusion matrix plot
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Non-Compliant", "Compliant"])
        disp.plot(cmap=plt.cm.Blues)

        # Save the plot to an in-memory file
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()
        return img
