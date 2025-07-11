// Dynamic module data interface definition
export interface ModuleItem {
  name: string;
  display_name: string;
  children?: ModuleItem[];
}

// Utility function: Get only first-level module names
export const buildModulesMap = (modules: ModuleItem[]): string[] => {
  return modules.map(module => module.name);
};

// Utility function: Recursively build sub-module mapping (supports multi-level nesting)
export const buildSubModulesMap = (modules: ModuleItem[]): { [key: string]: string[] } => {
  const subModulesMap: { [key: string]: string[] } = {};
  
  const processModule = (module: ModuleItem) => {
    if (module.children && module.children.length > 0) {
      // Collect direct sub-modules
      subModulesMap[module.name] = module.children.map(child => child.name);
      
      // Recursively process sub-modules
      module.children.forEach(child => {
        processModule(child);
      });
    }
  };
  
  modules.forEach(module => {
    processModule(module);
  });
  
  return subModulesMap;
};

// Utility function: Recursively get all editable modules (including all levels of sub-modules)
export const buildEditableModules = (modules: ModuleItem[]): string[] => {
  const editableModules: string[] = [];
  
  const collectAllModules = (items: ModuleItem[]) => {
    items.forEach(item => {
      editableModules.push(item.name);
      if (item.children && item.children.length > 0) {
        collectAllModules(item.children);
      }
    });
  };
  
  collectAllModules(modules);
  return editableModules;
};

// Utility function: Build module tree structure (for supporting multi-level display)
export const buildModuleTree = (modules: ModuleItem[]): { [key: string]: ModuleItem } => {
  const moduleTree: { [key: string]: ModuleItem } = {};
  
  const processModule = (module: ModuleItem) => {
    moduleTree[module.name] = module;
    if (module.children && module.children.length > 0) {
      module.children.forEach(child => {
        processModule(child);
      });
    }
  };
  
  modules.forEach(module => {
    processModule(module);
  });
  
  return moduleTree;
};

// Constants definition - Maintain backward compatibility, but these will be overridden by dynamic data
export const SUB_MODULE_MAP: { [key: string]: string[] } = {
  provider: ['llm_model', 'embed_model', 'rerank_model', 'ocr_model']
};