import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import { FaHelicopter, FaTicketAlt, FaDatabase, FaChartBar, FaClipboardList, FaBell, FaLaptopCode, FaCogs, FaChartLine, FaServer, FaBrain, FaFlask } from 'react-icons/fa';

const FeatureList = [
  {
    title: 'OpsPilot',
    icon: <FaHelicopter color="var(--ifm-color-primary)" />,
    gradient: 'gradient-1',
    badge: 'AI助手',
    metric: '自动化',
    highlights: ['智能诊断', '故障修复'],
    description: (
      <>
        AI 驱动的运维助手，支持故障诊断与修复建议，帮助快速定位和解决问题。
      </>
    ),
  },
  {
    title: 'ITSM',
    icon: <FaTicketAlt color="var(--ifm-color-primary)" />,
    gradient: 'gradient-2',
    badge: '服务管理',
    metric: '流程化',
    highlights: ['工单管理', '变更审批'],
    description: (
      <>
        轻量化 IT 服务管理平台，提供工单、变更、事件等流程管理能力。
      </>
    ),
  },
  {
    title: 'CMDB',
    icon: <FaDatabase color="var(--ifm-color-primary)" />,
    gradient: 'gradient-3',
    badge: '配置管理',
    metric: '资产视图',
    highlights: ['自动发现', '关联分析'],
    description: (
      <>
        配置管理数据库，统一管理资源与关系，支持自动发现和关联分析。
      </>
    ),
  },
  {
    title: '监控中心',
    icon: <FaChartBar color="var(--ifm-color-primary)" />,
    gradient: 'gradient-4',
    badge: '实时监控',
    metric: '全方位',
    highlights: ['性能监控', '根因定位'],
    description: (
      <>
        系统与应用的实时监控，涵盖性能与业务指标，支持问题根因定位。
      </>
    ),
  },
  {
    title: '日志中心',
    icon: <FaClipboardList color="var(--ifm-color-primary)" />,
    gradient: 'gradient-5',
    badge: '日志管理',
    metric: '海量存储',
    highlights: ['集中采集', '智能检索'],
    description: (
      <>
        集中式日志平台，支持采集、存储、检索与分析，提供查询与可视化能力。
      </>
    ),
  },
  {
    title: '告警中心',
    icon: <FaBell color="var(--ifm-color-primary)" />,
    gradient: 'gradient-6',
    badge: '智能告警',
    metric: '降噪分析',
    highlights: ['智能降噪', '及时响应'],
    description: (
      <>
        灵活的告警引擎，支持多维规则与降噪分析，确保关键问题及时响应。
      </>
    ),
  },
  {
    title: 'Console',
    icon: <FaLaptopCode color="var(--ifm-color-primary)" />,
    gradient: 'gradient-7',
    badge: '控制台',
    metric: '可视化',
    highlights: ['统一操作', '简化流程'],
    description: (
      <>
        统一的可视化控制台，聚合常用操作与管理入口，简化日常运维操作。
      </>
    ),
  },
  {
    title: '系统管理',
    icon: <FaCogs color="var(--ifm-color-primary)" />,
    gradient: 'gradient-8',
    badge: '系统治理',
    metric: '安全管控',
    highlights: ['权限管理', '审计日志'],
    description: (
      <>
        提供用户、权限、组织架构与审计日志等功能，支撑系统治理与安全管控。
      </>
    ),
  },
  {
    title: '运营分析',
    icon: <FaChartLine color="var(--ifm-color-primary)" />,
    gradient: 'gradient-9',
    badge: '数据分析',
    metric: '业务决策',
    highlights: ['趋势分析', '运营优化'],
    description: (
      <>
        支持多维度数据报表与趋势分析，为运维优化和决策提供参考。
      </>
    ),
  },
  {
    title: '节点管理',
    icon: <FaServer color="var(--ifm-color-primary)" />,
    gradient: 'gradient-10',
    badge: '集群管理',
    metric: '生命周期',
    highlights: ['批量操作', '自动运维'],
    description: (
      <>
        支持节点生命周期管理与批量操作，简化集群环境的基础设施管理。
      </>
    ),
  },
  {
    title: 'MLOps',
    icon: <FaBrain color="var(--ifm-color-primary)" />,
    gradient: 'gradient-11',
    badge: '机器学习',
    metric: 'AI运维',
    highlights: ['模型管理', '规模部署'],
    description: (
      <>
        面向运维场景的机器学习平台，覆盖模型训练、部署与监控全流程。
      </>
    ),
  },
  {
    title: 'PlayGround',
    icon: <FaFlask color="var(--ifm-color-primary)" />,
    gradient: 'gradient-12',
    badge: '实验环境',
    metric: '沙箱测试',
    highlights: ['快速验证', '安全实验'],
    description: (
      <>
        在线实验环境，支持快速验证与安全测试新功能。
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
            <div className={styles.iconEmoji}>{icon}</div>
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
