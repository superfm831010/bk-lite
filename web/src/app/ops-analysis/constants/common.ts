export interface ChartTypeItem {
  label: string;
  value: string;
}

export const getChartTypeList = (): ChartTypeItem[] => {
  return [
    { label: 'dataSource.lineChart', value: 'line' },
    { label: 'dataSource.barChart', value: 'bar' },
    { label: 'dataSource.pieChart', value: 'pie' },
    { label: 'dataSource.singleValue', value: 'single' },
  ];
};