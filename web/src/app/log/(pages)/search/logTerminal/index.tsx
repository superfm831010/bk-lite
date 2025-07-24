'use client';
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Button, Tooltip } from 'antd';
import {
  FullscreenOutlined,
  FullscreenExitOutlined,
  ClearOutlined,
  PauseOutlined,
  CaretRightOutlined,
} from '@ant-design/icons';
import { LogTerminalProps } from '@/app/log/types/search';
import terminalstyles from './index.module.scss';
import { useAuth } from '@/context/auth';
import useApiClient from '@/utils/request';
import { useTranslation } from '@/utils/i18n';

const LogTerminal: React.FC<LogTerminalProps> = ({
  searchParams,
  className = '',
  fetchData,
}) => {
  const { isLoading } = useApiClient();
  const { t } = useTranslation();
  const authContext = useAuth();
  const token = authContext?.token || null;
  const tokenRef = useRef(token);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const logContainerRef = useRef<HTMLDivElement>(null);
  const readerRef = useRef<ReadableStreamDefaultReader<Uint8Array> | null>(
    null
  );
  const containerRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // 自动滚动到底部
  const scrollToBottom = useCallback(() => {
    if (logContainerRef.current && !isPaused) {
      logContainerRef.current.scrollTo({
        top: logContainerRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [isPaused]);

  // 处理全屏切换
  const toggleFullscreen = useCallback(() => {
    if (!containerRef.current) return;
    if (!isFullscreen) {
      containerRef.current.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  }, [isFullscreen]);

  // 开始日志流
  const startLogStream = useCallback(async () => {
    if (isStreaming) return;
    try {
      setIsStreaming(true);
      // 创建AbortController用于取消请求
      const abortController = new AbortController();
      abortControllerRef.current = abortController;
      // 获取搜索参数
      const params = searchParams?.();
      // 构建查询参数
      const queryParams = new URLSearchParams({
        query: params?.query || '*',
      });
      // 直接使用fetch来处理EventStream，使用GET请求
      fetchData?.(true);
      const response = await fetch(
        `/api/proxy/log/search/tail?${queryParams.toString()}`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${tokenRef.current}`,
          },
          signal: abortController.signal,
        }
      );
      fetchData?.(false);
      // 检查响应状态
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // 检查响应是否包含可读流
      if (!response.body) {
        setIsStreaming(false);
        return;
      }
      const reader = response.body.getReader();
      readerRef.current = reader;
      const decoder = new TextDecoder();
      // 持续读取流数据
      while (!abortController.signal.aborted) {
        try {
          const { done, value } = await reader.read();
          if (done) {
            break;
          }
          const chunk = decoder.decode(value, { stream: true });
          // 处理Server-Sent Events格式的数据
          const lines = chunk.split('\n');
          for (const line of lines) {
            const trimmed = line.trim();
            // 跳过空行和SSE协议行
            if (
              !trimmed ||
              trimmed.startsWith('event:') ||
              trimmed === 'data:'
            ) {
              continue;
            }
            // 处理data:开头的数据行
            if (trimmed.startsWith('data:')) {
              const data = trimmed.substring(5).trim(); // 移除"data:"前缀
              if (data && data !== '[DONE]') {
                try {
                  // 尝试解析JSON数据
                  const logData = JSON.parse(data);
                  const logMessage = logData.message || logData.log || data;
                  setLogs((prevLogs) => {
                    const newLogs = [...prevLogs, logMessage];
                    return newLogs.slice(-1000); // 限制日志条数
                  });
                } catch {
                  // 如果不是JSON，直接作为文本处理
                  setLogs((prevLogs) => {
                    const newLogs = [...prevLogs, data];
                    return newLogs.slice(-1000);
                  });
                }
              }
            } else if (trimmed) {
              // 处理非SSE格式的普通文本
              setLogs((prevLogs) => {
                const newLogs = [...prevLogs, trimmed];
                return newLogs.slice(-1000);
              });
            }
          }
        } catch (error: any) {
          if (error?.name === 'AbortError') {
            console.log('Log stream was cancelled');
            break;
          }
          break;
        }
      }
    } catch (error: any) {
      console.log(error);
      fetchData?.(false);
    } finally {
      setIsStreaming(false);
      if (readerRef.current) {
        try {
          readerRef.current.releaseLock();
        } catch {
          // Reader可能已经被释放
        }
        readerRef.current = null;
      }
      abortControllerRef.current = null;
    }
  }, [searchParams, isStreaming]);

  // 停止日志流
  const stopLogStream = useCallback(() => {
    setIsStreaming(false);
    // 优先使用AbortController来取消请求，这会自动处理reader
    if (abortControllerRef.current) {
      try {
        abortControllerRef.current.abort();
      } catch {
        // AbortController可能已经被取消
      }
      abortControllerRef.current = null;
    }
    // 如果reader还存在，手动清理
    if (readerRef.current) {
      try {
        readerRef.current.releaseLock();
      } catch {
        // Lock可能已经被释放
      }
      readerRef.current = null;
    }
  }, []);

  // 清空日志
  const clearLogs = useCallback(() => {
    setLogs([]);
  }, []);

  // 切换暂停状态
  const togglePause = useCallback(() => {
    setIsPaused((prev) => !prev);
  }, []);

  // 自动滚动效果
  useEffect(() => {
    scrollToBottom();
  }, [logs, scrollToBottom]);

  // 组件挂载时自动开始日志流
  useEffect(() => {
    if (!isLoading) {
      startLogStream();
    }
    return () => {
      stopLogStream();
    };
  }, [stopLogStream, isLoading]);

  // 监听全屏状态变化
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className={`${terminalstyles.logTerminal} ${
        isFullscreen ? terminalstyles.fullscreen : ''
      } ${className}`}
    >
      <div className={terminalstyles.terminalHeader}>
        <div className={terminalstyles.controls}>
          <Tooltip
            autoAdjustOverflow
            getPopupContainer={(trigger) =>
              trigger.parentElement || document.body
            }
            title={
              isPaused
                ? t('log.search.enableScrolling')
                : t('log.search.stopScrolling')
            }
          >
            <Button
              size="small"
              icon={isPaused ? <CaretRightOutlined /> : <PauseOutlined />}
              onClick={togglePause}
            />
          </Tooltip>
          <Tooltip
            title={t('log.search.clearLogs')}
            autoAdjustOverflow
            getPopupContainer={(trigger) =>
              trigger.parentElement || document.body
            }
          >
            <Button size="small" icon={<ClearOutlined />} onClick={clearLogs} />
          </Tooltip>
          <Tooltip
            title={isFullscreen ? t('log.search.exit') : t('log.search.full')}
            autoAdjustOverflow
            getPopupContainer={(trigger) =>
              trigger.parentElement || document.body
            }
          >
            <Button
              size="small"
              icon={
                isFullscreen ? (
                  <FullscreenExitOutlined />
                ) : (
                  <FullscreenOutlined />
                )
              }
              onClick={toggleFullscreen}
            />
          </Tooltip>
        </div>
      </div>
      <div ref={logContainerRef} className={terminalstyles.logContainer}>
        {logs.map((log, index) => (
          <div key={index} className={terminalstyles.logLine}>
            <span className={terminalstyles.lineNumber}>{index + 1}</span>
            <span className={terminalstyles.logContent}>{log}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LogTerminal;
