
import { Button, Collapse, Upload, message, Select, Spin } from "antd";
import type { CollapseProps, UploadProps } from 'antd';
import { handleFileRead, formatProbability } from "@/app/playground/utils/common";
import { useCallback, useState, useEffect, useMemo } from "react";
import { useTranslation } from "@/utils/i18n";
import LineChart from "@/app/playground/components/charts/lineChart";
import CustomTable from "@/components/custom-table";
import { useLocalizedTime } from "@/hooks/useLocalizedTime";
import usePlayroundApi from "@/app/playground/api";
import cssStyle from './index.module.scss'
import { ColumnItem } from "@/types";
// const { Search } = Input;

const AnomalyDetection = () => {
  const { t } = useTranslation();
  const { convertToLocalizedTime } = useLocalizedTime();
  const { anomalyDetectionReason } = usePlayroundApi();
  const [currentFileId, setCurrentFileId] = useState<string | null>(null);
  const [fileData, setFileData] = useState<any>(null);
  const [selectId, setSelectId] = useState<number | null>(null);
  const [activeKey, setActiveKey] = useState<string[]>(['request']);
  const [chartData, setChartData] = useState<any[]>([]);
  const [infoText, setInfoText] = useState<any>({
    bannerTitle: '',
    bannerInfo: "",
    applicationScenario: []
  });
  const [chartLoading, setChartLoading] = useState<boolean>(false);
  const [timeline, setTimeline] = useState<any>({
    startIndex: 0,
    endIndex: 0,
  });

  const columns: ColumnItem[] = useMemo(() => [
    {
      title: '时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      width: 80,
      align: 'center',
      render: (_, record) => {
        const time = new Date(record.timestamp * 1000).toISOString();
        return <p>{convertToLocalizedTime(time.toString(), 'YYYY-MM-DD HH:mm:ss')}</p>;
      },
    },
    {
      title: '值',
      dataIndex: 'value',
      key: 'value',
      align: 'center',
      width: 30,
      render: (_, record) => {
        const value = Number(record.value).toFixed(2);
        return <p>{value}</p>
      },
    },
    {
      title: '异常概率',
      dataIndex: 'anomaly_probability',
      key: 'anomaly_probability',
      align: 'center',
      width: 40,
      render: (_, record) => {
        const value = formatProbability(record.anomaly_probability);
        return <p>{value}</p>
      },
    }
  ], [convertToLocalizedTime]);

  const anomalyData = useMemo(() =>
    chartData.filter((item) => item.label === 1),
  [chartData]);

  const RequestContent = useMemo(() => {
    const params = {
      // serving_id: 1,
      model_name: "RandomForest_1",
      model_version: "latest",
      algorithm: "RandomForest",
      // data: [
      //   {
      //     "timestamp": "2026-03-01",
      //     "value": 0.498,
      //     "label": 0
      //   },
      //   "..."
      // ],
      anomaly_threshold: 0.5,
    };

    return (
      <div className="h-[491px]">
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
  }, []);

  const ResponseContent = useMemo(() => {
    return (
      <div className="h-[491px] overflow-auto">
        <div>
          <div className="text-[var(--color-text-2)]">
            {/* <pre>
              {JSON.stringify(response, null, 2)}
            </pre> */}
            <CustomTable
              rowKey='timestamp'
              columns={columns}
              sticky={{ offsetHeader: 0 }}
              dataSource={anomalyData}
            />
          </div>
        </div>
      </div>
    )
  }, [columns, anomalyData]);

  const panelStyle: React.CSSProperties = {
    borderRadius: 0,
    padding: 0,
  }

  const items: CollapseProps['items'] = [
    { key: 'request', label: 'Request', children: RequestContent, style: panelStyle },
    { key: 'response', label: 'Response', children: ResponseContent, style: panelStyle }
  ];

  useEffect(() => {
    setInfoText({
      bannerTitle: '异常检测',
      bannerInfo: "基于机器学习的智能异常检测服务，能够自动识别时序数据中的异常模式和突变点。支持CSV文件上传，提供实时数据分析和可视化结果，帮助用户快速发现数据中的异常情况。广泛应用于系统监控、质量检测、金融风控、工业设备监控等场景。",
      applicationScenario: [
        {
          title: '系统监控',
          content: '实时监控服务器性能指标、网络流量、应用响应时间等关键指标，及时发现系统异常，确保业务连续性。支持CPU使用率、内存占用、磁盘I/O等多维度监控。'
        },
        {
          title: '工业设备监控',
          content: '对生产线设备的温度、压力、振动等传感器数据进行实时监控，提前预警设备故障风险。通过异常检测算法识别设备性能衰减趋势，实现预测性维护。'
        },
        {
          title: '网络安全',
          content: '分析网络流量模式，识别DDoS攻击、恶意入侵等安全威胁。通过监控网络连接行为、数据传输模式等，及时发现异常访问，保障网络安全。'
        },
        {
          title: '质量检测',
          content: '应用于制造业产品质量控制，检测生产过程中的异常波动。通过分析产品尺寸、重量、成分等关键指标，快速识别不合格产品，提高产品质量。'
        },
      ]
    })
  }, [])

  useEffect(() => {
    if (chartData.length) {
      const newTimeline = {
        startIndex: 0,
        endIndex: chartData.length > 10 ? Math.floor(chartData.length / 10) : (chartData.length > 1 ? chartData.length - 1 : 0)
      };

      if (newTimeline.startIndex !== timeline.startIndex || newTimeline.endIndex !== timeline.endIndex) {
        setTimeline(newTimeline);
      }
    }
  }, [chartData.length]);

  const onSelectChange = async (value: number) => {
    setActiveKey(['request']);
    if (!value) {
      setSelectId(null);
      setChartData([]);
      return;
    }
    setChartLoading(true);
    try {
      setSelectId(value);
      // const data = await getAnomalyTrainDataInfo(value as number, true, true);
      // const _data = data?.train_data.map((item: any) => ({
      //   timestamp: item.timestamp,
      //   value: item.value,
      //   label: 0
      // }));
      // setChartData(_data);
      setFileData(null);
    } catch (e) {
      console.log(e);
    } finally {
      setChartLoading(false);
    }
  };

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
      setFileData(data);
      setChartData(data);
    } catch (e) {
      console.log(e);
      setFileData(null);
    } finally {
      setChartLoading(false);
      setActiveKey(['request']);
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
        message.warning(t(`playground-common.uploadError`));
      }
      return isCSV;
    },
    accept: '.csv'
  };

  const onKeyChange = (keys: string[]) => {
    const [key] = activeKey;
    if (keys.length === 0) {
      setActiveKey(key === 'request' ? ['response'] : ['request']);
    } else {
      setActiveKey(keys);
    }
  };

  const handleSubmit = async () => {
    if (!selectId && !fileData) { return message.error(t(`playground-common.uploadMsg`)) };
    if (chartLoading) return;
    setChartLoading(true);
    try {
      const params = {
        serving_id: 1,
        model_name: "RandomForest_1",
        model_version: "latest",
        algorithm: "RandomForest",
        data: chartData,
        anomaly_threshold: 0.5
      };
      const data = await anomalyDetectionReason(params);
      const labelData = data.predictions?.map((item: any) => {
        return {
          timestamp: item.timestamp,
          value: item.value,
          label: item.is_anomaly,
          anomaly_probability: item.anomaly_probability
        }
      });
      setActiveKey(['response']);
      setChartData(labelData);
    } catch (e) {
      console.log(e)
    } finally {
      setChartLoading(false);
    }
  };

  const renderElement = () => {
    return infoText.applicationScenario.map((item: any) => (
      <div key={item.title} className="content overflow-auto pb-[20px] border-b mt-4">
        <div className="float-right w-[250px] h-[160px] bg-slate-400"></div>
        <div className="content-info mr-[300px]">
          <div className="content-title text-xl font-bold">{item.title}</div>
          <div className="content-intro mt-3">{item.content}</div>
        </div>
      </div>
    ))
  };

  return (
    <div className="relative pb-8">
      <div className="banner-content w-[90%] h-[380px] pr-[400px] mx-auto">
        <div className="banner-title text-5xl pt-5">
          {infoText.bannerTitle}
        </div>
        <div className="banner-info mt-8">
          {infoText.bannerInfo}
        </div>
        {/* <div className="banner-btn-list mt-[80px]">
            <Button type="primary" className="mr-3">立即使用</Button>
            <Button type="default">技术文档</Button>
          </div> */}
      </div>
      <div className="model-experience mt-[80px] bg-[var(--color-bg-4)] py-4">
        <div className="header text-3xl text-center">{t(`playground-common.functionExper`)}</div>
        <div className="content flex flex-col">
          <div className="file-input w-[70%] mx-auto">
            <div className={`link-search mt-8 flex justify-center `}>
              <div className="flex w-[80%] justify-start items-start">
                <Select className={`w-[70%] ${cssStyle.customSelect}`} size="large" allowClear options={[
                  { label: 'test1', value: 5 },
                  { label: 'test2', value: 6 },
                ]} placeholder={t(`playground-common.selectSampleMsg`)} onChange={onSelectChange} />
                <span className="mx-4 text-xl pt-1">{t(`playground-common.or`)}</span>
                <Upload {...props}>
                  <Button size="large" className="rounded-none">{t(`playground-common.localUpload`)}</Button>
                </Upload>
                <Button size="large" className="rounded-none ml-4" type="primary" onClick={handleSubmit}>{t(`playground-common.clickTest`)}</Button>
              </div>
            </div>
          </div>
          <div className="content w-[1180px] mx-auto h-[654px] mt-6">
            <div className="flex h-full overflow-auto">
              <Spin spinning={chartLoading} wrapperClassName="w-[70%] h-full" className="h-full">
                <div className="iframe w-full bg-[var(--color-bg-4)]" style={{ height: 604 }}>
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
          {t(`playground-common.useScenario`)}
        </div>
        <div className="mt-8 w-[80%] mx-auto">
          {renderElement()}
        </div>
      </div>
    </div>
  )
};

export default AnomalyDetection;