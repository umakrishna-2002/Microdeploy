from generator import load_config, generate_nginx_config, generate_docker_compose
from doc_generator import generate_deployment_summary

def deploy(config_path):
    print(f"📦 Loading config from {config_path}")
    data = load_config(config_path)
    services = data.get('services', [])
    if not services:
        print("❌ No services found in config.")
        return

    generate_nginx_config(services)
    generate_docker_compose(services)

    volumes = data.get('volumes', {}).keys()
    generate_deployment_summary(services, volumes)

    print("🚀 MicroDeploy completed successfully!")
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3 or sys.argv[1] != "deploy":
        print("Usage: python main.py deploy <config_path>")
    else:
        deploy(sys.argv[2]) 
