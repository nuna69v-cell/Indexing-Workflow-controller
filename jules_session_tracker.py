import json
import os
import datetime


class JulesSessionTracker:
    def __init__(self, session_file=".jules-session.json"):
        self.session_file = session_file
        self.session_data = self._load_session()

    def _load_session(self):
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {"sessions": []}

    def _save_session(self):
        with open(self.session_file, "w") as f:
            json.dump(self.session_data, f, indent=4)

    def log_action(self, action, details):
        timestamp = datetime.datetime.now().isoformat()

        if not self.session_data.get("sessions"):
            self.start_session()

        current_session = self.session_data["sessions"][-1]
        current_session["actions"].append(
            {"timestamp": timestamp, "action": action, "details": details}
        )
        self._save_session()

    def start_session(self):
        session_id = f"sess_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if "sessions" not in self.session_data:
            self.session_data["sessions"] = []

        self.session_data["sessions"].append(
            {
                "session_id": session_id,
                "start_time": datetime.datetime.now().isoformat(),
                "actions": [],
            }
        )
        self._save_session()
        print(f"Started Jules session: {session_id}")
        return session_id


if __name__ == "__main__":
    import sys

    tracker = JulesSessionTracker()

    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            tracker.start_session()
        elif sys.argv[1] == "log" and len(sys.argv) > 3:
            tracker.log_action(sys.argv[2], sys.argv[3])
    else:
        tracker.start_session()
