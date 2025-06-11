'use client';

import React from 'react';
import CommonProvider from '@/app/alarm/context/common';

export default function Layout({ children }: { children: React.ReactNode }) {
  return <CommonProvider>{children}</CommonProvider>;
}
