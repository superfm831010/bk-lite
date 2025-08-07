import React, { useState, useEffect } from 'react';
import { Radio, Button } from 'antd';
import OperateModal from '@/components/operate-modal';
import styles from './index.module.scss';
import { useTranslation } from '@/utils/i18n';
import { SelectOption } from '@/app/opspilot/constants/knowledge';

interface SelectModalProps {
  defaultSelected?: string;
  visible: boolean;
  onCancel: () => void;
  onConfirm: (selectedType: string) => void;
  title: string;
  options: SelectOption[];
}

const SelectModal: React.FC<SelectModalProps> = ({ 
  defaultSelected = '', 
  visible, 
  onCancel, 
  onConfirm, 
  title,
  options 
}) => {
  const [selectedType, setSelectedType] = useState<string>(defaultSelected);
  const { t } = useTranslation();

  useEffect(() => {
    if (visible) {
      const initialSelected = defaultSelected || (options.length > 0 ? options[0].value : '');
      setSelectedType(initialSelected);
    }
  }, [visible, defaultSelected, options]);

  const handleConfirm = () => {
    onConfirm(selectedType);  
  };

  return (
    <OperateModal
      title={title}
      visible={visible}
      onCancel={onCancel}
      footer={[
        <Button key="cancel" onClick={onCancel}>
          {t('common.cancel')}
        </Button>,
        <Button key="confirm" type="primary" onClick={handleConfirm} disabled={!selectedType}>
          {t('common.confirm')}
        </Button>,
      ]}
    >
      <Radio.Group onChange={e => setSelectedType(e.target.value)} value={selectedType}>
        {options.map(option => (
          <Radio
            key={option.value}
            value={option.value}
            className={`${styles['radioItem']} ${selectedType === option.value ? styles['radioItemSelected'] : ''}`}
          >
            <div>
              <h3 className="text-sm">{t(option.title)}</h3>
              <p className="mt-2 text-xs text-[var(--color-text-4)]">{t(option.subTitle)}</p>
            </div>
          </Radio>
        ))}
      </Radio.Group>
    </OperateModal>
  );
};

export default SelectModal;
