# doc_generator.py

def generate_deployment_summary(services, volumes=None, output_file="deployment_summary.md"):
    summary_lines = ["# Deployment Summary\n"]

    summary_lines.append("## Services:\n")
    for svc in services:
        port = svc.get("port", "N/A")
        proxy = " (proxied)" if svc.get("use_proxy") else ""
        summary_lines.append(f"- {svc['name']} : Port `{port}`{proxy}")

    summary_lines.append("\n## Dependencies:\n")
    for svc in services:
        if 'depends_on' in svc:
            for dep in svc['depends_on']:
                summary_lines.append(f"- {svc['name']} depends on {dep}")

    if volumes:
        summary_lines.append("\n## Volumes:\n")
        for vol in volumes:
            summary_lines.append(f"- {vol}")

    with open(output_file, "w", encoding="utf-8") as f:  # Add utf-8 for better compatibility
        f.write("\n".join(summary_lines))

    print(f"Deployment summary written to `{output_file}`")
