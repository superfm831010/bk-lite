import React, { useState, useCallback, ReactNode, useRef } from 'react';
import { Popconfirm, Button, Tooltip, Flex, ButtonProps } from 'antd';
import { FullscreenOutlined, FullscreenExitOutlined, SendOutlined } from '@ant-design/icons';
import { Bubble, Sender } from '@ant-design/x';
import { v4 as uuidv4 } from 'uuid';
import Icon from '@/components/icon';
import { useTranslation } from '@/utils/i18n';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';
import styles from '../custom-chat/index.module.scss';
import MessageActions from '../custom-chat/actions';
import KnowledgeBase from '../custom-chat/knowledgeBase';
import AnnotationModal from '../custom-chat/annotationModal';
import PermissionWrapper from '@/components/permission';
import { CustomChatMessage, Annotation } from '@/app/opspilot/types/global';
import { useSession } from 'next-auth/react';
import { useAuth } from '@/context/auth';

interface CustomChatSSEProps {
  handleSendMessage?: (userMessage: string) => Promise<{ url: string; payload: any }>;
  showMarkOnly?: boolean;
  initialMessages?: CustomChatMessage[];
  mode?: 'preview' | 'chat';
  guide?: string;
}

type ActionRender = (_: any, info: { components: { SendButton: React.ComponentType<ButtonProps>; LoadingButton: React.ComponentType<ButtonProps>; }; }) => ReactNode;

interface SSEChunk {
  choices: Array<{
    delta: {
      content?: string;
    };
    index: number;
    finish_reason: string | null;
  }>;
  id: string;
  object: string;
  created: number;
}

const md = new MarkdownIt({
  highlight: function (str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch { }
    }
    return '';
  },
});

