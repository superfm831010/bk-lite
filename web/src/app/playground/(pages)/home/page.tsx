'use client';
import { useSearchParams, useRouter } from 'next/navigation';
import { Dropdown, Space, Tabs, Divider } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import cssStyle from './index.module.scss';
import { lazy, useMemo, Suspense } from 'react';
import HomePage from './components/HomePage';

const OpenPlatform = () => {
  const searchParams = useSearchParams();
  const router = useRouter();
  const activeComponent = searchParams.get('page');

  const componentMap: Record<string, any> = useMemo(() => ({
    'home': HomePage,
    'anomaly-detection': lazy(() => import(`./components/AnomalyDetection`))
  }), []);

  // 动态获取组件
  const DynamicComponent = useMemo(() => {
    console.log(activeComponent);
    const componentKey = activeComponent || 'home';
    return componentMap[componentKey] || HomePage;
  }, [activeComponent]);

  const items = [
    {
      label: '异常检测',
      key: 'anomaly',
      children: (
        <div className='w-[100%] h-full flex items-start bg-white pt-2'>
          <div className='w-[25%]'>
            <div className={`${cssStyle.capabilities}`}>
              <h4 className='h-6 leading-6 font-bold'>单指标异常检测</h4>
              <Divider className='my-3 border-1.5' />
              <ul className={`${cssStyle.capabilities_list}`}>
                <li className='pl-2 py-1' onClick={() => router.push(`home?page=anomaly-detection`)}>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
              </ul>
            </div>
            <div className='capabilities'>
              <h4 className='h-6 leading-6 font-bold'>单指标异常检测</h4>
              <Divider className='my-2 border-1.5' />
              <ul className={`${cssStyle.capabilities_list}`}>
                <li className='pl-2 py-1'>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
                <li className='pl-2 py-1'>网络异常检测</li>
              </ul>
            </div>
          </div>
        </div>
      )
    }
  ];

  const TopSection = () => (
    <header className='h-12 place-content-center px-3'>
      <Dropdown
        dropdownRender={renderMenu}
      >
        <a onClick={(e) => e.preventDefault()} className='hover:text-blue-600 hover:cursor-pointer h-6 leading-6 font-bold'>
          <Space>
            开放能力
            <DownOutlined />
          </Space>
        </a>
      </Dropdown>
    </header>
  );

  const renderMenu = () => {
    return <Tabs
      tabPosition='left'
      className='w-full'
      style={{ width: `100vw`, height: 400, background: `var(--color-bg)` }}
      items={items}
    />
  };

  return (
    <>
      <div className='flex w-full flex-col bg-[var(--color-bg)]'>
        <div className='header'>
          <TopSection />
        </div>
        <div className='w-full'>
          <Suspense>
            <DynamicComponent />
          </Suspense>
        </div>
      </div>
    </>
  )
};

export default OpenPlatform;