WITH top_skills AS (
    SELECT skills_dim.skills,
        skills_dim.skill_id,
        job_postings_fact.job_title_short,
        COUNT(skills_job_dim.job_id) AS demand_count,
        ROUND(AVG(salary_year_avg), 0) AS avg_salary
    FROM job_postings_fact
        INNER JOIN skills_job_dim ON job_postings_fact.job_id = skills_job_dim.job_id
        INNER JOIN skills_dim ON skills_job_dim.skill_id = skills_dim.skill_id
    WHERE salary_year_avg IS NOT NULL
        AND job_title_short IN (
            'Data Analyst',
            'Data Scientist',
            'Data Engineer',
            'Machine Learning Engineer'
        )
    GROUP BY skills_dim.skills,
        skills_dim.skill_id,
        job_postings_fact.job_title_short
    
)
SELECT job_title_short,
demand_count,
    skills,
    avg_salary,
    DENSE_RANK() OVER (
        PARTITION BY job_title_short
        ORDER BY avg_salary DESC
    ) AS salary_rank
FROM top_skills
WHERE demand_count >10
ORDER BY job_title_short,salary_rank;