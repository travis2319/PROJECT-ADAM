import pandas as pd
from models.preprocessing import handle_missing_values
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

class MaintenanceModel:
    def __init__(self):
        """
        Initialize the Predictive Maintenance Model with RandomForestClassifier and StandardScaler.
        """
        self.model = RandomForestClassifier()
        self.scaler = StandardScaler()

    def preprocess_data(self, df):
        """
        Preprocess maintenance data:
        - Fill missing values.
        - Create labels based on wear and tear thresholds.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            X (pd.DataFrame): Feature set.
            y (pd.Series): Target labels.
        """
        df = df.copy()
        df.fillna(df.median(), inplace=True)

        # Example labels for maintenance: Binary labels based on a threshold
        df["maintenance_label"] = df["wear_and_tear"].apply(lambda x: 1 if x > 70 else 0)
        X = df.drop(["maintenance_label"], axis=1)
        y = df["maintenance_label"]
        return X, y

    def train(self, df):
        """
        Train the maintenance model.

        Args:
            df (pd.DataFrame): Training data.
        """
        X, y = self.preprocess_data(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        print("Classification Report:\n", classification_report(y_test, y_pred))

    def predict(self, data):
        """
        Predict maintenance requirements for new data.

        Args:
            data (pd.DataFrame): New input data.

        Returns:
            np.ndarray: Predicted labels.
        """
        data = self.scaler.transform(data)
        return self.model.predict(data)
