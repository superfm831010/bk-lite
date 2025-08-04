import React, { useState, useEffect, useRef, useMemo } from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { Popover, Spin, Tour } from 'antd';
import { CaretDownFilled } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import useModelExperience from '@/app/playground/hooks/useModelExperience';
import { usePermissions } from '@/context/permissions';
import { useClientData } from '@/context/client';
import { useUserInfoContext } from '@/context/userInfo';
import styles from './index.module.scss';
import type { TourProps } from 'antd';
import { TourItem, MenuItem, ClientData } from '@/types/index';
import UserInfo from '../user-info';
import Icon from '@/components/icon';

const TOUR_VIEWED_KEY_PREFIX = 'tour_viewed';

const TopMenu = () => {
  const { t } = useTranslation();
  const { menus: menuItems } = usePermissions();
  const pathname = usePathname();
  const {
    modelExpList,
    loading: modelExpLoading,
    error: modelExpError,
    reload } = useModelExperience(pathname?.startsWith('/playground'));
  const { clientData, loading } = useClientData();
  const { userId } = useUserInfoContext();
  const [tourOpen, setTourOpen] = useState(false);
  const [tourStep, setTourStep] = useState<TourProps['steps']>([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [hasViewedTour, setHasViewedTour] = useState(false);

  const menuRefs = useRef<{ [key: string]: React.RefObject<HTMLAnchorElement> }>({});

  const isOtherMode = pathname?.startsWith('/playground');

  const getTourViewedKey = () => {
    return `${userId}_${TOUR_VIEWED_KEY_PREFIX}`;
  };

  useEffect(() => {
    menuItems.forEach((item: MenuItem) => {
      if (item.tour && !menuRefs.current[item.url]) {
        menuRefs.current[item.url] = React.createRef();
      }
    });

    if (userId) {
      try {
        const tourViewedKey = getTourViewedKey();
        const viewed = localStorage.getItem(tourViewedKey) === 'true';
        setHasViewedTour(viewed);

        if (!viewed) {
          prepareTourSteps();
        }
      } catch (error) {
        console.warn('Unable to access localStorage:', error);
      }
    }
  }, [menuItems, userId]);

  const prepareTourSteps = () => {
    const tours = menuItems
      .filter((item: MenuItem) => item.tour)
      .map((item: MenuItem) => ({
        menuItem: item,
        tour: item.tour as TourItem
      }))
      .sort((a: { menuItem: MenuItem; tour: TourItem }, b: { menuItem: MenuItem; tour: TourItem }) => a.tour.order - b.tour.order);

    if (tours.length > 0) {
      const steps = tours.map(({ menuItem, tour }: { menuItem: MenuItem; tour: TourItem }) => {
        const step: NonNullable<TourProps['steps']>[0] = {
          title: tour.title,
          description: tour.description,
          target: () => {
            if (tour.target === menuItem.name) {
              const element = menuRefs.current[menuItem.url]?.current;
              return element || document.body;
            }
            const element = document.getElementById(tour.target);
            return element || document.body;
          },
        };

        if (tour.cover) {
          step.cover = (
            <img
              alt={tour.title}
              src={tour.cover}
            />
          );
        }

        if (tour.mask) {
          step.mask = tour.mask;
        }

        return step;
      });

      setTourStep(steps);

      // Show tour automatically if user hasn't viewed it before
      if (!hasViewedTour && steps.length > 0) {
        setTourOpen(true);
      }
    }
  };

  const handleTourChange: TourProps['onChange'] = (current: number) => {
    setCurrentStep(current);
  };

  const handleCloseTour = () => {
    setTourOpen(false);

    if (userId) {
      try {
        const tourViewedKey = getTourViewedKey();
        localStorage.setItem(tourViewedKey, 'true');
        setHasViewedTour(true);
      } catch (error) {
        console.warn('Unable to save tour viewed state to localStorage:', error);
      }
    }
  };

  const handleDocumentClick = () => {
    window.open('https://github.com/TencentBlueKing/bk-lite', '_blank');
  };

  const renderSubMenuPanel = useMemo(() => {
    if (modelExpLoading) return;
    const renderMenu = () => (
      modelExpList?.map((item: any, index: number) => {
        return (
          <div key={`category_${index}`}>
            <h3 className='text-base font-bold mb-4'>{item.name}</h3>
            <div className='flex flex-wrap justify-between'>
              {item?.children && item.children.map((child: any) => {
                return (
                  <div key={`child_${child?.id}`} className='mr-2 mb-4 w-[150px]'>
                    <Link href={child.url} prefetch={false}>
                      <div className={`${styles.menuItem} flex items-center cursor-pointer text-sm`}>
                        <span>{child.name}</span>
                      </div>
                      <p className='truncate text-[--color-text-3] text-sm'>{child.description}</p>
                    </Link>
                  </div>
                )
              })}
            </div>
          </div>
        )
      })
    )

    return (
      <div className='flex max-w-[80vw] ml-6 max-h-[80vh] overflow-y-auto'>
        <div>{renderMenu()}</div>
      </div>
    );
  }, [modelExpList, modelExpLoading, modelExpError, reload]);

  const renderContent = loading ? (
    <div className="flex justify-center items-center h-32">
      <Spin tip="Loading..." />
    </div>
  ) : (
    <div className="grid grid-cols-4 gap-4 max-h-[420px] overflow-auto">
      {clientData.map((app: ClientData) => (
        <div
          key={app.name}
          className={`group flex flex-col items-center p-4 rounded-sm cursor-pointer ${styles.navApp}`}
          onClick={() => window.open(app.url, '_blank')}
        >
          <Icon
            type={app.icon || app.name}
            className="text-2xl mb-1 transition-transform duration-300 transform group-hover:scale-125"
          />
          {app.display_name || app.name}
        </div>
      ))}
    </div>
  );

  return (
    <div className="z-30 flex flex-col grow-0 shrink-0 w-full basis-auto h-[56px] relative">
      <div className="flex items-center justify-between px-4 w-full h-full">
        <div className="flex items-center space-x-2">
          <Image src="/logo-site.png" className="block w-auto h-10" alt="logo" width={100} height={40} />
          <div className="font-medium">BlueKing Lite</div>
          <Popover content={renderContent} title={t('common.appList')} trigger="hover">
            <div className={`flex items-center justify-center cursor-pointer rounded-[10px] px-3 py-2 ${styles.nav}`}>
              <Icon type="caidandaohang" className="mr-1" />
              <CaretDownFilled className={`text-sm ${styles.icons}`} />
            </div>
          </Popover>
        </div>
        <div className="flex items-center flex-shrink-0 space-x-2">
          {hasViewedTour && (
            <div
              className="text-xs flex items-center mr-2 text-[var(--color-text-3)] cursor-pointer hover:text-[var(--color-primary)]"
              onClick={handleDocumentClick}
            >
              <Icon type="shiyongwendang" className="mr-1" />
              {t('common.officialDocument')}
            </div>
          )}
          <UserInfo />
        </div>
      </div>
      <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <div
          className="flex items-center space-x-4 overflow-x-auto"
          style={{ whiteSpace: 'nowrap' }}
        >
          {menuItems
            .filter((item: MenuItem) => item.url && !item.isNotMenuItem)
            .map((item: MenuItem) => {
              const isActive = item.url === '/' ? pathname === '/' : pathname?.startsWith(item.url);

              if (isOtherMode && item.name === 'capabilities') {

                return (
                  <Popover
                    key={item.url}
                    content={renderSubMenuPanel}
                    trigger="hover"
                    placement="bottom"
                    overlayClassName="top-menu-submenu-popover"
                    className='z-40'
                  >
                    <div>
                      <Link
                        href={item.url}
                        prefetch={false} legacyBehavior>
                        <a
                          ref={menuRefs.current[item.url] || null}
                          id={item.name}
                          className={`px-3 py-2 rounded-[10px] flex items-center ${styles.menuCol} ${isActive ? styles.active : ''}`}
                        >
                          <Icon type={item.icon} className="mr-2 w-4 h-4" />
                          {item.title}
                        </a>
                      </Link>
                    </div>
                  </Popover>
                );
              }

              return (
                <Link key={item.url} href={item.url} prefetch={false} legacyBehavior>
                  <a
                    ref={menuRefs.current[item.url] || null}
                    id={item.name}
                    className={`px-3 py-2 rounded-[10px] flex items-center ${styles.menuCol} ${isActive ? styles.active : ''}`}
                  >
                    <Icon type={item.icon} className="mr-2 w-4 h-4" />
                    {item.title}
                  </a>
                </Link>
              );
            })}
        </div>
      </div>
      <Tour
        open={tourOpen}
        onClose={handleCloseTour}
        steps={tourStep}
        current={currentStep}
        onChange={handleTourChange}
      />
    </div>
  );
};

export default TopMenu;
