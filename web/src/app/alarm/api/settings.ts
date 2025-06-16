import useApiClient from '@/utils/request';

export const useSettingApi = () => {
  const { get, post, del, put, patch } = useApiClient();

  const getAssignmentList = (params: any) =>
    get('/alerts/api/assignment/', { params });

  const getAssignment = (id: string | number) =>
    get(`/alerts/api/assignment/${id}/`);

  const createAssignment = (params: any) =>
    post('/alerts/api/assignment/', params);

  const updateAssignment = (id: string | number, params: any) =>
    put(`/alerts/api/assignment/${id}/`, params);

  const deleteAssignment = (id: string | number) =>
    del(`/alerts/api/assignment/${id}/`);

  const patchAssignment = (id: string | number, params: any) =>
    patch(`/alerts/api/assignment/${id}/`, params);

  const getShieldList = (params: any) => get('/alerts/api/shield/', { params });

  const getShield = (id: string | number) => get(`/alerts/api/shield/${id}/`);

  const createShield = (params: any) => post('/alerts/api/shield/', params);

  const updateShield = (id: string | number, params: any) =>
    put(`/alerts/api/shield/${id}/`, params);

  const deleteShield = (id: string | number) =>
    del(`/alerts/api/shield/${id}/`);

  const patchShield = (id: string | number, params: any) =>
    patch(`/alerts/api/shield/${id}/`, params);

  return {
    getAssignmentList,
    getAssignment,
    createAssignment,
    updateAssignment,
    deleteAssignment,
    patchAssignment,
    getShieldList,
    getShield,
    createShield,
    updateShield,
    deleteShield,
    patchShield,
  };
};
