# -- coding: utf-8 --
# @File: prometheus.py
# @Time: 2025/5/13 15:57
# @Author: windyzhao

import requests
from urllib.parse import urljoin
from typing import Dict, Any, List

from apps.alerts.common.source_adapter.base import AlertSourceAdapter

from apps.alerts.common.source_adapter import logger


class PrometheusAdapter(AlertSourceAdapter):
    """Prometheus告警源适配器"""

    def fetch_alerts(self) -> List[Dict[str, Any]]:
        base_url = self.config.get('base_url')
        api_path = self.config.get('api_path', '/api/v1/alerts')
        url = urljoin(base_url, api_path)

        try:
            response = requests.get(
                url,
                timeout=self.config.get('timeout', 10),
                verify=self.config.get('verify_ssl', True)
            )
            response.raise_for_status()
            return response.json().get('data', {}).get('alerts', [])
        except Exception as e:
            logger.error(f"Failed to fetch alerts from Prometheus: {e}")
            return []

    def test_connection(self) -> bool:
        base_url = self.config.get('base_url')
        api_path = self.config.get('api_path', '/api/v1/targets')
        url = urljoin(base_url, api_path)

        try:
            response = requests.get(
                url,
                timeout=self.config.get('timeout', 10),
                verify=self.config.get('verify_ssl', True)
            )
            return response.status_code == 200
        except Exception:
            return False

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        required_fields = ['base_url']
        return all(field in config for field in required_fields)

    def _map_prometheus_severity(self, severity: str) -> str:
        severity_map = {
            'critical': 'critical',
            'warning': 'warning',
            'none': 'info'
        }
        return severity_map.get(severity.lower(), 'info')

    def _map_prometheus_status(self, status: str) -> str:
        status_map = {
            'firing': 'firing',
            'resolved': 'resolved'
        }
        return status_map.get(status, 'unknown')
