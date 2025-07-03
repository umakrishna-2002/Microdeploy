import os
import yaml
from jinja2 import Environment, FileSystemLoader

# -------------------------
# Load and parse config.yaml
# -------------------------
def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# -------------------------
# Generate nginx.conf from template
# -------------------------
def generate_nginx_config(services):
    env = Environment(loader=FileSystemLoader('templates'))  # Load from 'templates/' folder
    template = env.get_template('nginx.conf.j2')              # Template file name

    output = template.render(services=services)               # Render with service data

    # ✅ Write nginx.conf directly to main directory
    with open('nginx.conf', 'w') as f:
        f.write(output)

    print("✅ nginx.conf generated")

# -------------------------
# Generate docker-compose.yml
# -------------------------
def generate_docker_compose(services):
    compose = {
        'version': '3',
        'services': {}
    }

    # Add all services from config.yaml
    for svc in services:
        config = {
            'expose': [str(svc['port'])]
        }

        # Either build from source or pull image
        if 'build' in svc:
            config['build'] = svc['build']
        elif 'image' in svc:
            config['image'] = svc['image']

        compose['services'][svc['name']] = config

    # Add nginx reverse proxy service (without fixed container_name)
    compose['services']['nginx'] = {
        'image': 'nginx:latest',
        'ports': ['8080:80'],
        'volumes': ['./nginx.conf:/etc/nginx/nginx.conf'],
        'depends_on': [svc['name'] for svc in services]
    }

    # ✅ Write docker-compose.yml directly to main directory
    with open('docker-compose.yml', 'w') as f:
        yaml.dump(compose, f, default_flow_style=False)

    print("✅ docker-compose.yml generated")
