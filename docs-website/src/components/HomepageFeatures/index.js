import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'CMDB',
    icon: '🏗️',
    gradient: 'gradient-1',
    description: (
      <>
        配置管理数据库，统一管理IT资源和配置信息，
        支持自动发现和智能关联分析，构建完整的IT资产视图。
      </>
    ),
  },
  {
    title: '监控',
    icon: '📊',
    gradient: 'gradient-2', 
    description: (
      <>
        全方位系统监控，支持基础设施、应用性能、业务指标监控，
        实时掌握系统运行状态，快速定位问题根因。
      </>
    ),
  },
  {
    title: '日志',
    icon: '�',
    gradient: 'gradient-3',
    description: (
      <>
        集中化日志管理平台，支持海量日志采集、存储、检索和分析，
        提供强大的日志查询和可视化能力。
      </>
    ),
  },
  {
    title: '告警',
    icon: '�',
    gradient: 'gradient-4',
    description: (
      <>
        智能告警引擎，支持多维度告警规则配置，
        智能降噪和根因分析，确保关键问题及时响应。
      </>
    ),
  },
  {
    title: '系统管理',
    icon: '⚙️',
    gradient: 'gradient-5',
    description: (
      <>
        统一系统管理平台，包含用户权限、组织架构、审计日志等功能，
        提供完善的系统治理和安全管控能力。
      </>
    ),
  },
  {
    title: '运营分析',
    icon: '📈',
    gradient: 'gradient-6',
    description: (
      <>
        业务运营数据分析，支持多维度报表和趋势分析，
        帮助企业优化运营效率和业务决策。
      </>
    ),
  },
  {
    title: '节点管理',
    icon: '🖥️',
    gradient: 'gradient-1',
    description: (
      <>
        集群节点统一管理，支持节点生命周期管理、
        批量操作和自动化运维，简化基础设施管理。
      </>
    ),
  },
  {
    title: 'OpsPilot',
    icon: '🚁',
    gradient: 'gradient-2',
    description: (
      <>
        AI驱动的运维助手，智能故障诊断、自动化修复建议，
        提升运维效率，降低人工成本。
      </>
    ),
  },
  {
    title: 'MLOps',
    icon: '🧠',
    gradient: 'gradient-3',
    description: (
      <>
        机器学习运维平台，支持模型训练、部署、监控全生命周期管理，
        加速AI应用落地和规模化部署。
      </>
    ),
  },
  {
    title: 'PlayGround',
    icon: '🧪',
    gradient: 'gradient-4',
    description: (
      <>
        在线实验环境，支持快速验证和测试新功能，
        提供沙箱环境进行安全的实验和开发。
      </>
    ),
  },
];

function Feature({icon, title, description, gradient}) {
  return (
    <div className={styles.featureItem}>
      <div className={styles.featureCard}>
        <div className={clsx(styles.featureIcon, styles[gradient])}>
          <span className={styles.iconEmoji}>{icon}</span>
        </div>
        <div className={styles.featureContent}>
          <Heading as="h3" className={styles.featureTitle}>
            {title}
          </Heading>
          <p className={styles.featureDescription}>{description}</p>
        </div>
        <div className={clsx(styles.featureGlow, styles[gradient])}></div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2" className={styles.sectionTitle}>
            产品模块
          </Heading>
          <p className={styles.sectionSubtitle}>
            完整的企业级运维解决方案，涵盖从基础设施到业务应用的全栈管理能力
          </p>
        </div>
        <div className={styles.featuresGrid}>
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
