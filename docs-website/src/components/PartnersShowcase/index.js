import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const Partners = [
  {
    name: '腾讯云',
    logo: '☁️',
    description: '云计算服务提供商',
  },
  {
    name: '微信',
    logo: '💬',
    description: '社交平台集成',
  },
  {
    name: '企业微信',
    logo: '🏢',
    description: '企业通讯解决方案',
  },
  {
    name: '钉钉',
    logo: '📌',
    description: '办公协作平台',
  },
  {
    name: '飞书',
    logo: '🚀',
    description: '团队协作工具',
  },
  {
    name: 'Kubernetes',
    logo: '⚓',
    description: '容器编排平台',
  },
];

const Stats = [
  {
    number: '100+',
    label: '企业客户',
    icon: '🏢',
  },
  {
    number: '1M+',
    label: '日活用户',
    icon: '👥',
  },
  {
    number: '99.9%',
    label: '系统稳定性',
    icon: '⚡',
  },
  {
    number: '24/7',
    label: '技术支持',
    icon: '🛠️',
  },
];

function PartnerCard({ name, logo, description }) {
  return (
    <div className={styles.partnerCard}>
      <div className={styles.partnerLogo}>
        <span className={styles.logoEmoji}>{logo}</span>
      </div>
      <div className={styles.partnerInfo}>
        <h4 className={styles.partnerName}>{name}</h4>
        <p className={styles.partnerDescription}>{description}</p>
      </div>
    </div>
  );
}

function StatCard({ number, label, icon }) {
  return (
    <div className={clsx('col col--3', styles.statCol)}>
      <div className={styles.statCard}>
        <div className={styles.statIcon}>
          <span className={styles.iconEmoji}>{icon}</span>
        </div>
        <div className={styles.statNumber}>{number}</div>
        <div className={styles.statLabel}>{label}</div>
      </div>
    </div>
  );
}

export default function PartnersShowcase() {
  return (
    <section className={styles.partnersSection}>
      <div className="container">
        {/* Statistics Section */}
        <div className={styles.statsSection}>
          <div className="text--center margin-bottom--xl">
            <Heading as="h2" className={styles.sectionTitle}>
              📊 值得信赖的选择
            </Heading>
            <p className={styles.sectionSubtitle}>
              全球众多知名企业选择BKLite构建AI驱动的数字化平台
            </p>
          </div>
          <div className="row">
            {Stats.map((props, idx) => (
              <StatCard key={idx} {...props} />
            ))}
          </div>
        </div>

        {/* Partners Section */}
        <div className={styles.partnersGrid}>
          <div className="text--center margin-bottom--xl">
            <Heading as="h3" className={styles.partnersTitle}>
              🤝 生态合作伙伴
            </Heading>
            <p className={styles.partnersSubtitle}>
              与行业领先平台深度集成，构建开放生态
            </p>
          </div>
          <div className={styles.partnersList}>
            {Partners.map((props, idx) => (
              <PartnerCard key={idx} {...props} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
