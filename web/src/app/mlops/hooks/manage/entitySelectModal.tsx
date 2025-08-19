"use client";
import { ModalRef } from "@/app/mlops/types";
import OperateModal from "@/components/operate-modal";
import { Option } from "@/types";
import { Form, Select, Input, Button, FormInstance } from "antd";
import { forwardRef, useEffect, useImperativeHandle, useState, useRef } from "react";
import { useTranslation } from "@/utils/i18n";
import useMlopsManageApi from "@/app/mlops/api/manage";

interface EntitySelectModalProps {
  dataset: string | number;
  onSuccess: (name: string) => void;
}

const EntitySelectModal = forwardRef<ModalRef, EntitySelectModalProps>(({ dataset, onSuccess }, ref) => {
  const { t } = useTranslation();
  const { getRasaEntityList, addRasaEntityFile } = useMlopsManageApi();
  const formRef = useRef<FormInstance>(null);
  const [options, setOptions] = useState<Option[]>([]);
  const [open, setOpen] = useState<boolean>(false);
  const [isAdd, setIsAdd] = useState<boolean>(false);
  const [confirmLoading, setConfirmLoading] = useState<boolean>(false);

  useImperativeHandle(ref, () => ({
    showModal: () => {
      setOpen(true);
    }
  }));

  useEffect(() => {
    if (open && !isAdd) {
      getList();
    }
  }, [open, isAdd]);

  const getList = async () => {
    const data = await getRasaEntityList({ dataset });
    const _options = data?.map((item: any) => {
      return {
        label: item?.name,
        value: item?.name
      }
    });
    setOptions(_options);
  };

  const handleSubmit = async () => {
    console.log('submit')
    setConfirmLoading(true);
    try {
      const data = await formRef.current?.validateFields();
      if (isAdd) {
        const param = {
          ...data,
          dataset: dataset,
          entity_type: 'Text',
          example: []
        };
        await addRasaEntityFile(param)
        setIsAdd(false);
      } else {
        console.log(isAdd);
        const { entity } = data;
        onSuccess(entity)
        setOpen(false);
      }
    } catch (e) {
      console.log(e);
    } finally {
      setConfirmLoading(false);
    }
  };

  const onCancel = () => {
    setOpen(false);
  }

  return (
    <OperateModal
      width={400}
      title="选择实体"
      open={open}
      footer={[
        <Button key="confirm" type="primary" loading={confirmLoading} onClick={handleSubmit} >{t(`common.confirm`)}</Button>,
        <Button key="cancel" onClick={onCancel}>{t(`common.cancel`)}</Button>
      ]}
    >
      <Form ref={formRef}>
        {isAdd ? (
          <Form.Item
            name={"name"}
            label={t(`common.name`)}
            rules={[
              { required: true, message: t(`common.selectMsg`) }
            ]}
          >
            <Input />
          </Form.Item>
        ) : (
          <>
            <Form.Item
              name="entity"
              label="添加实体"
              rules={[
                { required: true, message: t(`common.selectMsg`) }
              ]}
            >
              <Select options={options} placeholder="请选择一个实体" />
            </Form.Item>
            <p>若无合适实体，点击
              <a href="#" className="text-[var(--color-text-active)] font-" onClick={() => setIsAdd(true)}>新增</a>
            </p>
          </>
        )}
      </Form>
    </OperateModal>
  )
});

EntitySelectModal.displayName = 'EntitySelectModal';
export default EntitySelectModal;