import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class OBDDataPreprocessor:
    @staticmethod
    def extract_numeric_value(value):
        """
        Safely convert values to numeric types, handling strings and missing data.
        """
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            try:
                numeric_str = ''.join(char for char in value if char.isdigit() or char in '.-')
                return float(numeric_str) if numeric_str else np.nan
            except ValueError:
                return np.nan
        return np.nan

class EngineHealthPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.df = None
        self.X_test = None
        self.y_test = None
        self.single_class_mode = False
        logging.info("EngineHealthPredictor initialized.")

    def preprocess_data(self, df):
        """
        Preprocess the data to prepare it for ML training.
        """
        logging.info("Starting data preprocessing.")
        self.df = df.copy()

        # Standardize column names to lowercase and replace spaces with underscores
        self.df.columns = [col.lower().replace(' ', '_') for col in self.df.columns]
        logging.info("Normalized column names: %s", self.df.columns.tolist())

        # List of required features
        required_features = ['engine_load', 'coolant_temp', 'short_fuel_trim_1',
                             'long_fuel_trim_1', 'intake_pressure', 'rpm']

        # Check for missing required columns
        missing_features = [col for col in required_features if col not in self.df.columns]
        if missing_features:
            available_columns = self.df.columns.tolist()
            logging.error("Missing required columns: %s", missing_features)
            logging.info("Available columns: %s", available_columns)
            raise ValueError(
                f"Required columns are missing in the dataset: {missing_features}. Available columns: {available_columns}"
            )

        # Extract numeric values and handle missing data
        for feature in required_features:
            self.df[feature] = self.df[feature].apply(OBDDataPreprocessor.extract_numeric_value)
            logging.debug("Processed column '%s'. Sample values: %s", feature, self.df[feature].head().tolist())

        # Handle missing values
        self.df = self.df[required_features].fillna(self.df[required_features].median())
        logging.info("Missing values filled with median for required features.")

        logging.info("Preprocessed data sample: %s", self.df.head().to_dict(orient="records"))
        return self.df

    def prepare_data(self, df):
        """
        Prepare the dataset for training and testing.
        """
        logging.info("Preparing data for training and testing.")
        processed_df = self.preprocess_data(df)
        features = ['engine_load', 'coolant_temp', 'short_fuel_trim_1',
                    'long_fuel_trim_1', 'intake_pressure', 'rpm']
        X = processed_df[features]
        y = self._create_health_labels(processed_df)

        # Log label distribution
        unique_labels = y.value_counts()
        logging.info("Label distribution:\n%s", unique_labels)

        # Allow single-class training
        if len(unique_labels) < 2:
            logging.warning("Dataset contains only one class. The model will always predict this class.")
            self.single_class_mode = True
        else:
            self.single_class_mode = False

        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        logging.info("Data split completed. Scaling features.")
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        return X_train_scaled, self.X_test_scaled, y_train, self.y_test

    def _create_health_labels(self, df):
        """
        Create health labels based on diagnostic parameters.
        """
        logging.info("Creating engine health labels.")

        def classify_health(row):
            conditions = [
                row.get('engine_load', 0) > 70,  # Adjusted threshold
                row.get('coolant_temp', 0) > 95,  # Adjusted threshold
                abs(row.get('short_fuel_trim_1', 0)) > 8,  # Adjusted threshold
                abs(row.get('long_fuel_trim_1', 0)) > 12,  # Adjusted threshold
                row.get('intake_pressure', 0) < 60 or row.get('intake_pressure', 0) > 140,  # Expanded range
                row.get('rpm', 0) > 4500 or row.get('rpm', 0) < 600,  # Adjusted RPM thresholds
            ]
            issue_count = sum(conditions)
            if issue_count > 2:
                return 'Needs Attention'
            else:
                return 'Good'

        labels = df.apply(classify_health, axis=1)

        # Log label distribution
        label_distribution = labels.value_counts()
        logging.info("Generated label distribution: %s", label_distribution.to_dict())

        return labels

    def train_model(self, X_train, y_train):
        """
        Train the Gradient Boosting model.
        """
        if self.single_class_mode:
            logging.info("Single-class mode detected. Training a dummy model.")
            self.model = lambda x: np.full(len(x), y_train.iloc[0])  # Always predict the first class
            return

        logging.info("Training the Gradient Boosting model.")
        self.model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        self.model.fit(X_train, y_train)
        logging.info("Model training completed.")

    def evaluate_model(self, X_test, y_test):
        """
        Evaluate the model's performance and return the confusion matrix.
        """
        if self.single_class_mode:
            logging.info("Single-class mode: Skipping evaluation metrics.")
            return np.array([[len(y_test), 0], [0, 0]])  # Dummy confusion matrix for single class

        logging.info("Evaluating model performance.")
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info("Model Accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification Report:\n%s", classification_report(y_test, y_pred))
        cm = confusion_matrix(y_test, y_pred)
        return cm

    def visualize_confusion_matrix(self, cm):
        """
        Generate and return a confusion matrix visualization or summary for single-class mode.
        """
        if self.single_class_mode:
            logging.info("Single-class mode: Visualizing summary of predictions.")
            total_good = len(self.X_test)  # All predictions are "Good" in single-class mode

            plt.figure(figsize=(8, 6))
            plt.bar(['Good'], [total_good], color='green', alpha=0.7)
            plt.title('Prediction Summary: Single-Class Mode')
            plt.xlabel('Predicted Class')
            plt.ylabel('Count')
            plt.tight_layout()

            img = io.BytesIO()
            plt.savefig(img, format="png")
            img.seek(0)
            plt.close()
            return img

        # For normal mode, plot the confusion matrix
        logging.info("Generating confusion matrix visualization.")
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Good', 'Needs Attention'],
                    yticklabels=['Good', 'Needs Attention'])
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()
        return img
