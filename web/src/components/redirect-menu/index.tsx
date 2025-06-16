'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { usePermissions } from '@/context/permissions';

export default function RedirectToFirstMenu() {
  const router = useRouter();
  const { menus, loading } = usePermissions();

  useEffect(() => {
    if (!loading && menus?.length > 0 && menus[0]?.url) {
      router.replace(menus[0].url);
    }
  }, [loading, menus, router]);

  return null;
}