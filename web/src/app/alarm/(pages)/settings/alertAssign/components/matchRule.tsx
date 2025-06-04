'use client';

import React, { useState, useEffect } from 'react';
import styles from './match.module.scss';
import { useTranslation } from '@/utils/i18n';
import { useSettingApi } from '@/app/alarm/api/settings';
import { Select, Button, Input } from 'antd';
import { PlusCircleOutlined, MinusCircleOutlined } from '@ant-design/icons';
import { useCommon } from '@/app/alarm/context/common';

const { Option } = Select;

interface PolicyItem {
  target_key: string;
  condition: string;
  target_value: string;
  event_choose_list: { key: string; value: string }[];
}

const RulesMatch: React.FC = () => {
  const { getAlarmSource, getConditionList, getRuleList } = useSettingApi();
  const { levelList } = useCommon();
  const { t } = useTranslation();
  const [showSelect, setShowSelect] = useState(true);
  const [sourceList, setSourceList] = useState<any[]>([]);
  const [conditionList, setConditionList] = useState<any[]>([]);
  const [ruleList, setRuleList] = useState<any[]>([]);
  const [policyList, setPolicyList] = useState<PolicyItem[][]>([
    [
      {
        target_key: '',
        condition: '',
        target_value: '',
        event_choose_list: [],
      },
    ],
  ]);
  const policyItem: PolicyItem[] = [
    {
      target_key: '',
      condition: '',
      target_value: '',
      event_choose_list: [],
    },
  ];

  const conDisabledList = [
    'bk_biz_name',
    'bk_biz_id',
    'source_id',
    'level',
    'source_name',
    'event_id',
    'alarm_time',
    'item',
    'action',
  ];

  const valueInputList = [
    'bk_biz_name',
    'bk_biz_id',
    'source_id',
    'level',
    'source_name',
  ];

  useEffect(() => {
    fetchRuleList();
    fetchConditionList();
  }, []);

  const changeSelect = async (
    val: string,
    index: number,
    ind: number,
    type?: any
  ) => {
    const updatedPolicyList = [...policyList];
    const item = updatedPolicyList[index][ind];
    item.target_key = val;

    if (!type) {
      item.condition = '';
    }
    setShowSelect(false);

    if (val === 'level') {
      item.event_choose_list = levelList.map((el: any) => ({
        value: el.value,
        key: el.label,
      }));
    } else if (val === 'source_name' || val === 'source_id') {
      if (sourceList.length === 0) {
        await fetchAlarmSource();
      }
      item.event_choose_list = sourceList;
    } else if (val === 'bk_biz_name' || val === 'bk_biz_id') {
      item.event_choose_list = normalBusinessList.map((el) => ({
        value: el.bk_biz_id,
        key: el.bk_biz_name,
      }));
    }
    setPolicyList(updatedPolicyList);
    setShowSelect(true);
  };

  const addOr = () => {
    setPolicyList([...policyList, JSON.parse(JSON.stringify(policyItem))]);
  };

  const deleteOr = (index: number) => {
    const updatedPolicyList = [...policyList];
    updatedPolicyList.splice(index, 1);
    setPolicyList(updatedPolicyList);
  };

  const addAnd = (index: number) => {
    const updatedPolicyList = [...policyList];
    updatedPolicyList[index].push({ ...policyItem[0] });
    setPolicyList(updatedPolicyList);
  };

  const deleteAnd = (index: number, ind: number) => {
    const updatedPolicyList = [...policyList];
    updatedPolicyList[index].splice(ind, 1);
    setPolicyList(updatedPolicyList);
  };

  const fetchAlarmSource = async () => {
    const data: any = await getAlarmSource({});
    if (data) {
      setSourceList(data);
    } else {
      console.error('获取告警源列表失败');
    }
  };

  const fetchConditionList = async () => {
    const data: any = await getConditionList({});
    if (data) {
      setConditionList(data);
    } else {
      console.error('获取条件列表失败');
    }
  };

  const fetchRuleList = async () => {
    const data: any = await getRuleList({});
    if (data) {
      setRuleList(data);
    } else {
      console.error('获取规则列表失败');
    }
  };

  const normalBusinessList = [
    { bk_biz_id: '1', bk_biz_name: '业务A' },
    { bk_biz_id: '2', bk_biz_name: '业务B' },
  ];

  return (
    <div className="pl-[2px] border-l border-[#c4c6cc] w-full ml-[13px]">
      {policyList.map((orItem, index) => (
        <div key={index} className="relative -left-[15px] pb-[15px]">
          <div className={`absolute text-center ${styles.ruleOr}`}>或</div>
          <div className="bg-gray-100 ml-[33px] relative top-[17px]">
            <div className="px-[16px] py-[16px] space-y-4">
              {orItem.map((i, ind) => (
                <div key={ind} className="relative">
                  <div className={`ml-[10px] flex items-center`}>
                    <div className={styles.ruleAnd}>且</div>
                    <div className={styles.ruleItem}>
                      <div className={styles.keySelect}>
                        <Select
                          allowClear
                          value={i.target_key}
                          disabled={false}
                          placeholder={`${t('common.selectMsg')}`}
                          onChange={(value) => changeSelect(value, index, ind)}
                        >
                          {ruleList.map((item) => (
                            <Option key={item.name} value={item.name}>
                              {item.verbose_name}
                            </Option>
                          ))}
                        </Select>
                      </div>
                      <div className={styles.condSelect}>
                        <Select
                          allowClear
                          value={i.condition}
                          disabled={false}
                          placeholder={`${t('common.selectMsg')}`}
                          onChange={(value) => {
                            const updatedPolicyList = [...policyList];
                            updatedPolicyList[index][ind].condition = value;
                            setPolicyList(updatedPolicyList);
                          }}
                        >
                          {conditionList.map((item) => (
                            <Option
                              key={item.name}
                              value={item.name}
                              disabled={
                                conDisabledList.includes(i.target_key) &&
                                !['term', 'must_not_term'].includes(item.name)
                              }
                            >
                              {item.desc}
                            </Option>
                          ))}
                        </Select>
                      </div>
                      <div className={styles.valueInput}>
                        {valueInputList.includes(i.target_key) && showSelect ? (
                          <Select
                            value={i.target_value}
                            showSearch
                            placeholder={`${t('common.selectMsg')}`}
                            onChange={(value) => {
                              const updatedPolicyList = [...policyList];
                              updatedPolicyList[index][ind].target_value =
                                value;
                              setPolicyList(updatedPolicyList);
                            }}
                          >
                            {i.event_choose_list.map((ite) => (
                              <Option
                                key={ite.key}
                                value={
                                  ['bk_biz_name', 'source_name'].includes(
                                    i.target_key
                                  )
                                    ? ite.key
                                    : ite.value
                                }
                              >
                                {ite.key}
                              </Option>
                            ))}
                          </Select>
                        ) : (
                          <Input
                            value={i.target_value}
                            placeholder={t('common.inputMsg')}
                            onChange={(e) => {
                              const updatedPolicyList = [...policyList];
                              updatedPolicyList[index][ind].target_value =
                                e.target.value;
                              setPolicyList(updatedPolicyList);
                            }}
                          />
                        )}
                      </div>
                      <span className={styles.action}>
                        <PlusCircleOutlined
                          title="新增"
                          style={{
                            fontSize: '16px',
                            color: '#979BA5',
                            cursor: 'pointer',
                          }}
                          onClick={() => addAnd(index)}
                        />
                      </span>
                      <span className={styles.action}>
                        {orItem.length > 1 && (
                          <MinusCircleOutlined
                            title="删除"
                            style={{
                              fontSize: '16px',
                              color: '#979BA5',
                              cursor: 'pointer',
                            }}
                            onClick={() => deleteAnd(index, ind)}
                          />
                        )}
                      </span>
                    </div>

                    {ind > 0 && (
                      <div className="absolute left-[12px] -top-[20px] h-[25px] border-l border-[#c4c6cc]"></div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
          {policyList.length > 1 && (
            <MinusCircleOutlined
              onClick={() => deleteOr(index)}
              className="absolute right-[-5px] top-[10px] text-[18px] text-[#979BA5] cursor-pointer z-10"
            />
          )}
        </div>
      ))}
      <div className="relative -left-[15px] transform translate-y-[5px]">
        <Button onClick={addOr} size="small" className="add-button">
          <div className="relative text-[22px] text-[#979BA5] -top-[2px]">
            +
          </div>
        </Button>
      </div>
    </div>
  );
};

export default RulesMatch;
