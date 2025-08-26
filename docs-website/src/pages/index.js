import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import PlatformShowcase from '@site/src/components/AIShowcase';
import PartnersShowcase from '@site/src/components/PartnersShowcase';
import FinalCTA from '@site/src/components/FinalCTA';
import LiquidNavbar from '@site/src/components/LiquidNavbar';
import React, { useState } from 'react';
import confetti from 'canvas-confetti';
import styles from './index.module.css';

function HomepageHeader() {
  // 基础炮台效果
  const basicCannon = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  // 随机方向效果
  const randomDirection = () => {
    function randomInRange(min, max) {
      return Math.random() * (max - min) + min;
    }

    confetti({
      angle: randomInRange(55, 125),
      spread: randomInRange(50, 70),
      particleCount: randomInRange(50, 100),
      origin: { y: 0.6 }
    });
  };

  // 逼真效果
  const realisticLook = () => {
    const count = 200;
    const defaults = {
      origin: { y: 0.7 }
    };

    function fire(particleRatio, opts) {
      confetti({
        ...defaults,
        ...opts,
        particleCount: Math.floor(count * particleRatio)
      });
    }

    fire(0.25, {
      spread: 26,
      startVelocity: 55,
    });

    fire(0.2, {
      spread: 60,
    });

    fire(0.35, {
      spread: 100,
      decay: 0.91,
      scalar: 0.8
    });

    fire(0.1, {
      spread: 120,
      startVelocity: 25,
      decay: 0.92,
      scalar: 1.2
    });

    fire(0.1, {
      spread: 120,
      startVelocity: 45,
    });
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText('curl -sSL https://bklite.ai/install.run| bash -');
      
      // 随机选择一种撒花效果
      const effects = [basicCannon, randomDirection, realisticLook];
      const randomEffect = effects[Math.floor(Math.random() * effects.length)];
      randomEffect();
      
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

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
            AI 原生的轻量化运维平台，重塑智能运维体验
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
          <div className={styles.quickInstall}>
            <div className={styles.codeBlock}>
              <div className={styles.codeContentWrapper}>
                <pre className={styles.codeContent}>
                  <code>curl -sSL https://bklite.ai/install.run| bash -</code>
                </pre>
                <button 
                  className={styles.copyButton}
                  onClick={handleCopy}
                  title="复制脚本"
                >
                  <span className={styles.copyIcon}>
                    📋
                  </span>
                </button>
              </div>
            </div>
          </div>
          <div className={styles.buttons}>
            <Link
                className={clsx(styles.button, styles['button--primary'])}
                to="https://bklite.canway.net/">
                <span className={styles.buttonIcon}>🚀</span>
                在线体验
                <span className={styles.buttonArrow}>▶</span>
              </Link>
              <Link
                className={clsx(styles.button, styles['button--secondary'])}
                to="/docs/deploy/docker-compose">
                <span className={styles.buttonIcon}>📦</span>
                部署指南
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
      title={`${siteConfig.title} - 轻量级运维平台`}
      description="">
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
