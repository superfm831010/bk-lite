import React from 'react';
import { Drawer } from 'antd';
import { useTranslation } from '@/utils/i18n';

interface ContentDrawerProps {
  visible: boolean;
  onClose: () => void;
  content: string;
  title?: string;
}

const ContentDrawer: React.FC<ContentDrawerProps> = ({ visible, onClose, content, title }) => {
  const { t } = useTranslation();

  const formatContent = (text: string) => {
    return text.split('\n').map((line, index) => (
      <React.Fragment key={index}>
        {line}
        {index < text.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  return (
    <Drawer
      title={title || t('common.viewDetails')}
      placement="right"
      onClose={onClose}
      open={visible}
      width={600}
    >
      <div className="whitespace-pre-wrap leading-6">
        {formatContent(content)}
      </div>
    </Drawer>
  );
};

export default ContentDrawer;