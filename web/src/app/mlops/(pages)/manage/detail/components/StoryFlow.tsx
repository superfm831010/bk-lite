import FlowWrapper from "@/app/mlops/components/flows/FlowProvider";
import { NodeType, TableData } from '@/app/mlops/types';
import { Node, Edge } from "@xyflow/react";
import { message } from "antd";
import { useMemo, useState } from "react";
import { useTranslation } from "@/utils/i18n";
import useMlopsManageApi from "@/app/mlops/api/manage";

interface StoryFlowWrapperProps {
  dataset: string;
  backToList?: () => void;
  currentStory: TableData | null;
  onSuccess: () => void;
}

const StoryFlow: React.FC<StoryFlowWrapperProps> = ({
  dataset,
  // backToList,
  currentStory,
  onSuccess
}) => {
  const { t } = useTranslation();
  const { updateRasaStoryFile } = useMlopsManageApi();
  const [flowLoading, setFlowLoading] = useState<boolean>(false);
  const nodeTypes: NodeType[] = [
    { type: 'intent', label: t(`datasets.intentNode`), icon: 'tijiaoxiangfa' },
    { type: 'response', label: t(`datasets.responseNode`), icon: 'huifu-copy' },
    { type: 'slot', label: t(`datasets.slotNode`), icon: 'dangqianbianliang' },
    { type: 'form', label: t(`datasets.formNode`), icon: 'biaodan' },
    { type: 'action', label: t(`datasets.actionNode`), icon: 'dongzuo1' },
  ];

  const [initialNodes, initialEdges] = useMemo(() => {
    if (currentStory) {
      // 节点处理
      const edgeMap = new Map();
      const edges: Edge[] = [];
      const nodes: Node[] = currentStory.steps?.map((item: any) => {
        if (item.source) {
          const edgeId = `${item.source}-${item.id}`;
          if (!edgeMap.has(edgeId)) {
            edges.push({
              id: edgeId,
              source: item.id,
              target: item.source
            });
            edgeMap.set(edgeId, true);
          }
        }
        if (item.target) {
          const edgeId = `${item.id}-${item.target}`;
          if (!edgeMap.has(edgeId)) {
            edges.push({
              id: edgeId,
              source: item.target,
              target: item.id
            });
            edgeMap.set(edgeId, true);
          }
        }

        return {
          id: item?.id,
          type: item?.type,
          position: item.position,
          data: {
            id: item?.id,
            name: item?.name,
            source: item.source || null,
            target: item.target || null
          }
        };
      });
      return [nodes, edges];
    }
    return [[], []];
  }, [currentStory]);


  const updateStoryData = async (data: any) => {
    setFlowLoading(true);
    try {
      if (currentStory) {
        const steps = data.nodes.map((item: Node) => {
          return {
            id: item.id,
            name: item.data?.name || '',
            type: item.type,
            position: item.position,
            source: item.data?.source || null,
            target: item.data?.target || null,
          }
        });

        await updateRasaStoryFile(currentStory.id, {
          ...currentStory,
          steps
        });
        message.success(t('common.updateSuccess'));
        onSuccess();
      }
    } catch (e) {
      console.log(e);
    } finally {
      setFlowLoading(false);
    }
  };

  return (
    <FlowWrapper
      initialNodes={initialNodes}
      initialEdges={initialEdges}
      nodeTypes={nodeTypes}
      dataset={dataset}
      loading={flowLoading}
      // panel={[
      //   <Button key="back" size="small" variant="outlined" className="mr-2 text-xs" onClick={backToList}>{t(`mlops-common.backToList`)}</Button>,
      // ]}
      handleSaveFlow={(data) => updateStoryData(data)}
    />
  )
};

export default StoryFlow