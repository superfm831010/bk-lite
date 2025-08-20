import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '🤖 AI 智能化',
    icon: '🧠',
    description: (
      <>
        集成先进的AI技术，智能分析业务流程，自动优化运维策略，
        让人工智能成为您的数字化转型助手。
      </>
    ),
  },
  {
    title: '⚡ 轻量级架构',
    icon: '🚀',
    description: (
      <>
        采用云原生架构设计，资源占用少，部署简单，
        让中小企业也能轻松享受蓝鲸平台的强大能力。
      </>
    ),
  },
  {
    title: '🔧 可视化编排',
    icon: '🎯',
    description: (
      <>
        拖拽式工作流设计，无需编程基础，业务人员也能快速构建
        自动化流程，提升工作效率。
      </>
    ),
  },
  {
    title: '🔗 开放生态',
    icon: '🌐',
    description: (
      <>
        提供丰富的API接口和插件机制，轻松集成第三方系统，
        构建开放的企业级应用生态。
      </>
    ),
  },
  {
    title: '📊 实时监控',
    icon: '📈',
    description: (
      <>
        全方位的系统监控和业务指标分析，智能告警机制，
        让运维管理更加精准高效。
      </>
    ),
  },
  {
    title: '🛡️ 安全可靠',
    icon: '🔒',
    description: (
      <>
        企业级安全架构，多层防护体系，数据加密传输，
        保障您的业务数据安全无忧。
      </>
    ),
  },
];

function Feature({icon, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className={styles.featureIcon}>
          <span className={styles.iconEmoji}>{icon}</span>
        </div>
        <div className="text--center padding-horiz--md">
          <Heading as="h3" className={styles.featureTitle}>
            {title}
          </Heading>
          <p className={styles.featureDescription}>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="text--center margin-bottom--xl">
          <Heading as="h2" className={styles.sectionTitle}>
            🌟 为什么选择 BKLite？
          </Heading>
          <p className={styles.sectionSubtitle}>
            融合AI技术的下一代轻量级蓝鲸平台，让企业数字化转型更简单
          </p>
        </div>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
