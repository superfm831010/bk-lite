from apps.mlops.views.anomaly_detection_serving import AnomalyDetectionServingViewSet
from apps.mlops.views.anomaly_detection_train_job import AnomalyDetectionTrainJobViewSet
from rest_framework import routers

from apps.mlops.views.anomaly_detection_dataset import AnomalyDetectionDatasetViewSet
from apps.mlops.views.anomaly_detection_train_data import AnomalyDetectionTrainDataViewSet
from apps.mlops.views.rasa_dataset import RasaDatasetViewSet
from apps.mlops.views.rase_intent import RasaIntentViewSet

router = routers.DefaultRouter()

router.register(r'anomaly_detection_datasets', AnomalyDetectionDatasetViewSet)
router.register(r'anomaly_detection_train_data', AnomalyDetectionTrainDataViewSet)
router.register(r'anomaly_detection_train_jobs', AnomalyDetectionTrainJobViewSet, basename='anomaly_detection_train_jobs')
router.register(r'anomaly_detection_servings', AnomalyDetectionServingViewSet, basename='anomaly_detection_servings')
router.register(r'rasa_datasets', RasaDatasetViewSet, basename='rasa_datasets')
router.register(r'rasa_intent', RasaIntentViewSet, basename='rasa_intent')

urlpatterns = router.urls
