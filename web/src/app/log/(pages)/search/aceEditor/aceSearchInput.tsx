'use client';
import React, {
  useRef,
  useEffect,
  useImperativeHandle,
  forwardRef,
  useCallback,
  useMemo,
} from 'react';
import AceEditor from 'react-ace';
import ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/ext-language_tools';
import './customLuceneMode';
import './aceQueryInput';
import useIntegrationApi from '@/app/log/api/integration';
import styles from './aceSearchInput.module.scss';

// 字段值数据结构
interface FieldValueItem {
  value: string;
  hits: number;
}

// 字段配置
interface FieldData {
  caption: string;
  value: string;
  score: number;
  meta: string;
}

// 自动完成数据结构
interface CompletionItem {
  caption: string;
  value: string;
  score: number;
  meta: string;
}

export interface AceSearchInputProps {
  value?: string;
  onChange?: (value: string) => void;
  onPressEnter?: () => void;
  placeholder?: string;
  className?: string;
  fields?: string[]; // 字段名列表
  getTimeRange?: () => number[]; // 获取时间范围的方法
  addonAfter?: React.ReactNode;
  disabled?: boolean;
}

export interface AceSearchInputRef {
  setValue: (value: string) => void;
  getValue: () => string;
  focus: () => void;
}

const AceSearchInput = forwardRef<AceSearchInputRef, AceSearchInputProps>(
  (
    {
      value = '',
      onChange,
      onPressEnter,
      placeholder = '请输入搜索条件',
      className,
      fields = [],
      getTimeRange,
      addonAfter,
      disabled = false,
    },
    ref
  ) => {
    const editorRef = useRef<AceEditor>(null);
    const placeholderRef = useRef<HTMLSpanElement | null>(null);
    const contentRef = useRef<string>(value);
    const showPlaceholderRef = useRef<boolean>(!value);
    const valueMapsRef = useRef<Record<string, CompletionItem[]>>({});
    const onPressEnterRef = useRef<(() => void) | undefined>(onPressEnter);

    // 使用 API hook
    const { getFieldValues } = useIntegrationApi();

    // 更新回调函数的引用
    useEffect(() => {
      onPressEnterRef.current = onPressEnter;
    }, [onPressEnter]);

    // ACE 编辑器配置
    const aceOptions = useMemo(
      () => ({
        enableBasicAutocompletion: true,
        enableSnippets: false,
        enableLiveAutocompletion: true,
        printMarginColumn: 30,
        displayIndentGuides: false,
        enableEmmet: false,
        tabSize: 0,
        fontSize: 14,
        useWorker: false,
        showPrintMargin: false,
        enableMultiselect: true,
        readOnly: disabled,
        showFoldWidgets: false,
        fadeFoldWidgets: false,
        wrap: false,
        showGutter: false,
        highlightActiveLine: false,
        autoScrollEditorIntoView: true,
      }),
      [disabled]
    );

    // 字段数据转换
    const fieldData: FieldData[] = useMemo(() => {
      // 内置字段列表 - 这些字段在所有日志类型中都存在
      const builtInFields = ['_time', '_msg'];

      // 合并内置字段和传入的字段，去重
      const allFields = [...new Set([...builtInFields, ...fields])];

      return allFields.map((item) => ({
        caption: item,
        value: item,
        score: 9,
        meta: 'field',
      }));
    }, [fields]);

    // 获取字段值
    const getFieldValuesFromAPI = useCallback(
      async (fieldName: string): Promise<FieldValueItem[]> => {
        if (!getFieldValues) return [];

        try {
          const times = getTimeRange?.() || [];

          const params = {
            filed: fieldName, // 注意：API中使用的是 filed 而不是 field
            start_time: times[0] ? new Date(times[0]).toISOString() : '',
            end_time: times[1] ? new Date(times[1]).toISOString() : '',
            limit: 50,
          };

          const values = await getFieldValues(params);
          return values?.values || [];
        } catch (error) {
          console.error('Failed to fetch field values:', error);
          return [];
        }
      },
      [getFieldValues, getTimeRange]
    );

    // 处理字段值（转义特殊字符）
    const dealFieldValue = useCallback((val: string) => {
      return val.replace(/(\/)/g, '\\$1');
    }, []);

    // 设置自动完成数据
    const setCompleteData = useCallback(
      (
        tokens: any[],
        currentToken: any,
        currentTokenIdx: number,
        prefix: string,
        lastToken: any
      ) => {
        const combiningOperators: CompletionItem[] = [
          {
            caption: 'AND',
            value: 'AND ',
            score: 10,
            meta: 'operator',
          },
          {
            caption: 'OR',
            value: 'OR ',
            score: 10,
            meta: 'operator',
          },
        ];

        const operators: CompletionItem[] = [
          {
            caption: 'NOT',
            value: 'NOT ',
            score: 10,
            meta: 'operator',
          },
        ];

        const existsOperator: CompletionItem[] = [
          {
            caption: '_exists_:',
            value: '_exists_:',
            score: 10,
            meta: 'operator',
          },
        ];

        const fieldDataWithColon = fieldData.map((item) => {
          const { caption, value, ...remain } = item;
          return {
            caption: caption + ':',
            value: value + ':',
            ...remain,
          };
        });

        const _matchesFieldName = (prefix: string) => {
          return (field: CompletionItem) => field.caption.indexOf(prefix) >= 0;
        };
        const matchesFieldName = _matchesFieldName(prefix);

        const _lastNonEmptyToken = (tokens: any[], currentTokenIdx: number) => {
          return tokens
            .slice(0, currentTokenIdx)
            .reverse()
            .find(
              (token: any) => token.type !== 'text' || token.value.trim() !== ''
            );
        };
        const lastNonEmptyToken = _lastNonEmptyToken(tokens, currentTokenIdx);

        const isFollowingExistsOperator = (token: any) =>
          token?.value === existsOperator[0].caption;
        const isFollowingFieldName = (token: any) =>
          token?.type === 'keyword' && token.value.endsWith(':');

        const getValueList = (target: any) => {
          const key = (target?.value || '').slice(0, -1);
          return valueMapsRef.current[key] || [];
        };

        if (
          isFollowingFieldName(currentToken) &&
          !isFollowingExistsOperator(currentToken)
        ) {
          return getValueList(currentToken).filter(matchesFieldName);
        }

        if (
          isFollowingFieldName(lastToken) &&
          !isFollowingExistsOperator(lastToken)
        ) {
          return getValueList(lastToken).filter(matchesFieldName);
        }

        if (isFollowingExistsOperator(lastToken)) {
          return fieldData.filter(matchesFieldName);
        }

        if (
          currentToken?.type === 'string' ||
          (currentToken?.type === 'keyword' && !prefix)
        ) {
          return [];
        }

        if (
          !lastNonEmptyToken ||
          lastNonEmptyToken?.type === 'keyword.operator'
        ) {
          const result = [
            ...existsOperator,
            ...fieldDataWithColon,
            ...operators,
          ].filter(matchesFieldName);
          return result;
        }

        if (['string', 'text'].includes(lastToken?.type) || !lastToken) {
          const result = [
            ...combiningOperators,
            ...operators,
            ...existsOperator,
            ...fieldDataWithColon,
          ].filter(matchesFieldName);
          return result;
        }

        // 添加一个通用的字段匹配模式
        if (prefix && prefix.length > 0) {
          const result = [
            ...existsOperator,
            ...fieldDataWithColon,
            ...operators,
          ].filter(matchesFieldName);
          return result;
        }

        return [];
      },
      [fieldData]
    );

    // 处理输入变化
    const handleInput = useCallback(
      (val: string) => {
        contentRef.current = val;
        onChange?.(val);

        // 处理placeholder显示隐藏
        if (val && showPlaceholderRef.current) {
          showPlaceholderRef.current = false;
          if (placeholderRef.current) {
            placeholderRef.current.style.display = 'none';
          }
        }
        if (!val) {
          showPlaceholderRef.current = true;
          if (placeholderRef.current) {
            placeholderRef.current.style.display = 'block';
          }
        }
      },
      [onChange]
    );

    // 处理回车事件
    const handleKeyDown = (event: any) => {
      if (event.keyCode === 13) {
        event.preventDefault();
        onPressEnterRef.current?.();
      }
    };
    // 编辑器初始化
    const handleEditorLoad = useCallback(
      (editor: any) => {
        // 绑定change事件
        editor.getSession().on('change', () => {
          const value = editor.getValue();
          handleInput(value);

          // 当输入字段时，触发自动提示
          const doc = editor.getSession().getDocument();
          const lastToken = editor.session.getTokenAt(doc.getLength() - 1);
          if (
            lastToken?.type === 'keyword' &&
            lastToken?.value.endsWith(':') &&
            lastToken?.value !== '_exists_:'
          ) {
            const key = lastToken.value.slice(0, -1);
            if (!valueMapsRef.current[key]) {
              // 获取字段值建议列表
              getFieldValuesFromAPI(key).then((values) => {
                if (values && values.length > 0) {
                  valueMapsRef.current[key] = values.map(
                    (item: FieldValueItem) => ({
                      caption: item.value,
                      value: dealFieldValue(item.value),
                      score: 10,
                      meta: item.hits + ' hits',
                    })
                  );
                  editor.execCommand('startAutocomplete');
                }
              });
              return;
            }
            setTimeout(() => {
              editor.execCommand('startAutocomplete');
            }, 0);
          } else {
            // 在输入普通字符时也尝试触发自动完成
            // const currentValue = editor.getValue();
            const cursor = editor.getCursorPosition();
            const currentLine = editor.session.getLine(cursor.row);
            const beforeCursor = currentLine.substring(0, cursor.column);
            // 如果当前正在输入且不是在字段值模式下，尝试触发字段自动完成
            if (beforeCursor && !beforeCursor.includes(':')) {
              setTimeout(() => {
                editor.execCommand('startAutocomplete');
              }, 100);
            }
          }
        });

        // 给组件添加placeholder
        const editorElement = editor.container;
        const placeholderElement = document.createElement('span');
        placeholderElement.className = 'ace-placeholder';
        placeholderElement.textContent = placeholder || '请输入';
        placeholderRef.current = placeholderElement;
        editorElement.appendChild(placeholderElement);

        placeholderElement.onclick = () => {
          editor.focus();
        };

        editor.on('focus', () => {
          if (placeholderRef.current) {
            placeholderRef.current.style.display = 'none';
          }
        });

        editor.on('blur', () => {
          if (!contentRef.current && placeholderRef.current) {
            placeholderRef.current.style.display = 'block';
          }
        });

        // 自定义语法提示
        const lnTools = ace.require('ace/ext/language_tools');
        const completer = {
          getCompletions: (
            editors: any,
            session: any,
            pos: any,
            prefix: string,
            callback: any
          ) => {
            const tokens = session.getTokens(pos.row);
            const currentToken = session.getTokenAt(pos.row, pos.column);
            const currentTokenIdx = tokens.findIndex(
              (t: any) => t === currentToken
            );
            const lastToken =
              currentTokenIdx > 0 ? tokens[currentTokenIdx - 1] : null;
            const uniqResults = setCompleteData(
              tokens,
              currentToken,
              currentTokenIdx,
              prefix,
              lastToken
            );
            callback(null, uniqResults);
          },
        };

        // 自定义提示语法先清空本地缓存
        lnTools.setCompleters([]);
        // 添加自定义语法提示
        lnTools.addCompleter(completer);

        // 绑定键盘事件
        editor.keyBinding.addKeyboardHandler({
          handleKeyboard: (
            data: any,
            hash: any,
            keyString: string,
            keyCode: number,
            event: any
          ) => {
            if (keyCode === 13) {
              // Enter key
              handleKeyDown(event);
            } else if (keyCode === 32 && event.ctrlKey) {
              // Ctrl+Space 手动触发自动完成
              event.preventDefault();
              editor.execCommand('startAutocomplete');
              return { command: 'null' };
            }
          },
        });
      },
      [
        handleInput,
        getFieldValuesFromAPI,
        dealFieldValue,
        setCompleteData,
        handleKeyDown,
        placeholder,
      ]
    );

    // 暴露方法给父组件
    useImperativeHandle(
      ref,
      () => ({
        setValue: (val: string) => {
          if (editorRef.current) {
            const editor = (editorRef.current as any).editor;
            editor.setValue(val);
          }
        },
        getValue: () => {
          if (editorRef.current) {
            const editor = (editorRef.current as any).editor;
            return editor.getValue();
          }
          return '';
        },
        focus: () => {
          if (editorRef.current) {
            const editor = (editorRef.current as any).editor;
            editor.focus();
          }
        },
      }),
      []
    );

    // 监听 fields 变化，重新注册自动完成器
    useEffect(() => {
      if (editorRef.current) {
        const editor = (editorRef.current as any).editor;
        if (editor?.session) {
          const lnTools = ace.require('ace/ext/language_tools');
          const completer = {
            getCompletions: (
              editors: any,
              session: any,
              pos: any,
              prefix: string,
              callback: any
            ) => {
              const tokens = session.getTokens(pos.row);
              const currentToken = session.getTokenAt(pos.row, pos.column);
              const currentTokenIdx = tokens.findIndex(
                (t: any) => t === currentToken
              );
              const lastToken =
                currentTokenIdx > 0 ? tokens[currentTokenIdx - 1] : null;
              const uniqResults = setCompleteData(
                tokens,
                currentToken,
                currentTokenIdx,
                prefix,
                lastToken
              );
              callback(null, uniqResults);
            },
          };

          lnTools.setCompleters([]);
          lnTools.addCompleter(completer);
        }
      }
    }, [fieldData, setCompleteData]);

    // 初始化值
    useEffect(() => {
      if (value !== contentRef.current) {
        contentRef.current = value;
        showPlaceholderRef.current = !value;
      }
    }, [value]);

    return (
      <div
        className={`${styles.aceSearchInput} ${className || ''}`}
        style={{ position: 'relative' }}
      >
        <AceEditor
          ref={editorRef}
          mode="lucene"
          theme="ace-queryinput"
          value={value}
          onChange={handleInput}
          onLoad={handleEditorLoad}
          width="calc(100% - 36px)"
          height="32px"
          setOptions={aceOptions}
          editorProps={{ $blockScrolling: true }}
        />
        {addonAfter && <div className={styles.addonAfter}>{addonAfter}</div>}
      </div>
    );
  }
);

AceSearchInput.displayName = 'AceSearchInput';

export default AceSearchInput;
