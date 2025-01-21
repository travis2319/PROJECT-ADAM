import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Union, Tuple
from collections import defaultdict
from datetime import datetime

# Configure logging with user context
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - User: %(user)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(logger, {'user': 'VOID-001'})


class DTCAnalyzerConfig:
    """Configuration for DTC Analyzer"""
    CURRENT_UTC_TIME = "2025-01-18 11:16:25"
    CURRENT_USER = "VOID-001"
    DTC_HEALTH_THRESHOLDS = {
        'critical': 30,
        'warning': 60,
        'good': 100
    }


class DTCAnalyzer:
    """A comprehensive analyzer for Diagnostic Trouble Codes (DTC) data."""

    def __init__(self, df: pd.DataFrame, user_id: str = DTCAnalyzerConfig.CURRENT_USER):
        """Initialize the DTC Analyzer with DataFrame and user context."""
        self.df = df
        self.user_id = user_id
        self.timestamp = DTCAnalyzerConfig.CURRENT_UTC_TIME
        self.dtc_columns = [col for col in df.columns if "dtc" in col.lower()]
        self.numeric_dtc = {}
        self.categorical_dtc = {}
        self._categorize_columns()
        logger.info(f"Initialized DTCAnalyzer for user {self.user_id} at {self.timestamp}")

    def _safe_convert_to_float(self, value) -> float:
        """Safely convert various types to float."""
        try:
            if isinstance(value, (np.float16, np.float32, np.float64)):
                return float(value)
            elif isinstance(value, str):
                return float(value.strip())
            elif isinstance(value, (int, float)):
                return float(value)
            return 0.0
        except (ValueError, TypeError):
            return 0.0

    def _categorize_columns(self):
        """Separate numeric and categorical DTC columns."""
        try:
            for col in self.dtc_columns:
                try:
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        self.numeric_dtc[col] = self.df[col].apply(self._safe_convert_to_float)
                    else:
                        self.categorical_dtc[col] = self.df[col]
                except Exception as e:
                    logger.error(f"Error processing column {col}: {e}")
                    continue

            logger.info(
                f"Categorized {len(self.numeric_dtc)} numeric and {len(self.categorical_dtc)} categorical columns")
        except Exception as e:
            logger.error(f"Error in column categorization for user {self.user_id}: {e}")

    def analyze_numeric_dtc(self) -> Dict[str, Dict[str, Union[float, Dict]]]:
        """Analyze numeric DTC columns with detailed statistics."""
        try:
            numeric_analysis = {}
            for col, series in self.numeric_dtc.items():
                try:
                    clean_series = pd.to_numeric(series, errors='coerce')
                    analysis = {
                        'statistics': {
                            'mean': float(clean_series.mean() or 0.0),
                            'median': float(clean_series.median() or 0.0),
                            'std': float(clean_series.std() or 0.0),
                            'min': float(clean_series.min() or 0.0),
                            'max': float(clean_series.max() or 0.0),
                            'q1': float(clean_series.quantile(0.25) or 0.0),
                            'q3': float(clean_series.quantile(0.75) or 0.0)
                        },
                        'outliers': self._detect_outliers(clean_series),
                        'frequency': {str(k): float(v) for k, v in clean_series.value_counts().to_dict().items()},
                        'missing_values': int(clean_series.isna().sum()),
                        'timestamp': self.timestamp
                    }
                    numeric_analysis[col] = analysis
                except Exception as e:
                    logger.error(f"Error analyzing column {col}: {e}")
                    continue
            return numeric_analysis
        except Exception as e:
            logger.error(f"Error in numeric analysis for user {self.user_id}: {e}")
            return {}

    def _detect_outliers(self, series: pd.Series) -> Dict[str, List[float]]:
        """Detect outliers using IQR method with enhanced error handling."""
        try:
            clean_series = pd.to_numeric(series, errors='coerce')
            Q1 = clean_series.quantile(0.25)
            Q3 = clean_series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = {
                'low': [float(x) for x in clean_series[clean_series < lower_bound].tolist()],
                'high': [float(x) for x in clean_series[clean_series > upper_bound].tolist()]
            }
            return outliers
        except Exception as e:
            logger.error(f"Error detecting outliers for user {self.user_id}: {e}")
            return {'low': [], 'high': []}

    def analyze_categorical_dtc(self) -> Dict[str, Dict[str, Union[Dict, int]]]:
        """Analyze categorical DTC columns with pattern recognition."""
        try:
            categorical_analysis = {}
            for col, series in self.categorical_dtc.items():
                try:
                    analysis = {
                        'value_counts': {str(k): int(v) for k, v in series.value_counts().to_dict().items()},
                        'unique_count': int(series.nunique()),
                        'missing_values': int(series.isna().sum()),
                        'common_patterns': self._identify_patterns(series),
                        'error_codes': self._extract_error_codes(series),
                        'timestamp': self.timestamp
                    }
                    categorical_analysis[col] = analysis
                except Exception as e:
                    logger.error(f"Error analyzing categorical column {col}: {e}")
                    continue
            return categorical_analysis
        except Exception as e:
            logger.error(f"Error in categorical analysis for user {self.user_id}: {e}")
            return {}

    def _identify_patterns(self, series: pd.Series) -> Dict[str, int]:
        """Identify common patterns in categorical DTC data."""
        try:
            patterns = defaultdict(int)
            for value in series.dropna():
                if isinstance(value, str):
                    if value.startswith('P'):
                        patterns['Powertrain'] += 1
                    elif value.startswith('B'):
                        patterns['Body'] += 1
                    elif value.startswith('C'):
                        patterns['Chassis'] += 1
                    elif value.startswith('U'):
                        patterns['Network'] += 1
            return dict(patterns)
        except Exception as e:
            logger.error(f"Error identifying patterns for user {self.user_id}: {e}")
            return {}

    def _extract_error_codes(self, series: pd.Series) -> Dict[str, int]:
        """Extract and categorize specific error codes."""
        try:
            error_codes = defaultdict(int)
            for value in series.dropna():
                if isinstance(value, str):
                    code_match = ''.join(filter(str.isdigit, value))
                    if code_match:
                        error_codes[code_match] += 1
            return dict(error_codes)
        except Exception as e:
            logger.error(f"Error extracting error codes for user {self.user_id}: {e}")
            return {}

    def _calculate_health_score(self) -> float:
        """Calculate an overall vehicle health score based on DTC data."""
        try:
            score = 100.0

            # Reduce score based on number of DTCs
            for _, series in self.categorical_dtc.items():
                unique_dtcs = series.nunique()
                score -= min(float(unique_dtcs * 5), 30.0)

            # Reduce score based on numeric anomalies
            for _, series in self.numeric_dtc.items():
                clean_series = pd.to_numeric(series, errors='coerce')
                outliers = self._detect_outliers(clean_series)
                score -= min(len(outliers['high']) * 2.0, 20.0)

            return max(0.0, min(100.0, score))
        except Exception as e:
            logger.error(f"Error calculating health score for user {self.user_id}: {e}")
            return 0.0

    def generate_summary(self) -> Dict:
        """Generate a comprehensive summary of all DTC analysis."""
        try:
            if not self.dtc_columns:
                return {
                    "error": "No DTC-related columns found.",
                    "timestamp": self.timestamp,
                    "user_id": self.user_id
                }

            summary = {
                "metadata": {
                    "total_dtc_columns": len(self.dtc_columns),
                    "numeric_columns": len(self.numeric_dtc),
                    "categorical_columns": len(self.categorical_dtc),
                    "timestamp": self.timestamp,
                    "user_id": self.user_id
                },
                "numeric_analysis": self.analyze_numeric_dtc(),
                "categorical_analysis": self.analyze_categorical_dtc(),
                "overall_health_score": self._calculate_health_score()
            }
            logger.info(f"Successfully generated DTC summary for user {self.user_id}")
            return summary
        except Exception as e:
            logger.error(f"Error generating DTC summary for user {self.user_id}: {e}")
            return {
                "error": f"Error generating summary: {str(e)}",
                "timestamp": self.timestamp,
                "user_id": self.user_id
            }


def summarize_dtc_columns(
        df: pd.DataFrame,
        user_id: str = DTCAnalyzerConfig.CURRENT_USER
) -> Dict:
    """Enhanced function to summarize DTC-related columns from the database."""
    try:
        analyzer = DTCAnalyzer(df, user_id)
        summary = analyzer.generate_summary()
        logger.info(f"Successfully generated DTC summary for user {user_id}")
        return summary
    except Exception as e:
        logger.error(f"Error in DTC summary generation for user {user_id}: {e}")
        return {
            "error": f"Failed to generate DTC summary: {str(e)}",
            "timestamp": DTCAnalyzerConfig.CURRENT_UTC_TIME,
            "user_id": user_id
        }
