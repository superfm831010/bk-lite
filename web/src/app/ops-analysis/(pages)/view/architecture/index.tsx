'use client';

import React, {
  useState,
  useEffect,
  forwardRef,
  useImperativeHandle,
  useCallback,
  useRef,
} from 'react';
import styles from './index.module.scss';
import { iconList } from '@/app/cmdb/utils/common';
import { message, Spin } from 'antd';
import { useArchitectureApi } from '@/app/ops-analysis/api/architecture';
import { flattenCollections } from '@isoflow/isopacks/dist/utils';
import {
  DiagramData,
  ArchitectureProps,
} from '@/app/ops-analysis/types/architecture';
import dynamic from 'next/dynamic';
import awsIsopack from '@isoflow/isopacks/dist/aws';
import gcpIsopack from '@isoflow/isopacks/dist/gcp';
import azureIsopack from '@isoflow/isopacks/dist/azure';
import isoflowIsopack from '@isoflow/isopacks/dist/isoflow';
import kubernetesIsopack from '@isoflow/isopacks/dist/kubernetes';
import ArchitectureToolbar from './components/toolbar';

const Isoflow = dynamic(
  () => import('fossflow').then((mod) => ({ default: mod.Isoflow })),
  {
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-full">
        <Spin size="large" tip="Loading..." />
      </div>
    ),
  }
);

const svgToBase64 = async (svgPath: string): Promise<string> => {
  try {
    const response = await fetch(`/app/assets/assetModelIcon/${svgPath}.svg`);
    const svgText = await response.text();
    const base64 = btoa(unescape(encodeURIComponent(svgText)));
    return `data:image/svg+xml;base64,${base64}`;
  } catch (error) {
    const fallbackSvg =
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" fill="#e0e0e0"/><text x="12" y="12" text-anchor="middle" dominant-baseline="middle" font-size="8" fill="#666">?</text></svg>';
    const fallbackBase64 = btoa(unescape(encodeURIComponent(fallbackSvg)));
    return `data:image/svg+xml;base64,${fallbackBase64}`;
  }
};

const createCmdbIsopack = async () => {
  const icons = await Promise.all(
    iconList.map(async (icon) => ({
      id: `cmdb-${icon.key}`,
      name: icon.describe || icon.key,
      url: await svgToBase64(icon.url),
      isIsometric: true,
    }))
  );

  return {
    id: 'cmdb',
    name: 'CMDB',
    icons,
  };
};

const patchIconSize = (icon: any) => ({
  ...icon,
  width: icon.width || icon.size || 48,
  height: icon.height || icon.size || 48,
});

export interface ArchitectureRef {
  hasUnsavedChanges: () => boolean;
}

