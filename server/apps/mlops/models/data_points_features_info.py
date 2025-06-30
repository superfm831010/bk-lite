from django.db import models

class DataPointFeaturesInfo(models.Model):
    windows_size= models.IntegerField(
        default=30,
        verbose_name="",
        help_text="滚动窗口大小"
    )
        
    # enable_rolling_mean_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用滚动平均特征",
    #     help_text="是否启用滚动平均特征"
    # )
    
    # enable_rolling_std_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用滚动标准差特征",  
    #     help_text="是否启用滚动标准差特征"
    # )
    
    # enable_rolling_min_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用滚动最小值特征",
    #     help_text="是否启用滚动最小值特征"  
    # )
    
    # enable_rolling_max_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用滚动最大值特征",  
    #     help_text="是否启用滚动最大值特征"
    # )

    # enable_rolling_median_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用滚动中位数特征",
    #     help_text="是否启用滚动中位数特征"
    # )
    
    # enable_diff_1_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用一阶差分特征",
    #     help_text="是否启用一阶差分特征"
    # )
    
    # enable_diff_2_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用二阶差分特征",
    #     help_text="是否启用二阶差分特征"
    # )
    
    # enable_zscore_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用Z-score特征",
    #     help_text="是否启用Z-score特征"
    # )
    
    # enable_trend_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用趋势特征",
    #     help_text="是否启用趋势特征"
    # )
    
    # enable_autocorr_1_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用一阶自相关特征",
    #     help_text="是否启用一阶自相关特征"
    # )
    
    # enable_hour_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用小时特征",
    #     help_text="是否启用小时特征"
    # )
    
    # enable_minute_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用分钟特征",
    #     help_text="是否启用分钟特征"
    # )
    
    # enable_dayofweek_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用星期几特征",
    #     help_text="是否启用星期几特征"
    # )
    
    # enable_month_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用月份特征",
    #     help_text="是否启用月份特征"
    # )
    
    # enable_is_weekend_feature = models.BooleanField(
    #     default=True,
    #     verbose_name="启用是否周末特征",
    #     help_text="是否启用是否周末特征"
    # )
    