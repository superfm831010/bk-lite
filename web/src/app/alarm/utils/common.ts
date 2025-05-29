// 深克隆
export const deepClone = (obj: any, hash = new WeakMap()) => {
  if (Object(obj) !== obj) return obj;
  if (obj instanceof Set) return new Set(obj);
  if (hash.has(obj)) return hash.get(obj);

  const result =
    obj instanceof Date
      ? new Date(obj)
      : obj instanceof RegExp
        ? new RegExp(obj.source, obj.flags)
        : obj.constructor
          ? new obj.constructor()
          : Object.create(null);

  hash.set(obj, result);

  if (obj instanceof Map) {
    Array.from(obj, ([key, val]) => result.set(key, deepClone(val, hash)));
  }

  // 复制函数
  if (typeof obj === 'function') {
    return function (this: unknown, ...args: unknown[]): unknown {
      return obj.apply(this, args);
    };
  }

  // 递归复制对象的其他属性
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      // File不做处理
      if (obj[key] instanceof File) {
        result[key] = obj[key];
        continue;
      }
      result[key] = deepClone(obj[key], hash);
    }
  }

  return result;
};
