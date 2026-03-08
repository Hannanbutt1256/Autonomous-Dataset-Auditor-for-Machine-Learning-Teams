from crewai import Task
from agents.agents import create_schema_agent, create_bias_auditor_agent, create_leakage_hunter_agent, create_report_generator_agent
from api.models import AuditResponse

# Task 1
def schema_audit_task(agent, dataset_url):
    return Task(
        description=f"""
        Analyze the dataset located at: {dataset_url}.
        The dataset may be in CSV or Excel format.

        Perform the following analysis:

        1. Infer the dataset's domain or industry field
           (e.g., healthcare, finance, marketing, retail, education, etc.)

        2. Identify the dataset structure:
           - Number of rows
           - Number of columns
           - Column names

        3. Determine the data type for each column:
           - numeric
           - categorical
           - datetime
           - text
           - identifier

        4. Detect:
           - Missing values
           - Duplicate columns
           - High-cardinality categorical columns

        5. Identify potential roles of columns:
           - feature
           - target variable
           - identifier
           - metadata

        6. Provide an initial summary of dataset quality
           and highlight columns that may cause issues
           during machine learning training.
        """,
        expected_output="""
        A structured dataset schema report containing:

        1. Dataset Overview
        - Domain / Industry
        - Total Rows
        - Total Columns

        2. Column Schema Table
        - Column Name
        - Inferred Type
        - Missing Values %
        - Unique Values
        - Example Values
        - Column Role (feature / target / identifier)

        3. Initial Observations
        - Potential target variables
        - Possible identifier columns
        - Data quality warnings

        4. Recommendations
        - Columns requiring cleaning
        - Columns to drop or transform
        """,

        agent=agent
    )

# Task 2
def bias_audit_task(agent, dataset_url):

    return Task(
        description=f"""
        Analyze the dataset located at: {dataset_url} to detect
        potential bias and fairness risks.

        Perform the following checks:

        1. Identify the target variable if present.

        2. Analyze class distribution:
           - Detect class imbalance
           - Calculate class ratios

        3. Identify sensitive attributes such as:
           - gender
           - age
           - ethnicity
           - location
           - income level

        4. Evaluate representation balance across groups.

        5. Detect potential fairness risks where certain
           groups are significantly underrepresented.

        6. Highlight columns that may introduce bias
           into machine learning models.

        7. Provide mitigation suggestions such as:
           - resampling
           - reweighting
           - feature removal
        """,

        expected_output="""
        A structured bias audit report containing:

        1. Target Variable Analysis
        - Target column
        - Class distribution
        - Imbalance ratio

        2. Sensitive Attribute Detection
        - Columns potentially representing demographics
        - Distribution across groups

        3. Representation Analysis
        - Overrepresented groups
        - Underrepresented groups

        4. Bias Risk Assessment
        - High risk
        - Medium risk
        - Low risk

        5. Recommendations
        - Resampling strategies
        - Feature engineering suggestions
        - Bias mitigation methods
        """,

        agent=agent
    )
# Task 3

def leakage_audit_task(agent, dataset_url):

    return Task(
        description=f"""
        Analyze the dataset located at: {dataset_url}
        and identify potential target leakage risks.

        Perform the following checks:

        1. Identify the target variable.

        2. Detect columns that:
           - Contain the target name in their column name
           - Appear derived from the target
           - Have extremely high correlation with the target
           - Represent post-event outcomes

        3. Check for:
           - Timestamp columns occurring after the target event
           - Data collected after prediction time
           - Aggregated statistics that may include future data

        4. Identify:
           - ID columns encoding label information
           - Columns suspiciously predictive of the target

        5. Flag:
           - High leakage risk
           - Moderate leakage risk
           - Low risk

        6. Recommend actions:
           - Drop column
           - Transform
           - Time-based split
           - Re-collection of data
        """,

        expected_output="""
        A structured leakage analysis report including:

        1. Target Variable Identified

        2. Potential Leakage Columns:
           - Column Name
           - Leakage Type (Direct / Proxy / Temporal / ID-based)
           - Risk Level
           - Explanation

        3. Temporal Risk Analysis

        4. Data Split Risk Assessment

        5. Recommended Remediation Steps
        """,

        agent=agent
    )

