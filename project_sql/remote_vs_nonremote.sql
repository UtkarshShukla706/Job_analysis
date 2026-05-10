--analysis for the remote job and the onsite job and how much they get for it 
SELECT job_title_short,
    ROUND(
        AVG(
            CASE
                WHEN job_work_from_home = TRUE THEN salary_year_avg
                ELSE NULL
            END
        ),
        0
    ) AS remote_salary,
    ROUND(
        AVG(
            CASE
                WHEN job_work_from_home = FALSE THEN salary_year_avg
                ELSE NULL
            END
        ),
        0
    ) AS non_remote_salary,
    ROUND(
        (
            AVG(
                CASE
                    WHEN job_work_from_home = TRUE THEN salary_year_avg
                    ELSE NULL
                END
            )
        ) -(
            AVG(
                CASE
                    WHEN job_work_from_home = FALSE THEN salary_year_avg
                    ELSE NULL
                END
            )
        ),
        0
    ) AS premium
FROM job_postings_fact
WHERE salary_year_avg IS NOT NULL
GROUP BY job_title_short
ORDER BY premium DESC;
