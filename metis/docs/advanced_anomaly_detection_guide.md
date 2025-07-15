# AIOps 异常检测算法优化指南

## 📋 概述

本项目实现了企业级的AIOps异常检测解决方案，基于随机森林算法，集成了先进的特征工程、超参数优化和MLflow实验管理功能。

## 🚀 核心优化特性

### 1. 增强的特征工程
- **50+ 时序特征**：统计特征、差分特征、趋势特征、周期性特征等
- **智能缺失值处理**：线性插值 + 前后向填充 + 均值填充
- **异常值检测特征**：IQR方法和Z-score方法
- **时间编码**：sin/cos编码处理周期性

### 2. 智能超参数优化
- **多层次搜索空间**：生产/开发/快速测试模式
- **早停机制**：避免过度搜索，提升效率
- **最优阈值自动发现**：基于验证集的F1分数优化
- **参数重要性分析**：了解哪些参数最影响模型性能

### 3. 全面的模型评估
- **多维度指标**：F1、精确率、召回率、AUC、特异性等
- **交叉验证**：5折分层交叉验证确保模型稳定性
- **特征稳定性分析**：评估特征在不同数据子集上的一致性
- **混淆矩阵和分类报告**：详细的分类性能分析

### 4. 企业级MLflow集成
- **完整实验追踪**：参数、指标、模型、配置文件
- **自动模型注册**：支持模型版本管理和阶段转换
- **可视化分析**：ROC/PR曲线、特征重要性、参数探索历史
- **实验比较**：多个实验运行的对比分析

### 5. 数据不平衡处理
- **类别权重平衡**：自动计算最优类别权重
- **SMOTE过采样**：合成少数类样本
- **欠采样**：随机欠采样处理数据不平衡

## 🛠️ 使用指南

### 基础使用

```python
from src.anomaly_detection.random_forest_detector import RandomForestAnomalyDetector

# 创建检测器
detector = RandomForestAnomalyDetector()

# 训练模型
results = detector.train(
    experiment_name="my_anomaly_detection",
    train_data_path="data/train.csv",
    val_data_path="data/val.csv", 
    test_data_path="data/test.csv",
    freq='5T',  # 5分钟频率
    window=24,  # 2小时窗口
    data_balance_strategy='class_weight'
)

# 预测异常
predictions = detector.predict(new_data, "my_anomaly_detection")
```

### 高级配置

```python
# 使用预设配置
from config.anomaly_detection_config import get_config_for_scenario

# 生产环境配置
config = get_config_for_scenario("production")

results = detector.train(
    experiment_name="production_anomaly_detection",
    train_data_path="data/train.csv",
    val_data_path="data/val.csv",
    test_data_path="data/test.csv",
    **config
)
```

### 自定义超参数搜索

```python
# 自定义超参数优化配置
hyperopt_config = {
    "search_mode": "default",
    "max_evals": 100,
    "early_stop_patience": 20,
    "space": {
        "n_estimators": {"type": "choice", "options": [200, 300, 500]},
        "max_depth": {"type": "choice", "options": [15, 20, None]},
        "class_weight": {"type": "choice", "options": ["balanced"]}
    }
}

results = detector.train(
    experiment_name="custom_optimization",
    # ... 其他参数
    hyperopt_config=hyperopt_config
)
```

## 📊 数据格式要求

### 输入数据格式
CSV文件必须包含以下列：
- `timestamp`: 时间戳 (格式：YYYY-MM-DD HH:MM:SS)
- `value`: 监控指标数值
- `label`: 标签 (0=正常, 1=异常)

示例：
```csv
timestamp,value,label
2024-01-01 00:00:00,45.2,0
2024-01-01 00:05:00,47.1,0
2024-01-01 00:10:00,89.5,1
```

### 预测输出格式
```csv
timestamp,value,anomaly_probability,is_anomaly,confidence
2024-01-01 00:00:00,45.2,0.1,0,0.8
2024-01-01 00:05:00,47.1,0.15,0,0.7
2024-01-01 00:10:00,89.5,0.85,1,0.7
```

## 🎯 性能优化建议

### 1. 数据频率选择
- **高频数据** (秒级): 使用较大窗口(60-120), 较少树(100-200)
- **中频数据** (分钟级): 使用中等窗口(24-48), 中等树数(200-300)
- **低频数据** (小时级): 使用较小窗口(7-24), 较多树(300-500)

