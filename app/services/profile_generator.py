def generate_role_profile(role_data: dict):
    return {
        "summary": f"A {role_data['career_level']} {role_data['single_role']} working in {role_data['sub_family']}, part of the {role_data['job_family']} family ({role_data['job_type']}).",
        "essential_functions": [
            f"Perform key functions of {role_data['single_role']}",
            f"Support {role_data['job_family']} objectives",
            f"Collaborate across {role_data['job_type']} departments"
        ],
        "qualifications": [
            f"{role_data['career_level']} level education and experience required",
            "Strong communication and teamwork"
        ]
    }
