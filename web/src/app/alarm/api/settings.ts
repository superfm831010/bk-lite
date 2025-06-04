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

  const getAlarmSource = async (params: any) => {
    console.log('getAlarmSource', params);
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { key: '源A', value: 'sourceA' },
          { key: '源B', value: 'sourceB' },
        ]);
      }, 1000);
    });
  };

  const getConditionList = async (params: any) => {
    console.log('getConditionList', params);
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { name: 'equals', desc: '等于' },
          { name: 'includes', desc: '包含' },
          { name: 'regex', desc: '正则' },
          { name: 'not_includes', desc: '不包含' },
          { name: 'not_equals', desc: '不等于' },
        ]);
      }, 1000);
    });
  };

  const getRuleList = async (params: any) => {
    console.log('getRuleList', params);
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            name: 'title',
            verbose_name: '标题',
            source_name_list: ['源A', '源B'],
          },
          {
            name: 'source_name',
            verbose_name: '告警源',
            source_name_list: ['源A'],
          },
          { name: 'level', verbose_name: '级别', source_name_list: ['源B'] },
          { name: 'category', verbose_name: '类型对象', source_name_list: [] },
          { name: 'instance', verbose_name: '对象实例', source_name_list: [] },
          { name: 'content', verbose_name: '内容', source_name_list: [] },
        ]);
      }, 1000);
    });
  };

  return {
    getAlertAssignList,
    delAlertAssign,
    getAlarmSource,
    getConditionList,
    getRuleList,
  };
};
