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
│
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


==<b>main.py</b>== this is the entrypoint for CLI.  It reads a config file, then triggers the automatic generation of nginx.conf and docker-compose.yml.