const Architecture = forwardRef<ArchitectureRef, ArchitectureProps>(
  ({ selectedArchitecture }, ref) => {
    const { getArchitectureDetail, saveArchitecture } = useArchitectureApi();

    const [diagramName, setDiagramName] = useState('');
    const [fossflowKey, setFossflowKey] = useState(0);
    const [currentModel, setCurrentModel] = useState<DiagramData | null>(null);
    const [hasUnsaved, setHasUnsaved] = useState(false);
    const [loading, setLoading] = useState(false);
    const [uniqueIcons, setUniqueIcons] = useState<any[]>([]);
    const [isEditMode, setIsEditMode] = useState(false);
    const [loadedArchitectureId, setLoadedArchitectureId] = useState<
      string | null
    >(null);

    const debounceTimeoutRef = useRef<NodeJS.Timeout | null>(null);
    const lastModelUpdateRef = useRef<string>('');
    const isUpdatingRef = useRef<boolean>(false);
    const defaultColors = [
      { id: 'blue', value: '#0066cc' },
      { id: 'green', value: '#00aa00' },
      { id: 'red', value: '#cc0000' },
      { id: 'orange', value: '#ff9900' },
      { id: 'purple', value: '#9900cc' },
      { id: 'black', value: '#000000' },
      { id: 'gray', value: '#666666' },
    ];

    const [diagramData, setDiagramData] = useState<DiagramData>(() => {
      return {
        title: 'Untitled Diagram',
        icons: [],
        colors: defaultColors,
        items: [],
        views: [],
        fitToScreen: true,
      };
    });

    useEffect(() => {
      let isMounted = true;
      createCmdbIsopack().then((cmdbIsopack) => {
        const allIcons = flattenCollections([
          cmdbIsopack,
          {
            ...isoflowIsopack,
            icons: isoflowIsopack.icons.map(patchIconSize),
          },
          awsIsopack,
          azureIsopack,
          gcpIsopack,
          kubernetesIsopack,
        ]);
        const unique = allIcons.filter(
          (icon, index, self) =>
            index === self.findIndex((i) => i.id === icon.id)
        );
        if (isMounted) {
          setUniqueIcons(unique);
        }
      });
      return () => {
        isMounted = false;
      };
    }, []);

    useEffect(() => {
      if (uniqueIcons.length === 0) return;

      const currentArchitectureId = selectedArchitecture?.data_id;

      // 只有在架构图ID真正改变时才重新加载
      if (
        currentArchitectureId &&
        currentArchitectureId !== loadedArchitectureId
      ) {
        (async () => {
          try {
            setLoading(true);
            isUpdatingRef.current = true;

            setCurrentModel(null);
            setDiagramData({
              title: 'Loading...',
              icons: uniqueIcons,
              colors: defaultColors,
              items: [],
              views: [],
              fitToScreen: true,
            });
            setFossflowKey((prev) => prev + 1);

            const data = await getArchitectureDetail(currentArchitectureId);
            const viewSets = Array.isArray(data.view_sets)
              ? { items: [], views: [] }
              : data.view_sets || { items: [], views: [] };
            if (data) {
              const mergedData: DiagramData = {
                items: viewSets.items || [],
                views: viewSets.views || [],
                title: data.name || diagramName,
                icons: uniqueIcons,
                colors: defaultColors,
                fitToScreen: true,
              };

              setDiagramName(data.name || '');
              setDiagramData({ ...mergedData });
              setCurrentModel({ ...mergedData });
              setFossflowKey((prev) => prev + 1);
              setHasUnsaved(false);
              setLoadedArchitectureId(currentArchitectureId);
              setIsEditMode(false); // 切换架构图后默认为视图模式

              lastModelUpdateRef.current = JSON.stringify({
                items: viewSets.items || [],
                views: viewSets.views || [],
              });
            }
          } catch (error) {
            console.error('Load failed:', error);
            message.error('加载失败');
          } finally {
            setLoading(false);
            setTimeout(() => {
              isUpdatingRef.current = false;
            }, 1000);
          }
        })();
      } else if (!currentArchitectureId && loadedArchitectureId) {
        // 清空选择时重置状态
        setCurrentModel(null);
        setDiagramData({
          title: 'Untitled Diagram',
          icons: uniqueIcons,
          colors: defaultColors,
          items: [],
          views: [],
          fitToScreen: true,
        });
        setFossflowKey((prev) => prev + 1);
        setHasUnsaved(false);
        setIsEditMode(false); // 清空选择时重置为视图模式
        setLoadedArchitectureId(null);
        lastModelUpdateRef.current = '';
      }
    }, [uniqueIcons, selectedArchitecture?.data_id, loadedArchitectureId]);

    const toggleEditMode = () => {
      const newEditMode = !isEditMode;
      setIsEditMode(newEditMode);
      if (newEditMode) {
        // 进入编辑模式时重置未保存状态
        setHasUnsaved(false);
      }
      // 切换编辑模式时更新 key，但不重新加载数据
      setFossflowKey((prev) => prev + 1);
    };

    const saveDiagram = async () => {
      if (!selectedArchitecture?.data_id || !currentModel) {
        message.error('无法保存：缺少必要信息');
        return;
      }
      try {
        setLoading(true);

        const saveData = {
          name: diagramName,
          view_sets: {
            views: currentModel.views || [],
            items: currentModel.items || [],
          },
        };

        await saveArchitecture(selectedArchitecture.data_id, saveData);

        // 更新最后保存的模型快照，避免刷新时重新加载
        lastModelUpdateRef.current = JSON.stringify({
          items: currentModel.items || [],
          views: currentModel.views || [],
        });

        setHasUnsaved(false);
        setIsEditMode(false); // 保存后退出编辑模式
        message.success('图表已保存');
      } catch (error) {
        console.error('Save failed:', error);
        message.error('保存失败');
      } finally {
        setLoading(false);
      }
    };

    const handleModelUpdated = useCallback(
      (model: any) => {
        if (isUpdatingRef.current) {
          return;
        }

        if (!selectedArchitecture?.data_id) {
          return;
        }

        try {
          const modelSnapshot = JSON.stringify({
            items: model.items || [],
            views: model.views || [],
          });

          if (modelSnapshot === lastModelUpdateRef.current) {
            return;
          }

          if (debounceTimeoutRef.current) {
            clearTimeout(debounceTimeoutRef.current);
          }

          debounceTimeoutRef.current = setTimeout(() => {
            try {
              const newModelData = {
                items: JSON.parse(JSON.stringify(model.items)) || [],
                views: JSON.parse(JSON.stringify(model.views)) || [],
              };

              setCurrentModel((prevModel) => {
                if (!prevModel) return null;
                return {
                  ...prevModel,
                  items: newModelData.items,
                  views: newModelData.views,
                };
              });
              if (isEditMode) {
                setHasUnsaved(true);
              }
              lastModelUpdateRef.current = modelSnapshot;
            } catch (error) {
              console.error('Error updating model state:', error);
            }
          }, 300);
        } catch (error) {
          console.error('Error in handleModelUpdated:', error);
        }
      },
      [selectedArchitecture?.data_id, isEditMode]
    );

    const hasUnsavedChanges = () => {
      return isEditMode && hasUnsaved;
    };

    useImperativeHandle(ref, () => ({
      hasUnsavedChanges,
    }));

    useEffect(() => {
      return () => {
        if (debounceTimeoutRef.current) {
          clearTimeout(debounceTimeoutRef.current);
        }
      };
    }, []);

    return (
      <div className="h-full flex-1 p-4 pb-0 overflow-auto flex flex-col">
        <ArchitectureToolbar
          selectedArchitecture={selectedArchitecture}
          isEditMode={isEditMode}
          loading={loading}
          onEdit={toggleEditMode}
          onSave={saveDiagram}
        />

        <div
          className={`flex-1 relative architecture-canvas ${styles.architectureCanvas}`}
          style={{ minHeight: '500px' }}
        >
          {loading && (
            <div className="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-50">
              <Spin size="large" tip="加载架构图..." />
            </div>
          )}
          <Isoflow
            key={`${fossflowKey}-edit`}
            initialData={diagramData}
            onModelUpdated={handleModelUpdated}
            editorMode={isEditMode ? 'EDITABLE' : 'EXPLORABLE_READONLY'}
          />
        </div>
      </div>
    );
  }
);

Architecture.displayName = 'Architecture';

export default Architecture;
