import { Pagination, TableDataItem } from '@/app/log/types';
import React from 'react';

export interface SearchTableProps {
  dataSource: TableDataItem[];
  pagination: Pagination;
  expand: boolean;
  loading?: boolean;
  onChange: (pagination: any) => void;
  addToQuery: (row: TableDataItem, type: string) => void;
}

export interface SearchParams {
  query?: string;
  start_time?: string;
  end_time?: string;
  field?: string;
  fields_limit?: number;
  step?: string;
  limit?: number | null;
}

export interface LogStream {
  fields: {
    _stream: string;
  };
  timestamps: string[];
  values: number[];
  total: number;
}

export interface DetailItem {
  instance_id: string;
  value: number;
}

export interface AggregatedResult {
  time: React.Key;
  value: number;
  detail: DetailItem[];
}

export interface LogTerminalProps {
  searchParams?: () => SearchParams;
  className?: string;
  fetchData?: (loading: boolean) => void;
}
