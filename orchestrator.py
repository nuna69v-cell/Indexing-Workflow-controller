import logging

logger = logging.getLogger("Brain.Orchestrator")

class NodeOrchestrator:
    def __init__(self):
        self.nodes = {
            "forex-01": {"status": "OFFLINE", "type": "MT5"},
            "crypto-01": {"status": "OFFLINE", "type": "BYBIT"}
        }

    def start_nodes(self):
        for node_id in self.nodes:
            self.nodes[node_id]["status"] = "ONLINE"
            logger.info(f"Node {node_id} started successfully.")

    def check_health(self):
        online_count = sum(1 for n in self.nodes.values() if n["status"] == "ONLINE")
        return f"{online_count}/{len(self.nodes)} Nodes Online"

    def stop_all(self):
        for node_id in self.nodes:
            self.nodes[node_id]["status"] = "OFFLINE"
            logger.info(f"Node {node_id} stopped.")
