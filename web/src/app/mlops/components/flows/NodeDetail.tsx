import { Option } from "@/types";
import { Button, Drawer, Form, Select, Input } from "antd";
import { useEffect, useRef, useState } from "react";
import { useTranslation } from "@/utils/i18n";
import useMlopsManageApi from "@/app/mlops/api/manage";
import { Node } from "@xyflow/react";
import { FormInstance } from "antd/lib";

interface NodeOption extends Option {
  data: any
}

const NodeDetailDrawer = ({
  dataset,
  node,
  open = false,
  onChange,
  onClose,
  handleDelNode,
}: {
  dataset: string;
  node: Node;
  open: boolean;
  onChange: (data: any) => void;
  onClose: () => void;
  handleDelNode: () => void;
}) => {
  const { t } = useTranslation();
  const { getRasaIntentFileList, getRasaResponseFileList, getRasaSlotList, getRasaFormList, getRasaActionList } = useMlopsManageApi();
  const [loading, setLoading] = useState<boolean>(false);
  const [options, setOptions] = useState<NodeOption[]>([]);
  const formRef = useRef<FormInstance>(null);

  useEffect(() => {
    if (open) {
      getOptions();
    }
  }, [open])

  const getOptions = async () => {
    setLoading(true);
    let data = [];
    try {
      switch (node?.type) {
        case 'intent':
          data = await getRasaIntentFileList({ dataset });
          break;
        case 'response':
          data = await getRasaResponseFileList({ dataset });
          break;
        case 'slot':
          data = await getRasaSlotList({ dataset });
          break;
        case 'form':
          data = await getRasaFormList({ dataset });
          break;
        case 'action':
          data = await getRasaActionList({ dataset })
        default:
          break;
      }

      const options = data?.map((item: any) => {
        return {
          label: item?.name,
          value: item?.id,
          data: {
            ...item
          }
        }
      });
      setOptions(options);
      if (node.data) {
        formRef.current?.setFieldsValue({
          name: node.data?.name || null
        });
      }
    } catch (e) {
      console.log(e)
    } finally {
      setLoading(false);
    }
  };

  const handleOptionChange = (value: any) => {
    const item = options.find(item => item.value === value);
    onChange(item?.data?.name);
  };

  const validateVariableName = (value: string) => {
    const variableNameRegex = /^[a-zA-Z_][a-zA-Z0-9_]*$/;
    return variableNameRegex.test(value);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;

    if (value === '') {
      onChange(value);
      return;
    }

    if (validateVariableName(value)) {
      onChange(value);
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    const key = event.key;
    const currentValue = (event.target as HTMLInputElement).value;

    const allowedKeys = [
      'Backspace', 'Delete', 'ArrowLeft', 'ArrowRight',
      'ArrowUp', 'ArrowDown', 'Home', 'End', 'Tab', 'Enter'
    ];

    if (allowedKeys.includes(key)) {
      return;
    }

    if (key.length === 1) {
      if (currentValue === '' && /[0-9]/.test(key)) {
        event.preventDefault();
        return;
      }

      if (!/[a-zA-Z0-9_]/.test(key)) {
        event.preventDefault();
      }
    }
  };

  const handleInput = (event: React.FormEvent<HTMLInputElement>) => {
    const target = event.target as HTMLInputElement;
    const value = target.value;

    const filteredValue = value.replace(/[^a-zA-Z0-9_]/g, '');

    const finalValue = filteredValue.replace(/^[0-9]/, '');

    if (value !== finalValue) {
      target.value = finalValue;
      const syntheticEvent = {
        target: target,
        currentTarget: target
      } as React.ChangeEvent<HTMLInputElement>;
      handleInputChange(syntheticEvent);
    }
  };

  const closeDrawer = () => {
    onClose();
    setOptions([]);
    formRef.current?.resetFields();
  };

  const delNode = () => {
    handleDelNode();
    closeDrawer();
  };

  return (
    <Drawer
      title={t(`mlops-common.nodeDetail`)}
      open={open}
      width={400}
      onClose={closeDrawer}
      footer={[
        <Button key="delete" className="float-right" danger onClick={delNode}>{t(`mlops-common.delNode`)}</Button>,
      ]}
    >
      <div className="w-full h-full">
        <Form ref={formRef} layout="vertical">
          <Form.Item
            label={t(`common.select`)}
            name="name"
            rules={[
              {
                validator: (_, value) => {
                  if (node.type === 'checkpoint') {
                    if (!value) {
                      return Promise.reject(new Error('请输入变量名'));
                    }
                    if (!validateVariableName(value)) {
                      return Promise.reject(new Error('变量名只能包含字母、数字、下划线，且不能以数字开头'));
                    }
                    return Promise.resolve();
                  }
                }
              }
            ]}
          >
            {node?.type !== 'checkpoint'
              ? <Select options={options} placeholder={t(`common.selectMsg`)} onChange={handleOptionChange} loading={loading} />
              : <Input
                placeholder="请输入变量名（如：my_checkpoint_1）"
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                onInput={handleInput}
                maxLength={50}
              />
            }
          </Form.Item>
        </Form>
      </div>
    </Drawer>
  )
};

export default NodeDetailDrawer;