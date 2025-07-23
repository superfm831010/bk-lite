'use client';
import React, { useState } from 'react';
// import Link from 'next/link';
import { useTranslation } from '@/utils/i18n';
import {
  // usePathname, 
  useSearchParams,
  useRouter
} from 'next/navigation';
import { Spin, Modal, Menu, Button } from 'antd';
import Icon from '@/components/icon';
import { ArrowLeftOutlined, MenuUnfoldOutlined, MenuFoldOutlined } from '@ant-design/icons';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import {
  // AnomalyTrainData, 
  AsideProps
} from '@/app/mlops/types/manage'
import sideMenuStyle from './index.module.scss';
const { confirm } = Modal;

const Aside = ({
  // children,
  menuItems,
  loading,
  isChange,
  onChange,
  changeFlag }: AsideProps) => {
  // const pathname = usePathname();
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const folder_id = searchParams.get('folder_id') || '';
  const folder_name = searchParams.get('folder_name') || '';
  const description = searchParams.get('description');
  const activeTap = searchParams.get('activeTap');
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);

  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  const buildUrlWithParams = (id: number) => {
    return `?id=${id}&folder_id=${folder_id}&folder_name=${folder_name}&description=${description}&activeTap=${activeTap}`;
  };

  // const isActive = (id: number): boolean => {
  //   if (pathname === null) return false;
  //   return searchParams.get('id') === id.toString();
  // };

  const menuItem = (item: any) => (
    <div className='flex w-[160px] ' onClick={(e) => onClick(e, item)}>
      <Icon type={'yingpan'} className="text-xl pr-1.5" />
      <EllipsisWithTooltip
        text={item.name}
        className={`w-[160px] overflow-hidden text-ellipsis whitespace-nowrap} `}
      />
    </div>
  )

  const renderMenuItems = () => {
    return menuItems.map((item: any) => {
      return {
        key: item.id,
        label: menuItem(item)
        // label:
        //   <Link
        //     href={buildUrlWithParams(item.id)}
        //     className={`group flex w-full items-center overflow-hidden h-9 rounded-md py-2 px-3 ${isActive(item.id) ? `${sideMenuStyle.active} bg-blue-50 text-blue-600` : ''}`}
        //     onClick={(e) => onClick(e, item)}
        //   >

        //   </Link>,
      }
    })
  };

  const goBack = (e: any) => {
    e.preventDefault();
    if (isChange) {
      return confirm({
        title: t('datasets.leave'),
        content: t('datasets.leaveContent'),
        okText: t('common.confirm'),
        cancelText: t('common.cancel'),
        centered: true,
        onOk() {
          return new Promise(async (resolve) => {
            resolve(true);
            onChange(false);
            router.replace(`/mlops/manage/detail?folder_id=${folder_id}&folder_name=${folder_name}&description=${description}&activeTap=${activeTap}`);
          })
        }
      })
    }

    router.replace(`/mlops/manage/detail?folder_id=${folder_id}&folder_name=${folder_name}&description=${description}&activeTap=${activeTap}`);
  };

  const showConfirm = (id: number) => {
    confirm({
      title: t('datasets.leave'),
      content: t('datasets.leaveContent'),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      centered: true,
      onOk() {
        return new Promise(async (resolve) => {
          resolve(true);
          onChange(false);
          changeFlag(true);
          router.push(buildUrlWithParams(id));
        })
      }
    })
  };

  const onClick = async (e: any, item: any) => {
    console.log(item);
    e.preventDefault();
    if (isChange) {
      return showConfirm(item.id)
    }
    changeFlag(true);
    router.push(buildUrlWithParams(item.id));
  };

  return (
    <>
      <aside className={` relative pr-4 flex flex-shrink-0 flex-col h-full ${sideMenuStyle.sideMenu} font-sans`}>
        <button
          className="absolute z-10 top-4 left-0 flex items-center content-center py-2 px-4 rounded-md text-sm font-medium text-gray-600 cursor-pointer hover:text-blue-600"
          onClick={goBack}
        >
          <ArrowLeftOutlined className="mr-2" />
        </button>
        <nav className={`flex-1 pt-[54px] relative rounded-md ${sideMenuStyle.nav}`}>
          {loading ? (
            <div className="min-h-[300px] flex items-center justify-center">
              <Spin spinning={loading}></Spin>
            </div>
          ) : (
            <>

              <Menu
                items={renderMenuItems()}
                inlineCollapsed={collapsed}
              // onClick={({ item, domEvent }) => onClick(domEvent, item)}
              />
              <Button type="primary" onClick={toggleCollapsed} style={{ marginBottom: 16 }} className='absolute left-0 bottom-0'>
                {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              </Button>
            </>
            // <ul className="p-3 overflow-auto max-h-[65vh]">
            //   {menuItems.map((item: any) => (
            //     <li key={item.id} className={`rounded-md mb-1 ${isActive(item.id) ? `${sideMenuStyle.active} bg-blue-50 text-blue-600` : ''}`}>
            //       <Link
            //         href={buildUrlWithParams(item.id)}
            //         className="group flex items-center overflow-hidden h-9 rounded-md py-2 px-3"
            //         onClick={(e) => onClick(e, item)}
            //       >
            //         <Icon type={'yingpan'} className="text-xl pr-1.5" />
            //         <EllipsisWithTooltip
            //           text={item.name}
            //           className={`w-[100px] overflow-hidden text-ellipsis whitespace-nowrap}`}
            //         />
            //       </Link>
            //     </li>
            //   ))}
            // </ul>
          )}

        </nav>
      </aside>
    </>
  )
};

export default Aside;