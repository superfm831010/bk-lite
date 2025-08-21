import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const platformFeatures = [
  {
    icon: '🔒',
    title: '涉密环境支持',
    description: '支持涉密环境部署，提供端到端的安全保障机制，确保敏感数据和关键业务系统的安全运行。',
    badge: '安全可信',
    color: 'purple',
    highlights: ['等保三级', '国密算法', '数据隔离']
  },
  {
    icon: '⚡',
    title: '能耗比高',
    description: '采用轻量化架构设计，优化资源调度算法，在保证性能的同时大幅降低系统能耗。',
    badge: '绿色节能',
    color: 'green',
    highlights: ['50%↓能耗', '智能调度', '绿色运维']
  },
  {
    icon: '💰',
    title: '持有成本低',
    description: '简化部署流程，降低运维复杂度，通过自动化和智能化手段显著减少总体持有成本。',
    badge: '成本优化',
    color: 'blue',
    highlights: ['60%↓成本', '免运维', '按需付费']
  },
  {
    icon: '🚀',
    title: '边缘自治',
    description: '支持边缘环境自主运行，具备断网续航能力，确保边缘节点的独立运维和故障自愈。',
    badge: '边缘计算',
    color: 'orange',
    highlights: ['离线运行', '自动修复', '智能决策']
  },
  {
    icon: '🤖',
    title: 'AI原生设计',
    description: '从底层架构融入AI能力，提供智能运维、故障预测、性能优化等AI驱动的核心功能。',
    badge: 'AI驱动',
    color: 'indigo',
    highlights: ['智能预测', '自动化', 'ML集成']
  },
  {
    icon: '📈',
    title: '无感扩容',
    description: '支持平滑扩展，自动检测负载变化并进行弹性伸缩，用户无需关心底层资源管理。',
    badge: '弹性伸缩',
    color: 'teal',
    highlights: ['自动扩容', '零停机', '负载均衡']
  },
  {
    icon: '🌍',
    title: '国际化',
    description: '支持多语言界面，适配不同地区的合规要求，为企业全球化部署提供完整解决方案。',
    badge: '全球化',
    color: 'cyan',
    highlights: ['多语言', '合规适配', '全球部署']
  },
  {
    icon: '🔗',
    title: '生态化',
    description: '开放的插件体系和API接口，支持第三方系统集成，构建完整的企业数字化生态。',
    badge: '开放生态',
    color: 'pink',
    highlights: ['开放API', '插件系统', '生态集成']
  }
];

function PlatformFeature({icon, title, description, badge, color, highlights}) {
  return (
    <div className={styles.platformFeatureItem}>
      <div className={clsx(styles.platformFeatureCard, styles[color])}>
        <div className={styles.cardHeader}>
          <div className={styles.platformFeatureIcon}>
            <span className={styles.iconEmoji}>{icon}</span>
          </div>
          <div className={styles.cardBadge}>{badge}</div>
        </div>
        
        <div className={styles.platformFeatureContent}>
          <Heading as="h3" className={styles.platformFeatureTitle}>
            {title}
          </Heading>
          <p className={styles.platformFeatureDescription}>
            {description}
          </p>
          
          <div className={styles.highlightsGrid}>
            {highlights.map((highlight, idx) => (
              <div key={idx} className={styles.highlight}>
                <span className={styles.highlightDot}></span>
                <span className={styles.highlightText}>{highlight}</span>
              </div>
            ))}
          </div>
        </div>
        
        <div className={styles.cardGlow}></div>
      </div>
    </div>
  );
}

export default function PlatformShowcase() {
  return (
    <section className={styles.platformShowcase}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <div className={styles.sectionBadge}>
            <span className={styles.badgeIcon}>⭐</span>
            平台核心优势
          </div>
          <Heading as="h2" className={styles.sectionTitle}>
            关键特性
          </Heading>
          <p className={styles.sectionSubtitle}>
            基于企业实际需求打造的八大核心特性，为数字化转型提供全方位支撑
          </p>
        </div>
        
        <div className={styles.platformFeatureGrid}>
          {platformFeatures.map((feature, idx) => (
            <PlatformFeature key={idx} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}