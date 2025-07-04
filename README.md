# Microdeploy
This project is made to Zero-config proxy  and Docker COmpose generator for Docker containers.

🚀 What Is MicroDeploy?

MicroDeploy is a CLI tool that auto-generates:

✅ nginx.conf (reverse proxy)

✅ docker-compose.yml (service orchestration)
…from a single config.yaml file that defines your microservices.

You no longer need to manually write Dockerfiles, Compose files, or reverse proxy rules for every service.
MicroDeploy does it all for you.

```plaintext
MicroDeploy/
│
├── main.py                # CLI entrypoint
├── generator.py           # Core logic for generating nginx.conf & docker-compose.yml
├── config.yaml            # User-defined microservices configuration
├── nginx.conf.j2          # Jinja2 template for generating NGINX config
├── nginx.conf             # Auto-generated NGINX config (output)
├── docker-compose.yml     # Auto-generated Docker Compose file (output)
│
├── go-app/                # Example Go microservice
│   ├── main.go
│   └── Dockerfile    
│                            # You can add your applications and pack your app dependencies in the following paths and attch them in config.yaml 
├── python-app/            # Example Python microservice
│   ├── app.py
│   └── Dockerfile
│
└── README.md              # Project documentation
```

Pack your application, requirements in a folder and add it to config.yaml file along with the Internal port container.

- We need to mention the name of the container we wanted to be in.

- The URL path prefix for NGINX reverse proxy routing.

- The internal port your app listens on (inside its Docker container).

- The relative directory path that contains the app and its Dockerfile

The work flow goes as follows:

- The generator.py will reads the config.yaml which contains the desired container name, port and the path of the application and its Dockerfile.

- Then generates the nginx.conif file by using the nginx.conf.j2, dynamically generate the main Nginx configuration file nginx.conf

- Here comes the main part: Docker compose file generation.
  1. Adds the services from config.yaml.

  2. Checks if need to pull the image or it will build the image.

   3. Now it will add the nginx reverse proxy (here we didn't fixed any name to the container), which makes the code reusable.

   ```
   compose['services']['nginx'] = {
        'image': 'nginx:latest',
        'ports': ['8080:80'],
        'volumes': ['./nginx.conf:/etc/nginx/nginx.conf'],
        'depends_on': [svc['name'] for svc in services]
    }

    ``` 
 When you explicitly name a container, Docker prevents creating multiple containers with the same name. To avoid the name conflix while we want to generate docker-compose for two different applications, name was ignored.

```main.py ``` this is the entrypoint for CLI. It reads a config file, then triggers the automatic generation of ```nginx.conf``` and ```docker-compose.yml.```

```
from generator import load_config, generate_nginx_config, generate_docker_compose
```

These functions are defined in generator.py and handle: 

- Loading the YAML config

- Rendering nginx.conf from a template

- Creating the docker-compose.yml file

If the import fails, it shows a helpful message asking to install the missing dependencies:

```
 Missing required modules. Please install them using 'pip install -r requirements.txt'.

``` 

- Then a function is called to deploy the microservices
```
def deploy(config_path):
```

```
services = data.get('services', [])
if not services:
    print("❌ No services found in config.")
    return
```
- The checks the defined microservices.

- Finally generates ginx.conf and docker-compose.yml based on the defined services

```
generate_nginx_config(services)
generate_docker_compose(services)
```

Execute the generated docker-compose file

```
python main.py deploy config.yaml
 ```
- It reads the config.yaml file passed as an argument

- Then it automatically builds the proxy and Docker Compose files using the services defined

``` http://localhost:8080/path ```    #it will take the path we given the config.yaml

- http://localhost:8080/go

- http://localhost:8080/python   