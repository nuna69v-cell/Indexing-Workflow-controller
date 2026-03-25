import argparse
import json
import os
import subprocess
import sys
import webbrowser

CONFIG_FILE = "launcher_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"teams": {}}
    return {"teams": {}}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def add_team(args):
    config = load_config()
    team_name = args.name
    if team_name in config["teams"]:
        print(f"Team '{team_name}' already exists.")
    else:
        config["teams"][team_name] = []
        save_config(config)
        print(f"Team '{team_name}' added successfully.")

def add_app(args):
    config = load_config()
    team_name = args.team
    app_path = args.path
    
    if team_name not in config["teams"]:
        print(f"Error: Team '{team_name}' does not exist. Create it first using 'add-team'.")
        return
        
    if app_path in config["teams"][team_name]:
        print(f"App '{app_path}' is already in team '{team_name}'.")
    else:
        config["teams"][team_name].append(app_path)
        save_config(config)
        print(f"App '{app_path}' added to team '{team_name}'.")

def list_teams(args):
    config = load_config()
    teams = config.get("teams", {})
    
    if not teams:
        print("No teams configured. Use 'add-team' to create one.")
        return
        
    print("Configured Teams and Apps:")
    for team, apps in teams.items():
        print(f"\n[{team}]")
        if not apps:
            print("  (No apps added yet)")
        for app in apps:
            print(f"  - {app}")

def launch_team(args):
    config = load_config()
    team_name = args.team
    
    if team_name not in config["teams"]:
        print(f"Error: Team '{team_name}' does not exist.")
        return
        
    apps = config["teams"][team_name]
    if not apps:
        print(f"No apps configured for team '{team_name}'.")
        return
        
    print(f"Launching apps for team '{team_name}'...")
    success_count = 0
    
    for app in apps:
        try:
            if app.startswith("http://") or app.startswith("https://"):
                print(f"Opening URL: {app}")
                webbrowser.open(app)
                success_count += 1
            else:
                print(f"Launching application: {app}")
                if sys.platform == "win32":
                    os.startfile(app)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", app])
                else:
                    subprocess.Popen(["xdg-open", app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                success_count += 1
        except Exception as e:
            print(f"Failed to launch '{app}': {e}")
            
    print(f"\nSuccessfully launched {success_count} out of {len(apps)} apps.")

def main():
    parser = argparse.ArgumentParser(description="Smart Team Launcher - Automate launching applications and URLs.")
    subparsers = parser.add_subparsers(title="commands", dest="command")
    subparsers.required = True

    # add-team
    parser_add_team = subparsers.add_parser("add-team", help="Add a new team")
    parser_add_team.add_argument("name", help="Name of the team")
    parser_add_team.set_defaults(func=add_team)

    # add-app
    parser_add_app = subparsers.add_parser("add-app", help="Add an app or URL to a team")
    parser_add_app.add_argument("team", help="Name of the team")
    parser_add_app.add_argument("path", help="Path to the application or URL (e.g., https://github.com)")
    parser_add_app.set_defaults(func=add_app)

    # list
    parser_list = subparsers.add_parser("list", help="List all teams and their apps")
    parser_list.set_defaults(func=list_teams)

    # launch
    parser_launch = subparsers.add_parser("launch", help="Launch all apps for a specific team")
    parser_launch.add_argument("team", help="Name of the team to launch")
    parser_launch.set_defaults(func=launch_team)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
