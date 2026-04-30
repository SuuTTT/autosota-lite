import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def _load_env_local() -> None:
    """Source the nearest .env.local into os.environ if it exists."""
    for candidate in (Path.cwd() / ".env.local", Path("/workspace/autosota-lite/.env.local")):
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
            return


class ResultLogger:
    def __init__(self, workspace_root="/workspace"):
        _load_env_local()
        self.workspace_root = Path(workspace_root)
        self.scores_path = self.workspace_root / "scores.jsonl"
        self.wandb_api_key = os.getenv("WANDB_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")

    def load_last_score(self):
        """Loads the most recent entry from scores.jsonl."""
        if not self.scores_path.exists():
            logging.warning(f"No scores file found at {self.scores_path}")
            return None
        
        with open(self.scores_path, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if not lines:
                return None
            last_line = lines[-1]
            logging.info(f"Successfully loaded data: {last_line}")
            return json.loads(last_line)

    def log_to_wandb(self, project_name, run_name, metrics):
        """Logs metrics to Weights & Biases."""
        if not self.wandb_api_key:
            logging.error("WANDB_API_KEY not found in environment.")
            return False
        
        try:
            import wandb
            wandb.login(key=self.wandb_api_key, relogin=True, verify=False)
            run = wandb.init(project=project_name, name=run_name, resume="allow")
            run.log(metrics)
            run.finish()
            logging.info(f"Successfully logged metrics to WandB project {project_name}")
            return True
        except ImportError:
            logging.error("wandb library not installed.")
            return False
        except Exception as e:
            logging.error(f"Failed to log to WandB: {str(e)}")
            return False

    def update_github_gist(self, gist_id, filename, content):
        """Updates a GitHub Gist with the latest results for dashboarding."""
        if not self.github_token:
            logging.error("GITHUB_TOKEN not found in environment.")
            return False
        
        import requests
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "files": {
                filename: {"content": content}
            }
        }
        
        response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)
        if response.status_code == 200:
            logging.info(f"Successfully updated GitHub Gist {gist_id}")
            return True
        else:
            logging.error(f"Failed to update GitHub Gist: {response.status_code} {response.text}")
            return False

if __name__ == "__main__":
    # Example usage for the skill execution
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["wandb", "github", "both"], required=True)
    parser.add_argument("--project", default="autosota-research")
    parser.add_argument("--run_name", default=f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--gist_id", help="GitHub Gist ID for reporting")
    
    args = parser.parse_args()
    logger = ResultLogger()
    last_run = logger.load_last_score()
    
    if not last_run:
        logging.error("No data found to log.")
        exit(1)

    if args.mode in ["wandb", "both"]:
        logger.log_to_wandb(args.project, args.run_name, last_run)
    
    if args.mode in ["github", "both"] and args.gist_id:
        # Convert full history or just last result to readable text
        content = json.dumps(last_run, indent=2)
        logger.update_github_gist(args.gist_id, f"results_{args.run_name}.json", content)
