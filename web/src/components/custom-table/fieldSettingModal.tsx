import React, { useState, forwardRef, useImperativeHandle } from 'react';
import { Checkbox, Button } from 'antd';
import OperateModal from '@/components/operate-modal';
import { useTranslation } from '@/utils/i18n';
import type { CheckboxProps } from 'antd';
import fieldSettingModalStyle from './index.module.scss';
import { HolderOutlined, CloseOutlined } from '@ant-design/icons';
import { cloneDeep } from 'lodash';
import { ColumnItem, GroupFieldItem } from '@/types/index';

interface DragItem {
  index: number;
  [key: string]: unknown;
}

interface FieldModalProps {
  onConfirm: (fieldKeys: string[]) => void;
  choosableFields: ColumnItem[];
  displayFieldKeys: string[];
  groupFields?: GroupFieldItem[];
}

export interface FieldModalRef {
  showModal: () => void;
}

const FieldSettingModal = forwardRef<FieldModalRef, FieldModalProps>(
  ({ onConfirm, choosableFields, displayFieldKeys, groupFields }, ref) => {
    const { t } = useTranslation();
    const [title, setTitle] = useState<string>('');
    const [visible, setVisible] = useState<boolean>(false);
    const [checkedFields, setCheckedFields] = useState<string[]>(
      choosableFields.map((field) => field.key)
    );
    const [dragFields, setDragFields] = useState<ColumnItem[]>([]);
    const [dragItem, setDragItem] = useState<DragItem | null>(null);
    const [dragOverItem, setDragOverItem] = useState<DragItem | null>(null);
    const checkAll = choosableFields.length === checkedFields.length;
    const indeterminate =
      checkedFields.length > 0 && checkedFields.length < choosableFields.length;

    useImperativeHandle(ref, () => ({
      showModal: () => {
        setTitle(t('cutomTable.fieldSetting'));
        handleCheckboxChange(displayFieldKeys);
        setVisible(true);
      },
    }));

    const onCheckAllChange: CheckboxProps['onChange'] = (e) => {
      setCheckedFields(
        e.target.checked ? choosableFields.map((item) => item.key) : []
      );
      setDragFields(e.target.checked ? choosableFields : []);
    };

    const handleCheckboxChange = (checkedValues: string[]) => {
      setCheckedFields(checkedValues);
      const fields: ColumnItem[] = [];
      checkedValues.forEach((key) => {
        const target = choosableFields.find((field) => field.key === key);
        if (target) {
          fields.push(target);
        }
      });
      setDragFields(fields);
    };

    const clearCheckedItem = (key: string) => {
      const fields = cloneDeep(dragFields);
      const targetIndex = fields.findIndex(
        (item: ColumnItem) => item.key === key
      );
      if (targetIndex !== -1) {
        fields.splice(targetIndex, 1);
        setDragFields(fields);
        setCheckedFields(fields.map((item: ColumnItem) => item.key));
      }
    };

    const handleClear = () => {
      setCheckedFields([]);
    };

    const handleSubmit = () => {
      onConfirm(dragFields.map((item) => item.key));
      handleCancel();
    };

    const handleCancel = () => {
      setVisible(false);
    };

    const handleDragStart = (item: DragItem) => {
      if (!item) return;
      setDragItem(item);
    };

    const handleDragEnter = (item: DragItem) => {
      if (!item) return;
      setDragOverItem(item);
    };

    const handleDragEnd = () => {
      if (dragItem === null || dragOverItem === null) {
        return;
      }
      const newItems = Array.from(dragFields);
      const [draggedItem] = newItems.splice(dragItem.index, 1);
      newItems.splice(dragOverItem.index, 0, draggedItem);
      setDragItem(null);
      setDragOverItem(null);
      setDragFields(newItems);
    };

    const renderCheckBox = (fields: ColumnItem[]) => {
      return fields.map((field) => (
        <Checkbox
          className="w-[166px] mb-[10px]"
          key={field.key}
          value={field.key}
        >
          <span
            title={field.title}
            className={fieldSettingModalStyle.fieldLabel}
          >
            {field.title}
          </span>
        </Checkbox>
      ));
    };

    return (
      <OperateModal
        visible={visible}
        title={title}
        width={600}
        onCancel={handleCancel}
        footer={
          <div>
            <Button
              disabled={!checkedFields.length}
              className="mr-[10px]"
              type="primary"
              onClick={handleSubmit}
            >
              {t('common.confirm')}
            </Button>
            <Button onClick={handleCancel}>{t('common.cancel')}</Button>
          </div>
        }
      >
        <div className={`${fieldSettingModalStyle.settingFields} flex`}>
          <div
            className={`${fieldSettingModalStyle.leftSide} w-2/3 p-4 border-r`}
          >
            <div>
              <Checkbox
                className="mb-[10px]"
                indeterminate={indeterminate}
                onChange={onCheckAllChange}
                checked={checkAll}
              >
                {t('common.selectAll')}
              </Checkbox>
            </div>
            <Checkbox.Group
              value={checkedFields}
              onChange={handleCheckboxChange}
            >
              {groupFields?.length ? (
                groupFields.map((item) => (
                  <div key={item.key}>
                    <div className="font-bold mb-[10px]">{item.title}</div>
                    <div className="flex items-center flex-wrap">
                      {renderCheckBox(item.child)}
                    </div>
                  </div>
                ))
              ) : (
                <div className="flex items-center flex-wrap">
                  {renderCheckBox(choosableFields)}
                </div>
              )}
            </Checkbox.Group>
          </div>
          {/* Right drag list */}
          <div className={`${fieldSettingModalStyle.rightSide} w-1/3 p-4`}>
            <div className="flex justify-between items-center">
              <span>
                {t('common.selected')}(
                <span className="text-[var(--color-text-3)]">
                  {`${checkedFields.length} ${t('common.items')}`}
                </span>
                )
              </span>
              <Button type="link" onClick={handleClear}>
                {t('common.clear')}
              </Button>
            </div>
            <div className="mt-4">
              {dragFields
                .filter((field) => checkedFields.includes(field.key))
                .map((field, index) => (
                  <div
                    className={`p-2 bg-white shadow-sm ${fieldSettingModalStyle.fieldItem}`}
                    key={index}
                    draggable
                    onDragStart={() =>
                      handleDragStart({
                        ...field,
                        index,
                      })
                    }
                    onDragEnter={() =>
                      handleDragEnter({
                        ...field,
                        index,
                      })
                    }
                    onDragEnd={handleDragEnd}
                  >
                    <HolderOutlined
                      className={`mr-[4px] ${fieldSettingModalStyle.dragTrigger}`}
                    />
                    <span
                      className={fieldSettingModalStyle.dragLabel}
                      title={field.title}
                    >
                      {field.title}
                    </span>
                    <CloseOutlined
                      className={fieldSettingModalStyle.clearItem}
                      onClick={() => clearCheckedItem(field.key)}
                    ></CloseOutlined>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </OperateModal>
    );
  }
);
FieldSettingModal.displayName = 'fieldSettingModal';
export default FieldSettingModal;
