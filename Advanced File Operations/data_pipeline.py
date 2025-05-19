import os
import json
import yaml
from collections import defaultdict, deque
from datetime import datetime

class PipelineStep:
    def __init__(self, name, module, description, depends_on, parameters):
        self.name = name
        self.module = module
        self.description = description
        self.depends_on = depends_on or []
        self.parameters = parameters or {}
        self.status = "PENDING"

class DataPipeline:
    def __init__(self, config_path):
        self.config_path = config_path
        self.pipeline_config = self.load_config()
        self.steps = self.build_steps()
        self.dag = self.build_dag()
        self.execution_log = []

    def load_config(self):
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def build_steps(self):
        return {
            step["name"]: PipelineStep(**step)
            for step in self.pipeline_config["pipeline"]["steps"]
        }

    def build_dag(self):
        dag = defaultdict(list)
        for step in self.steps.values():
            for dependency in step.depends_on:
                dag[dependency].append(step.name)
        return dag

    def execute(self):
        start_time = datetime.now()
        print("=== Sales Data Analyzer Pipeline ===")
        print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        order = self.topological_sort()
        for step_name in order:
            step = self.steps[step_name]
            try:
                print(f"Executing: {step.name} - {step.description}")
                step.status = "COMPLETED"
                self.execution_log.append(f"{step.name} [COMPLETED]")
            except Exception as e:
                step.status = "FAILED"
                self.execution_log.append(f"{step.name} [FAILED] - {str(e)}")
                break

        end_time = datetime.now()
        print(f"Status: COMPLETED\nExecution time: {(end_time - start_time).total_seconds():.1f} seconds")
        self.print_log()

    def topological_sort(self):
        in_degree = {name: 0 for name in self.steps}
        for deps in self.dag.values():
            for step in deps:
                in_degree[step] += 1

        queue = deque([name for name, deg in in_degree.items() if deg == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in self.dag[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return result

    def print_log(self):
        print("== Step Execution ==")
        for log_entry in self.execution_log:
            print("-", log_entry)

if __name__ == "__main__":
    pipeline = DataPipeline("pipeline_config.yaml")
    pipeline.execute()
