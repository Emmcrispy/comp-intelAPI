import argparse
from services.classification_service import classify_role

def run_cli():
    parser = argparse.ArgumentParser(description="Classify a job into the correct role bucket.")
    parser.add_argument("--job_type", required=True, help="e.g., Non-clinical Professional")
    parser.add_argument("--job_family", required=True, help="e.g., Finance")
    parser.add_argument("--sub_family", required=True, help="e.g., Tax Accounting")
    parser.add_argument("--single_role", required=True, help="e.g., Tax Accountant")
    parser.add_argument("--career_level", required=True, help="e.g., Senior Professional")

    args = parser.parse_args()

    input_data = {
        "job_type": args.job_type,
        "job_family": args.job_family,
        "sub_family": args.sub_family,
        "single_role": args.single_role,
        "career_level": args.career_level
    }

    result = classify_role(input_data)
    print("🧠 Classification Result:")
    print(result)

if __name__ == "__main__":
    run_cli()
