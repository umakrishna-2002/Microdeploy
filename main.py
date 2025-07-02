import sys
try:
    from generator import load_config, generate_nginx_config, generate_docker_compose
except ImportError:
    print("❌ Missing required modules. Please install them using 'pip install -r requirements.txt'.")
    sys.exit(1)

def deploy(config_path):
    print(f"📦 Loading config from {config_path}")
    data = load_config(config_path)

    services = data.get('services', [])
    if not services:
        print("❌ No services found in config.")
        return

    generate_nginx_config(services)
    generate_docker_compose(services)
    print("🚀 MicroDeploy completed successfully!")

if __name__ == "__main__":
    config_path = sys.argv[2]

    deploy(config_path)
  