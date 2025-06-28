from sklearn.ensemble import RandomForestClassifier
from apps.mlops.algorithm.anomaly_detection.base_anomaly_detection import BaseAnomalyDetection
from hyperopt import hp


class RandomForestAnomalyDetector(BaseAnomalyDetection):
    # def get_default_hyperopt_config(self):
    #     return {
    #         "n_estimators": hp.randint("n_estimators", 100, 500),
    #         "max_depth": hp.randint("max_depth", 10, 50),
    #         "min_samples_split": hp.randint("min_samples_split", 2, 10),
    #         "min_samples_leaf": hp.randint("min_samples_leaf", 1, 5),
    #         "max_features": hp.choice("max_features", ["sqrt", "log2", None]),
    #         "bootstrap": hp.choice("bootstrap", [True, False]),
    #         "class_weight": hp.choice("class_weight", ["balanced", "balanced_subsample", None]),
    #     }
        
    def build_model(self, train_params):
        model = RandomForestClassifier(**train_params)
        return model