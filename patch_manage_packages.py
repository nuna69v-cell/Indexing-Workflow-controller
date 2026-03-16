import sys
import re

with open("scripts/utils/manage_packages.py", "r") as f:
    content = f.read()

new_functions = """
def map_ea_environments(master_map: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    \"\"\"Maps EA environment settings including IPs, Ports, and Jules API Keys.\"\"\"
    logger.info("Mapping EA environments with Jules API Keys...")

    # Retrieve Jules API Keys from environment
    jules_keys = []
    for key, value in os.environ.items():
        if key.startswith("JULES_API") and value:
            jules_keys.append({"name": key, "key": value})

    if not jules_keys:
        logger.warning("No JULES_API keys found in environment.")
        # Default mock fallback for demonstration if needed based on memory
        # jules_keys = [{"name": "JULES_API_V1", "key": "AQ.Ab8RN6K..."}]

    # Apply to repositories that look like EAs or Trading Systems
    for account, repos in master_map.items():
        for i, repo in enumerate(repos):
            name_lower = repo["name"].lower()
            if "ea" in name_lower or "trade" in name_lower or "genx" in name_lower or "bot" in name_lower:
                # Setup specific EA configurations
                key_index = i % len(jules_keys) if jules_keys else 0
                selected_key = jules_keys[key_index]["key"] if jules_keys else ""

                # Base port is 5555, increment for each EA to avoid conflicts
                assigned_port = 5555 + i

                repo["ea_config"] = {
                    "mapped": True,
                    "target_ip": "127.0.0.1",
                    "target_port": assigned_port,
                    "jules_api_key": selected_key,
                    "status": "Ready for injection"
                }
                logger.info(f"  - Mapped EA config for {repo['name']}: Port {assigned_port}")

    return master_map

def generate_ea_config_file(master_map: Dict[str, List[Dict[str, Any]]]):
    \"\"\"Generates a configuration file specifically for EAs based on mapped data.\"\"\"
    ea_configs = {}

    for account, repos in master_map.items():
        for repo in repos:
            if "ea_config" in repo:
                ea_configs[repo["name"]] = repo["ea_config"]

    if ea_configs:
        try:
            with open("ea_port_mapping.json", "w") as f:
                json.dump(ea_configs, f, indent=4)
            logger.info("Generated EA port mapping at ea_port_mapping.json")
        except IOError as e:
            logger.error(f"Failed to write EA mapping: {e}")
"""

# Insert the new functions before generate_master_map
content = content.replace(
    "def generate_master_map", new_functions + "\ndef generate_master_map"
)

# Update main function to call the new functions
main_update = """
    master_map = map_repositories(accounts)

    if not master_map:
        logger.warning("No repositories mapped. Exiting.")
        return

    master_map = map_ea_environments(master_map)
    generate_master_map(master_map)
    generate_ea_config_file(master_map)
"""
content = re.sub(
    r"    master_map = map_repositories\(accounts\).*?generate_master_map\(master_map\)",
    main_update,
    content,
    flags=re.DOTALL,
)

with open("scripts/utils/manage_packages.py", "w") as f:
    f.write(content)

print("Patch applied successfully.")
