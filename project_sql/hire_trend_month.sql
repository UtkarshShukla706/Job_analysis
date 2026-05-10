SELECT 
    
    EXTRACT (MONTH FROM job_posted_date) AS month,
    EXTRACT (YEAR FROM job_posted_date) AS year,

    COUNT(job_id) AS total_jobs,
    ROUND(AVG(salary_year_avg),0) AS avg_salary

FROM job_postings_fact
WHERE salary_year_avg IS NOT NULL
GROUP BY 
    EXTRACT(YEAR  FROM job_posted_date),
    EXTRACT(MONTH FROM job_posted_date)
ORDER BY 
    year ASC,
    month ASC;