### 2. 窗口大小建议
- **1小时窗口**: window=12 (5分钟频率)
- **2小时窗口**: window=24 (5分钟频率)
- **4小时窗口**: window=48 (5分钟频率)
- **1天窗口**: window=24 (1小时频率)

### 3. 超参数优化策略
- **快速测试**: max_evals=20, early_stop_patience=5
- **开发阶段**: max_evals=50, early_stop_patience=15
- **生产部署**: max_evals=100, early_stop_patience=20

### 4. 数据不平衡处理
- **轻微不平衡** (1-10%): 使用class_weight='balanced'
- **中度不平衡** (0.1-1%): 使用class_weight='balanced_subsample'
- **严重不平衡** (<0.1%): 使用SMOTE过采样

## 📈 MLflow实验管理

### 查看实验结果
```bash
# 启动MLflow UI
mlflow ui --backend-store-uri <your_mlflow_uri>
```

### 关键指标含义
- **val_f1**: 验证集F1分数（主要优化目标）
- **test_f1**: 测试集F1分数（最终性能）
- **optimal_threshold**: 最优分类阈值
- **feature_importance_***: 特征重要性
- **cv_f1_mean**: 交叉验证平均F1分数

### 模型选择准则
1. **验证F1分数** > 0.8
2. **测试F1分数** 与验证F1分数差异 < 0.05
3. **交叉验证标准差** < 0.02
4. **特征重要性分布** 合理（非过度集中）

## 🔧 故障排除

### 常见问题

1. **内存不足**
   - 减少`n_estimators`参数
   - 减少`max_evals`参数
   - 使用`max_samples`参数限制采样

2. **训练时间过长**
   - 使用"quick"搜索模式
   - 减少`window`大小
   - 设置较小的`early_stop_patience`

3. **模型性能差**
   - 检查数据质量和标签正确性
   - 增加`window`大小
   - 尝试不同的`data_balance_strategy`
   - 增加训练数据量

4. **特征重要性异常**
   - 检查数据中是否有数据泄露
   - 验证时间特征的编码是否正确
   - 检查是否有常数特征

### 调试模式
```python
import logging
logging.basicConfig(level=logging.INFO)

# 启用详细日志
detector.train(
    # ... 参数
    enable_cross_validation=True,  # 启用交叉验证调试
    enable_feature_selection=True  # 启用特征分析
)
```

## 📚 API 参考

### RandomForestAnomalyDetector

#### train()方法
```python
def train(
    experiment_name: str,           # MLflow实验名称
    train_data_path: str,          # 训练数据路径
    val_data_path: str,            # 验证数据路径 
    test_data_path: str,           # 测试数据路径
    freq: str = 'infer',           # 时间频率
    window: int = 30,              # 滑动窗口大小
    random_state: int = 42,        # 随机种子
    hyperopt_config: Dict = None,  # 超参数优化配置
    enable_feature_selection: bool = True,    # 启用特征选择
    enable_cross_validation: bool = True,     # 启用交叉验证
    data_balance_strategy: str = 'class_weight'  # 数据平衡策略
) -> Dict[str, Any]
```

#### predict()方法  
```python
def predict(
    data: pd.DataFrame,    # 输入数据
    model_name: str        # 模型名称
) -> pd.DataFrame
```

### AiopsUtils

主要工具方法：
- `load_timestamp_csv_data()`: 加载时序数据
- `prepare_timestamp_features()`: 特征工程
- `calculate_comprehensive_metrics()`: 计算评估指标
- `cross_validate_model()`: 交叉验证
- `prepare_balanced_data()`: 数据平衡处理

## 🎉 示例运行

运行完整示例：
```bash
# 完整演示
python examples/advanced_anomaly_detection_example.py --mode full

# 快速演示  
python examples/advanced_anomaly_detection_example.py --mode quick
```

## 📝 更新日志

### v2.0 (当前版本)
- ✅ 50+ 增强时序特征
- ✅ 智能超参数优化
- ✅ 企业级MLflow集成
- ✅ 数据不平衡处理
- ✅ 交叉验证和稳定性分析
- ✅ 最优阈值自动发现
- ✅ 全面的模型诊断

### v1.0 (原版本)
- 基础随机森林实现
- 简单特征工程
- 基础MLflow记录

---

🎯 **核心价值**: 通过科学的方法论和工程最佳实践，打造高精度、高稳定性的AIOps异常检测解决方案。
