/*
Question: What are the top paying data analyst jobs?
- Identify the top 10 highest paying data analyst roles that are available remotely
- focuses on job_postings with specified salary (remove nulls)
- highlight the top paying oppurtunities for the data analyst offering insights

*/


SELECT
    job_id,
    job_title,
    job_location,
    job_schedule_type,
    salary_year_avg,
    job_posted_date,
    name AS company_name

FROM job_postings_fact

LEFT JOIN
    company_dim ON 
    job_postings_fact.company_id=company_dim.company_id

--hence we need to find the jobs for the data analyst and location remotely
WHERE 
    job_title_short= 'Data Analyst' AND
    job_location='Anywhere' 

    --job with the specified salary
    AND salary_year_avg is not NULL


--we need to find the top 10 jobs as per the situation so 

ORDER BY 
    salary_year_avg DESC

LIMIT 10;


