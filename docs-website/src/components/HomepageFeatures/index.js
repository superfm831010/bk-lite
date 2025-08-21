import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'OpsPilot',
    icon: '🚁',
    gradient: 'gradient-1',
    badge: 'AI助手',
    metric: '自动化',
    highlights: ['智能诊断', '故障修复'],
    description: (
      <>
        AI驱动的运维助手，智能故障诊断、自动化修复建议，
        提升运维效率，降低人工成本。
      </>
    ),
  },
  {
    title: 'ITSM',
    icon: '🎫',
    gradient: 'gradient-2',
    badge: '服务管理',
    metric: '流程化',
    highlights: ['工单管理', '变更审批'],
    description: (
      <>
        IT服务管理平台，支持工单管理、变更管理、事件管理，
        标准化IT服务流程，提升服务质量和效率。
      </>
    ),
  },
  {
    title: 'CMDB',
    icon: '🏗️',
    gradient: 'gradient-3',
    badge: '配置管理',
    metric: '资产视图',
    highlights: ['自动发现', '关联分析'],
    description: (
      <>
        配置管理数据库，统一管理IT资源和配置信息，
        支持自动发现和智能关联分析，构建完整的IT资产视图。
      </>
    ),
  },
  {
    title: '监控中心',
    icon: '📊',
    gradient: 'gradient-4',
    badge: '实时监控',
    metric: '全方位',
    highlights: ['性能监控', '根因定位'],
    description: (
      <>
        全方位系统监控，支持基础设施、应用性能、业务指标监控，
        实时掌握系统运行状态，快速定位问题根因。
      </>
    ),
  },
  {
    title: '日志中心',
    icon: '📋',
    gradient: 'gradient-5',
    badge: '日志管理',
    metric: '海量存储',
    highlights: ['集中采集', '智能检索'],
    description: (
      <>
        集中化日志管理平台，支持海量日志采集、存储、检索和分析，
        提供强大的日志查询和可视化能力。
      </>
    ),
  },
  {
    title: '告警中心',
    icon: '🚨',
    gradient: 'gradient-6',
    badge: '智能告警',
    metric: '降噪分析',
    highlights: ['智能降噪', '及时响应'],
    description: (
      <>
        智能告警引擎，支持多维度告警规则配置，
        智能降噪和根因分析，确保关键问题及时响应。
      </>
    ),
  },
  {
    title: 'Console',
    icon: '💻',
    gradient: 'gradient-7',
    badge: '控制台',
    metric: '可视化',
    highlights: ['统一操作', '简化流程'],
    description: (
      <>
        统一控制台界面，提供可视化操作和管理功能，
        简化复杂操作流程，提升用户体验和工作效率。
      </>
    ),
  },
  {
    title: '系统管理',
    icon: '⚙️',
    gradient: 'gradient-8',
    badge: '系统治理',
    metric: '安全管控',
    highlights: ['权限管理', '审计日志'],
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
    gradient: 'gradient-9',
    badge: '数据分析',
    metric: '业务决策',
    highlights: ['趋势分析', '运营优化'],
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
    gradient: 'gradient-10',
    badge: '集群管理',
    metric: '生命周期',
    highlights: ['批量操作', '自动运维'],
    description: (
      <>
        集群节点统一管理，支持节点生命周期管理、
        批量操作和自动化运维，简化基础设施管理。
      </>
    ),
  },
  {
    title: 'MLOps',
    icon: '🧠',
    gradient: 'gradient-11',
    badge: '机器学习',
    metric: 'AI运维',
    highlights: ['模型管理', '规模部署'],
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
    gradient: 'gradient-12',
    badge: '实验环境',
    metric: '沙箱测试',
    highlights: ['快速验证', '安全实验'],
    description: (
      <>
        在线实验环境，支持快速验证和测试新功能，
        提供沙箱环境进行安全的实验和开发。
      </>
    ),
  },
];

function Feature({title, description, gradient, icon, badge, metric, highlights}) {
  return (
    <div className={styles.featureItem}>
      <div className={clsx(styles.featureCard, styles[gradient])}>
        <div className={styles.cardHeader}>
          <div className={styles.featureIcon}>
            <span className={styles.iconEmoji}>{icon}</span>
          </div>
          <div className={styles.cardBadge}>{badge}</div>
        </div>
        
        <div className={styles.featureContent}>
          <Heading as="h3" className={styles.featureTitle}>
            {title}
          </Heading>
          <p className={styles.featureDescription}>{description}</p>
          
          <div className={styles.metricHighlight}>
            <span className={styles.metricValue}>{metric}</span>
            <div className={styles.highlightTags}>
              {highlights.map((highlight, idx) => (
                <span key={idx} className={styles.highlightTag}>
                  {highlight}
                </span>
              ))}
            </div>
          </div>
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
            灵活可扩展的运维模块体系，支持从基础设施到业务应用的全栈管理
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
