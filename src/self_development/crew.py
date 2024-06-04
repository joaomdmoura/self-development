from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool
# from self_development.tools.Supabase import SupabaseTool

@CrewBase
class SelfDevelopmentCrew():
	"""SelfDevelopment crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def journal_analyzer(self) -> Agent:
			return Agent(
					config=self.agents_config['journal_analyzer'],
					verbose=True
			)

	@agent
	def researcher(self) -> Agent:
			return Agent(
					config=self.agents_config['researcher'],
					tools=[SerperDevTool()],  # Example of custom tool, loaded on the beginning of file
					verbose=True
			)

	@agent
	def planner(self) -> Agent:
			return Agent(
					config=self.agents_config['planner'],
					verbose=True
			)

	@task
	def analyze_journal_task(self) -> Task:
			return Task(
					config=self.tasks_config['analyze_journal_task'],
					agent=self.journal_analyzer()
			)

	@task
	def research_task(self) -> Task:
			return Task(
					config=self.tasks_config['research_task'],
					agent=self.researcher()
			)

	@task
	def compile_actions_task(self) -> Task:
			return Task(
					config=self.tasks_config['compile_actions_task'],
					agent=self.planner(),
					output_file='next_actions.md'
			)

	@crew
	def crew(self) -> Crew:
			"""Creates the SelfDevelopment crew"""
			return Crew(
					agents=self.agents,  # Automatically created by the @agent decorator
					tasks=self.tasks,  # Automatically created by the @task decorator
					process=Process.sequential,
					verbose=2,
					# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			)