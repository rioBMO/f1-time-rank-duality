"""
GitHub Repository Setup Script for F1 Time-Rank Duality Analysis
================================================================

This script helps you prepare and upload your F1 research project to GitHub.
It handles Git initialization, file organization, and provides step-by-step guidance.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and return the result"""
    try:
        if description:
            print(f"🔧 {description}")
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            if description:
                print(f"✅ {description} - Success")
            return True, result.stdout.strip()
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

def check_git_installation():
    """Check if Git is installed"""
    success, output = run_command("git --version", "Checking Git installation")
    if success:
        print(f"✅ Git is installed: {output}")
        return True
    else:
        print("❌ Git is not installed. Please install Git first.")
        print("Download from: https://git-scm.com/downloads")
        return False

def initialize_git_repo():
    """Initialize Git repository if not already done"""
    if os.path.exists(".git"):
        print("✅ Git repository already exists")
        return True
    
    success, _ = run_command("git init", "Initializing Git repository")
    if success:
        # Set default branch to main
        run_command("git branch -M main", "Setting default branch to main")
        return True
    return False

def create_initial_commit():
    """Create initial commit with all files"""
    
    # Add all files
    success, _ = run_command("git add .", "Adding all files to Git")
    if not success:
        return False
    
    # Create commit
    commit_message = """Initial commit: F1 Time-Rank Duality Analysis

- Complete 5-stage analysis pipeline
- Monte Carlo validation with 99.99% accuracy
- Exponential distribution modeling
- Statistical regression analysis
- Comprehensive documentation and README

Features:
- Stage 1: Odds data parsing and conversion
- Stage 2: Probability normalization
- Stage 3: Lambda parameter estimation (grouped approach)
- Stage 4: Mu and sigma calculation
- Stage 5: Stepwise regression analysis
- Monte Carlo simulation with 10,000+ iterations
- Statistical validation and significance testing
- Professional documentation and visualization"""
    
    success, _ = run_command(f'git commit -m "{commit_message}"', "Creating initial commit")
    return success

def check_project_structure():
    """Verify that all important files are present"""
    
    essential_files = [
        "README.md",
        "requirements.txt", 
        "LICENSE",
        ".gitignore",
        "main.py",
        "config.py",
        "utils.py"
    ]
    
    stage_files = [
        "stage1_extract.py",
        "stage2_probabilities.py", 
        "stage3_estimate_lambda.py",
        "stage4_mu_sigma.py",
        "stage5_regression.py"
    ]
    
    validation_files = [
        "monte_carlo_simulation.py",
        "significance_analysis.py",
        "statistical_explanation.py",
        "diagram_analysis.py"
    ]
    
    data_files = [
        "data/odds_table1.csv",
        "data/f1seconddata.txt"
    ]
    
    print("\n📋 Checking project structure...")
    
    all_good = True
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ Missing: {file}")
            all_good = False
    
    for file in stage_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  Optional: {file}")
    
    for file in validation_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  Optional: {file}")
            
    for file in data_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  Data file: {file}")
    
    return all_good

def print_github_instructions():
    """Print detailed instructions for GitHub setup"""
    
    print("\n" + "="*60)
    print("🚀 GITHUB REPOSITORY SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ CREATE NEW REPOSITORY ON GITHUB:")
    print("   • Go to: https://github.com/new")
    print("   • Repository name: f1-time-rank-duality")
    print("   • Description: Formula 1 Driver Performance Analysis using Time-Rank Duality")
    print("   • Visibility: Public (recommended for research) or Private")
    print("   • ❌ Do NOT initialize with README, .gitignore, or license")
    print("   • Click 'Create repository'")
    
    print("\n2️⃣ CONNECT LOCAL REPOSITORY TO GITHUB:")
    print("   Copy and run these commands in your terminal:")
    print("   (Replace YOUR_USERNAME with your actual GitHub username)")
    print()
    print("   git remote add origin https://github.com/YOUR_USERNAME/f1-time-rank-duality.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n3️⃣ ADD REPOSITORY TOPICS (Optional but recommended):")
    print("   • Go to your repository page on GitHub")
    print("   • Click the gear icon ⚙️ next to 'About'")
    print("   • Add these topics:")
    print("     - formula1")
    print("     - statistical-analysis") 
    print("     - monte-carlo-simulation")
    print("     - exponential-distribution")
    print("     - python")
    print("     - data-science")
    print("     - research")
    print("     - motorsport")
    
    print("\n4️⃣ OPTIONAL ENHANCEMENTS:")
    print("   • Add a repository description")
    print("   • Add a website URL (if you have one)")
    print("   • Enable Issues and Discussions")
    print("   • Create a release tag (e.g., v1.0.0)")
    
    print("\n5️⃣ SHARING YOUR RESEARCH:")
    print("   • Share the repository link in research communities")
    print("   • Consider submitting to journals or conferences")
    print("   • Add citations if based on published work")
    
    print("\n" + "="*60)
    print("✅ Your F1 research project is ready for GitHub!")
    print("="*60)

def main():
    """Main function to set up GitHub repository"""
    
    print("="*60)
    print("🏎️  F1 TIME-RANK DUALITY - GITHUB SETUP")
    print("="*60)
    
    # Check Git installation
    if not check_git_installation():
        return False
    
    # Check project structure
    if not check_project_structure():
        print("\n⚠️  Some files are missing, but you can still proceed.")
        proceed = input("\nDo you want to continue? (y/n): ").lower().strip()
        if proceed != 'y':
            print("Setup cancelled.")
            return False
    
    # Initialize Git repository
    if not initialize_git_repo():
        print("❌ Failed to initialize Git repository")
        return False
    
    # Create initial commit
    if not create_initial_commit():
        print("❌ Failed to create initial commit")
        return False
    
    # Print GitHub instructions
    print_github_instructions()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Setup completed successfully!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")