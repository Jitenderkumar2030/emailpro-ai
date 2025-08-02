# Option 1: Use GitHub CLI (recommended)
gh auth login
git push origin main

# Option 2: Use Personal Access Token
# Go to GitHub Settings > Developer settings > Personal access tokens
# Create a new token with repo permissions
# Use token as password when prompted

# Option 3: Use SSH (if configured)
git remote set-url origin git@github.com:Jitenderkumar2030/emailpro-ai.git
git push origin main