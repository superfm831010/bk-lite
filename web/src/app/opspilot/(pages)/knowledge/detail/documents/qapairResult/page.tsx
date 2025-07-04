'use client';
import React, { useState, useEffect } from 'react';
import { Card, Input, Spin, Pagination, Divider } from 'antd';
import { useSearchParams } from 'next/navigation';
import { useTranslation } from '@/utils/i18n';
import ContentDrawer from '@/components/content-drawer';
import useContentDrawer from '@/app/opspilot/hooks/useContentDrawer';
import { useKnowledgeApi } from '@/app/opspilot/api/knowledge';
import Icon from '@/components/icon';

interface QAPair {
  id: string;
  question: string;
  answer: string;
}

const QAPairResultPage: React.FC = () => {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [qaPairsState, setQaPairsState] = useState<QAPair[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(20);
  const [totalItems, setTotalItems] = useState<number>(0);
  const searchParams = useSearchParams();
  const qaPairId = searchParams ? searchParams.get('qaPairId') : null;
  const { fetchQAPairDetails } = useKnowledgeApi();

  const {
    drawerVisible,
    drawerContent,
    showDrawer,
    hideDrawer,
  } = useContentDrawer();

  const fetchData = async (page: number, pageSize: number, searchValue?: string) => {
    if (qaPairId) {
      setLoading(true);
      try {
        const params = {
          qa_pair_id: parseInt(qaPairId, 10),
          page,
          page_size: pageSize,
          search_text: searchValue || ''
        };
        const data = await fetchQAPairDetails(params);
        setQaPairsState(data.items || []);
        setTotalItems(data.count || 0);
      } catch (error) {
        console.error(`${t('common.errorFetch')}: ${error}`);
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    fetchData(currentPage, pageSize, searchTerm);
  }, [qaPairId]);

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    setCurrentPage(1);
    fetchData(1, pageSize, value);
  };

  const handlePageChange = (page: number, pageSize?: number) => {
    setCurrentPage(page);
    if (pageSize) {
      setPageSize(pageSize);
    }
    fetchData(page, pageSize || 20, searchTerm);
  };

  const handleCardClick = (qaPair: QAPair) => {
    const content = `Q: ${qaPair.question}\n\nA: ${qaPair.answer}`;
    showDrawer(content);
  };

  return (
    <div className="w-full h-full">
      <div className="flex justify-end items-center mb-4">
        <Input.Search
          placeholder={`${t('common.search')}...`}
          allowClear
          enterButton
          size="middle"
          onSearch={handleSearch}
          style={{ width: '240px' }}
        />
      </div>
      {loading ? (
        <div className="flex justify-center items-center w-full h-full">
          <Spin size="large" />
        </div>
      ) : (
        <>
          <div className="h-[calc(100%-100px)] overflow-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4">
              {qaPairsState.map((qaPair) => (
                <div key={qaPair.id}>
                  <Card
                    size="small"
                    className="
                      min-h-[160px] cursor-pointer transition-all duration-200 ease-in-out
                      hover:-translate-y-0.5 hover:shadow-lg bg-[var(--color-fill-2)]
                      [&_.ant-card-body]:h-auto [&_.ant-card-body]:min-h-[120px] [&_.ant-card-body]:p-4
                    "
                    onClick={() => handleCardClick(qaPair)}
                    hoverable
                  >
                    <div className="flex flex-col h-full">
                      <div className="flex-1 flex flex-col">
                        <div className="flex-1 rounded-md transition-colors duration-200">
                          <div className="flex items-start gap-2">
                            <Icon type="question-circle-fill" className="text-lg mt-1 flex-shrink-0" />
                            <p className="
                              line-clamp-2 text-ellipsis overflow-hidden
                              leading-6 m-0 text-xs text-[var(--color-text-1)] font-medium
                            ">
                              {qaPair.question || '--'}
                            </p>
                          </div>
                        </div>
                      </div>
                      <Divider className="my-3" />
                      <div className="flex-1 flex flex-col">
                        <div className="flex-1 rounded-md transition-colors duration-200">
                          <div className="flex items-start gap-2">
                            <Icon type="answer" className="text-lg mt-1 flex-shrink-0" />
                            <p className="
                              line-clamp-2 text-ellipsis overflow-hidden
                              leading-6 m-0 text-xs text-[var(--color-text-3)]
                            ">
                              {qaPair.answer || '--'}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Card>
                </div>
              ))}
            </div>
          </div>
          <div className="flex justify-end mt-4">
            <Pagination
              current={currentPage}
              pageSize={pageSize}
              total={totalItems}
              onChange={handlePageChange}
              showSizeChanger
              pageSizeOptions={['10', '20', '50', '100']}
            />
          </div>
        </>
      )}
      <ContentDrawer
        visible={drawerVisible}
        onClose={hideDrawer}
        content={drawerContent}
      />
    </div>
  );
};

export default QAPairResultPage;