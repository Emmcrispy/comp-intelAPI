def generate_role_profile(role_info: dict):

    job_type = role_info.get("job_type")
    job_family = role_info.get("job_family")
    sub_family = role_info.get("sub_family")
    role = role_info.get("single_role")
    level = role_info.get("career_level")


    summary = f"{role} is a {level.lower()} position in the {job_family.lower()} function, under the {job_type.lower()} umbrella. The role focuses on delivering results within the {sub_family.lower()} sub-domain."
    functions = [f"Execute responsibilities aligned to the {sub_family} function.", "Ensure compliance with policy and process.", "Collaborate cross-functionally on strategic goals."]
    qualifications = [f"{level} level experience in {job_family}.", "Relevant degree or certification.", "Strong communication and analytical skills."]

    return {
        "summary": summary,
        "essential_functions": functions,
        "qualifications": qualifications
    }
