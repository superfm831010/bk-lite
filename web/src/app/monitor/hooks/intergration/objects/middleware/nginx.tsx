import { useNginxTelegraf } from '../../plugins/middleware/nginxTelegraf';
import { useNginxExporter } from '../../plugins/middleware/nginxExporter';

export const useNginxConfig = () => {
  const nginxTelegraf = useNginxTelegraf();
  const nginxExporter = useNginxExporter();

  const plugins = {
    Nginx: nginxTelegraf,
    'Nginx-Exporter': nginxExporter,
  };

  return {
    instance_type: 'nginx',
    dashboardDisplay: [],
    tableDiaplay: [
      { type: 'value', key: 'nginx_requests' },
      { type: 'value', key: 'nginx_active' },
    ],
    groupIds: {},
    plugins,
  };
};
