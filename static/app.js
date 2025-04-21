const apiBase = "/api/jobs";

async function fetchDropdown(endpoint, targetId, query = {}) {
    const url = new URL(`${apiBase}/${endpoint}`, window.location.origin);
    Object.entries(query).forEach(([k, v]) => url.searchParams.append(k, v));

    const res = await fetch(url);
    const data = await res.json();
    const select = document.getElementById(targetId);
    select.innerHTML = `<option disabled selected>Select ${targetId.replace('_', ' ')}</option>`;
    data.forEach(option => {
    select.innerHTML += `<option value="${option}">${option}</option>`;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    fetchDropdown("job-types", "job_type");

    document.getElementById("job_type").addEventListener("change", e => {
    fetchDropdown("job-families", "job_family", { job_type: e.target.value });
    });

    document.getElementById("job_family").addEventListener("change", e => {
    const job_type = document.getElementById("job_type").value;
    fetchDropdown("sub-families", "sub_family", {
        job_type, job_family: e.target.value
    });
    });

    document.getElementById("sub_family").addEventListener("change", e => {
    const job_type = document.getElementById("job_type").value;
    const job_family = document.getElementById("job_family").value;
    fetchDropdown("single-roles", "single_role", {
        job_type, job_family, sub_family: e.target.value
    });
    });

    document.getElementById("single_role").addEventListener("change", e => {
    const job_type = document.getElementById("job_type").value;
    const job_family = document.getElementById("job_family").value;
    const sub_family = document.getElementById("sub_family").value;
    fetchDropdown("career-levels", "career_level", {
        job_type, job_family, sub_family, single_role: e.target.value
    });
    });

    document.getElementById("profile-form").addEventListener("submit", async e => {
    e.preventDefault();
    const payload = {
    job_type: document.getElementById("job_type").value,
    job_family: document.getElementById("job_family").value,
    sub_family: document.getElementById("sub_family").value,
    single_role: document.getElementById("single_role").value,
    career_level: document.getElementById("career_level").value,
    };
    const res = await fetch(`${apiBase}/generate-profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
    });
    const data = await res.json();
    document.getElementById("profile-result").innerText = JSON.stringify(data, null, 2);
});
});
