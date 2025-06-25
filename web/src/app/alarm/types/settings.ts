export interface AlertAssignListItem {
    id: number;
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
    name: string;
    match_type: string;
    match_rules: Record<string, any>;
    personnel: string[];
    notify_channels: string;
    notification_scenario: string;
    config: {
        type: string;
        end_time: string;
        start_time: string;
        week_month: string;
    };
    notification_frequency: Record<
        string,
        { max_count: number; interval_minutes: number }
    >;
    is_active: boolean;
}

export interface AlertShieldListItem {
    id: number;
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
    name: string;
    match_type: string;
    match_rules: Array<Array<{
        key: string;
        value: string;
        operator: string;
    }>>;
    suppression_time: {
        type: string;
        end_time: string;
        start_time: string;
        week_month: string[];
    };
    is_active: boolean;
}

export interface AggregationRule {
    id: number;
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
    rule_id: string;
    name: string;
    description: string;
    [key: string]: any;
}
export interface CorrelationRule {
    id: number;
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
    name: string;
    type: string;
    scope: string;
    description: string | null;
    aggregation_rules: number[];
    [key: string]: any;
}
