import React from 'react';
import MatchRule from './matchRule';
import EffectiveTime from './effectiveTime';
import { useCommon } from '@/app/alarm/context/common';
import { useTranslation } from '@/utils/i18n';
import { CaretRightOutlined } from '@ant-design/icons';
import {
  Tag,
  Form,
  Input,
  Select,
  Checkbox,
  Button,
  Drawer,
  Radio,
  Collapse,
  InputNumber,
} from 'antd';

interface OperateModalProps {
  open: boolean;
  currentRow?: any;
  onClose: () => void;
}

const OperateModalPage: React.FC<OperateModalProps> = ({
  open,
  currentRow,
  onClose,
}) => {
  const { t } = useTranslation();
  const { levelList, levelMap } = useCommon();
  const personnelOptions = [
    { label: 'Alice', value: 'alice' },
    { label: 'Bob', value: 'bob' },
  ];
  const notifyOptions = [
    { label: '邮件', value: 'email' },
    { label: '微信', value: 'wechat' },
  ];
  const [form] = Form.useForm();
  const ruleType = Form.useWatch('matchingRules', form);

  const onFinish = (values: any) => {
    console.log('提交数据：', values, currentRow);
    onClose();
  };
  return (
    <Drawer
      title={
        currentRow
          ? t('settings.assignStrategy.editTitle')
          : t('settings.assignStrategy.addTitle')
      }
      placement="right"
      width={720}
      open={open}
      onClose={onClose}
      footer={
        <div style={{ textAlign: 'right' }}>
          <Button type="primary" onClick={() => form.submit()}>
            {t('settings.assignStrategy.submit')}
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={onClose}>
            {t('common.cancel')}
          </Button>
        </div>
      }
    >
      <Form
        form={form}
        layout="horizontal"
        labelCol={{ span: 4 }}
        onFinish={onFinish}
      >
        <Form.Item
          name="name"
          label={t('settings.assignStrategy.formName')}
          rules={[
            {
              required: true,
              message: t('common.inputMsg'),
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          initialValue="ALL"
          name="matchingRules"
          label={t('settings.assignStrategy.formMatchingRules')}
          rules={[
            {
              required: true,
              message: t('common.inputMsg'),
            },
          ]}
        >
          <Radio.Group className="mt-1 ml-4">
            <Radio value="ALL">{t('settings.assignStrategy.ruleAll')}</Radio>
            <Radio value="Filter">
              {t('settings.assignStrategy.ruleFilter')}
            </Radio>
          </Radio.Group>
        </Form.Item>

        {ruleType === 'Filter' && (
          <Form.Item style={{ marginLeft: '94px', marginTop: '-10px' }}>
            <MatchRule />
          </Form.Item>
        )}

        <Form.Item
          name="personnel"
          label={t('settings.assignStrategy.formPersonnelSelect')}
          rules={[
            {
              required: true,
              message: t('common.selectMsg'),
            },
          ]}
        >
          <Select
            mode="multiple"
            options={personnelOptions}
            placeholder={`${t('common.selectMsg')}`}
          />
        </Form.Item>
        <Form.Item
          name="notifyMethods"
          label={t('settings.assignStrategy.formNotifyMethod')}
          rules={[
            {
              required: true,
              message: t('common.selectMsg'),
            },
          ]}
        >
          <Checkbox.Group options={notifyOptions} />
        </Form.Item>
        <Collapse
          ghost
          expandIcon={({ isActive }) => (
            <CaretRightOutlined
              rotate={isActive ? 90 : 0}
              className="text-base"
            />
          )}
        >
          <Collapse.Panel
            header={
              <div className="flex items-center text-base font-bold">
                {t('common.advanced')}
              </div>
            }
            key="advanced"
          >
            <Form.Item
              name="effectiveTime"
              label={t('settings.assignStrategy.effectiveTime')}
              rules={[
                {
                  required: true,
                  message: t('common.selectMsg'),
                },
              ]}
            >
              <EffectiveTime />
            </Form.Item>
            <Form.Item
              name="notificationScenario"
              label={t('settings.assignStrategy.notificationScenario')}
            >
              <Checkbox.Group
                options={[
                  {
                    label: t('settings.assignStrategy.assignment'),
                    value: 'assignment',
                  },
                  {
                    label: t('settings.assignStrategy.recovery'),
                    value: 'recovery',
                  },
                ]}
              />
            </Form.Item>
            <Form.Item
              name="notificationFrequency"
              label={t('settings.assignStrategy.notificationFrequency')}
            >
              <div className="mt-[5px]">
                {t('settings.assignStrategy.frequencyMsg')}
              </div>
              <div className="flex flex-row align-center gap-2 mt-2">
                <span className="mt-[4px]">
                  {t('settings.assignStrategy.notRespondMsg')}
                </span>
                <div className="flex flex-col">
                  {levelList.map(({ level_display_name, level_id }) => (
                    <div key={level_id} className="flex items-center mb-2">
                      <Tag color={levelMap[level_id]}>
                        {level_display_name || '--'}
                      </Tag>
                      <span>{t('settings.assignStrategy.notifyEvery')}</span>
                      <InputNumber
                        className="ml-2 w-[150px]"
                        defaultValue={30}
                        min={0}
                        addonAfter={t('settings.assignStrategy.frequencyUnit')}
                      />
                    </div>
                  ))}
                </div>
              </div>
            </Form.Item>
          </Collapse.Panel>
        </Collapse>
      </Form>
    </Drawer>
  );
};

export default OperateModalPage;
