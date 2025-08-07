export interface SelectOption {
  value: string;
  title: string;
  subTitle: string;
}

export const SOURCE_FILE_OPTIONS: SelectOption[] = [
  {
    value: 'file',
    title: 'knowledge.localFile',
    subTitle: 'knowledge.fileSubTitle',
  },
  {
    value: 'web_page',
    title: 'knowledge.webLink',
    subTitle: 'knowledge.linkSubTitle',
  },
  {
    value: 'manual',
    title: 'knowledge.cusText',
    subTitle: 'knowledge.cusTextSubTitle',
  },
];

export const QA_PAIR_OPTIONS: SelectOption[] = [
  {
    value: 'documents',
    title: 'knowledge.qaPairs.generate',
    subTitle: 'knowledge.qaPairs.generateDesc',
  },
  {
    value: 'import',
    title: 'knowledge.qaPairs.import',
    subTitle: 'knowledge.qaPairs.importDesc',
  },
  {
    value: 'custom',
    title: 'knowledge.qaPairs.custom',
    subTitle: 'knowledge.qaPairs.customDesc',
  }
];

export const KNOWLEDGE_TAB_KEYS = {
  SOURCE_FILES: 'source_files',
  QA_PAIRS: 'qa_pairs',
  KNOWLEDGE_GRAPH: 'knowledge_graph',
} as const;

export const DOCUMENT_TYPES = {
  FILE: 'file',
  WEB_PAGE: 'web_page',
  MANUAL: 'manual',
} as const;