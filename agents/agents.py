import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()

# llm = LLM(
#     model="claude-haiku-4-5-20251001",
#     api_key=os.getenv("ANTHROPIC_API_KEY"),
#     max_tokens=10000,
#     temperature=0.7,
#     verbose=True
# )
from agents.tools import read_dataset_content

llm = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    max_tokens=10000,
    temperature=0.7
    )
# Agent 1
def create_schema_agent():
    return Agent(
        role='Dataset Schema Auditor',
        goal='Analyze CSV or Excel datasets to understand their structure, infer the datasets domain, and generate a detailed schema report that will guide further data quality and ML-readiness checks.',
        backstory="""
        You are a senior data scientist and data governance expert who
        specializes in auditing raw datasets before they enter machine
        learning pipelines.

        Your job is to quickly understand unfamiliar datasets by examining
        their structure, column names, value patterns, and statistics.
        """,
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# Agent 2
def create_bias_auditor_agent():
    return Agent(
        role="Dataset Bias and Fairness Auditor",
        goal="Evaluate datasets for potential bias, class imbalance, and fairness risks.",
        backstory="Expert in responsible AI and ML fairness.",
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# Agent 3
def create_leakage_hunter_agent():
    return Agent(
        role="Target Leakage Detection Specialist",
        goal="Identify features that may leak information about the target variable.",
        backstory="Senior ML auditor specializing in detecting subtle data leakage.",
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# Agent 4
def create_data_quality_agent():
    return Agent(
        role="Data Quality Auditor",
        goal="Perform a comprehensive data quality audit of the dataset.",
        backstory="Senior data quality engineer specializing in dataset anomalies.",
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# Agent 5
def create_feature_readiness_agent():
    return Agent(
        role="Machine Learning Feature Readiness Analyst",
        goal="Evaluate dataset features for ML suitability.",
        backstory="Senior ML feature engineer.",
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# Agent 6
def create_preprocessing_planner_agent():
    return Agent(
        role="Machine Learning Preprocessing Strategist",
        goal="Design a complete and effective data preprocessing strategy.",
        backstory="Senior ML pipeline architect.",
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# Agent 7
def create_model_compatibility_agent():
    return Agent(
        role="Machine Learning Model Compatibility Advisor",
        goal="Recommend the most suitable ML models for training.",
        backstory="Senior ML scientist with expertise in algorithm selection.",
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# Agent 8
def create_pipeline_code_generator_agent():
    return Agent(
        role="Machine Learning Pipeline Code Generator",
        goal="Generate a complete and executable Python preprocessing pipeline.",
        backstory="Senior ML engineer responsible for functional pipelines.",
        tools=[read_dataset_content],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

#Agent 9
def create_report_generator_agent():
    return Agent(
        role="Dataset Audit Report Generator",

        goal="""
        Combine findings from all previous dataset auditing agents and produce a
        highly structured dataset audit result. The output must strictly follow
        the provided Pydantic JSON schema structure.
        """,

        backstory="""
        You are a senior AI documentation specialist and machine learning
        governance expert. Your job is to transform technical analysis from
        multiple dataset auditing agents into a professional report that
        ML teams can easily understand and act upon.

        You carefully organize information about:
        - dataset structure
        - domain context
        - bias and fairness risks
        - data leakage threats
        - feature quality issues

        Your reports are concise, well-structured, and actionable, helping
        organizations decide whether a dataset is ready for machine learning
        or requires further cleaning and validation.
        """,

        llm=llm,

        verbose=True,

        allow_delegation=False
    )

