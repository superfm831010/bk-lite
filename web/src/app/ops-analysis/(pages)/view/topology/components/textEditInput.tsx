import React from 'react';
import { useTranslation } from '@/utils/i18n';
import { TextEditInputProps } from '@/app/ops-analysis/types/topology';

const TextEditInput: React.FC<TextEditInputProps> = ({
  isEditingText,
  editPosition,
  inputWidth,
  tempTextInput,
  setTempTextInput,
  finishTextEdit,
  cancelTextEdit,
}) => {
  const { t } = useTranslation();

  if (!isEditingText) return null;

  return (
    <div
      className="absolute z-50 bg-[var(--color-bg-1)] border border-gray-300 rounded px-2 py-1 shadow-lg"
      style={{
        left: `${editPosition.x}px`,
        top: `${editPosition.y}px`,
        transform: 'translate(-50%, -50%)',
        width: `${inputWidth}px`,
        minWidth: '120px',
      }}
    >
      <input
        type="text"
        value={tempTextInput}
        onChange={(e) => setTempTextInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            finishTextEdit();
          } else if (e.key === 'Escape') {
            cancelTextEdit();
          }
        }}
        onBlur={finishTextEdit}
        onFocus={(e) => e.target.select()}
        autoFocus
        className="w-full outline-none text-sm"
        placeholder={t('common.inputTip')}
      />
    </div>
  );
};

export default TextEditInput;
