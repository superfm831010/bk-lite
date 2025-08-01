
import { Button, Upload, message, Select, Spin } from "antd";
import type { UploadProps } from 'antd';
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
  // const [activeKey, setActiveKey] = useState<string[]>(['request']);
  const [chartData, setChartData] = useState<any[]>([
    {
      "value": 27.43789942218143,
      "timestamp": 1704038400
    },
    {
      "value": 26.033612999373652,
      "timestamp": 1704038460
    },
    {
      "value": 36.30777324191053,
      "timestamp": 1704038520
    },
    {
      "value": 33.70226097527219,
      "timestamp": 1704038580
    }
  ]);
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

  const anomalyData = useMemo(() => {
    return chartData.filter((item) => item.label === 1)
  }, [chartData]);

  // const RequestContent = useMemo(() => {
  //   const params = {
  //     // serving_id: 1,
  //     model_name: "RandomForest_1",
  //     model_version: "latest",
  //     algorithm: "RandomForest",
  //     // data: [
  //     //   {
  //     //     "timestamp": "2026-03-01",
  //     //     "value": 0.498,
  //     //     "label": 0
  //     //   },
  //     //   "..."
  //     // ],
  //     anomaly_threshold: 0.5,
  //   };

  //   return (
  //     <div className="h-[491px]">
  //       <div className="ml-4">
  //         <div className="text-[var(--color-text-1)] text-base">Params</div>
  //         <div className="text-[var(--color-text-2)]">
  //           <pre>
  //             {JSON.stringify(params, null, 2)}
  //           </pre>
  //         </div>
  //       </div>
  //     </div>
  //   )
  // }, []);

  // const ResponseContent = useMemo(() => {
  //   return (
  //     <div className="h-[491px] overflow-auto">
  //       <div>
  //         <div className="text-[var(--color-text-2)]">
  //           {/* <pre>
  //             {JSON.stringify(response, null, 2)}
  //           </pre> */}
  //           <CustomTable
  //             rowKey='timestamp'
  //             columns={columns}
  //             sticky={{ offsetHeader: 0 }}
  //             dataSource={anomalyData}
  //           />
  //         </div>
  //       </div>
  //     </div>
  //   )
  // }, [columns, anomalyData]);

  // const panelStyle: React.CSSProperties = {
  //   borderRadius: 0,
  //   padding: 0,
  // }

  // const items: CollapseProps['items'] = [
  //   // { key: 'request', label: 'Request', children: RequestContent, style: panelStyle },
  //   { key: 'response', label: 'Response', children: ResponseContent, style: panelStyle }
  // ];

  useEffect(() => {
    setInfoText({
      bannerTitle: '异常检测',
      bannerInfo: "基于机器学习的智能异常检测服务，能够自动识别时序数据中的异常模式和突变点。支持CSV文件上传，提供实时数据分析和可视化结果，帮助用户快速发现数据中的异常情况。广泛应用于系统监控、质量检测、金融风控、工业设备监控等场景。",
      applicationScenario: [
        {
          title: '资源状态监控',
          content: '通过持续采集CPU、内存、磁盘等关键指标时序数据，构建动态基线模型，可精准识别资源使用率异常波动、内存泄漏等潜在风险。',
          img: `bg-[url(/app/anomaly_detection_1.png)]`
        },
        {
          title: '网络流量分析',
          content: '基于流量时序特征建模，检测DDoS攻击、端口扫描等异常流量模式，支持实时阻断与安全告警',
          img: `bg-[url(/app/anomaly_detection_2.png)]`
        },
        {
          title: '数据库性能诊断',
          content: '分析SQL执行耗时、事务日志等时序数据，定位慢查询、死锁等性能瓶颈问题。',
          img: `bg-[url(/app/anomaly_detection_3.png)]`
        },
        {
          title: '容器健康管理',
          content: '监控容器化环境中Pod的资源使用、重启频率等时序指标，实现服务异常的早期预警。',
          img: `bg-[url(/app/anomaly_detection_4.png)]`
        },
      ]
    });
    handleSubmit();
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
    // setActiveKey(['request']);
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
      // setActiveKey(['request']);
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

  // const onKeyChange = (keys: string[]) => {
  //   const [key] = activeKey;
  //   if (keys.length === 0) {
  //     setActiveKey(key === 'request' ? ['response'] : ['request']);
  //   } else {
  //     setActiveKey(keys);
  //   }
  // };

  const handleSubmit = async () => {
    console.log(selectId, fileData);
    if (!chartData) { return message.error(t(`playground-common.uploadMsg`)) };
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
      // setActiveKey(['response']);
      setChartData(labelData);
    } catch (e) {
      console.log(e);
      message.error(t(`common.error`))
    } finally {
      setChartLoading(false);
    }
  };

  const renderElement = () => {
    return infoText.applicationScenario.map((item: any) => (
      <div key={item.title} className="content overflow-auto pb-[20px] border-b mt-4">
        <div className={`float-right w-[250px] h-[160px] ${item.img} bg-cover`}></div>
        <div className="content-info mr-[300px]">
          <div className="content-title text-lg font-bold">{item.title}</div>
          <div className="content-intro mt-3 text-sm text-[var(--color-text-3)]">{item.content}</div>
        </div>
      </div>
    ))
  };

  return (
    <div className="relative">
      <div className="banner-content w-full h-[460px] pr-[400px] pl-[200px] pt-[80px] bg-[url(/app/pg_banner_1.png)] bg-cover">
        <div className="banner-title text-5xl font-bold pt-5">
          {infoText.bannerTitle}
        </div>
        <div className="banner-info mt-8 max-w-[500px] text-[var(--color-text-3)]">
          {infoText.bannerInfo}
        </div>
        {/* <div className="banner-btn-list mt-[80px]">
            <Button type="primary" className="mr-3">立即使用</Button>
            <Button type="default">技术文档</Button>
          </div> */}
      </div>
      <div className="model-experience bg-[#F8FCFF] py-4">
        <div className="header text-3xl text-center">{t(`playground-common.functionExper`)}</div>
        <div className="content flex flex-col">
          <div className="file-input w-[90%] mx-auto">
            <div className={`link-search mt-8 flex justify-center `}>
              <div className="flex w-full justify-center items-center">
                <span className="align-middle text-sm mr-4">使用系统样本文件: </span>
                <Select className={`w-[70%] max-w-[500px] text-sm ${cssStyle.customSelect}`} size="large" allowClear options={[
                  { label: 'test1', value: 5 },
                  { label: 'test2', value: 6 },
                ]} placeholder={t(`playground-common.selectSampleMsg`)} onChange={onSelectChange} />
                <span className="mx-4 text-base pt-1">{t(`playground-common.or`)}</span>
                <Upload {...props}>
                  <Button size="large" className="rounded-none text-sm">{t(`playground-common.localUpload`)}</Button>
                </Upload>
                <Button size="large" className="rounded-none ml-4 text-sm" type="primary" onClick={handleSubmit}>{t(`playground-common.clickTest`)}</Button>
              </div>
            </div>
          </div>
          <div className="content w-[1180px] mx-auto h-[604px] mt-6">
            <div className="flex h-full overflow-auto">
              <Spin spinning={chartLoading} wrapperClassName="w-[70%] h-full" className="h-full">
                <div className="iframe w-full bg-[var(--color-bg-4)] border" style={{ height: 604 }}>
                  <LineChart
                    data={chartData}
                    timeline={timeline}
                    allowSelect={false}
                  />
                </div>
              </Spin>
              <div className="params w-[30%] bg-[var(--color-bg-4)]">
                <header className="pl-2">
                  <span className="inline-block h-[60px] text-[var(--color-text-2)] content-center ml-10 text-sm">检测结果</span>
                  <span
                    className={`
                      inline-block h-[60px] text-[var(--color-text-2)] 
                      content-center ml-10 text-sm 
                      hover:text-[var(--color-text-active)] cursor-pointer`
                    }
                  >请求参数</span>
                  {/* <a href="#" className="text-base text-[var(--color-text-1)]">请求参数</a> */}
                </header>
                <div className="border-r [&_.ant-table]:!h-[543px]">
                  <CustomTable
                    virtual
                    className="h-[543px]"
                    scroll={{ y: 543 }}
                    rowKey='timestamp'
                    columns={columns}
                    sticky={{ offsetHeader: 0 }}
                    dataSource={anomalyData}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="usage-scenarios pt-[80px] bg-[#F8FCFF]">
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