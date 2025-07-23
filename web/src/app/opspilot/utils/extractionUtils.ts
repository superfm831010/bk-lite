export const getDefaultExtractionMethod = (extension: string): string => {
  const ext = extension.toLowerCase();
  
  if (ext === 'docx' || ext === 'doc') {
    return 'chapter';
  } else if (ext === 'xlsx' || ext === 'xls' || ext === 'csv') {
    return 'fullText';
  } else if (ext === 'pdf') {
    return 'page';
  } else {
    return 'fullText';
  }
};

export const getExtractionMethodMap = (method: string): string => {
  const methodMapping: Record<string, string> = {
    fullText: 'full',
    chapter: 'paragraph',
    page: 'page',
    worksheet: 'excel_full_content_parse',
    row: 'excel_header_row_parse',
  };
  return methodMapping[method] || 'full';
};

export const getReverseExtractionMethodMap = (value: string): string => {
  const reverseMapping: Record<string, string> = {
    full: 'fullText',
    paragraph: 'chapter',
    page: 'page',
    excel_full_content_parse: 'worksheet',
    excel_header_row_parse: 'row',
  };
  
  return reverseMapping[value] || 'fullText';
};