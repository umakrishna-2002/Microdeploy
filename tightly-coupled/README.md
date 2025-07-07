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
