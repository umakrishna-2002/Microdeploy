import os
import yaml
import json
from jinja2 import Environment, FileSystemLoader

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def validate_services(services):
    for svc in services:
        if 'name' not in svc or 'port' not in svc:
            raise ValueError("Each service must have a 'name' and 'port'")

def generate_nginx_config(services, proxy_type="nginx"):
    if not services:
        print("⚠️  No services provided for reverse proxy configuration.")
        return

    # Only generate reverse proxy config if needed
    services_with_proxy = [s for s in services if s.get('use_proxy')]
    if not services_with_proxy:
        print("ℹ️  Skipping proxy config generation: no services require it.")
        return

    env = Environment(loader=FileSystemLoader('templates'))
    template_file = f"{proxy_type}.conf.j2"
    template = env.get_template(template_file)

    output = template.render(services=services_with_proxy)
    with open("nginx.conf", "w") as f:
        f.write(output)
    print("✅ Reverse proxy config generated: nginx.conf")

def generate_docker_compose(services):
    compose = {
        'version': '3.8',
        'services': {},
        'volumes': {},
    }

    for svc in services:
        config = {
            'container_name': svc['name'],
            'expose': [str(svc['port'])] if 'port' in svc else [],
            'ports': [f"{svc['port']}:{svc['port']}"] if 'port' in svc else [],
        }

        if 'build' in svc:
            config['build'] = svc['build']
        elif 'image' in svc:
            config['image'] = svc['image']

        if 'depends_on' in svc:
            config['depends_on'] = svc['depends_on']

        if 'environment' in svc:
            config['environment'] = svc['environment']

        if 'volumes' in svc:
            config['volumes'] = svc['volumes']
            for vol in svc['volumes']:
                vol_name = vol.split(':')[0]
                compose['volumes'][vol_name] = {'driver': 'local'}

        compose['services'][svc['name']] = config

    # Add nginx only if needed
    services_with_proxy = [s for s in services if s.get('use_proxy')]
    if services_with_proxy:
        compose['services']['nginx'] = {
            'image': 'nginx:latest',
            'ports': ['8080:80'],
            'volumes': ['./nginx.conf:/etc/nginx/nginx.conf'],
            'depends_on': [s['name'] for s in services_with_proxy]
        }

    with open("docker-compose.yml", "w") as f:
        yaml.dump(compose, f, default_flow_style=False, sort_keys=False)
    print("✅ Docker Compose file generated: docker-compose.yml")
