'use client'
import React, { memo, useMemo } from 'react';
import { useSearchParams } from 'next/navigation';
import { useTranslation } from '@/utils/i18n';
import AnomalyDetail from './AnomalyDetail';
import Icon from '@/components/icon';
import SubLayout from '@/components/sub-layout';

const Intro = memo(({
  folder_name,
  description,
}: {
  folder_name: string;
  description: string;
}) => {
  return (
    <div>
      <div className="flex justify-center items-center w-full">
        <Icon
          type="chakanshuji"
          className="h-16 w-16"
          style={{ height: '36px', width: '36px', color: 'blue' }}
        />
        <h1 className="text-center truncate">{folder_name}</h1>
      </div>
      <p className="text-xs">{description}</p>
    </div>
  )
});
Intro.displayName = 'Intro';

const Topsection = memo(({
  t
}: {
  t: (id: string) => string
}) => {
  return (
    <div className="flex flex-col h-[90px] p-4 overflow-hidden">
      <h1 className="text-lg truncate w-full mb-1">{t('datasets.title')}</h1>
      <p className="text-sm overflow-hidden w-full min-w-[1000px] mt-[8px]">
        {t('datasets.detail')}
      </p>
    </div>
  );
});
Topsection.displayName = 'Topsection';

const Detail = () => {
  const { t } = useTranslation();
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
  }), [activeTap])

  return (
    <>
      <div className='w-full'>
        <SubLayout
          topSection={<Topsection t={t} />}
          intro={<Intro folder_name={folder_name} description={description} />}
          showBackButton={true}
        >
          <div className='w-full relative'>
            {renderPage[activeTap]}
          </div>
        </SubLayout>
      </div>
    </>
  )
};

export default Detail;