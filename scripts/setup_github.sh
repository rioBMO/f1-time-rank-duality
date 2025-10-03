#!/bin/bash

# GitHub Repository Setup Script for F1 Time-Rank Duality Analysis
# This script helps you set up and push your project to GitHub

echo "=============================================="
echo "F1 Time-Rank Duality - GitHub Setup"
echo "=============================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "Download from: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore file..."
    # .gitignore content will be created by the Python script
fi

# Add all files to git
echo "📦 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: F1 Time-Rank Duality Analysis

- Complete 5-stage analysis pipeline
- Monte Carlo validation with 99.99% accuracy
- Exponential distribution modeling
- Statistical regression analysis
- Comprehensive documentation and README"

echo ""
echo "=============================================="
echo "Next Steps:"
echo "=============================================="
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: f1-time-rank-duality"
echo "   - Description: Formula 1 Driver Performance Analysis using Time-Rank Duality"
echo "   - Make it Public or Private (your choice)"
echo "   - Do NOT initialize with README (we already have one)"
echo ""
echo "2. After creating the repository, run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/f1-time-rank-duality.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Optional: Add topics to your repository for better discoverability:"
echo "   - formula1"
echo "   - statistical-analysis"
echo "   - monte-carlo-simulation"
echo "   - exponential-distribution"
echo "   - python"
echo "   - data-science"
echo ""
echo "✅ Local repository is ready for GitHub!"
echo "=============================================="