#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from dotenv import load_dotenv
from sympy import true

from engineering_team.crew import EngineeringTeam

# Load environment variables from .env file
load_dotenv(override=true)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)
os.makedirs('output/execution', exist_ok=True)
os.makedirs('output/tests', exist_ok=True)
os.makedirs('output/deployment', exist_ok=True)
os.makedirs('output/frontend', exist_ok=True)

# Example requirements for MVP development
default_requirements = """
Create a simple Todo List application with the following features:
1. Add new todo items
2. Mark todos as complete/incomplete
3. Delete todo items
4. Filter todos by status (all, active, completed)
5. Simple and clean user interface
6. Data persistence using local storage or SQLite
7. RESTful API for backend operations

Remember: Build only MVP with essential features, nothing extra.
"""

def run():
    """
    Run the enhanced engineering team crew
    """
    print("\n" + "="*60)
    print("🚀 ENHANCED ENGINEERING TEAM - MVP BUILDER")
    print("="*60)
    
    # Get requirements from user or use default
    print("\nEnter your project requirements (or press Enter for default Todo app):")
    print("(Type 'END' on a new line when finished)")
    
    user_requirements = []
    while True:
        line = input()
        if line == 'END':
            break
        user_requirements.append(line)
    
    requirements = '\n'.join(user_requirements) if user_requirements else default_requirements
    
    print("\n" + "="*60)
    print("📋 PROJECT REQUIREMENTS:")
    print("="*60)
    print(requirements)
    print("="*60)
    
    # Confirm before starting
    confirm = input("\nProceed with these requirements? (y/n): ")
    if confirm.lower() != 'y':
        print("Exiting...")
        return
    
    print("\n🔧 Initializing Engineering Team...")
    print("📊 This will go through 4 phases:")
    print("  1️⃣  Planning Phase (Project Manager, Architects)")
    print("  2️⃣  Development Phase (Backend & Frontend Developers)")
    print("  3️⃣  Testing Phase (QA Engineers)")
    print("  4️⃣  Integration & Deployment Phase")
    print("\n⏳ This process may take several minutes...")
    print("="*60 + "\n")
    
    # Prepare inputs
    inputs = {
        'requirements': requirements
    }
    
    try:
        # Create and run the crew
        engineering_team = EngineeringTeam()
        result = engineering_team.crew().kickoff(inputs=inputs)
        
        print("\n" + "="*60)
        print("✅ PROJECT COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📁 Output files have been generated in the 'output' directory:")
        print("  - Project Analysis Report")
        print("  - Backend Architecture")
        print("  - Frontend Architecture")
        print("  - Backend Modules")
        print("  - Frontend Components")
        print("  - Test Suites")
        print("  - Integration Report")
        print("  - Deployment Package")
        print("\n🎉 Your MVP is ready!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error occurred: {str(e)}")
        print("Please check the logs for more details")
        sys.exit(1)


def run_with_custom_requirements(requirements: str):
    """
    Run the crew with custom requirements programmatically
    
    Args:
        requirements: String containing project requirements
    """
    inputs = {
        'requirements': requirements
    }
    
    engineering_team = EngineeringTeam()
    return engineering_team.crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("""
Enhanced Engineering Team - MVP Builder

Usage:
  python main.py              - Run interactively
  python main.py --help       - Show this help message
  python main.py --example    - Run with example Todo app requirements

This tool creates a complete MVP application using a team of AI agents:
- Project Manager for requirements analysis
- System Architects for design
- Developers for implementation
- Testers for quality assurance
- Integration and Deployment specialists

All agents work together to build a functional MVP with minimal features.
            """)
            sys.exit(0)
        elif sys.argv[1] == "--example":
            run_with_custom_requirements(default_requirements)
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
            sys.exit(1)
    else:
        run()