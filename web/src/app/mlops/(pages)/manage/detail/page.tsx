'use client'
import React, { useMemo } from 'react';
import { 
  useSearchParams, 
} from 'next/navigation';
import AnomalyDetail from './AnomalyDetail';
import PageLayout from '@/components/page-layout';
import TopSection from '@/components/top-section';


const Detail = () => {
  const searchParams = useSearchParams();
  const {
    folder_name,
    description,
    activeTap,
  } = useMemo(() => ({
    folder_name: searchParams.get('folder_name') || '',
    description: searchParams.get('description') || '',
    activeTap: searchParams.get('activeTap') || '',
  }), [searchParams]);

  const renderPage: Record<string, React.ReactNode> = useMemo(() => ({
    anomaly: <AnomalyDetail />
  }), [activeTap]);

  return (
    <>
      <div className='w-full'>
        <PageLayout
          topSection={<TopSection title={folder_name} content={description} />}
          rightSection={
            <div className='w-full relative'>
              {renderPage[activeTap]}
            </div>
          }
        />
      </div>
    </>
  )
};

export default Detail;