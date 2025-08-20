import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

export default function FinalCTA() {
  return (
    <section className={styles.finalCTA}>
      <div className="container">
        <div className={styles.ctaContainer}>
          <div className={styles.ctaContent}>
            <div className={styles.ctaIcon}>
              <span className={styles.iconEmoji}>🚀</span>
            </div>
            <Heading as="h2" className={styles.ctaTitle}>
              开启您的 AI 驱动数字化转型之旅
            </Heading>
            <p className={styles.ctaDescription}>
              BKLite 为您提供完整的轻量级蓝鲸解决方案，从部署到运维，从监控到自动化，
              让 AI 成为您业务增长的强大引擎。现在就开始，体验下一代智能运维平台的魅力。
            </p>
            <div className={styles.ctaButtons}>
              <Link
                className={clsx(styles.ctaButton, styles.ctaPrimary)}
                to="/docs/intro"
              >
                🎯 免费试用
              </Link>
              <Link
                className={clsx(styles.ctaButton, styles.ctaSecondary)}
                to="https://github.com/TencentBlueKing/bk-lite"
              >
                📖 查看源码
              </Link>
              <Link
                className={clsx(styles.ctaButton, styles.ctaTertiary)}
                to="/contact"
              >
                💬 联系专家
              </Link>
            </div>
            <div className={styles.ctaFeatures}>
              <div className={styles.feature}>
                <span className={styles.featureIcon}>✅</span>
                <span>30天免费试用</span>
              </div>
              <div className={styles.feature}>
                <span className={styles.featureIcon}>⚡</span>
                <span>5分钟快速部署</span>
              </div>
              <div className={styles.feature}>
                <span className={styles.featureIcon}>🛡️</span>
                <span>企业级安全保障</span>
              </div>
            </div>
          </div>
          <div className={styles.ctaVisual}>
            <div className={styles.visualCard}>
              <div className={styles.visualHeader}>
                <div className={styles.dots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className={styles.visualTitle}>BKLite Dashboard</span>
              </div>
              <div className={styles.visualContent}>
                <div className={styles.visualMetric}>
                  <span className={styles.metricLabel}>系统健康度</span>
                  <div className={styles.metricBar}>
                    <div className={clsx(styles.metricFill, styles.success)}></div>
                  </div>
                  <span className={styles.metricValue}>98.5%</span>
                </div>
                <div className={styles.visualMetric}>
                  <span className={styles.metricLabel}>AI 检测精度</span>
                  <div className={styles.metricBar}>
                    <div className={clsx(styles.metricFill, styles.excellent)}></div>
                  </div>
                  <span className={styles.metricValue}>99.2%</span>
                </div>
                <div className={styles.visualMetric}>
                  <span className={styles.metricLabel}>响应时间</span>
                  <div className={styles.metricBar}>
                    <div className={clsx(styles.metricFill, styles.good)}></div>
                  </div>
                  <span className={styles.metricValue}>&lt; 100ms</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
