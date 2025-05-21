export const baseStates = ['pending', 'processing', 'unassigned'] as const;
export const allStates = [...baseStates, 'closed', 'recovered'] as const;
export const batchMenuKeys = ['close', 'assign', 'reassign', 'acknowledge'] as const;
export const incidentStates = ['pending', 'processing', 'closed'] as const;
