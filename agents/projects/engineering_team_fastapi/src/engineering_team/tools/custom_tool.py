"""
Custom tools for the Engineering Team agents
"""

from crewai.tools import BaseTool
from typing import Type, Dict, List, Any
from pydantic import BaseModel, Field
import subprocess
import json
import os
from datetime import datetime


class ProgressTrackerInput(BaseModel):
    """Input schema for Progress Tracker"""
    action: str = Field(..., description="Action to perform: 'add', 'update', 'complete', 'report'")
    task_name: str = Field(None, description="Name of the task")
    status: str = Field(None, description="Status: 'pending', 'in_progress', 'completed', 'blocked'")
    details: str = Field(None, description="Additional details about the task")


class ProgressTracker(BaseTool):
    name: str = "Progress Tracker"
    description: str = "Tracks project progress, tasks completion, and maintains a progress report"
    args_schema: Type[BaseModel] = ProgressTrackerInput
    tasks: Dict[str, Any] = {}
    progress_file: str = "output/progress_report.json"
    
    def __init__(self):
        super().__init__()
        self.tasks = {}
        self.progress_file = "output/progress_report.json"
        os.makedirs("output", exist_ok=True)
    
    def _run(self, action: str, task_name: str = None, status: str = None, details: str = None) -> str:
        """Track project progress"""
        if action == "add":
            if task_name:
                self.tasks[task_name] = {
                    "status": status or "pending",
                    "details": details or "",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                self._save_progress()
                return f"Task '{task_name}' added to tracking"
        
        elif action == "update":
            if task_name and task_name in self.tasks:
                if status:
                    self.tasks[task_name]["status"] = status
                if details:
                    self.tasks[task_name]["details"] = details
                self.tasks[task_name]["updated_at"] = datetime.now().isoformat()
                self._save_progress()
                return f"Task '{task_name}' updated"
        
        elif action == "complete":
            if task_name and task_name in self.tasks:
                self.tasks[task_name]["status"] = "completed"
                self.tasks[task_name]["completed_at"] = datetime.now().isoformat()
                self.tasks[task_name]["updated_at"] = datetime.now().isoformat()
                self._save_progress()
                return f"Task '{task_name}' marked as completed"
        
        elif action == "report":
            return self._generate_report()
        
        return "Invalid action or parameters"
    
    def _save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def _generate_report(self) -> str:
        """Generate a progress report"""
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return "No tasks tracked yet"
        
        completed = sum(1 for t in self.tasks.values() if t["status"] == "completed")
        in_progress = sum(1 for t in self.tasks.values() if t["status"] == "in_progress")
        pending = sum(1 for t in self.tasks.values() if t["status"] == "pending")
        blocked = sum(1 for t in self.tasks.values() if t["status"] == "blocked")
        
        completion_percentage = (completed / total_tasks) * 100 if total_tasks > 0 else 0
        
        report = f"""
        === PROGRESS REPORT ===
        Total Tasks: {total_tasks}
        Completed: {completed} ({completion_percentage:.1f}%)
        In Progress: {in_progress}
        Pending: {pending}
        Blocked: {blocked}
        
        Task Details:
        """
        
        for task_name, task_info in self.tasks.items():
            report += f"\n  - {task_name}: {task_info['status']}"
            if task_info.get('details'):
                report += f" ({task_info['details']})"
        
        return report


class CodeExecutorInput(BaseModel):
    """Input schema for Code Executor"""
    code: str = Field(None, description="Code string to execute")
    file_path: str = Field(None, description="Path to file to execute")
    language: str = Field("python", description="Programming language: python or javascript")


class CodeExecutor(BaseTool):
    name: str = "Code Executor"
    description: str = "Executes Python or JavaScript code and returns the output or errors"
    args_schema: Type[BaseModel] = CodeExecutorInput
    execution_dir: str = "output/execution"
    
    def __init__(self):
        super().__init__()
        self.execution_dir = "output/execution"
        os.makedirs(self.execution_dir, exist_ok=True)
    
    def _run(self, code: str = None, file_path: str = None, language: str = "python") -> str:
        """Execute code and return output"""
        try:
            if language == "python":
                return self._execute_python(code, file_path)
            elif language == "javascript":
                return self._execute_javascript(code, file_path)
            else:
                return f"Language {language} not supported yet"
        except Exception as e:
            return f"Execution error: {str(e)}"
    
    def _execute_python(self, code: str = None, file_path: str = None) -> str:
        """Execute Python code"""
        if file_path:
            try:
                result = subprocess.run(
                    ["python", file_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.execution_dir
                )
                return self._format_result(result)
            except subprocess.TimeoutExpired:
                return "Execution timeout (30 seconds)"
            except Exception as e:
                return f"Error executing file: {str(e)}"
        
        elif code:
            temp_file = os.path.join(self.execution_dir, "temp_exec.py")
            try:
                with open(temp_file, 'w') as f:
                    f.write(code)
                
                result = subprocess.run(
                    ["python", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.execution_dir
                )
                return self._format_result(result)
            except subprocess.TimeoutExpired:
                return "Execution timeout (30 seconds)"
            except Exception as e:
                return f"Error executing code: {str(e)}"
            finally:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        
        return "No code or file path provided"
    
    def _execute_javascript(self, code: str = None, file_path: str = None) -> str:
        """Execute JavaScript code using Node.js"""
        if file_path:
            try:
                result = subprocess.run(
                    ["node", file_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.execution_dir
                )
                return self._format_result(result)
            except subprocess.TimeoutExpired:
                return "Execution timeout (30 seconds)"
            except FileNotFoundError:
                return "Node.js not installed or not in PATH"
            except Exception as e:
                return f"Error executing file: {str(e)}"
        
        elif code:
            temp_file = os.path.join(self.execution_dir, "temp_exec.js")
            try:
                with open(temp_file, 'w') as f:
                    f.write(code)
                
                result = subprocess.run(
                    ["node", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.execution_dir
                )
                return self._format_result(result)
            except subprocess.TimeoutExpired:
                return "Execution timeout (30 seconds)"
            except FileNotFoundError:
                return "Node.js not installed or not in PATH"
            except Exception as e:
                return f"Error executing code: {str(e)}"
            finally:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        
        return "No code or file path provided"
    
    def _format_result(self, result) -> str:
        """Format execution result"""
        output = ""
        if result.stdout:
            output += f"Output:\n{result.stdout}\n"
        if result.stderr:
            output += f"Errors:\n{result.stderr}\n"
        if result.returncode != 0:
            output += f"Exit code: {result.returncode}\n"
        elif not result.stdout and not result.stderr:
            output = "Execution completed successfully (no output)"
        return output.strip()


class CustomFileWriterInput(BaseModel):
    """Input schema for Custom File Writer"""
    filename: str = Field(..., description="Name of the file to write")
    content: str = Field(..., description="Content to write to the file")
    directory: str = Field("output", description="Directory to write the file to")
    overwrite: bool = Field(True, description="Whether to overwrite existing file")


class CustomFileWriter(BaseTool):
    name: str = "Custom File Writer"
    description: str = "Writes content to files with proper directory handling for the engineering team workflow"
    args_schema: Type[BaseModel] = CustomFileWriterInput
    
    def __init__(self):
        super().__init__()
    
    def _run(self, filename: str, content: str, directory: str = "output", overwrite: bool = True) -> str:
        """Write content to a file in the specified directory"""
        try:
            # Force all files to go to output directory (ignore /tmp requests)
            if directory == "/tmp" or directory.startswith("/tmp/"):
                directory = "output"
            
            # Ensure directory exists
            os.makedirs(directory, exist_ok=True)
            
            # Create full file path
            file_path = os.path.join(directory, filename)
            
            # Check if file exists and overwrite is False
            if os.path.exists(file_path) and not overwrite:
                return f"File {filename} already exists in {directory}. Use overwrite=True to replace it."
            
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Content successfully written to {file_path}"
            
        except Exception as e:
            return f"Error writing to file {filename}: {str(e)}"
