from crewai import Crew, Process
from agents.agents import create_schema_agent, create_bias_auditor_agent, create_leakage_hunter_agent, create_report_generator_agent,create_data_quality_agent, create_feature_readiness_agent, create_preprocessing_planner_agent, create_model_compatibility_agent, create_pipeline_code_generator_agent
from agents.tasks import schema_audit_task, bias_audit_task, leakage_audit_task, generate_audit_report_task, create_data_quality_task, create_feature_readiness_task, create_preprocessing_planner_task, create_model_compatibility_task, create_pipeline_code_generator_task

class AuditorCrew:
    def __init__(self, dataset_url: str):
        self.dataset_url = dataset_url

    def run(self):
        schema_agent = create_schema_agent()
        bias_agent = create_bias_auditor_agent()
        leakage_agent = create_leakage_hunter_agent()
        data_quality_agent = create_data_quality_agent()
        feature_readiness_agent = create_feature_readiness_agent()
        preprocessing_planner_agent = create_preprocessing_planner_agent()
        model_compatibility_agent = create_model_compatibility_agent()
        pipeline_code_generator_agent = create_pipeline_code_generator_agent()
        reporter = create_report_generator_agent()

        task1 = schema_audit_task(schema_agent, self.dataset_url)
        task2 = bias_audit_task(bias_agent, self.dataset_url)
        task3 = leakage_audit_task(leakage_agent, self.dataset_url)
        task4 = create_data_quality_task(data_quality_agent, self.dataset_url)
        task5 = create_feature_readiness_task(feature_readiness_agent, self.dataset_url)
        task6 = create_preprocessing_planner_task(preprocessing_planner_agent, self.dataset_url)
        task7 = create_model_compatibility_task(model_compatibility_agent, self.dataset_url)
        task8 = create_pipeline_code_generator_task(pipeline_code_generator_agent, self.dataset_url)
        task9 = generate_audit_report_task(reporter)

        crew = Crew(
            agents=[schema_agent, bias_agent, leakage_agent, data_quality_agent, feature_readiness_agent, preprocessing_planner_agent, model_compatibility_agent, pipeline_code_generator_agent, reporter],
            tasks=[task1, task2, task3, task4, task5, task6, task7, task8, task9],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result
