--analysis for the skills that are most in demand and pays wells for the skills
SELECT
    job_title_short,
    COUNT(job_id) AS total_jobs,
    ROUND(AVG(salary_year_avg),0) AS avg_salary,
    ROUND(MAX(salary_year_avg),0) AS max_salary,
    ROUND(MIN(salary_year_avg),0) AS min_salary,

   -- ROUND(SUM(CASE WHEN job_work_from_home =TRUE THEN 1 ELSE 0 END)/ COUNT(job_id), 1) AS remote_percent,

    DENSE_RANK() OVER (ORDER BY AVG(salary_year_avg) DESC) AS salary_rank,
    DENSE_RANK() OVER (ORDER BY COUNT(job_id) DESC) AS job_rank
FROM job_postings_fact
WHERE salary_rate IS NOT NULL
GROUP BY job_title_short
ORDER BY avg_salary DESC;
