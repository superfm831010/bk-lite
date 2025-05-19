import React from 'react';
import Collapse from '@/components/collapse';
import alertStyle from './index.module.scss';
import { Checkbox, Space } from 'antd';
import { ClearOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { FiltersConfig } from '@/app/alarm/types/monitor';
import { LEVEL_MAP } from '@/app/alarm/constants/monitor';

interface Props {
  filters: FiltersConfig;
  onFilterChange: (vals: string[], field: keyof FiltersConfig) => void;
  clearFilters: (field: keyof FiltersConfig) => void;
}

const AlarmFilters: React.FC<Props> = ({
  filters,
  onFilterChange,
  clearFilters,
}) => {
  const { t } = useTranslation();

  const filterConfigs = [
    {
      field: 'level' as keyof FiltersConfig,
      title: t('monitor.events.level'),
      options: [
        { value: 'critical', label: t('monitor.events.critical') },
        { value: 'error', label: t('monitor.events.error') },
        { value: 'warning', label: t('monitor.events.warning') },
      ],
    },
    {
      field: 'state' as keyof FiltersConfig,
      title: t('monitor.events.state'),
      options: [
        { value: 'pending', label: t('monitor.events.pending') },
        { value: 'processing', label: t('monitor.events.processing') },
        { value: 'unassigned', label: t('monitor.events.unassigned') },
      ],
    },
  ];

  const groupObjects = [
    { label: t('monitor.events.source'), value: 'monitor' },
    { label: t('monitor.logs'), value: 'log' },
  ];

  return (
    <div className={alertStyle.filters}>
      <h3 className="font-[800] mb-[16px] text-[15px]">
        {t('monitor.events.filterItems')}
      </h3>
      <div className={alertStyle.container}>
        {filterConfigs.map(({ field, title, options }) => (
          <div key={field} className={alertStyle.item}>
            <Collapse
              title={
                <div className={alertStyle.header}>
                  <span>{title}</span>
                  <ClearOutlined
                    onClick={(e) => {
                      e.stopPropagation();
                      clearFilters(field);
                    }}
                    className={alertStyle.clearIcon}
                  />
                </div>
              }
            >
              <Checkbox.Group
                className={alertStyle.group}
                value={filters[field]}
                onChange={(vals) => onFilterChange(vals as string[], field)}
              >
                <Space direction="vertical">
                  {options.map(({ value, label }: any) => (
                    <Checkbox key={value} value={value}>
                      {value && LEVEL_MAP[value] && (
                        <span
                          className={alertStyle.levelBar}
                          style={{
                            backgroundColor: `${LEVEL_MAP[value]}`,
                          }}
                        ></span>
                      )}
                      {label}
                    </Checkbox>
                  ))}
                </Space>
              </Checkbox.Group>
            </Collapse>
          </div>
        ))}
        <div className={alertStyle.item}>
          <Collapse
            title={
              <div className={alertStyle.header}>
                <span>{t('monitor.events.source')}</span>
                <ClearOutlined
                  onClick={(e) => {
                    e.stopPropagation();
                    clearFilters('alarm_source');
                  }}
                  className={alertStyle.clearIcon}
                />
              </div>
            }
          >
            <Checkbox.Group
              className={alertStyle.group}
              value={filters.alarm_source}
              onChange={(vals) =>
                onFilterChange(vals as string[], 'alarm_source')
              }
            >
              <Space direction="vertical">
                {groupObjects.map((o) => (
                  <Checkbox key={o.value} value={o.value}>
                    {o.label}
                  </Checkbox>
                ))}
              </Space>
            </Checkbox.Group>
          </Collapse>
        </div>
      </div>
    </div>
  );
};

export default AlarmFilters;
