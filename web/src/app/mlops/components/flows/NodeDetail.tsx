import { Option } from "@/types";
import { Button, Drawer, Form, Select } from "antd";
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
  const { getRasaIntentFileList, getRasaResponseFileList, getRasaSlotList, getRasaFormList } = useMlopsManageApi();
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
      if(node.data) {
        formRef.current?.setFieldsValue({
          select: node.data?.name
        });
      }
    } catch (e) {
      console.log(e)
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (value: any) => {
    const item = options.find(item => item.value === value);
    onChange(item?.data);
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
          <Form.Item label={t(`common.select`)} name="select">
            <Select options={options} placeholder={t(`common.selectMsg`)} onChange={handleChange} loading={loading} />
          </Form.Item>
        </Form>
      </div>
    </Drawer>
  )
};

export default NodeDetailDrawer;