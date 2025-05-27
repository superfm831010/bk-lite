export const useSettingApi = () => {
  const getAlertAssignList = async (params: any) => {
    console.log('getAlertAssignList', params);
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          count: 2,
          items: [
            {
              id: '1',
              assignName: '分配规则1',
              description: '这是分配规则1的描述',
              created_at: Date.now(),
              updated_at: Date.now(),
            },
            {
              id: '2',
              assignName: '分配规则2',
              description: '这是分配规则2的描述',
              created_at: Date.now(),
              updated_at: Date.now(),
            },
          ],
        });
      }, 1000);
    });
  };
  const delAlertAssign = async (id: string | number) => {
    console.log('delAlertAssign', id);
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([]);
      }, 1000);
    });
  };
  return { getAlertAssignList, delAlertAssign };
};
