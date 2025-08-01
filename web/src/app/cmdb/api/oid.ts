import useApiClient from '@/utils/request';

export const useOidApi = () => {
  const { get, post, put, del } = useApiClient();

  // 获取OID列表
  const getOidList = (params?: any) =>
    get('/cmdb/api/oid/', { params });

  // 创建OID
  const createOid = (params: any) =>
    post('/cmdb/api/oid/', params);

  // 更新OID
  const updateOid = (oidId: string, params: any) =>
    put(`/cmdb/api/oid/${oidId}/`, params);

  // 删除OID
  const deleteOid = (oidId: string) =>
    del(`/cmdb/api/oid/${oidId}/`);

  return {
    getOidList,
    createOid,
    updateOid,
    deleteOid,
  };
};
