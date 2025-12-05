import git
import os
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class GitManager:
    """
    Manages Git operations for the agent, specifically for syncing documentation.
    """
    def __init__(self, repo_url: str = "git@github.com:parmarjh/-N8N-Workflow-Documentation.git", local_path: str = "docs_repo"):
        self.repo_url = repo_url
        self.local_path = os.path.abspath(local_path)
        self.repo: Optional[git.Repo] = None
        self._setup_repo()

    def _setup_repo(self):
        """Initializes the repo: clones if not exists, otherwise opens it."""
        if not os.path.exists(self.local_path):
            try:
                logger.info(f"Cloning {self.repo_url} to {self.local_path}...")
                self.repo = git.Repo.clone_from(self.repo_url, self.local_path)
                logger.info("Clone successful.")
            except Exception as e:
                logger.error(f"Failed to clone repo: {e}")
                # Fallback: create dir and init if clone fails (e.g. auth issue)
                os.makedirs(self.local_path, exist_ok=True)
                self.repo = git.Repo.init(self.local_path)
        else:
            try:
                self.repo = git.Repo(self.local_path)
                logger.info("Opened existing repo.")
            except git.InvalidGitRepositoryError:
                logger.warning("Invalid git repo found. Re-initializing.")
                self.repo = git.Repo.init(self.local_path)

    def pull_changes(self) -> str:
        """Pulls latest changes from remote."""
        if not self.repo:
            return "Repository not initialized."
        try:
            origin = self.repo.remotes.origin
            origin.pull()
            return "Successfully pulled latest changes."
        except Exception as e:
            return f"Failed to pull changes: {str(e)}"

    def push_changes(self, commit_message: str = "Agent auto-update") -> str:
        """Stages, commits, and pushes all changes to remote."""
        if not self.repo:
            return "Repository not initialized."
        try:
            # Add all changes
            self.repo.git.add(A=True)
            
            # Commit if there are changes
            if self.repo.is_dirty() or self.repo.untracked_files:
                self.repo.index.commit(commit_message)
                logger.info(f"Committed changes: {commit_message}")
            else:
                return "No changes to commit."

            # Push
            origin = self.repo.remotes.origin
            origin.push()
            return "Successfully pushed all changes to remote."
        except Exception as e:
            return f"Failed to push changes: {str(e)}"

    def get_status(self) -> Dict:
        """Returns the current status of the repo."""
        if not self.repo:
            return {"status": "error", "message": "Repo not initialized"}
        
        return {
            "active_branch": self.repo.active_branch.name,
            "is_dirty": self.repo.is_dirty(),
            "untracked_files": len(self.repo.untracked_files),
            "last_commit": str(self.repo.head.commit.hexsha[:7]),
            "last_commit_msg": str(self.repo.head.commit.message).strip()
        }

# Tool definitions for AutoGen
def pull_repo() -> str:
    manager = GitManager()
    return manager.pull_changes()

def push_repo(commit_message: str = "Agent update") -> str:
    manager = GitManager()
    return manager.push_changes(commit_message)

def get_repo_status() -> Dict:
    manager = GitManager()
    return manager.get_status()
