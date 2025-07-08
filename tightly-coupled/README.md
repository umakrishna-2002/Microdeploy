MicroDeploy is built to support multiple reverse proxy engines like NGINX, Apache, or even Traefik — without requiring users to change any core logic in the codebase.

Typical workflow would be:

```
MicroDeploy/
├── templates/
│   ├── nginx.conf.j2      # Default NGINX reverse proxy template
│   └── apache.conf.j2     # (Optional) Apache reverse proxy template
├── generator.py           # Automatically selects template based on config.yaml
├── config.yaml            # Define services and reverse proxy engine
└── ...
```

Can choose the reverse_proxy if nned for the application that need to be get deployed.

🔁 Choose reverse_proxy Only When Needed
MicroDeploy is smartly designed to allow you to include a reverse proxy only when it's required by your application architecture. Not every microservice setup needs a reverse proxy — and that’s totally okay.

By default, reverse proxy setup is optional and fully config-driven.

✅ How it works:
In your config.yaml, you can optionally specify a reverse_proxy key (e.g., nginx, apache, etc.).

If this key is present, MicroDeploy:

Looks into the /templates directory for the corresponding .j2 (Jinja2) configuration template.

Renders the config (e.g., nginx.conf, apache.conf) based on your services.

Automatically adds the reverse proxy as a service in the docker-compose.yml.


If no reverse_proxy is mentioned:

- The tool skips reverse proxy generation entirely.

- Only your application containers (frontend, backend, DB, etc.) are added to docker-compose.yml.