#Task 4
def create_data_quality_task(agent, dataset_url):
    return Task(
        description=(
            f"""
            Perform a comprehensive data quality audit for the dataset located at:
            {dataset_url}
            Your analysis should include:

            1. Duplicate records
            2. Missing values per column
            3. Outliers in numerical columns
            4. Distribution skewness
            5. Inconsistent data formatting
            6. Invalid or impossible values
            7. Constant or near-constant columns
            8. Columns with extremely high cardinality

            Provide insights on how these issues might affect machine learning models.
            """
        ),
        expected_output=(
            """
            A structured data quality report containing:

            - Dataset overview
            - Duplicate row statistics
            - Missing value summary per column
            - Outlier detection results
            - Skewness analysis
            - Invalid or inconsistent values
            - Constant or near-zero variance columns
            - High cardinality categorical columns
            - Recommended data cleaning actions
            """
        ),
        agent=agent
    )
#Task 5
def create_feature_readiness_task(agent, dataset_url, target_column=None):
    return Task(
        description=f"""
        Analyze the dataset located at:

        {dataset_url}

        Your objective is to evaluate whether the dataset features are suitable for machine learning.

        Perform the following analysis:

        1. Identify identifier columns that should not be used as features
        2. Detect constant or near-constant columns
        3. Detect high-cardinality categorical features
        4. Identify highly correlated numerical features
        5. Detect redundant or duplicated features
        6. Identify features with weak predictive potential
        7. Evaluate categorical vs numerical feature balance
        8. Determine whether features require encoding or scaling
        9. Identify features that may require transformation

        Target column: {target_column}

        Explain how each issue could affect machine learning models.
        """,

        expected_output="""
        A structured Feature Readiness Report containing:

        1. Dataset Feature Overview
        - total number of features
        - numerical vs categorical feature counts

        2. Identifier Columns
        - columns that uniquely identify records

        3. Constant / Near-Zero Variance Columns
        - features with little to no variation

        4. High Cardinality Features
        - categorical columns with many unique values

        5. Highly Correlated Features
        - pairs of numerical features with strong correlation

        6. Redundant or Duplicate Features

        7. Feature Encoding Requirements
        - categorical features needing encoding

        8. Feature Scaling Requirements
        - numerical features that may require normalization or scaling

        9. Recommended Feature Actions
        - drop
        - keep
        - encode
        - scale
        - transform

        10. Summary of Feature Readiness for Machine Learning
        """,

        agent=agent
    )

#Task 6
def create_preprocessing_planner_task(agent, dataset_url, target_column=None):
    return Task(
        description=f"""
        Using the findings from previous dataset analysis agents, design a complete preprocessing plan
        for the dataset located at:

        {dataset_url}

        Target column: {target_column}

        Consider the following information from previous audits:

        - Schema analysis results
        - Data quality issues
        - Bias detection results
        - Data leakage risks
        - Feature readiness evaluation

        Based on these findings, create a structured preprocessing plan that prepares the dataset
        for machine learning.

        Your plan should include:

        1. Handling missing values
        2. Removing duplicates
        3. Handling outliers
        4. Encoding categorical variables
        5. Scaling or normalizing numerical features
        6. Dropping irrelevant or problematic columns
        7. Addressing class imbalance if present
        8. Feature selection recommendations
        9. Data transformations (log transforms, binning, etc.)
        10. Steps to avoid data leakage during training
        """,

        expected_output="""
        A structured preprocessing strategy including:

        1. Dataset Cleaning Steps
        - duplicate removal
        - invalid data corrections

        2. Missing Value Handling Strategy
        - columns requiring imputation
        - recommended imputation methods

        3. Outlier Handling
        - columns requiring outlier treatment
        - recommended method (remove, cap, transform)

        4. Feature Engineering Strategy
        - features to transform
        - new features to create (if applicable)

        5. Feature Encoding Plan
        - categorical features requiring encoding
        - recommended encoding method

        6. Feature Scaling Plan
        - numerical features requiring scaling

        7. Feature Removal Plan
        - identifier columns
        - redundant features
        - leakage-prone features

        8. Bias Mitigation Strategy
        - balancing techniques if needed

        9. Final ML-Ready Dataset Description
        - expected dataset after preprocessing

        10. Step-by-Step Preprocessing Pipeline Plan
        """,

        agent=agent
    )