const CustomChatSSE: React.FC<CustomChatSSEProps> = ({ 
  handleSendMessage, 
  showMarkOnly = false, 
  initialMessages = [], 
  mode = 'chat',
  guide
}) => {
  const { t } = useTranslation();
  const { data: session } = useSession();
  const authContext = useAuth();
  const token = session?.user?.token || authContext?.token || null;

  const [isFullscreen, setIsFullscreen] = useState(false);
  const [value, setValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<CustomChatMessage[]>(initialMessages.length ? initialMessages : []);
  const [annotationModalVisible, setAnnotationModalVisible] = useState(false);
  const [annotation, setAnnotation] = useState<Annotation | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const currentBotMessageRef = useRef<CustomChatMessage | null>(null);

  // Parse guide text and extract content within [] as quick send items
  const parseGuideItems = useCallback((guideText: string) => {
    if (!guideText) return { text: '', items: [], renderedHtml: '' };
    
    const regex = /\[([^\]]+)\]/g;
    const items: string[] = [];
    let match;
    
    // Extract all content within []
    while ((match = regex.exec(guideText)) !== null) {
      items.push(match[1]);
    }
    
    // Preserve line breaks, convert newlines to <br> tags first, then process [] content
    const processedText = guideText.replace(/\n/g, '<br>');
    
    // Convert [] content to clickable HTML elements
    const renderedHtml = processedText.replace(regex, (match, content) => {
      return `<span class="guide-clickable-item" data-content="${content}" style="color: #1890ff; cursor: pointer; font-weight: 600; margin: 0 2px;">${content}</span>`;
    });
    
    return { text: guideText, items, renderedHtml };
  }, []);

  // Handle click events for clickable elements in guide text
  const handleGuideClick = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    const target = event.target as HTMLElement;
    if (target.classList.contains('guide-clickable-item')) {
      const content = target.getAttribute('data-content');
      if (content && !loading && token) {
        handleSend(content);
      }
    }
  }, [loading, token]);

  const handleFullscreenToggle = () => {
    setIsFullscreen(!isFullscreen);
  };

  const handleClearMessages = () => {
    setMessages([]);
  };

  const stopSSEConnection = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setLoading(false);
  }, []);

  // Handle SSE streaming response
  const handleSSEStream = useCallback(async (url: string, payload: any, botMessage: CustomChatMessage) => {
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    try {
      // Use simplified request headers to avoid 406 errors
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Only add Authorization header when token exists
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload),
        credentials: 'include',
        signal: abortController.signal,
      });

      if (!response.ok) {
        console.error(`HTTP ${response.status}: ${response.statusText}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Check response type
      const contentType = response.headers.get('content-type');
      console.log('Response content-type:', contentType);

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('Failed to get response reader');
      }

      const decoder = new TextDecoder();
      let accumulatedContent = '';
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        
        // Process data line by line
        const lines = buffer.split('\n');
        // Keep the last line (might be incomplete)
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (trimmedLine === '') continue;
          
          // Process SSE data lines
          if (trimmedLine.startsWith('data: ')) {
            const dataStr = trimmedLine.slice(6).trim();
            
            // Check for end marker
            if (dataStr === '[DONE]') {
              console.log('SSE stream completed with [DONE]');
              setLoading(false);
              return;
            }

            try {
              const sseData: SSEChunk = JSON.parse(dataStr);
              
              // Process streaming content
              if (sseData.choices && sseData.choices.length > 0) {
                const choice = sseData.choices[0];
                
                // Check if completed
                if (choice.finish_reason === 'stop') {
                  console.log('SSE stream completed with finish_reason: stop');
                  setLoading(false);
                  return;
                }

                // Accumulate content
                if (choice.delta && choice.delta.content) {
                  accumulatedContent += choice.delta.content;
                  
                  // Update message content in real-time
                  setMessages(prevMessages => 
                    prevMessages.map(msgItem => 
                      msgItem.id === botMessage.id 
                        ? { 
                          ...msgItem, 
                          content: accumulatedContent,
                          updateAt: new Date().toISOString()
                        }
                        : msgItem
                    )
                  );
                }
              }
            } catch (parseError) {
              console.warn('Failed to parse SSE chunk:', dataStr, parseError);
              continue;
            }
          }
        }
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.log('SSE connection aborted');
        return;
      }
      
      console.error('SSE stream error:', error);
      
      // Update error message
      setMessages(prevMessages => 
        prevMessages.map(msgItem => 
          msgItem.id === botMessage.id 
            ? { ...msgItem, content: `${t('chat.connectionError')}: ${error.message}` }
            : msgItem
        )
      );
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  }, [token, t]);

  const handleSend = useCallback(async (msg: string) => {
    if (msg.trim() && !loading && token) {
      setLoading(true);
      
      // Create user message
      const newUserMessage: CustomChatMessage = {
        id: uuidv4(),
        content: msg,
        role: 'user',
        createAt: new Date().toISOString(),
        updateAt: new Date().toISOString(),
      };

      // Create bot loading message
      const botLoadingMessage: CustomChatMessage = {
        id: uuidv4(),
        content: '',
        role: 'bot',
        createAt: new Date().toISOString(),
        updateAt: new Date().toISOString(),
      };

      const updatedMessages = [...messages, newUserMessage, botLoadingMessage];
      setMessages(updatedMessages);
      currentBotMessageRef.current = botLoadingMessage;

      try {
        if (handleSendMessage) {
          const { url, payload } = await handleSendMessage(msg);
          await handleSSEStream(url, payload, botLoadingMessage);
        }
      } catch (error: any) {
        console.error(`${t('chat.sendFailed')}:`, error);
        
        setMessages(prevMessages => 
          prevMessages.map(msgItem => 
            msgItem.id === botLoadingMessage.id 
              ? { ...msgItem, content: t('chat.connectionError') }
              : msgItem
          )
        );
        setLoading(false);
      }
    }
  }, [loading, handleSendMessage, messages, t, token, handleSSEStream]);

  const handleCopyMessage = (content: string) => {
    navigator.clipboard.writeText(content).then(() => {
      console.log(t('chat.copied'));
    }).catch(err => {
      console.error(`${t('chat.copyFailed')}:`, err);
    });
  };

  const handleDeleteMessage = (id: string) => {
    setMessages(messages.filter(msg => msg.id !== id));
  };

  const handleRegenerateMessage = useCallback(async (id: string) => {
    const messageToRegenerate = messages.find(msg => msg.id === id);
    if (messageToRegenerate && token) {
      const lastUserMessage = messages.filter(msg => msg.role === 'user').pop();
      if (lastUserMessage) {
        setLoading(true);
        
        // Create new bot message
        const newMessage: CustomChatMessage = {
          id: uuidv4(),
          content: '',
          role: 'bot',
          createAt: new Date().toISOString(),
          updateAt: new Date().toISOString(),
        };

        const updatedMessages = [...messages, newMessage];
        setMessages(updatedMessages);
        currentBotMessageRef.current = newMessage;

        try {
          if (handleSendMessage) {
            const { url, payload } = await handleSendMessage(lastUserMessage.content);
            await handleSSEStream(url, payload, newMessage);
          }
        } catch (error: any) {
          console.error(`${t('chat.regenerateFailed')}:`, error);

          setMessages(prevMessages =>
            prevMessages.map(msgItem =>
              msgItem.id === newMessage.id
                ? { ...msgItem, content: t('chat.connectionError') }
                : msgItem
            )
          );
          setLoading(false);
        }
      }
    }
  }, [messages, handleSendMessage, t, token, handleSSEStream]);

  const renderContent = (msg: CustomChatMessage) => {
    const { content, knowledgeBase } = msg;
    return (
      <>
        <div
          dangerouslySetInnerHTML={{ __html: md.render(content || '...') }}
          className={styles.markdownBody}
        />
        {(Array.isArray(knowledgeBase) && knowledgeBase.length) ? <KnowledgeBase knowledgeList={knowledgeBase} /> : null}
      </>
    );
  };

  const renderSend = (props: ButtonProps & { ignoreLoading?: boolean; placeholder?: string } = {}) => {
    const { ignoreLoading, placeholder, ...btnProps } = props;

    return (
      <PermissionWrapper
        requiredPermissions={['Test']}>
        <Sender
          className={styles.sender}
          value={value}
          onChange={setValue}
          loading={loading}
          onSubmit={(msg: string) => {
            setValue('');
            handleSend(msg);
          }}
          placeholder={placeholder}
          onCancel={() => {
            stopSSEConnection();
          }}
          actions={((_: any, info: { components: { SendButton: React.ComponentType<ButtonProps>; LoadingButton: React.ComponentType<ButtonProps> } }) => {
            const { SendButton, LoadingButton } = info.components;
            if (!ignoreLoading && loading) {
              return (
                <Tooltip title={t('chat.clickCancel')}>
                  <LoadingButton />
                </Tooltip>
              );
            }
            let node: ReactNode = <SendButton {...btnProps} />;
            if (!ignoreLoading) {
              node = (
                <Tooltip title={value ? `${t('chat.send')}\u21B5` : t('chat.inputMessage')}>{node}</Tooltip>
              );
            }
            return node;
          }) as ActionRender}
        />
      </PermissionWrapper>
    );
  };

  const toggleAnnotationModal = (message: CustomChatMessage) => {
    if (message?.annotation) {
      setAnnotation(message.annotation);
    } else {
      const lastUserMessage = messages.slice(0, messages.indexOf(message)).reverse().find(msg => msg.role === 'user') as CustomChatMessage;
      setAnnotation({
        answer: message,
        question: lastUserMessage,
        selectedKnowledgeBase: '',
        tagId: 0,
      })
    }
    setAnnotationModalVisible(!annotationModalVisible);
  };

  const updateMessagesAnnotation = (id: string | undefined, newAnnotation?: Annotation) => {
    if (!id) return;
    setMessages((prevMessages) =>
      prevMessages.map((msg) =>
        msg.id === id
          ? { ...msg, annotation: newAnnotation }
          : msg
      )
    );
    setAnnotationModalVisible(false);
  };

  const handleSaveAnnotation = (annotation?: Annotation) => {
    updateMessagesAnnotation(annotation?.answer?.id, annotation);
  };

  const handleRemoveAnnotation = (id: string | undefined) => {
    if (!id) return;
    updateMessagesAnnotation(id, undefined);
  };

  // Cleanup SSE connection on component unmount
  React.useEffect(() => {
    return () => {
      stopSSEConnection();
    };
  }, [stopSSEConnection]);

  const guideData = parseGuideItems(guide || '');

  return (
    <div className={`rounded-lg h-full ${isFullscreen ? styles.fullscreen : ''}`}>
      {mode === 'chat' &&
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-base font-semibold">{t('chat.test')}</h2>
          <div>
            <button title="fullScreen" onClick={handleFullscreenToggle} aria-label="Toggle Fullscreen">
              {isFullscreen ? <FullscreenExitOutlined /> : <FullscreenOutlined />}
            </button>
          </div>
        </div>
      }
      <div className={`flex flex-col rounded-lg p-4 h-full overflow-hidden ${styles.chatContainer}`} style={{ height: isFullscreen ? 'calc(100vh - 70px)' : (mode === 'chat' ? 'calc(100% - 40px)' : '100%') }}>
        {/* Guide content display area */}
        {guide && guideData.renderedHtml && (
          <div className="mb-4 flex items-start gap-3" onClick={handleGuideClick}>
            <div className="flex-shrink-0 mt-1">
              <Icon type="jiqiren3" className={styles.guideAvatar} />
            </div>
            <div
              dangerouslySetInnerHTML={{ __html: guideData.renderedHtml }}
              className={`${styles.markdownBody} flex-1 p-3 bg-[var(--color-bg)] rounded-lg`}
            />
          </div>
        )}
        
        <div className="flex-1 chat-content-wrapper overflow-y-auto overflow-x-hidden pb-4">
          <Flex gap="small" vertical>
            {messages.map((msg) => (
              <Bubble
                key={msg.id}
                className={styles.bubbleWrapper}
                placement={msg.role === 'user' ? 'end' : 'start'}
                loading={msg.content === '' && loading}
                content={renderContent(msg)}
                avatar={{ icon: <Icon type={msg.role === 'user' ? 'yonghu' : 'jiqiren3'} className={styles.avatar} /> }}
                footer={msg.content === '' ? null : (
                  <MessageActions
                    message={msg}
                    onCopy={handleCopyMessage}
                    onRegenerate={handleRegenerateMessage}
                    onDelete={handleDeleteMessage}
                    onMark={toggleAnnotationModal}
                    showMarkOnly={showMarkOnly}
                  />
                )}
              />
            ))}
          </Flex>
        </div>
        
        {mode === 'chat' && (
          <>
            <div className="flex justify-end pb-2">
              <Popconfirm
                title={t('chat.clearConfirm')}
                okButtonProps={{ danger: true }}
                onConfirm={handleClearMessages}
                okText={t('chat.clear')}
                cancelText={t('common.cancel')}
              >
                <Button type="text" className="mr-2" icon={<Icon type="shanchu" className="text-2xl" />} />
              </Popconfirm>
            </div>
            <Flex vertical gap="middle">
              {renderSend({
                variant: 'text',
                placeholder: `${t('chat.inputPlaceholder')}`,
                color: 'primary',
                icon: <SendOutlined />,
                shape: 'default',
              })}
            </Flex>
          </>
        )}
      </div>
      {annotation && (
        <AnnotationModal
          visible={annotationModalVisible}
          showMarkOnly={showMarkOnly}
          annotation={annotation}
          onSave={handleSaveAnnotation}
          onRemove={handleRemoveAnnotation}
          onCancel={() => setAnnotationModalVisible(false)}
        />
      )}
    </div>
  );
};

export default CustomChatSSE;