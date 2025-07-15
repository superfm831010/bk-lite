
import { Button, Collapse, Upload, message, Select, Spin } from "antd";
import type { CollapseProps, UploadProps } from 'antd';
import { handleFileRead } from "@/app/playground/utils/common";
import { useCallback, useState, useEffect } from "react";
import LineChart from "@/app/mlops/components/charts/lineChart";
import useMlopsManageApi from "@/app/mlops/api/manage";
import usePlayroundApi from "@/app/playground/api";
import cssStyle from './index.module.scss'
// const { Search } = Input;

const AnomalyDetection = () => {
  const { getAnomalyTrainDataInfo } = useMlopsManageApi();
  const { anomalyDetectionReason } = usePlayroundApi();
  const [currentFileId, setCurrentFileId] = useState<string | null>(null);
  const [fileData, setFileData] = useState<any>(null);
  const [selectId, setSelectId] = useState<number | null>(null);
  const [activeKey, setActiveKey] = useState<string[]>(['request']);
  const [chartData, setChartData] = useState<any[]>([]);
  const [chartLoading, setChartLoading] = useState<boolean>(false);
  const [timeline, setTimeline] = useState<any>({
    startIndex: 0,
    endIndex: 0,
  });


  useEffect(() => {
    if (chartData.length) {
      setTimeline({
        startIndex: 0,
        endIndex: chartData.length > 10 ? Math.floor(chartData.length / 10) : (chartData.length > 1 ? chartData.length - 1 : 0)
      });
    }
  }, [chartData]);

  const onUploadChange: UploadProps['onChange'] = useCallback(async ({ fileList }: { fileList: any }) => {
    if (!fileList.length) {
      setCurrentFileId(null);
      setFileData(null);
      setChartData([])
      return;
    }

    const file = fileList[0];
    const fileId = file?.uid;

    if (currentFileId === fileId) return;
    setCurrentFileId(fileId);
    setChartLoading(true);
    try {
      const text = await file?.originFileObj?.text();
      const data = handleFileRead(text as string);
      console.log(data);
      setFileData(data);
      setChartData(data);
    } catch (e) {
      console.log(e);
      setFileData(null);
    } finally {
      setChartLoading(false);
    }
  }, [currentFileId]);

  const props: UploadProps = {
    name: 'file',
    multiple: false,
    maxCount: 1,
    showUploadList: false,
    onChange: onUploadChange,
    beforeUpload: (file) => {
      const isCSV = file.type === "text/csv" || file.name.endsWith('.csv');
      if (!isCSV) {
        message.warning(`上传的文件类型错误`);
      }
      return isCSV;
    },
    accept: '.csv'
  };

  const RequestContent = () => {
    const params = {
      model_name: "dev",
      model_version: "latest",
      algorithm: "RandomForest",
      data: [
        {
          "timestamp": "2026-03-01",
          "value": 0.498,
          "label": 0
        },
        "..."
      ],
      anomaly_threshold: 0.5
    };

    return (
      <div className="h-[367px]">
        <div className="ml-4">
          <div className="text-[var(--color-text-1)] text-base">Params</div>
          <div className="text-[var(--color-text-2)]">
            <pre>
              {JSON.stringify(params, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    )
  };

  const ResponseContent = () => {
    const response = {
      log_id: 1,
      result: [
        {
          timestamp: "2026-03-01",
          value: 0.498,
          label: 1
        },
        "..."
      ]
    };

    return (
      <div className="h-[367px]">
        <div className="ml-4">
          <div className="text-[var(--color-text-2)]">
            <pre>
              <pre>
                {JSON.stringify(response, null, 2)}
              </pre>
            </pre>
          </div>
        </div>
      </div>
    )
  };

  const items: CollapseProps['items'] = [
    { key: 'request', label: 'Request', children: <RequestContent /> },
    { key: 'response', label: 'Response', children: <ResponseContent /> }
  ];

  const onSelectChange = async (value: number) => {
    if (!value) return setChartData([]);
    setChartLoading(true);
    try {
      setSelectId(value);
      const data = await getAnomalyTrainDataInfo(value as number, true, true);
      const _data = data?.train_data.map((item: any) => ({
        timestamp: item.timestamp,
        value: item.value,
        label: 0
      }));
      setChartData(_data);
    } catch (e) {
      console.log(e);
    } finally {
      setChartLoading(false);
    }
  };

  const onKeyChange = (keys: string[]) => {
    const [key] = activeKey;
    if (keys.length === 0) {
      setActiveKey(key === 'request' ? ['response'] : ['request'])
    } else {
      setActiveKey(keys)
    }
  };

  const handleSubmit = async () => {
    if (!selectId && !fileData) { return message.error(`请选择一份文件或者从本地上传文件`) };
    if(chartLoading) return;
    setChartLoading(true);
    try {
      const params = {
        model_name: "dev",
        model_version: "latest",
        algorithm: "RandomForest",
        data: chartData,
        anomaly_threshold: 0.5
      };
      const data = await anomalyDetectionReason(params);
      console.log(data);
    } catch (e) {
      console.log(e)
    } finally {
      setChartLoading(false);
    }
  };

  return (
    <>
      <div className="relative pb-8">
        <div className="banner-content w-[90%] h-[300px] pr-[400px] mx-auto">
          <div className="banner-title text-5xl">
            异常检测
          </div>
          <div className="banner-info mt-8">
            基于机器学习的智能异常检测服务，能够自动识别时序数据中的异常模式和突变点。支持CSV文件上传，提供实时数据分析和可视化结果，帮助用户快速发现数据中的异常情况。广泛应用于系统监控、质量检测、金融风控、工业设备监控等场景。
          </div>
          {/* <div className="banner-btn-list mt-[80px]">
            <Button type="primary" className="mr-3">立即使用</Button>
            <Button type="default">技术文档</Button>
          </div> */}
        </div>
        <div className="model-experience mt-[80px] bg-[var(--color-bg-4)] py-4">
          <div className="header text-3xl text-center">功能体验</div>
          <div className="content flex flex-col">
            <div className="file-input w-[70%] mx-auto">
              <div className={`link-search mt-8 flex justify-center `}>
                <div className="flex w-[80%] justify-start items-start">
                  <Select className={`w-[70%] ${cssStyle.customSelect}`} size="large" allowClear options={[
                    { label: 'test1', value: 5 },
                    { label: 'test2', value: 6 },
                  ]} placeholder="请选择一份样本文件" onChange={onSelectChange} />
                  <span className="mx-4 text-xl pt-1">或</span>
                  <Upload {...props}>
                    <Button size="large" className="rounded-none">本地上传</Button>
                  </Upload>
                  <Button size="large" className="rounded-none ml-4" type="primary" onClick={handleSubmit}>点击检测</Button>
                </div>
              </div>
            </div>
            <div className="content w-[85%] mx-auto h-[480px] mt-6">
              <div className="flex h-full overflow-auto">
                <Spin spinning={chartLoading} wrapperClassName="w-[70%] h-full" className="h-full">
                  <div className="iframe w-full bg-[var(--color-bg-4)]" style={{ height: 480 }}>
                    <LineChart
                      data={chartData}
                      timeline={timeline}
                      allowSelect={false}
                    />
                  </div>
                </Spin>
                <div className="params w-[30%]">
                  <Collapse
                    accordion
                    items={items}
                    bordered={false}
                    activeKey={activeKey}
                    onChange={onKeyChange}
                  ></Collapse>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="usage-scenarios mt-[80px]">
          <div className="header text-center text-3xl">
            应用场景
          </div>
          <div className="mt-8 w-[80%] mx-auto">
            <div className="content overflow-auto pb-[20px] border-b">
              <div className="float-right w-[250px] h-[160px] bg-slate-400"></div>
              <div className="content-info mr-[300px]">
                <div className="content-title text-xl font-bold">系统监控</div>
                <div className="content-intro mt-3">实时监控服务器性能指标、网络流量、应用响应时间等关键指标，及时发现系统异常，确保业务连续性。支持CPU使用率、内存占用、磁盘I/O等多维度监控。</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
};

export default AnomalyDetection;