import useApiClient from '@/utils/request';

export const useChangeRecordApi = () => {
  const { get } = useApiClient();

  // 获取变更记录列表
  const getChangeRecords = (params?: any) =>
    get('/cmdb/api/change_record', { params });

  // 获取指定实例的变更记录
  const getInstanceChangeRecords = (params: any) =>
    get('/cmdb/api/change_record/', { params });

  // 获取变更记录详情
  const getChangeRecordDetail = (recordId: string | number) =>
    get(`/cmdb/api/change_record/${recordId}/`);

  // 获取变更记录枚举数据
  const getChangeRecordEnumData = () =>
    get('/cmdb/api/change_record/enum_data/');

  return {
    getChangeRecords,
    getInstanceChangeRecords,
    getChangeRecordDetail,
    getChangeRecordEnumData,
  };
};
