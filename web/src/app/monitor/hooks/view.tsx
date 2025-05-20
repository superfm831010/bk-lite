import { ApartmentOutlined, BarsOutlined } from '@ant-design/icons';

export const useTableOptions = () => {
  return [
    { value: 'list', icon: <BarsOutlined /> },
    { value: 'view', icon: <ApartmentOutlined /> },
  ]
}