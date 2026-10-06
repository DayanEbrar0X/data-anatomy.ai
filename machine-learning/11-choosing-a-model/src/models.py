"""Candidate models, simplest first, each behind the same preprocessing."""
import warnings

from sklearn.compose import make_column_transformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

# the baseline never predicts churn, so its precision is 0 by definition
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

NUMERIC = ["tenure", "monthly_charges", "support_tickets"]


def prep(model):
    """Fill gaps with the median, scale numbers, one-hot the contract."""
    numbers = make_pipeline(SimpleImputer(strategy="median"),
                            StandardScaler())
    cols = make_column_transformer((numbers, NUMERIC),
                                   (OneHotEncoder(), ["contract"]))
    return make_pipeline(cols, model)


def candidates():
    # churners are rare, so every real model weights them up ("balanced")
    w = "balanced"
    return {
        "baseline": prep(DummyClassifier(strategy="most_frequent")),
        "logistic": prep(LogisticRegression(class_weight=w,
                                            max_iter=1000)),
        "tree": prep(DecisionTreeClassifier(max_depth=4, class_weight=w,
                                            random_state=0)),
        "forest": prep(RandomForestClassifier(n_estimators=300,
                                              min_samples_leaf=10,
                                              class_weight=w,
                                              random_state=0)),
    }
