# =========================================================
# notebook_parameter_sample.py
# Purpose:
# Sample Fabric notebook parameter handling for Bronze / Silver / Gold
# =========================================================

from datetime import datetime
import uuid


def generate_run_id() -> str:
    """
    Generate a fallback run id when notebook is executed manually
    outside Fabric pipeline orchestration.
    """
    return str(uuid.uuid4())


def get_config(environment: str) -> dict:
    """
    Sample environment config.
    Replace these paths with your actual Fabric / Lakehouse paths.
    """
    config_map = {
        "dev": {
            "raw_base_path": "Files/dev/raw",
            "bronze_base_path": "Tables/bronze",
            "silver_base_path": "Tables/silver",
            "gold_base_path": "Tables/gold"
        },
        "test": {
            "raw_base_path": "Files/test/raw",
            "bronze_base_path": "Tables/bronze",
            "silver_base_path": "Tables/silver",
            "gold_base_path": "Tables/gold"
        },
        "prod": {
            "raw_base_path": "Files/prod/raw",
            "bronze_base_path": "Tables/bronze",
            "silver_base_path": "Tables/silver",
            "gold_base_path": "Tables/gold"
        }
    }

    return config_map.get(environment, config_map["dev"])


# =========================================================
# PARAMETERS
# These values are expected to be passed from Fabric pipeline.
# Fallback defaults allow manual notebook execution as well.
# =========================================================

pipeline_name = globals().get("pipeline_name", "pl_retail_analytics_medallion")

pipeline_start_time = globals().get(
    "pipeline_start_time",
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

environment = globals().get("environment", "dev")
run_id = globals().get("run_id", generate_run_id())
rerun_mode = globals().get("rerun_mode", "FULL")   # FULL / FAILED_ONLY


# =========================================================
# CONFIG RESOLUTION
# =========================================================

config = get_config(environment)

raw_base_path = config["raw_base_path"]
bronze_base_path = config["bronze_base_path"]
silver_base_path = config["silver_base_path"]
gold_base_path = config["gold_base_path"]


# =========================================================
# DEBUG / VALIDATION OUTPUT
# =========================================================

print("========== FABRIC NOTEBOOK PARAMETER VALIDATION ==========")
print(f"pipeline_name       = {pipeline_name}")
print(f"pipeline_start_time = {pipeline_start_time}")
print(f"environment         = {environment}")
print(f"run_id              = {run_id}")
print(f"rerun_mode          = {rerun_mode}")
print(f"raw_base_path       = {raw_base_path}")
print(f"bronze_base_path    = {bronze_base_path}")
print(f"silver_base_path    = {silver_base_path}")
print(f"gold_base_path      = {gold_base_path}")
print("==========================================================")


# =========================================================
# SAMPLE NOTEBOOK STAGE USAGE
# Replace this section with actual Bronze / Silver / Gold logic
# =========================================================

print(f"Notebook execution started for environment '{environment}' with run_id '{run_id}'.")

if rerun_mode not in ["FULL", "FAILED_ONLY"]:
    raise ValueError("Invalid rerun_mode. Allowed values: FULL, FAILED_ONLY")

print("Parameter initialization completed successfully.")