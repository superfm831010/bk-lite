'use client';

import React from 'react';
import CommonProvider from '@/app/alarm/context/common';
import { AliveScope } from 'react-activation';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <CommonProvider>
      <AliveScope>{children}</AliveScope>
    </CommonProvider>
  );
}
