'use client';
import React from 'react';
import Link from 'next/link';
import { useTranslation } from '@/utils/i18n';
import { usePathname, useSearchParams, useRouter } from 'next/navigation';
import { Spin, Modal } from 'antd';
import Icon from '@/components/icon';
import { ArrowLeftOutlined } from '@ant-design/icons';
import EllipsisWithTooltip from '@/components/ellipsis-with-tooltip';
import { AnomalyTrainData } from '@/app/mlops/types';
import sideMenuStyle from './index.module.scss';
const { confirm } = Modal;

const Aside = ({ children, menuItems, loading, isChange, onChange, changeFlag }: { children: any, menuItems: AnomalyTrainData[], loading: boolean, isChange: boolean, onChange: (value: boolean) => void, changeFlag: (value: boolean) => void }) => {
  const pathname = usePathname();
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const folder_id = searchParams.get('folder_id') || '';
  const folder_name = searchParams.get('folder_name') || '';
  const description = searchParams.get('description');
  const activeTap = searchParams.get('activeTap');
  const router = useRouter();

  const buildUrlWithParams = (id: number) => {
    return `?id=${id}&folder_id=${folder_id}&folder_name=${folder_name}&description=${description}&activeTap=${activeTap}`;
  };

  const isActive = (id: number): boolean => {
    if (pathname === null) return false;
    return searchParams.get('id') === id.toString();
  };

  const goBack = (e: any) => {
    e.preventDefault();
    if (isChange) {
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
            router.replace(`/mlops/manage/detail?folder_id=${folder_id}&folder_name=${folder_name}&description=${description}&activeTap=${activeTap}`);
          })
        }
      })
    } else {
      router.replace(`/mlops/manage/detail?folder_id=${folder_id}&folder_name=${folder_name}&description=${description}&activeTap=${activeTap}`);
    }
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

  return (
    <>
      <aside className={`w-[216px] pr-4 flex flex-shrink-0 flex-col h-full ${sideMenuStyle.sideMenu} font-sans`}>
        <div className={`p-4 rounded-md mb-3 h-[80px] ${sideMenuStyle.introduction}`}>
          {children}
        </div>
        <nav className={`flex-1 relative rounded-md ${sideMenuStyle.nav}`}>
          {loading ? (
            <div className="min-h-[300px] flex items-center justify-center">
              <Spin spinning={loading}></Spin>
            </div>
          ) : (
            <ul className="p-3 overflow-auto max-h-[65vh]">
              {menuItems.map((item: any) => (
                <li key={item.id} className={`rounded-md mb-1 ${isActive(item.id) ? `${sideMenuStyle.active} bg-blue-50 text-blue-600` : '' }`}>
                  <Link
                    href={buildUrlWithParams(item.id)}
                    className="group flex items-center overflow-hidden h-9 rounded-md py-2 px-3"
                    onClick={async (e) => {
                      e.preventDefault();
                      if (isChange) {
                        showConfirm(item.id)
                      } else {
                        changeFlag(true);
                        router.push(buildUrlWithParams(item.id));
                      }
                    }}
                  >
                    <Icon type={'chakanshuji'} className="text-xl pr-1.5" />
                    <EllipsisWithTooltip
                      text={item.name}
                      className={`w-[100px] overflow-hidden text-ellipsis whitespace-nowrap}`}
                    />
                  </Link>
                </li>
              ))}
            </ul>
          )}
          <button
            className="absolute bottom-4 left-4 flex items-center content-center py-2 px-4 rounded-md text-sm font-medium text-gray-600 cursor-pointer hover:text-blue-600"
            onClick={goBack}
          >
            <ArrowLeftOutlined className="mr-2" />
          </button>
        </nav>
      </aside>
    </>
  )
};

export default Aside;