from models.preprocessing import handle_missing_values
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, precision_recall_curve, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

class EmissionsModel:
    def __init__(self):
        """
        Initialize the Emissions Model with multiple classifiers and StandardScaler.
        """
        self.models = {
            "Random Forest": RandomForestClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
        }
        self.best_model = None
        self.scaler = StandardScaler()

    def preprocess_data(self, df):
        """
        Preprocess the emissions data:
        - Fill missing values.
        - Create compliance labels based on emission values.

        Args:
            df (pd.DataFrame): Input data.

        Returns:
            X (pd.DataFrame): Feature set.
            y (pd.Series): Target labels.
        """
        df = df.copy()
        df.fillna(df.median(), inplace=True)

        # Example compliance label: Binary labels based on a threshold
        df["compliance_label"] = df["emission_value"].apply(lambda x: 1 if x < 100 else 0)
        X = df.drop(["compliance_label"], axis=1)
        y = df["compliance_label"]
        return X, y

    def train(self, df):
        """
        Train multiple models and select the best one based on accuracy.

        Args:
            df (pd.DataFrame): Training data.
        """
        X, y = self.preprocess_data(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        best_score = 0
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = accuracy_score(y_test, y_pred)

            print(f"{name} Accuracy: {score}")
            if score > best_score:
                best_score = score
                self.best_model = model

    def visualize(self, X, y):
        """
        Provide visualizations for the emissions data, including compliance distribution.

        Args:
            X (pd.DataFrame): Feature set.
            y (pd.Series): Target labels.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(y, kde=False, bins=30, color="blue", label="Compliance Distribution")
        plt.legend()
        plt.title("Compliance Distribution")
        plt.show()
