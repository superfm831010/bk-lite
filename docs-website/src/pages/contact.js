import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './contact.module.css';

const ContactMethods = [
  {
    icon: '📧',
    title: '邮件咨询',
    description: '发送详细需求到我们的邮箱',
    contact: 'bklite@tencent.com',
    action: '发送邮件',
  },
  {
    icon: '💬',
    title: '在线客服',
    description: '工作日 9:00-18:00 在线支持',
    contact: '微信客服',
    action: '开始对话',
  },
  {
    icon: '📞',
    title: '电话咨询',
    description: '专业售前顾问为您答疑',
    contact: '400-000-8888',
    action: '立即拨打',
  },
];

const OfficeLocations = [
  {
    city: '深圳总部',
    address: '深圳市南山区科技园腾讯大厦',
    phone: '0755-86013388',
    email: 'shenzhen@tencent.com',
  },
  {
    city: '北京分公司',
    address: '北京市海淀区知春路腾讯北京总部大楼',
    phone: '010-62671188',
    email: 'beijing@tencent.com',
  },
  {
    city: '上海分公司',
    address: '上海市徐汇区宜山路腾讯上海总部大厦',
    phone: '021-61334488',
    email: 'shanghai@tencent.com',
  },
];

function ContactCard({ icon, title, description, contact, action }) {
  return (
    <div className={clsx('col col--4', styles.contactCol)}>
      <div className={styles.contactCard}>
        <div className={styles.contactIcon}>
          <span className={styles.iconEmoji}>{icon}</span>
        </div>
        <div className={styles.contactContent}>
          <h3 className={styles.contactTitle}>{title}</h3>
          <p className={styles.contactDescription}>{description}</p>
          <div className={styles.contactInfo}>
            <strong>{contact}</strong>
          </div>
          <button className={styles.contactButton}>
            {action}
          </button>
        </div>
      </div>
    </div>
  );
}

function OfficeCard({ city, address, phone, email }) {
  return (
    <div className={clsx('col col--4', styles.officeCol)}>
      <div className={styles.officeCard}>
        <h3 className={styles.officeCity}>{city}</h3>
        <div className={styles.officeDetails}>
          <div className={styles.officeDetail}>
            <span className={styles.detailIcon}>📍</span>
            <span className={styles.detailText}>{address}</span>
          </div>
          <div className={styles.officeDetail}>
            <span className={styles.detailIcon}>📞</span>
            <span className={styles.detailText}>{phone}</span>
          </div>
          <div className={styles.officeDetail}>
            <span className={styles.detailIcon}>📧</span>
            <span className={styles.detailText}>{email}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Contact() {
  return (
    <Layout
      title="联系我们"
      description="联系BKLite团队，获取专业的技术支持和商务咨询">
      <main className={styles.contactPage}>
        <header className={styles.contactHeader}>
          <div className="container">
            <div className={styles.headerContent}>
              <Heading as="h1" className={styles.pageTitle}>
                💬 联系我们
              </Heading>
              <p className={styles.pageSubtitle}>
                我们的专业团队随时为您提供技术支持和商务咨询服务
              </p>
            </div>
          </div>
        </header>

        <section className={styles.contactMethodsSection}>
          <div className="container">
            <div className="text--center margin-bottom--xl">
              <Heading as="h2" className={styles.sectionTitle}>
                🚀 多种联系方式
              </Heading>
              <p className={styles.sectionSubtitle}>
                选择最适合您的联系方式，我们将尽快为您提供帮助
              </p>
            </div>
            <div className="row">
              {ContactMethods.map((method, index) => (
                <ContactCard key={index} {...method} />
              ))}
            </div>
          </div>
        </section>

        <section className={styles.formSection}>
          <div className="container">
            <div className={styles.formContainer}>
              <div className={styles.formContent}>
                <Heading as="h2" className={styles.formTitle}>
                  📝 在线咨询
                </Heading>
                <p className={styles.formDescription}>
                  填写下方表单，我们将在24小时内回复您
                </p>
                <form className={styles.contactForm}>
                  <div className={styles.formGroup}>
                    <label className={styles.formLabel}>姓名 *</label>
                    <input 
                      type="text" 
                      className={styles.formInput}
                      placeholder="请输入您的姓名"
                      required
                    />
                  </div>
                  <div className={styles.formGroup}>
                    <label className={styles.formLabel}>邮箱 *</label>
                    <input 
                      type="email" 
                      className={styles.formInput}
                      placeholder="请输入您的邮箱地址"
                      required
                    />
                  </div>
                  <div className={styles.formGroup}>
                    <label className={styles.formLabel}>公司名称</label>
                    <input 
                      type="text" 
                      className={styles.formInput}
                      placeholder="请输入您的公司名称"
                    />
                  </div>
                  <div className={styles.formGroup}>
                    <label className={styles.formLabel}>咨询类型</label>
                    <select className={styles.formSelect}>
                      <option value="">请选择咨询类型</option>
                      <option value="technical">技术支持</option>
                      <option value="sales">商务咨询</option>
                      <option value="partnership">合作伙伴</option>
                      <option value="other">其他</option>
                    </select>
                  </div>
                  <div className={styles.formGroup}>
                    <label className={styles.formLabel}>详细需求 *</label>
                    <textarea 
                      className={styles.formTextarea}
                      placeholder="请详细描述您的需求或问题"
                      rows="5"
                      required
                    ></textarea>
                  </div>
                  <button type="submit" className={styles.submitButton}>
                    🚀 提交咨询
                  </button>
                </form>
              </div>
              <div className={styles.formVisual}>
                <div className={styles.visualCard}>
                  <div className={styles.visualIcon}>
                    <span className={styles.iconEmoji}>🤝</span>
                  </div>
                  <h3 className={styles.visualTitle}>专业服务承诺</h3>
                  <div className={styles.visualFeatures}>
                    <div className={styles.visualFeature}>
                      <span className={styles.featureIcon}>⚡</span>
                      <span>24小时内响应</span>
                    </div>
                    <div className={styles.visualFeature}>
                      <span className={styles.featureIcon}>🎯</span>
                      <span>定制化解决方案</span>
                    </div>
                    <div className={styles.visualFeature}>
                      <span className={styles.featureIcon}>🛡️</span>
                      <span>企业级技术支持</span>
                    </div>
                    <div className={styles.visualFeature}>
                      <span className={styles.featureIcon}>📈</span>
                      <span>业务增长保障</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.officesSection}>
          <div className="container">
            <div className="text--center margin-bottom--xl">
              <Heading as="h2" className={styles.sectionTitle}>
                🏢 办公地点
              </Heading>
              <p className={styles.sectionSubtitle}>
                欢迎到我们的办公室进行面对面交流
              </p>
            </div>
            <div className="row">
              {OfficeLocations.map((office, index) => (
                <OfficeCard key={index} {...office} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
