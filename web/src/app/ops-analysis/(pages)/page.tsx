'use client';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function IntegrationPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace('/ops-analysis/view');
  }, [router]);
  return null;
}
