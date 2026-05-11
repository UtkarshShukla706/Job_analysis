

SELECT 
job_postings_fact.job_title_short AS job_name,
company_dim.name AS company_name,
 ROUND(AVG(salary_year_avg), 0) AS avg_salary,

COUNT(job_postings_fact.job_id) AS total_jobs,

DENSE_RANK() OVER (
    PARTITION BY job_postings_fact.job_title_short
    ORDER BY AVG(salary_year_avg) DESC
    ) AS salary_rank

FROM job_postings_fact
INNER JOIN company_dim ON job_postings_fact.company_id=company_dim.company_id
WHERE salary_year_avg IS NOT NULL
GROUP BY 
    job_title_short,
    name
ORDER BY avg_salary DESC
;