#Task 7
def create_model_compatibility_task(agent, dataset_url, target_column=None):
    return Task(
        description=f"""
        Analyze the dataset located at:

        {dataset_url}

        Target column: {target_column}

        Based on the dataset structure and previous analysis results from other agents
        (schema analysis, data quality audit, bias detection, feature readiness, and
        preprocessing strategy), determine which machine learning models are suitable
        for this dataset.

        Your evaluation should consider:

        1. Type of machine learning problem
           - classification
           - regression
           - clustering
           - anomaly detection

        2. Target variable characteristics
        3. Dataset size and dimensionality
        4. Feature types (categorical vs numerical)
        5. Class imbalance
        6. Presence of noisy or missing data
        7. Feature relationships and correlations

        Based on this information, recommend suitable machine learning models and explain why.
        """,

        expected_output="""
        A structured Model Compatibility Report including:

        1. Problem Type Identification
        - classification / regression / clustering / other

        2. Target Variable Analysis
        - type of target variable
        - number of classes (if classification)

        3. Dataset Complexity Assessment
        - dataset size
        - number of features
        - feature types

        4. Recommended Machine Learning Models
        - list of suitable algorithms
        - explanation for each recommendation

        5. Models to Avoid
        - algorithms that are unsuitable for the dataset
        - explanation why

        6. Suggested Baseline Models
        - simple models to try first

        7. Advanced Models for Performance Optimization
        - more complex models that may improve performance

        8. Additional Training Considerations
        - handling class imbalance
        - cross validation strategy
        - evaluation metrics
        """,

        agent=agent
    )
#Task 8
def create_pipeline_code_generator_task(agent, dataset_url, target_column=None):
    return Task(
        description=f"""
        Using the findings and recommendations from all dataset audit agents, generate a complete
        Python preprocessing pipeline for the dataset located at:

        {dataset_url}

        Target column: {target_column}

        Your code should implement recommendations from:

        - Schema analysis
        - Data quality audit
        - Bias detection
        - Data leakage detection
        - Feature readiness evaluation
        - Preprocessing planning
        - Model compatibility analysis

        The generated code should:

        1. Load the dataset
        2. Remove duplicate rows
        3. Handle missing values
        4. Remove problematic columns (identifiers, leakage features, etc.)
        5. Encode categorical features
        6. Scale numerical features
        7. Handle outliers if required
        8. Split features and target variable
        9. Create a clean preprocessing pipeline using scikit-learn
        10. Prepare the dataset for model training

        Ensure the code is clean, modular, well-commented, and ready to execute.
        """,

        expected_output="""
        A complete Python script that includes:

        1. Required imports
        2. Dataset loading
        3. Data cleaning operations
        4. Missing value handling
        5. Feature removal
        6. Feature encoding
        7. Feature scaling
        8. Feature/target split
        9. A scikit-learn preprocessing pipeline
        10. Final dataset ready for model training

        The code should be production-quality, well-commented, and executable.
        """,

        agent=agent
    )

#Task 9
def generate_audit_report_task(agent):

    return Task(
        description="""
        Generate a comprehensive dataset audit report by combining the
        results from previous agents in the pipeline:

        1. Schema & Context Analysis
        2. Bias and Fairness Audit
        3. Data Leakage Detection
        4. Data Quality Audit
        5. Feature Readiness Evaluation
        6. Preprocessing Planning
        7. Model Compatibility Analysis
        8. Pipeline Code Generation

        Your task is to organize these findings into a structured report
        suitable for ML teams.

        The report should clearly summarize:
        - Dataset overview
        - Schema insights
        - Bias and fairness risks
        - Leakage risks
        - Overall dataset readiness
        - Recommended actions before model training
        """,

        expected_output="""
        A structured JSON Dataset Audit Report strictly adhering to the Pydantic schema provided.
        
        Ensure you populate:
        - summary: A DatasetSummary object (dataset_name, rows, columns, domain, ml_readiness, bias_risk, leakage_risk, data_quality_risk, feature_readiness_risk, preprocessing_plan_risk, model_compatibility_risk, pipeline_code_risk).
        - schema_analysis: A detailed dictionary of schema findings.
        - bias_analysis: A detailed dictionary of bias/fairness warnings.
        - leakage_analysis: A detailed dictionary of target leakage risks.
        - recommendations: A list of actionable string recommendations.
        - data_quality_analysis: A detailed dictionary of data quality findings.
        - feature_readiness_analysis: A detailed dictionary of feature readiness findings.
        - preprocessing_plan: A detailed dictionary of preprocessing plan findings.
        - model_compatibility_analysis: A detailed dictionary of model compatibility findings.
        - pipeline_code: A detailed string containing the generated python pipeline code.
        - human_report: A comprehensive Markdown string of the full report.
        """,
        # output_pydantic=AuditResponse,
        agent=agent
    )