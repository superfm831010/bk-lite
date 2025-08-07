'use client';
import { useSearchParams } from 'next/navigation';
// import { Dropdown, Space, Tabs, Divider } from 'antd';
// import { DownOutlined } from '@ant-design/icons';
// import cssStyle from './index.module.scss';
import { lazy, useMemo, Suspense } from 'react';
import HomePage from './components/HomePage';

const OpenPlatform = () => {
  const searchParams = useSearchParams();
  // const router = useRouter();
  const activeComponent = searchParams.get('page');
  const componentMap: Record<string, any> = useMemo(() => ({
    'home': HomePage,
    'anomaly-detection': lazy(() => import(`./components/AnomalyDetection`))
  }), []);

  // 动态获取组件
  const DynamicComponent = useMemo(() => {
    const componentKey = activeComponent || 'anomaly-detection';
    return componentMap[componentKey] || HomePage;
  }, [activeComponent]);


  return (
    <>
      <div className='flex w-full flex-col bg-[var(--color-bg)]'>
        {/* <div className='header'>
          <TopSection />
        </div> */}
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