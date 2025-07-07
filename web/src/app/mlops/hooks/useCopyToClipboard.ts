import { useState } from 'react';
import { message } from 'antd';

export const useCopyToClipboard = () => {
  const [isCopying, setIsCopying] = useState(false);

  const copyToClipboard = async (text: string, successMessage = '复制成功') => {
    if (!text) {
      message.warning('没有可复制的内容');
      return false;
    }

    setIsCopying(true);

    try {
      // Clipboard API
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        // 降级
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.left = '0';
        textArea.style.top = '0';
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);

        if (!successful) {
          throw new Error('execCommand failed');
        }
      }

      message.success(successMessage);
      return true;
    } catch (e) {
      console.log(e);
      message.error('复制失败');
    } finally {
      setIsCopying(false);
    }
  };

  return { copyToClipboard, isCopying };
}