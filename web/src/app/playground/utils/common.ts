const handleFileRead = (text: string) => {
  // 统一换行符为 \n
  const lines = text.replace(/\r\n|\r|\n/g, '\n')?.split('\n').filter(line => line.trim() !== '');
  if (!lines.length) return [];
  
  const headers = ['timestamp', 'value'];
  const data = lines.slice(1).map((line) => {
    const values = line.split(',');
    return headers.reduce((obj: Record<string, any>, key, idx) => {
      const value = values[idx];
      
      if (key === 'timestamp') {
        obj[key] = new Date(value).getTime() / 1000;
      } 
      // else if (key === 'label') {
      //   // 🎯 处理 label 字段：如果值不存在或为空或转换为 NaN，则设为 0
      //   const numValue = Number(value);
      //   obj[key] = (!value || value.trim() === '' || isNaN(numValue)) ? 0 : numValue;
      // }
      else {
        // 处理其他数字字段（如 value）
        const numValue = Number(value);
        obj[key] = isNaN(numValue) ? 0 : numValue;
      }
      
      // obj['index'] = index;
      return obj;
    }, {});
  });
  
  return data;
};

export {
  handleFileRead
}