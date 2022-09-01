from random import choice
from loguru import logger
from yaml import safe_load
from os import path
from flask import Flask

from mtd_sources.config import get_config
from mtd_sources.logger import initialize
from mtd_sources.k8s_client import K8s

app = Flask(__name__)


@app.route("/update")
def update():
    config = get_config(CONFIG_FILE_PATH)
    services_names = config["SERVICES_NAMES"]
    patch_file_template = config["PATCH_FILE_TEMPLATE"]
    if not isinstance(services_names, list) or len(services_names) < 1:
        raise ValueError(
            f"Invalid services names in config (either not a list or empty list)"
        )

    k8s = K8s()
    for name in services_names:
        k8s.check_resource_existence(name, "service")

    # Patch services or (TODO) create new services
    legit_service_name = choice(services_names)
    template = load_template(patch_file_template)
    for name in services_names:
        if name == legit_service_name:
            ready_template = template
            ready_template["spec"]["selector"] = {"app": "legit-app"}
        else:
            ready_template = template
            ready_template["spec"]["selector"] = {"app": "false-app"}
        k8s.patch_service(name=name, body=ready_template)
        logger.info(f"Patched {name}")
    logger.success(
        f"All services patched. Legit app is exposed on {legit_service_name} NodePort now"
    )

    nodeports = list()
    for name in services_names:
        nodeports.append(k8s.get_nodeport(name))
    report = dict(zip(services_names, nodeports))
    logger.success(report)
    return {
        "legit_app": legit_service_name,
        "legit_app_port": report[legit_service_name],
        "services_report": report,
    }


@logger.catch
def load_template(template_path: str):
    with open(path.join(path.dirname(__file__), template_path)) as f:
        file_content = safe_load(f)
    if not file_content:
        raise TypeError("Template is empty or has invalid path")
    return file_content


if __name__ == "__main__":
    CONFIG_FILE_PATH = "./config.yaml"
    initialize(CONFIG_FILE_PATH)
    app.run(host="0.0.0.0", port=5100)
