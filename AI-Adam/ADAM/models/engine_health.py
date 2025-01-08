from models.preprocessing import handle_missing_values
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class EngineHealthModel:
    def __init__(self):
        """
        Initialize the Engine Health Model with GradientBoostingClassifier and StandardScaler.
        """
        self.model = GradientBoostingClassifier()
        self.scaler = StandardScaler()

    def preprocess_data(self, df):
        """
        Preprocess the engine health data:
        - Fill missing values.
        - Convert to numeric values.
        - Create labels for engine health based on diagnostic parameters.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            X (pd.DataFrame): Feature set.
            y (pd.Series): Target labels.
        """
        df = df.copy()
        df.fillna(df.median(), inplace=True)
        df = df.apply(pd.to_numeric, errors="coerce")
        df.dropna(inplace=True)

        # Example label creation: Binary labels based on a threshold
        df["health_label"] = df["diagnostic_param"].apply(lambda x: 1 if x < 50 else 0)
        X = df.drop(["health_label"], axis=1)
        y = df["health_label"]
        return X, y

    def train(self, df):
        """
        Train the engine health model using the provided data.

        Args:
            df (pd.DataFrame): Training data.
        """
        X, y = self.preprocess_data(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    def predict(self, data):
        """
        Predict engine health for new data.

        Args:
            data (pd.DataFrame): New input data.

        Returns:
            np.ndarray: Predicted labels.
        """
        data = self.scaler.transform(data)
        return self.model.predict(data)
