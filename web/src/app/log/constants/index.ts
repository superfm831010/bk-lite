const TIMEOUT_UNITS: string[] = ['s'];
const M_TIMEOUT_UNITS: string[] = ['ms'];
const NODE_STATUS_MAP: Record<string, string> = {
  normal: 'green',
  inactive: 'yellow',
  unavailable: 'gray',
};

export { TIMEOUT_UNITS, NODE_STATUS_MAP, M_TIMEOUT_UNITS };
