export interface ModelConfig {
    openai_api_key?: string;
    api_key?: string;
    openai_base_url?: string;
    base_url?: string;
    model?: string;
}

export interface Model {
    id: number;
    name: string;
    enabled: boolean;
    is_build_in?: boolean;
    team?: boolean;
    llm_model_type?: string;
    model_type?: string;
    model_type_name?: string;
    icon?: string;
    llm_config?: ModelConfig;
    embed_config?: ModelConfig;
    rerank_config?: ModelConfig;
    ocr_config?: ModelConfig;
    consumer_team: string;
    permissions?: string[];
}

export interface TabConfig {
    key: string;
    label: string;
    type: string;
}
