const isProd = process.env.NODE_ENV === 'production';

const internalHost = process.env.TAURI_DEV_HOST || 'localhost';

/** @type {import('next').NextConfig} */
const nextConfig = {
  // 生产环境使用静态导出
  output: isProd ? 'export' : undefined,

  images: {
    unoptimized: true,
  },

  assetPrefix: isProd ? undefined : `http://${internalHost}:3001`,

  // 开发环境代理配置（生产环境自动忽略）
  async rewrites() {
    // 生产环境（静态导出）不需要 rewrites
    if (isProd) return [];

    const apiTarget = process.env.NEXT_PUBLIC_API_URL || 'https://bklite.canway.net';

    console.log('[Next.js Rewrites] Proxying /dev-proxy/* to', apiTarget);

    return [
      {
        source: '/dev-proxy/:path(.*)',
        destination: `${apiTarget}/:path`,
      },
    ];
  },
};

export default nextConfig;