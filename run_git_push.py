import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from modules.git_manager import push_repo, GitManager

import shutil

if __name__ == "__main__":
    print("Initializing GitManager...")
    manager = GitManager()
    
    # Copy README to the repo folder
    source = "README_ZERO_TO_END.md"
    destination = os.path.join(manager.local_path, "README.md")
    
    if os.path.exists(source):
        print(f"Copying {source} to {destination}...")
        shutil.copy2(source, destination)
    else:
        print(f"Warning: {source} not found.")

    print("Attempting to push to repository...")
    result = push_repo(commit_message="Auto-update: Added Zero to End Guide")
    print(f"Result: {result}")
