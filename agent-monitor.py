#!/usr/bin/env python3
"""
OCR Scanner Agent - Monitor and Maintenance Script
"""

import os
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path

class OCRScannerAgent:
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path)
        self.config = self.load_config()
        
    def load_config(self):
        """Load agent configuration"""
        config_path = self.repo_path / ".github" / "ocr-agent-config.json"
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {
            "last_check": None,
            "dependencies": {
                "ncnn": "20250220",
                "opencv": "24.10"
            },
            "build_settings": {
                "android_sdk": "33",
                "ndk_version": "29.0.14206865"
            },
            "github": {
                "owner": "Finn-Chaosmedia",
                "repo": "ncnn-ppocrv5"
            }
        }
    
    def check_dependency_updates(self):
        """Check for dependency updates"""
        print("🔍 Checking for dependency updates...")
        
        updates = []
        
        try:
            # Check ncnn releases
            ncnn_response = requests.get(
                "https://api.github.com/repos/Tencent/ncnn/releases/latest",
                timeout=10
            )
            if ncnn_response.status_code == 200:
                latest_ncnn = ncnn_response.json()["tag_name"].replace("v", "")
                if latest_ncnn != self.config["dependencies"]["ncnn"]:
                    updates.append(("ncnn", self.config["dependencies"]["ncnn"], latest_ncnn))
        except Exception as e:
            print(f"⚠️ Failed to check ncnn updates: {e}")
        
        try:
            # Check OpenCV Mobile releases
            opencv_response = requests.get(
                "https://api.github.com/repos/nihui/opencv-mobile/releases/latest",
                timeout=10
            )
            if opencv_response.status_code == 200:
                latest_opencv = opencv_response.json()["tag_name"].replace("v", "")
                if latest_opencv != self.config["dependencies"]["opencv"]:
                    updates.append(("opencv", self.config["dependencies"]["opencv"], latest_opencv))
        except Exception as e:
            print(f"⚠️ Failed to check OpenCV updates: {e}")
        
        return updates
    
    def check_build_status(self):
        """Check GitHub Actions build status"""
        print("📊 Checking build status...")
        
        try:
            # This would use GitHub API to check workflow runs
            # For now, just check local build
            build_log = self.repo_path / "build.log"
            if build_log.exists():
                with open(build_log) as f:
                    last_build = f.read()
                    if "BUILD SUCCESSFUL" in last_build:
                        return "success"
                    elif "BUILD FAILED" in last_build:
                        return "failed"
            return "unknown"
        except Exception as e:
            print(f"⚠️ Failed to check build status: {e}")
            return "error"
    
    def run_build(self):
        """Run automated build"""
        print("🏗️ Running automated build...")
        
        # Change to repo directory
        original_dir = os.getcwd()
        os.chdir(self.repo_path)
        
        try:
            # Make scripts executable
            scripts_dir = Path("scripts")
            if scripts_dir.exists():
                for script in scripts_dir.glob("*.sh"):
                    script.chmod(0o755)
            
            # Run build script
            result = subprocess.run(
                ["./scripts/build.sh"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Save build log
            with open("build.log", "w") as f:
                f.write(f"Build started: {datetime.now()}\n")
                f.write(f"Stdout:\n{result.stdout}\n")
                f.write(f"Stderr:\n{result.stderr}\n")
                f.write(f"Return code: {result.returncode}\n")
            
            if result.returncode == 0:
                print("✅ Build successful!")
                return True
            else:
                print(f"❌ Build failed: {result.stderr[:200]}...")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Build timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def create_issue_report(self, updates, build_status):
        """Create issue report for problems or updates"""
        print("📝 Creating issue report...")
        
        issues = []
        
        # Check for dependency updates
        if updates:
            for dep, current, latest in updates:
                issues.append({
                    "title": f"Update {dep} from {current} to {latest}",
                    "body": f"""## Dependency Update Available

**Dependency:** {dep}
**Current Version:** {current}
**Latest Version:** {latest}

### Action Required
Please update the dependency configuration:
1. Update `scripts/config.sh`
2. Update `.github/ocr-agent-config.json`
3. Test the new version

### Impact
- **Security:** May include security fixes
- **Performance:** May include performance improvements
- **Features:** May include new features

### Testing
After updating, run:
```bash
./scripts/build.sh
```"""
                })
        
        # Check for build failures
        if build_status == "failed":
            issues.append({
                "title": "Build Failure Detected",
                "body": """## Build Failure

The latest build has failed. Please investigate.

### Steps to Investigate
1. Check the build logs
2. Review recent changes
3. Test locally if possible

### Common Issues
- Missing dependencies
- Configuration errors
- Code compilation errors

### Next Steps
1. Fix the build issue
2. Run tests
3. Verify the fix"""
            })
        
        return issues
    
    def save_issues(self, issues):
        """Save issues to file (would create GitHub issues in real implementation)"""
        if not issues:
            print("✅ No issues to report")
            return
        
        issues_file = self.repo_path / ".github" / "agent-issues.json"
        issues_data = {
            "generated": datetime.now().isoformat(),
            "issues": issues
        }
        
        with open(issues_file, "w") as f:
            json.dump(issues_data, f, indent=2)
        
        print(f"📄 Saved {len(issues)} issues to {issues_file}")
        
        # Print issue summaries
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['title']}")
            print(f"   {issue['body'][:100]}...")
    
    def run(self):
        """Main agent loop"""
        print("🤖 OCR Scanner Agent starting...")
        print(f"📁 Repository: {self.repo_path}")
        print(f"⏰ Last check: {self.config.get('last_check', 'Never')}")
        
        # Check for updates
        updates = self.check_dependency_updates()
        if updates:
            print(f"🔄 Found {len(updates)} dependency update(s):")
            for dep, current, latest in updates:
                print(f"   • {dep}: {current} → {latest}")
        
        # Check build status
        build_status = self.check_build_status()
        print(f"🔨 Build status: {build_status}")
        
        # Run build if needed
        should_build = input("\n🚀 Run build now? (y/n): ").lower() == 'y'
        build_success = None
        
        if should_build:
            build_success = self.run_build()
            build_status = "success" if build_success else "failed"
        
        # Create issue report
        issues = self.create_issue_report(updates, build_status)
        self.save_issues(issues)
        
        # Update last check time
        self.config["last_check"] = datetime.now().isoformat()
        self.save_config()
        
        print("\n🎉 Agent completed successfully!")
        print(f"📊 Summary:")
        print(f"   • Dependency updates: {len(updates)}")
        print(f"   • Build status: {build_status}")
        print(f"   • Issues reported: {len(issues)}")
    
    def save_config(self):
        """Save agent configuration"""
        config_path = self.repo_path / ".github" / "ocr-agent-config.json"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        
        print(f"💾 Configuration saved to {config_path}")

if __name__ == "__main__":
    agent = OCRScannerAgent()
    agent.run()