import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import AIShowcase from '@site/src/components/AIShowcase';
import PartnersShowcase from '@site/src/components/PartnersShowcase';
import FinalCTA from '@site/src/components/FinalCTA';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroContent}>
        <Heading as="h1" className={styles.heroTitle}>
          {siteConfig.title}
        </Heading>
        <p className={styles.heroSubtitle}>
          下一代轻量级蓝鲸平台，融合AI技术，让企业数字化转型更简单
        </p>
        <div className={styles.buttons}>
          <Link
            className={clsx(styles.button, styles['button--primary'])}
            to="/docs/intro">
            🚀 立即开始
          </Link>
          <Link
            className={clsx(styles.button, styles['button--secondary'])}
            to="https://github.com/TencentBlueKing/bk-lite">
            ⭐ GitHub 源码
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} - 轻量级蓝鲸平台`}
      description="BKLite是下一代轻量级蓝鲸平台，融合AI技术，为企业提供简单高效的数字化转型解决方案">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <AIShowcase />
        <PartnersShowcase />
        <FinalCTA />
      </main>
    </Layout>
  );
}
