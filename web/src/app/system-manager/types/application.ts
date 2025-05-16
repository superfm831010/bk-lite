export interface Role {
  id: number;
  name: string;
}

export interface User {
  id: string;
  name: string;
  group: string;
  roles: string[];
  username?: string;
}

export interface Menu {
  name: string;
  display_name?: string;
  operation?: string[];
  children?: Menu[];
}

