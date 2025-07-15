from apps.mlops.views.anomaly_detection_serving import AnomalyDetectionServingViewSet
from apps.mlops.views.anomaly_detection_train_job import AnomalyDetectionTrainJobViewSet
from rest_framework import routers

from apps.mlops.views.anomaly_detection_dataset import AnomalyDetectionDatasetViewSet
from apps.mlops.views.anomaly_detection_train_data import AnomalyDetectionTrainDataViewSet

router = routers.DefaultRouter()

router.register(r'anomaly_detection_datasets', AnomalyDetectionDatasetViewSet)
router.register(r'anomaly_detection_train_data', AnomalyDetectionTrainDataViewSet)
router.register(r'anomaly_detection_train_jobs', AnomalyDetectionTrainJobViewSet, basename='anomaly_detection_train_jobs')
router.register(r'anomaly_detection_servings', AnomalyDetectionServingViewSet, basename='anomaly_detection_servings')

urlpatterns = router.urls
