import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const AIFeatures = [
  {
    title: '智能运维',
    icon: '🤖',
    description: '基于机器学习的智能故障预测和自动修复',
    gradient: 'ai-gradient-1',
  },
  {
    title: '流程优化',
    icon: '⚡',
    description: 'AI驱动的业务流程分析和优化建议',
    gradient: 'ai-gradient-2',
  },
  {
    title: '智能监控',
    icon: '👁️',
    description: '实时监控异常检测和智能告警推送',
    gradient: 'ai-gradient-3',
  },
  {
    title: '自然语言交互',
    icon: '💬',
    description: '与AI助手对话，用自然语言操作系统',
    gradient: 'ai-gradient-1',
  },
];

function AIFeature({ title, icon, description, gradient }) {
  return (
    <div className={clsx('col col--6', styles.aiFeatureCol)}>
      <div className={clsx(styles.aiFeatureCard, styles[gradient])}>
        <div className={styles.aiFeatureIcon}>
          <span className={styles.iconEmoji}>{icon}</span>
        </div>
        <div className={styles.aiFeatureContent}>
          <Heading as="h3" className={styles.aiFeatureTitle}>
            {title}
          </Heading>
          <p className={styles.aiFeatureDescription}>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function AIShowcase() {
  return (
    <section className={styles.aiShowcase}>
      <div className="container">
        <div className="text--center margin-bottom--xl">
          <Heading as="h2" className={styles.sectionTitle}>
            🧠 AI 驱动的智能化体验
          </Heading>
          <p className={styles.sectionSubtitle}>
            融合最新AI技术，让运维管理更智能、更高效
          </p>
        </div>
        <div className="row">
          {AIFeatures.map((props, idx) => (
            <AIFeature key={idx} {...props} />
          ))}
        </div>
        <div className="text--center margin-top--xl">
          <div className={styles.ctaSection}>
            <Heading as="h3" className={styles.ctaTitle}>
              准备好体验AI的力量了吗？
            </Heading>
            <p className={styles.ctaDescription}>
              立即开始使用BKLite，让AI成为您的最佳运维伙伴
            </p>
            <div className={styles.ctaButtons}>
              <a
                href="/docs/intro"
                className={clsx(styles.ctaButton, styles.ctaPrimary)}
              >
                🚀 立即体验
              </a>
              <a
                href="https://github.com/TencentBlueKing/bk-lite"
                className={clsx(styles.ctaButton, styles.ctaSecondary)}
              >
                📚 查看文档
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
