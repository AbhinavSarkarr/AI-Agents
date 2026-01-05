from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileWriterTool, FileReadTool
from .tools.custom_tool import ProgressTracker, CodeExecutor, CustomFileWriter


@CrewBase
class EngineeringTeam():
    """Enhanced Engineering Team with comprehensive development workflow"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize tools
        self.search_tool = SerperDevTool()
        self.file_writer = CustomFileWriter()
        self.file_reader = FileReadTool()
        self.progress_tracker = ProgressTracker()
        self.code_executor = CodeExecutor()

    # Phase 1: Planning Agents
    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project_manager'],
            tools=[self.search_tool, self.progress_tracker, self.file_writer],
            verbose=True,
        )

    @agent
    def backend_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_architect'],
            tools=[self.file_writer, self.file_reader],
            verbose=True,
        )

    @agent
    def frontend_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_architect'],
            tools=[self.file_writer, self.file_reader],
            verbose=True,
        )

    # Phase 2: Development Agents
    @agent
    def backend_developer_1(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer_1'],
            tools=[self.file_writer, self.file_reader, self.code_executor],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3
        )

    @agent
    def backend_developer_2(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer_2'],
            tools=[self.file_writer, self.file_reader, self.code_executor],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3
        )

    @agent
    def frontend_developer_1(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer_1'],
            tools=[self.file_writer, self.file_reader],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3
        )

    @agent
    def frontend_developer_2(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer_2'],
            tools=[self.file_writer, self.file_reader],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3
        )

    # Phase 3: Testing Agents
    @agent
    def backend_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_tester'],
            tools=[self.file_writer, self.file_reader, self.code_executor],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3
        )

    @agent
    def frontend_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_tester'],
            tools=[self.file_writer, self.file_reader, self.code_executor],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3
        )

    # Phase 4: Integration & Deployment Agents
    @agent
    def integration_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['integration_specialist'],
            tools=[self.file_reader, self.code_executor, self.file_writer],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=500,
            max_retry_limit=3
        )

    @agent
    def deployment_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['deployment_engineer'],
            tools=[self.file_writer, self.file_reader, self.code_executor],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=1000,
            max_retry_limit=3
        )

    # Task definitions
    @task
    def project_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_analysis_task']
        )

    @task
    def backend_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_architecture_task']
        )

    @task
    def frontend_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_architecture_task']
        )

    @task
    def backend_module_1_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_module_1_task']
        )

    @task
    def backend_module_2_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_module_2_task']
        )

    @task
    def frontend_module_1_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_module_1_task']
        )

    @task
    def frontend_module_2_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_module_2_task']
        )

    @task
    def backend_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_testing_task']
        )

    @task
    def frontend_testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_testing_task']
        )

    @task
    def integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['integration_task']
        )

    @task
    def deployment_task(self) -> Task:
        return Task(
            config=self.tasks_config['deployment_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the enhanced engineering team crew with phased workflow"""
        
        # Define the workflow sequence
        # Phase 1: Planning (Sequential)
        planning_tasks = [
            self.project_analysis_task(),
            self.backend_architecture_task(),
            self.frontend_architecture_task()
        ]
        
        # Phase 2: Development (Parallel where possible)
        development_tasks = [
            self.backend_module_1_task(),
            self.backend_module_2_task(),
            self.frontend_module_1_task(),
            self.frontend_module_2_task()
        ]
        
        # Phase 3: Testing (Parallel)
        testing_tasks = [
            self.backend_testing_task(),
            self.frontend_testing_task()
        ]
        
        # Phase 4: Integration & Deployment (Sequential)
        deployment_tasks = [
            self.integration_task(),
            self.deployment_task()
        ]
        
        # Combine all tasks in order
        all_tasks = planning_tasks + development_tasks + testing_tasks + deployment_tasks
        
        return Crew(
            agents=self.agents,
            tasks=all_tasks,
            process=Process.sequential,  # Main process is sequential
            verbose=True,
            full_output=True,
            share_crew=True,  # Enable context sharing between agents
        )