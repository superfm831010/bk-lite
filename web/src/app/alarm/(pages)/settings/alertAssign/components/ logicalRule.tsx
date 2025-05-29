'use client';

import React, { useState } from 'react';
import type { SelectProps } from 'antd';
import { Button, Select, Input, Row, Col, Card } from 'antd';
import { PlusOutlined, MinusOutlined } from '@ant-design/icons';

interface Condition {
  field: string;
  operator: string;
  value: string;
}

interface ConditionGroup {
  conditions: Condition[];
}

const fieldOptions: SelectProps['options'] = [
  { value: 'alert_source', label: '告警源' },
  { value: 'severity', label: '告警级别' },
];

const operatorOptions: SelectProps['options'] = [
  { value: 'equals', label: '等于' },
  { value: 'not_equals', label: '不等于' },
];

const LogicalConditionBuilder: React.FC = () => {
  const [conditionGroups, setConditionGroups] = useState<ConditionGroup[]>([
    { conditions: [{ field: '', operator: '', value: '' }] },
  ]);

  const addCondition = (groupIndex: number) => {
    const newGroups = [...conditionGroups];
    newGroups[groupIndex].conditions.push({
      field: '',
      operator: '',
      value: '',
    });
    setConditionGroups(newGroups);
  };

  const removeCondition = (groupIndex: number, conditionIndex: number) => {
    const newGroups = [...conditionGroups];
    newGroups[groupIndex].conditions.splice(conditionIndex, 1);
    if (newGroups[groupIndex].conditions.length === 0) {
      newGroups.splice(groupIndex, 1);
    }
    setConditionGroups(newGroups);
  };

  const addConditionGroup = () => {
    setConditionGroups([
      ...conditionGroups,
      { conditions: [{ field: '', operator: '', value: '' }] },
    ]);
  };

  const removeConditionGroup = (groupIndex: number) => {
    const newGroups = [...conditionGroups];
    newGroups.splice(groupIndex, 1);
    setConditionGroups(newGroups);
  };

  const onConditionChange = (
    groupIndex: number,
    conditionIndex: number,
    field: keyof Condition,
    value: string
  ) => {
    const newGroups = [...conditionGroups];
    newGroups[groupIndex].conditions[conditionIndex][field] = value;
    setConditionGroups(newGroups);
  };

  return (
    <div style={{ padding: '20px' }}>
      {conditionGroups.map((group, groupIndex) => (
        <Row
          key={groupIndex}
          gutter={16}
          align="middle"
          style={{
            marginBottom: '16px',
            position: 'relative',
            display: 'flex',
          }}
        >
          <Col
            span={2}
            style={{
              position: 'relative',
              display: 'flex',
              justifyContent: 'center',
            }}
          >
            {/* 左侧固定圆圈 */}
            <div
              style={{
                width: 24,
                height: 24,
                lineHeight: 24,
                zIndex: 1,
                border: '1px solid #1890ff',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: '#fff',
              }}
            >
              且
            </div>
          </Col>

          {/* 组间实线 */}
          {
            <div
              style={{
                position: 'absolute',
                width: 1,
                left: 26,
                top: groupIndex ? 0 : 'calc(50% + 10px)',
                height: groupIndex ? 'calc(100% + 16px)' : 'calc(50% + 6px)',
                transform: 'translateX(-50%)',
                background: '#1890ff',
              }}
            />
          }

          <Col span={22}>
            <Card
              style={{
                position: 'relative',
                border: '1px solid #d9d9d9',
              }}
            >
              <Button
                type="default"  
                size="small"
                danger
                shape="circle"
                icon={<MinusOutlined />}
                onClick={() => removeConditionGroup(groupIndex)}
                style={{
                  position: 'absolute',
                  top: -12,
                  right: -12,
                  zIndex: 1,
                }}
              />
              {group.conditions.map((condition, conditionIndex) => (
                <Row
                  key={conditionIndex}
                  align="middle"
                  gutter={16}
                  style={{
                    marginBottom:
                      conditionIndex < group.conditions.length - 1
                        ? '8px'
                        : '0',
                  }}
                >
                  <Col span={5}>
                    <Select
                      placeholder="请选择字段"
                      value={condition.field}
                      options={fieldOptions}
                      onChange={(value) =>
                        onConditionChange(
                          groupIndex,
                          conditionIndex,
                          'field',
                          value
                        )
                      }
                      style={{ width: '100%' }}
                    />
                  </Col>
                  <Col span={5}>
                    <Select
                      placeholder="请选择操作"
                      value={condition.operator}
                      options={operatorOptions}
                      onChange={(value) =>
                        onConditionChange(
                          groupIndex,
                          conditionIndex,
                          'operator',
                          value
                        )
                      }
                      style={{ width: '100%' }}
                    />
                  </Col>
                  <Col span={8}>
                    <Input
                      placeholder="请输入值"
                      value={condition.value}
                      onChange={(e) =>
                        onConditionChange(
                          groupIndex,
                          conditionIndex,
                          'value',
                          e.target.value
                        )
                      }
                    />
                  </Col>
                  <Col span={2}>
                    <Button
                      type="default"
                      size="small"
                      shape="circle"
                      icon={<PlusOutlined />}
                      onClick={() => addCondition(groupIndex)}
                    />
                  </Col>
                  <Col span={2}>
                    <Button
                      type="default"
                      size="small"
                      shape="circle"
                      icon={<MinusOutlined />}
                      onClick={() =>
                        removeCondition(groupIndex, conditionIndex)
                      }
                    />
                  </Col>
                </Row>
              ))}
            </Card>
          </Col>
        </Row>
      ))}
      <Button
        type="dashed"
        onClick={addConditionGroup}
        style={{ marginTop: '2px' }}
      >
        <PlusOutlined /> 新增条件组
      </Button>
    </div>
  );
};

export default LogicalConditionBuilder;
