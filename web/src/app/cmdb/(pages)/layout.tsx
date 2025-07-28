'use client';

import React from 'react';
import CommonProvider from '@/app/cmdb/context/common';
import { AliveScope } from 'react-activation';

export default function CMDBLayout({ children }: { children: React.ReactNode }) {
  return (
    <CommonProvider>
      <AliveScope>
        {children}
      </AliveScope>
    </CommonProvider>
  );
}
