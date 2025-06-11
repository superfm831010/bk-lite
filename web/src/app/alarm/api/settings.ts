import useApiClient from '@/utils/request';

export const useSettingApi = () => {
  const { get, post, del, put } = useApiClient();

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

  return {
    getAssignmentList,
    getAssignment,
    createAssignment,
    updateAssignment,
    deleteAssignment,
  };
};
