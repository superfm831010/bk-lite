'use client'
import React, { useMemo } from 'react';
import {
  useSearchParams,
} from 'next/navigation';
import { useTranslation } from '@/utils/i18n';
import AnomalyDetail from './AnomalyDetail';
import RasaDetail from './RasaDetail';
// import PageLayout from '@/components/page-layout';
import Sublayout from '@/components/sub-layout';
import TopSection from '@/components/top-section';
import { MenuItem } from '@/types';


const Detail = () => {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const {
    folder_id,
    folder_name,
    description,
    activeTap,
    menu,
  } = useMemo(() => ({
    folder_id: searchParams.get('folder_id') || '',
    folder_name: searchParams.get('folder_name') || '',
    description: searchParams.get('description') || '',
    activeTap: searchParams.get('activeTap') || '',
    menu: searchParams.get('menu') || '',
  }), [searchParams]);

  const datasetInfo = `folder_id=${folder_id}&folder_name=${folder_name}&description=${description}&activeTap=${activeTap}`;

  const RasaContent = (menu: string) => {
    switch (menu) {
      case 'intent':
        return '用来描述对话流程的关键部分，他相当于对话机器人的"训练样本"，帮助模型学习如何在不同的用户输入下选择正确的动作或回复';
      case 'response':
        return '用来描述对话流程的关键部分，他相当于对话机器人的"训练样本"，帮助模型学习如何在不同的用户输入下选择正确的动作或回复';
      case 'rule':
        return '用来描述对话流程的关键部分，他相当于对话机器人的"训练样本"，帮助模型学习如何在不同的用户输入下选择正确的动作或回复';
      case 'story':
        return '用来描述对话流程的关键部分，他相当于对话机器人的"训练样本"，帮助模型学习如何在不同的用户输入下选择正确的动作或回复';
      case 'entity':
        return '用来描述对话流程的关键部分，他相当于对话机器人的"训练样本"，帮助模型学习如何在不同的用户输入下选择正确的动作或回复';
      case 'slot':
        return '用来描述对话流程的关键部分，他相当于对话机器人的"训练样本"，帮助模型学习如何在不同的用户输入下选择正确的动作或回复';
      default:
        return '';
    }
  };

  const rasaMenus: MenuItem[] = [
    {
      name: 'intent',
      title: t(`datasets.intent`),
      url: `/mlops/manage/detail?${datasetInfo}&menu=intent`,
      icon: 'Gc_103_face-Data',
      operation: []
    },
    {
      name: 'response',
      title: t(`datasets.response`),
      url: `/mlops/manage/detail?${datasetInfo}&menu=response`,
      icon: 'huifu1',
      operation: []
    },
    {
      name: 'rule',
      title: t(`datasets.rule`),
      url: `/mlops/manage/detail?${datasetInfo}&menu=rule`,
      icon: 'guanlianguize',
      operation: []
    },
    {
      name: 'story',
      title: t(`datasets.story`),
      url: `/mlops/manage/detail?${datasetInfo}&menu=story`,
      icon: 'guanlianguize',
      operation: []
    },
    {
      name: 'entity',
      title: t(`datasets.entity`),
      url: `/mlops/manage/detail?${datasetInfo}&menu=entity`,
      icon: 'shiti',
      operation: []
    },
    {
      name: 'slot',
      title: t(`datasets.slot`),
      url: `/mlops/manage/detail?${datasetInfo}&menu=slot`,
      icon: 'bianliang1',
      operation: []
    },
  ];

  const showSideMenu = useMemo(() => {
    return activeTap === 'anomaly' ? false : true;
  }, [activeTap])

  const renderPage: Record<string, React.ReactNode> = useMemo(() => ({
    anomaly: <AnomalyDetail />,
    rasa: <RasaDetail />
  }), [activeTap]);

  const Intro = useMemo(() => (
    <div className="flex h-[58px] flex-col items-center justify-center">
      <h2 className="text-base font-semibold mb-2">{folder_name}</h2>
      <h1 className="text-center">{description}</h1>
    </div>
  ), [folder_name]);

  const topSection = useMemo(() => {
    if (menu) {
      return (
        <TopSection title={t(`datasets.${menu}`)} content={RasaContent(menu)} />
      )
    }
    return <TopSection title={folder_name} content={description} />
  }, [menu]);

  return (
    <>
      <div className='w-full'>
        <Sublayout
          intro={Intro}
          topSection={topSection}
          showSideMenu={showSideMenu}
          activeKeyword
          keywordName='menu'
          customMenuItems={activeTap === 'rasa' ? rasaMenus : []}
          // onBackButtonClick={}
        >
          <div className='w-full relative'>
            {renderPage[activeTap]}
          </div>
        </Sublayout>
      </div>
    </>
  )
};

export default Detail;