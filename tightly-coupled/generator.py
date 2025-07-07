import yaml
import os
from jinja2 import Environment, FileSystemLoader

# Load config.yaml file that defines all services
def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# Generate the NGINX reverse proxy configuration dynamically
def generate_nginx_config(services):
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Load the nginx.conf template (Jinja2 format)
    template = env.get_template('nginx.conf.j2')

    # Render the final nginx.conf by passing service list
    output = template.render(services=services)

    # Write the rendered output to nginx.conf
    with open('nginx.conf', 'w') as f:
        f.write(output)
    
    print("✅ Generated nginx.conf")

# Generate docker-compose.yml file from config.yaml input
def generate_docker_compose(services):
    compose = {
        'version': '3',
        'services': {},
    }

    # Iterate through each microservice defined in config.yaml
    for svc in services:
        config = {
            # This is the container name used by other containers to communicate
            'container_name': svc['name'],
            
            # Expose internal ports (e.g., Flask = 5000, Node = 3000)
            'expose': [str(svc['port'])] if 'port' in svc else [],
        }

        # Either build from Dockerfile or pull image from Docker Hub
        if 'build' in svc:
            config['build'] = svc['build']
        elif 'image' in svc:
            config['image'] = svc['image']

        # Handle dependencies — useful in tightly coupled services
        if 'depends_on' in svc:
            config['depends_on'] = svc['depends_on']

        # Optional: Add environment variables
        if 'environment' in svc:
            config['environment'] = svc['environment']

        # Optional: Mount volumes if defined
        if 'volumes' in svc:
            config['volumes'] = svc['volumes']

        # Add final service block to Compose dictionary
        compose['services'][svc['name']] = config

    # Add the NGINX reverse proxy to route requests to correct service
    compose['services']['nginx'] = {
        'image': 'nginx:latest',
        'ports': ['8080:80'],
        'volumes': ['./nginx.conf:/etc/nginx/nginx.conf'],
        'depends_on': [svc['name'] for svc in services],  # Make sure NGINX waits for app services
    }

    # Write the entire Compose spec to a file
    with open('docker-compose.yml', 'w') as f:
        yaml.dump(compose, f, default_flow_style=False)

    print("✅ Generated docker-compose.yml")
