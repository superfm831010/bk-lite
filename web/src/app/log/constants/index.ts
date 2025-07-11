const TIMEOUT_UNITS: string[] = ['s'];
const NODE_STATUS_MAP: Record<string, string> = {
  normal: 'green',
  inactive: 'yellow',
  unavailable: 'gray',
};

export { TIMEOUT_UNITS, NODE_STATUS_MAP };
