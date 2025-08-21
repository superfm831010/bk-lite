// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'BlueKing Lite',
  tagline: 'AI 原生的轻量化蓝鲸平台，重塑智能运维体验',
  favicon: 'img/logo-site.png',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://bklite.tencent.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'TencentBlueKing', // Usually your GitHub org/user name.
  projectName: 'bk-lite', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans', 'en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/TencentBlueKing/bk-lite/tree/main/docs-website/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/TencentBlueKing/bk-lite/tree/main/docs-website/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/bklite-social-card.jpg',
      navbar: {
        title: 'BlueKing Lite',
        logo: {
          alt: 'BKLite Logo',
          src: 'img/logo-site.png',
        },
        items: [
          {
            href: 'https://github.com/TencentBlueKing/bk-lite',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: '产品',
            items: [
              {
                label: '在线体验',
                href: 'https://bklite.canway.net/',
              },
              {
                label: '快速入门',
                to: '/docs/intro',
              },
              {
                label: 'API 文档',
                to: '/docs/tutorial-extras/manage-docs-versions',
              },
            ],
          },
          {
            title: '社区',
            items: [
              {
                label: '腾讯蓝鲸',
                href: 'https://bk.tencent.com/',
              },
              {
                label: '开发者论坛',
                href: 'https://bbs.bk.tencent.com/',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/TencentBlueKing/bk-lite',
              },
            ],
          },
          {
            title: '更多',
            items: [
              {
                label: '博客',
                to: '/blog',
              },
              {
                label: '企业服务',
                href: 'https://cloud.tencent.com/',
              },
              {
                label: '开源协议',
                href: 'https://github.com/TencentBlueKing/bk-lite/blob/main/LICENSE',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} BlueKing Lite.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
