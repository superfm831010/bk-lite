from rest_framework import routers

from apps.mlops.views.anomaly_detection_dataset import AnomalyDetectionDatasetViewSet
from apps.mlops.views.anomaly_detection_train_data import AnomalyDetectionTrainDataViewSet

router = routers.DefaultRouter()
router.register(r'anomaly_detection_datasets', AnomalyDetectionDatasetViewSet)
router.register(r'anomaly_detection_train_data', AnomalyDetectionTrainDataViewSet)

urlpatterns = router.urls
