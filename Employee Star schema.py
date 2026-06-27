import pandas as pd

# 1. Load the IBM HR dataset
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")

# 2. Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# 3. Add EmployeeKey if not already available
df["EmployeeKey"] = range(1, len(df) + 1)

# -----------------------------
# Dimension Tables
# -----------------------------

def create_dimension(df, column_name, key_name):
    dim = df[[column_name]].drop_duplicates().reset_index(drop=True)
    dim[key_name] = range(1, len(dim) + 1)
    dim = dim[[key_name, column_name]]
    return dim

dim_department = create_dimension(df, "Department", "DepartmentKey")
dim_jobrole = create_dimension(df, "JobRole", "JobRoleKey")
dim_educationfield = create_dimension(df, "EducationField", "EducationFieldKey")
dim_gender = create_dimension(df, "Gender", "GenderKey")
dim_maritalstatus = create_dimension(df, "MaritalStatus", "MaritalStatusKey")
dim_businesstravel = create_dimension(df, "BusinessTravel", "BusinessTravelKey")
dim_overtime = create_dimension(df, "OverTime", "OverTimeKey")
dim_attrition = create_dimension(df, "Attrition", "AttritionKey")

# -----------------------------
# Merge Keys Back to Fact Table
# -----------------------------

df = df.merge(dim_department, on="Department", how="left")
df = df.merge(dim_jobrole, on="JobRole", how="left")
df = df.merge(dim_educationfield, on="EducationField", how="left")
df = df.merge(dim_gender, on="Gender", how="left")
df = df.merge(dim_maritalstatus, on="MaritalStatus", how="left")
df = df.merge(dim_businesstravel, on="BusinessTravel", how="left")
df = df.merge(dim_overtime, on="OverTime", how="left")
df = df.merge(dim_attrition, on="Attrition", how="left")

# -----------------------------
# Fact Table
# -----------------------------

fact_employee = df[
    [
        "EmployeeKey",
        "EmployeeNumber",
        "Age",
        "DailyRate",
        "DistanceFromHome",
        "Education",
        "EnvironmentSatisfaction",
        "HourlyRate",
        "JobInvolvement",
        "JobLevel",
        "JobSatisfaction",
        "MonthlyIncome",
        "MonthlyRate",
        "NumCompaniesWorked",
        "PercentSalaryHike",
        "PerformanceRating",
        "RelationshipSatisfaction",
        "StockOptionLevel",
        "TotalWorkingYears",
        "TrainingTimesLastYear",
        "WorkLifeBalance",
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion",
        "YearsWithCurrManager",
        "DepartmentKey",
        "JobRoleKey",
        "EducationFieldKey",
        "GenderKey",
        "MaritalStatusKey",
        "BusinessTravelKey",
        "OverTimeKey",
        "AttritionKey"
    ]
]

# -----------------------------
# Export Tables
# -----------------------------

output_folder = "hr_star_schema_output"

import os
os.makedirs(output_folder, exist_ok=True)

fact_employee.to_csv(f"{output_folder}/FactEmployee.csv", index=False)
dim_department.to_csv(f"{output_folder}/DimDepartment.csv", index=False)
dim_jobrole.to_csv(f"{output_folder}/DimJobRole.csv", index=False)
dim_educationfield.to_csv(f"{output_folder}/DimEducationField.csv", index=False)
dim_gender.to_csv(f"{output_folder}/DimGender.csv", index=False)
dim_maritalstatus.to_csv(f"{output_folder}/DimMaritalStatus.csv", index=False)
dim_businesstravel.to_csv(f"{output_folder}/DimBusinessTravel.csv", index=False)
dim_overtime.to_csv(f"{output_folder}/DimOverTime.csv", index=False)
dim_attrition.to_csv(f"{output_folder}/DimAttrition.csv", index=False)

print("Star schema files created successfully!")