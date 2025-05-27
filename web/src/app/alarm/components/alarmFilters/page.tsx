import React from 'react';
import Collapse from '@/components/collapse';
import alertStyle from './index.module.scss';
import { Checkbox, Space } from 'antd';
import { ClearOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';
import { FiltersConfig } from '@/app/alarm/types/alarms';
import { LEVEL_MAP } from '@/app/alarm/constants/monitor';

interface Props {
  filters: FiltersConfig;
  filterSource?: boolean;
  stateOptions: { value: string; label: string }[];
  onFilterChange: (vals: string[], field: keyof FiltersConfig) => void;
  clearFilters: (field: keyof FiltersConfig) => void;
}

const AlarmFilters: React.FC<Props> = ({
  filters,
  filterSource = true,
  stateOptions,
  onFilterChange,
  clearFilters,
}) => {
  const { t } = useTranslation();

  const filterConfigs = [
    {
      field: 'level' as keyof FiltersConfig,
      title: t('alarms.level'),
      options: [
        { value: 'critical', label: t('alarms.critical') },
        { value: 'error', label: t('alarms.error') },
        { value: 'warning', label: t('alarms.warning') },
      ],
    },
    {
      field: 'state' as keyof FiltersConfig,
      title: t('alarms.state'),
      options: stateOptions,
    },
  ];

  const groupObjects = [
    { label: t('alarms.monitor'), value: 'monitor' },
    { label: t('alarms.logs'), value: 'log' },
  ];

  return (
    <div className={alertStyle.filters}>
      <h3 className="font-[800] mb-[16px] text-[15px]">
        {t('alarms.filterItems')}
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
        {filterSource && (
          <div className={alertStyle.item}>
            <Collapse
              title={
                <div className={alertStyle.header}>
                  <span>{t('alarms.source')}</span>
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
        )}
      </div>
    </div>
  );
};

export default AlarmFilters;
