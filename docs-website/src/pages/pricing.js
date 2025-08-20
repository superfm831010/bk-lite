import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './pricing.module.css';

const PricingPlans = [
  {
    name: '社区版',
    price: '免费',
    period: '永久',
    description: '适合个人开发者和小团队',
    features: [
      '最多 5 个应用',
      '基础监控功能',
      '社区支持',
      '标准 API 限制',
      '基础 AI 功能',
    ],
    buttonText: '立即开始',
    buttonLink: '/docs/intro',
    popular: false,
    gradient: 'community',
  },
  {
    name: '专业版',
    price: '¥299',
    period: '每月',
    description: '适合中小企业和成长团队',
    features: [
      '无限制应用数量',
      '高级监控和告警',
      '优先技术支持',
      '扩展 API 配额',
      '完整 AI 功能',
      '自定义集成',
      '数据备份',
    ],
    buttonText: '免费试用 30 天',
    buttonLink: '/contact',
    popular: true,
    gradient: 'professional',
  },
  {
    name: '企业版',
    price: '定制',
    period: '按需',
    description: '适合大型企业和复杂场景',
    features: [
      '私有化部署',
      '专属客户经理',
      'SLA 保障',
      '定制开发',
      '高级安全功能',
      '多租户支持',
      '企业级集成',
      '现场培训',
    ],
    buttonText: '联系销售',
    buttonLink: '/contact',
    popular: false,
    gradient: 'enterprise',
  },
];

function PricingCard({ name, price, period, description, features, buttonText, buttonLink, popular, gradient }) {
  return (
    <div className={clsx('col col--4', styles.pricingCol)}>
      <div className={clsx(styles.pricingCard, styles[gradient], { [styles.popular]: popular })}>
        {popular && (
          <div className={styles.popularBadge}>
            ⭐ 最受欢迎
          </div>
        )}
        <div className={styles.pricingHeader}>
          <h3 className={styles.planName}>{name}</h3>
          <div className={styles.priceContainer}>
            <span className={styles.price}>{price}</span>
            {period && <span className={styles.period}>/{period}</span>}
          </div>
          <p className={styles.planDescription}>{description}</p>
        </div>
        <div className={styles.pricingFeatures}>
          <ul className={styles.featuresList}>
            {features.map((feature, index) => (
              <li key={index} className={styles.feature}>
                <span className={styles.featureIcon}>✅</span>
                <span className={styles.featureText}>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className={styles.pricingAction}>
          <a
            href={buttonLink}
            className={clsx(styles.pricingButton, styles[`button${gradient}`])}
          >
            {buttonText}
          </a>
        </div>
      </div>
    </div>
  );
}

export default function Pricing() {
  return (
    <Layout
      title="价格方案"
      description="选择适合您的BKLite价格方案，从免费社区版到企业级解决方案">
      <main className={styles.pricingPage}>
        <header className={styles.pricingHeader}>
          <div className="container">
            <div className={styles.headerContent}>
              <Heading as="h1" className={styles.pageTitle}>
                💰 选择适合您的方案
              </Heading>
              <p className={styles.pageSubtitle}>
                从免费开始，随业务增长升级。无隐藏费用，随时可取消。
              </p>
            </div>
          </div>
        </header>
        
        <section className={styles.pricingSection}>
          <div className="container">
            <div className="row">
              {PricingPlans.map((plan, index) => (
                <PricingCard key={index} {...plan} />
              ))}
            </div>
          </div>
        </section>

        <section className={styles.faqSection}>
          <div className="container">
            <div className="text--center margin-bottom--xl">
              <Heading as="h2" className={styles.faqTitle}>
                🤔 常见问题
              </Heading>
            </div>
            <div className={styles.faqGrid}>
              <div className={styles.faqItem}>
                <h3 className={styles.faqQuestion}>可以随时升级或降级吗？</h3>
                <p className={styles.faqAnswer}>
                  当然可以！您可以随时根据业务需要升级或降级您的方案，费用按比例计算。
                </p>
              </div>
              <div className={styles.faqItem}>
                <h3 className={styles.faqQuestion}>支持哪些付款方式？</h3>
                <p className={styles.faqAnswer}>
                  我们支持支付宝、微信支付、银行转账等多种付款方式，企业客户可申请月结。
                </p>
              </div>
              <div className={styles.faqItem}>
                <h3 className={styles.faqQuestion}>数据安全如何保障？</h3>
                <p className={styles.faqAnswer}>
                  我们采用企业级安全措施，包括数据加密、访问控制、定期备份等，确保您的数据安全。
                </p>
              </div>
              <div className={styles.faqItem}>
                <h3 className={styles.faqQuestion}>是否提供技术支持？</h3>
                <p className={styles.faqAnswer}>
                  专业版和企业版用户享有优先技术支持，企业版还配备专属客户经理。
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
