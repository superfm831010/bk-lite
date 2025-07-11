'use client';

import CommonProvider from '@/app/log/context/common';
import '@/app/log/styles/index.css';
import useApiClient from '@/utils/request';

export default function RootLog({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { isLoading } = useApiClient();
  return <CommonProvider>{isLoading ? null : children}</CommonProvider>;
}
