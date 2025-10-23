"""
🧪 Verification Script

Quick test to verify everything is set up correctly.
"""

import os
import sys
from pathlib import Path


def check_file(path: str, description: str) -> bool:
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False


def check_directory(path: str, description: str) -> bool:
    """Check if a directory exists"""
    if os.path.isdir(path):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False


def main():
    """Run all checks"""
    print("🧪 Verifying 5.5-advanced-sessions setup...")
    print("=" * 60)
    
    base_path = Path(__file__).parent
    all_good = True
    
    # Check main folders
    print("\n📁 Checking folder structure...")
    folders = [
        (base_path / "agent", "Agent folder"),
        (base_path / "1-web-ui-creator", "Web UI folder"),
        (base_path / "2-rest-api-manager", "REST API folder"),
        (base_path / "3-cli-interactive", "CLI folder"),
        (base_path / "4-programmatic-examples", "Examples folder")
    ]
    
    for folder_path, desc in folders:
        if not check_directory(str(folder_path), desc):
            all_good = False
    
    # Check agent files
    print("\n📄 Checking agent files...")
    agent_files = [
        (base_path / "agent" / "__init__.py", "Agent __init__.py"),
        (base_path / "agent" / "agent.py", "Agent definition")
    ]
    
    for file_path, desc in agent_files:
        if not check_file(str(file_path), desc):
            all_good = False
    
    # Check Web UI files
    print("\n🎨 Checking Web UI files...")
    webui_files = [
        (base_path / "1-web-ui-creator" / "app.py", "Streamlit app"),
        (base_path / "1-web-ui-creator" / "requirements.txt", "Web UI requirements"),
        (base_path / "1-web-ui-creator" / "README.md", "Web UI README")
    ]
    
    for file_path, desc in webui_files:
        if not check_file(str(file_path), desc):
            all_good = False
    
    # Check REST API files
    print("\n🔌 Checking REST API files...")
    api_files = [
        (base_path / "2-rest-api-manager" / "session_manager.py", "SessionManager class"),
        (base_path / "2-rest-api-manager" / "examples.py", "API examples"),
        (base_path / "2-rest-api-manager" / "README.md", "API README")
    ]
    
    for file_path, desc in api_files:
        if not check_file(str(file_path), desc):
            all_good = False
    
    # Check CLI files
    print("\n⌨️ Checking CLI files...")
    cli_files = [
        (base_path / "3-cli-interactive" / "create_session.py", "CLI session creator"),
        (base_path / "3-cli-interactive" / "README.md", "CLI README")
    ]
    
    for file_path, desc in cli_files:
        if not check_file(str(file_path), desc):
            all_good = False
    
    # Check example files
    print("\n🚀 Checking example files...")
    example_files = [
        (base_path / "4-programmatic-examples" / "multi_user_demo.py", "Multi-user demo"),
        (base_path / "4-programmatic-examples" / "async_sessions.py", "Async demo"),
        (base_path / "4-programmatic-examples" / "README.md", "Examples README")
    ]
    
    for file_path, desc in example_files:
        if not check_file(str(file_path), desc):
            all_good = False
    
    # Check documentation
    print("\n📚 Checking documentation...")
    doc_files = [
        (base_path / "README.md", "Main README"),
        (base_path / "QUICKSTART.md", "Quick start guide"),
        (base_path / "COMPARISON.md", "Comparison guide"),
        (base_path / ".env", "Environment file")
    ]
    
    for file_path, desc in doc_files:
        if not check_file(str(file_path), desc):
            all_good = False
    
    # Check agent content
    print("\n🔍 Checking agent configuration...")
    agent_file = base_path / "agent" / "agent.py"
    if agent_file.exists():
        content = agent_file.read_text()
        
        checks = [
            ("dynamic_session_agent", "Agent name is correct"),
            ("root_agent", "Root agent alias exists"),
            ("{%- if user_name %}", "Jinja2 conditionals present"),
            ("gemini-2.0-flash", "Using correct model")
        ]
        
        for check_str, desc in checks:
            if check_str in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc} - NOT FOUND")
                all_good = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✅ All checks passed! You're ready to go!")
        print("\n🚀 Next steps:")
        print("  1. Make sure .env has your GOOGLE_API_KEY")
        print("  2. Run: adk web")
        print("  3. Choose a method and create sessions!")
        print("\n📖 Read QUICKSTART.md for detailed instructions")
    else:
        print("❌ Some checks failed!")
        print("\n🔧 Please fix the issues above and run again")
    print("=" * 60)
    
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
