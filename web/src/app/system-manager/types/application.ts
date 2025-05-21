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

export interface IconGlyph {
  icon_id: string;
  name: string;
  font_class: string;
  unicode: string;
  unicode_decimal: number;
}

export interface IconFontData {
  id: string;
  name: string;
  font_family: string;
  css_prefix_text: string;
  description: string;
  glyphs: IconGlyph[];
}

export interface ApplicationFormData {
  name: string;
  display_name: string;
  description: string;
  url: string;
  icon?: string | null;
  tags?: string[];
}

export interface ApplicationFormModalProps {
  visible: boolean;
  initialData?: ApplicationFormData;
  isEdit?: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

