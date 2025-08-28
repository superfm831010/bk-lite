import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import { FaHelicopter, FaTicketAlt, FaDatabase, FaChartBar, FaClipboardList, FaBell, FaLaptopCode, FaCogs, FaChartLine, FaServer, FaBrain, FaFlask } from 'react-icons/fa';

const FeatureList = [
  {
    title: 'OpsPilot',
    icon: <FaHelicopter color="var(--ifm-color-primary)" />,
    gradient: 'gradient-opspilot',
    badge: '智能运维',
    highlights: ['智能诊断','自主修复'],
    description: (
      <>
       整合诊断、定位与修复能力，助力企业从人工驱动运维模式升级为智能化运维体系
      </>
    ),
  },
  {
    title: '监控中心',
    icon: <FaChartBar color="var(--ifm-color-primary)" />,
    gradient: 'gradient-monitoring',
    badge: '基础监控',
    metric: '全栈覆盖',
    highlights: ['秒级监控', '边缘自治'],
    description: (
      <>
        统一的基础监控能力，支持多环境指标采集与告警，保障系统稳定。
      </>
    ),
  },  
  {
    title: '日志中心',
    icon: <FaClipboardList color="var(--ifm-color-primary)" />,
    gradient: 'gradient-log',
    badge: '日志管理',
    metric: '集中可视',
    highlights: ['统一采集', '快速检索'],
    description: (
      <>
        提供集中化的日志采集与存储，支持高效检索和可视化分析，助力运维故障排查与系统优化。
      </>
    ),
  },
  {
    title: 'CMDB',
    icon: <FaDatabase color="var(--ifm-color-primary)" />,
    gradient: 'gradient-3',
    badge: '配置管理',
    metric: '全局视图',
    highlights: ['自动发现', '关系拓扑'],
    description: (
      <>
        配置管理数据库，支持资源自动发现、动态关系建模与统一管理。
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
    title: '告警中心',
    icon: <FaBell color="var(--ifm-color-primary)" />,
    gradient: 'gradient-6',
    badge: '智能告警',
    metric: '降噪分析',
    highlights: ['多源接入', '灵活分派'],
    description: (
      <>
        统一的告警中心，支持多源事件接入与复杂分析，结合灵活派单机制，确保关键问题高效响应。
      </>
    ),
  },

  {
    title: '运营分析',
    icon: <FaChartLine color="var(--ifm-color-primary)" />,
    gradient: 'gradient-9',
    badge: '数据分析',
    metric: '全局洞察',
    highlights: ['联邦分析', '业务优化'],
    description: (
      <>
        统一使用系统内的各类数据，支持多维报表与趋势洞察，助力运维与业务决策优化。
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
    title: '节点管理',
    icon: <FaServer color="var(--ifm-color-primary)" />,
    gradient: 'gradient-10',
    badge: '集群管理',
    metric: '节点运维',
    highlights: ['进程托管', '探针分发'],
    description: (
      <>
        支持节点探针的生命周期管理与批量操作，简化集群环境的基础设施管理。
      </>
    ),
  },

  {
    title: 'MLOps',
    icon: <FaBrain color="var(--ifm-color-primary)" />,
    gradient: 'gradient-11',
    badge: '机器学习',
    metric: 'AI运维',
    highlights: ['数据管理', '模型训练'],
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
    badge: '体验环境',
    metric: '沙箱测试',
    highlights: ['快速验证', '安全实验'],
    description: (
      <>
        在线体验AI能力的环境，支持快速验证与安全测试新功能。
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
