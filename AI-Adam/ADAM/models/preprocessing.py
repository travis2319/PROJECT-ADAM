import pandas as pd


def handle_missing_values(df):
    """
    Handle missing values in the DataFrame by filling with the median.

    Args:
        df (pd.DataFrame): Input data.

    Returns:
        pd.DataFrame: Processed data.
    """
    return df.fillna(df.median())


def convert_to_numeric(df):
    """
    Convert all columns in the DataFrame to numeric, coercing errors to NaN.

    Args:
        df (pd.DataFrame): Input data.

    Returns:
        pd.DataFrame: Converted data.
    """
    return df.apply(pd.to_numeric, errors="coerce")


def split_data(X, y, test_size=0.2):
    """
    Split data into training and testing sets.

    Args:
        X (pd.DataFrame): Feature set.
        y (pd.Series): Target labels.
        test_size (float): Proportion of test data.

    Returns:
        tuple: Train and test splits for features and labels.
    """
    from sklearn.model_selection import train_test_split
    return train_test_split(X, y, test_size=test_size, random_state=42)
