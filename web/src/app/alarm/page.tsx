'use client';
import React from 'react';
import { Card, Table } from 'antd';
import { Line } from '@ant-design/charts';

const DashboardPage: React.FC = () => {
  // Mock 数据
  const cardData = [
    { title: 'Card 1', value: 100 },
    { title: 'Card 2', value: 200 },
    { title: 'Card 3', value: 300 },
    { title: 'Card 4', value: 400 },
  ];

  const lineData = [
    { date: '2023-01-01', value: 30 },
    { date: '2023-01-02', value: 40 },
    { date: '2023-01-03', value: 35 },
    { date: '2023-01-04', value: 50 },
  ];

  const tableData = [
    { key: '1', name: 'John Brown', age: 32, address: 'New York No. 1 Lake Park' },
    { key: '2', name: 'Jim Green', age: 42, address: 'London No. 1 Lake Park' },
    { key: '3', name: 'Joe Black', age: 32, address: 'Sidney No. 1 Lake Park' },
  ];

  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Age', dataIndex: 'age', key: 'age' },
    { title: 'Address', dataIndex: 'address', key: 'address' },
  ];

  const lineConfig = {
    data: lineData,
    xField: 'date',
    yField: 'value',
    point: { size: 5, shape: 'diamond' },
    height: 200, // 调整折线图高度
  };

  return (
    <div className="container mx-auto p-6 min-h-screen">
      <div className="grid grid-cols-4 gap-6">
        {cardData.map((card, index) => (
          <div key={index} className="col-span-1">
            <Card title={card.title} className="w-full shadow-lg rounded-lg">{card.value}</Card>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-2 gap-6 mt-6">
        <div className="col-span-1">
          <Card title="Line Chart 1" className="w-full shadow-lg rounded-lg">
            <Line {...lineConfig} />
          </Card>
        </div>
        <div className="col-span-1">
          <Card title="Line Chart 2" className="w-full shadow-lg rounded-lg">
            <Line {...lineConfig} />
          </Card>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-6 mt-6">
        <div className="col-span-1">
          <Card title="Table 1" className="w-full shadow-lg rounded-lg">
            <Table dataSource={tableData} columns={columns} pagination={false} />
          </Card>
        </div>
        <div className="col-span-1">
          <Card title="Table 2" className="w-full shadow-lg rounded-lg">
            <Table dataSource={tableData} columns={columns} pagination={false} />
          </Card>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;