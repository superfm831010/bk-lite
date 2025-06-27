import { useSession } from 'next-auth/react';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';

dayjs.extend(utc);
dayjs.extend(timezone);

export const useLocalizedTime = () => {
  const { data: session } = useSession();

  const convertToLocalizedTime = (
    isoString: string,
    format: string = 'YYYY-MM-DD HH:mm:ss'
  ): string => {
    if (!session || !session.user) {
      return dayjs(isoString).format(format);
    }

    const date = dayjs(isoString).tz("Asia/Shanghai");
    return date.format(format);
  };

  return {
    convertToLocalizedTime,
  };
};
