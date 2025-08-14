import { useEffect, useRef } from 'react';

/**
 * 自定义轮询Hook
 * 遵循BK-Lite Web项目的定时器处理标准
 * 
 * @param callback 轮询执行的回调函数
 * @param interval 轮询间隔时间（毫秒）
 * @param enabled 是否启用轮询
 */
export const usePolling = (
  callback: () => void,
  interval: number,
  enabled: boolean
) => {
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const savedCallback = useRef(callback);

  // 保存最新的回调函数引用
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // 清理定时器函数
  const clearTimer = () => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  };

  // 定时器管理
  useEffect(() => {
    // 先清理之前的定时器
    clearTimer();

    if (!enabled) {
      return;
    }

    // 设置新的定时器
    timerRef.current = setTimeout(() => {
      savedCallback.current();
      // 递归设置下一次定时器
      if (enabled) {
        timerRef.current = setTimeout(savedCallback.current, interval);
      }
    }, interval);

    // 组件卸载时清理定时器
    return () => clearTimer();
  }, [interval, enabled]);

  // 组件卸载时确保清理定时器
  useEffect(() => {
    return () => clearTimer();
  }, []);

  return { clearTimer };
};

export default usePolling;