'use client';

import React from 'react';
import CommonProvider from '@/app/alarm/context/common';

export const AlarmRootLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <CommonProvider>
      {children}
    </CommonProvider>
  );
};

export default AlarmRootLayout;
