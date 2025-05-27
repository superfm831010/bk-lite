import toml
import yaml
from urllib.parse import urlencode, urlparse, parse_qs

class ConfigFormat:
    @staticmethod
    def toml_to_dict(toml_config):
        config_dict = toml.loads(toml_config)
        result = {}
        for key1, value1 in config_dict.items():
            for key2, value2 in value1.items():
                result["plugin"] = (key1, key2)
                result["config"] = value2[0]
        return result

    @staticmethod
    def json_to_toml(json_config):
        data = {json_config["plugin"][0]: {json_config["plugin"][1]: [json_config["config"]]}}
        result = toml.dumps(data)
        result = result.replace("[inputs]", '')  # 将单引号替换为双引号
        return result

    @staticmethod
    def yaml_to_dict(yaml_config):
        """将 YAML 格式的配置转换为字典"""
        return yaml.safe_load(yaml_config)

    @staticmethod
    def json_to_yaml(json_config):
        """将 JSON 格式的配置转换为 YAML 格式"""
        return yaml.dump(json_config, default_flow_style=False)

    @staticmethod
    def query_params_to_url(base_url, query_params):
        """将 JSON 格式的 query_params 转换回原始 URL 格式"""
        query_string = urlencode(query_params, doseq=True)  # 生成查询字符串
        return f"{base_url}?{query_string}"

    @staticmethod
    def extract_query_params(url):
        """解析 URL 并提取查询参数"""
        parsed_url = urlparse(url)  # 解析 URL
        query_params = parse_qs(parsed_url.query)  # 解析查询参数
        # 转换 query_params，去掉列表包装
        query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        return query_params
