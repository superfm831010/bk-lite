import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import PlatformShowcase from '@site/src/components/AIShowcase';
import PartnersShowcase from '@site/src/components/PartnersShowcase';
import FinalCTA from '@site/src/components/FinalCTA';
import LiquidNavbar from '@site/src/components/LiquidNavbar';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroBackground}>
        <div className={styles.floatingShapes}>
          <div className={styles.shape1}></div>
          <div className={styles.shape2}></div>
          <div className={styles.shape3}></div>
        </div>
      </div>
      <div className={styles.heroContent}>
        <div className={styles.heroAnimation}>
          <div className={styles.heroTitleAccent}>BlueKing Lite</div>
          <p className={styles.heroSubtitle}>
            AI 原生的轻量化蓝鲸平台，重塑智能运维体验
          </p>
          <div className={styles.heroStats}>
            <div className={styles.statCard}>
              <div className={styles.statValue}>AI原生</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>渐进式体验</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>轻量化架构</div>
            </div>
          </div>
          <div className={styles.buttons}>
            <Link
                className={clsx(styles.button, styles['button--primary'])}
                to="https://bklite.canway.net/">
                <span className={styles.buttonIcon}>⚡</span>
                在线体验
                <span className={styles.buttonArrow}>→</span>
              </Link>
              <Link
                className={clsx(styles.button, styles['button--secondary'])}
                to="/docs/tutorial-basics/create-a-document">
                <span className={styles.buttonIcon}>📖</span>
                快速入门
              </Link>
          </div>
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
      <LiquidNavbar />
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <PlatformShowcase />
        <PartnersShowcase />
        <FinalCTA />
      </main>
    </Layout>
  );
}
