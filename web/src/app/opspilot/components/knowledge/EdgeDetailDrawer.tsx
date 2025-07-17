import React from 'react';
import { Drawer, Typography, Button, message } from 'antd';
import { CopyOutlined } from '@ant-design/icons';
import { useTranslation } from '@/utils/i18n';

const { Text } = Typography;

interface EdgeDetailDrawerProps {
  visible: boolean;
  edge: {
    fact: string;
    label: string;
    source_name: string;
    target_name: string;
  } | null;
  onClose: () => void;
}

const EdgeDetailDrawer: React.FC<EdgeDetailDrawerProps> = ({ visible, edge, onClose }) => {
  const { t } = useTranslation();

  const copyToClipboard = async (value: string) => {
    if (!value || value === '-') {
      message.warning(t('common.noContentToCopy'));
      return;
    }

    try {
      await navigator.clipboard.writeText(value);
      message.success(t('common.copySuccess'));
    } catch (error) {
      console.error('Copy to clipboard failed:', error);
      message.error(t('common.copyFailed'));
    }
  };

  const renderFieldRow = (label: string, value: string | undefined | null, index: number) => {
    const displayValue = value || '-';
    const isEmpty = !value;
    const isEven = index % 2 === 0;

    return (
      <div
        key={label}
        className={`flex items-center justify-between py-2 px-6 transition-all duration-200 hover:bg-blue-50 ${
          isEven ? 'bg-gray-50' : 'bg-white'
        }`}
      >
        <div className="flex items-center space-x-6 flex-1 min-w-0">
          <div className="w-24 flex-shrink-0">
            <Text className="text-xs font-semibold text-gray-700">{label}</Text>
          </div>
          <div className="flex-1 min-w-0">
            <Text
              className={`text-xs ${isEmpty ? 'text-gray-400 italic' : 'text-gray-900'}`}
              style={{ wordBreak: 'break-word', overflowWrap: 'break-word', lineHeight: '1.0' }}
            >
              {displayValue}
            </Text>
          </div>
        </div>
        <div className="flex-shrink-0 ml-4">
          <Button
            type="text"
            size="small"
            icon={<CopyOutlined />}
            onClick={() => copyToClipboard(displayValue)}
            title={t('common.copy')}
            className={`${isEmpty ? 'cursor-not-allowed text-gray-300' : 'text-blue-500 hover:text-blue-700 hover:bg-blue-100'} border-0 shadow-none transition-all duration-200`}
            disabled={isEmpty}
            style={{ minWidth: '32px', height: '32px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          />
        </div>
      </div>
    );
  };

  return (
    <Drawer
      title="Relationship Property"
      open={visible}
      onClose={onClose}
      width={680}
      placement="right"
    >
      {edge && (
        <div className="bg-white rounded-md">
          <div className="border-t-0">
            {[
              { label: 'fact', value: edge.fact },
              { label: 'relationType', value: edge.label },
              { label: 'sourceName', value: edge.source_name },
              { label: 'targetName', value: edge.target_name }
            ].map((field, index) => renderFieldRow(field.label, field.value, index))}
          </div>
        </div>
      )}
    </Drawer>
  );
};

export default EdgeDetailDrawer;