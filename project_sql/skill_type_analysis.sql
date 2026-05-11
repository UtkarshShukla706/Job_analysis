SELECT 
    skills_dim.type AS skill_type,
    COUNT(job_postings_fact.job_id) AS total_jobs,
    ROUND(AVG(job_postings_fact.salary_year_avg),0) AS avg_salary

FROM job_postings_fact
INNER JOIN skills_job_dim ON job_postings_fact.job_id=skills_job_dim.job_id
INNER JOIN skills_dim ON skills_job_dim.skill_id=skills_dim.skill_id

WHERE salary_year_avg IS NOT NULL
GROUP BY 
    skill_type
ORDER BY avg_salary DESC;