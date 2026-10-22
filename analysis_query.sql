-- Creates a table with monthly COVID-19 deaths by age group
SELECT Dataset.year, Dataset.month, age_group.age_group, Dataset.covid_19_deaths
FROM Dataset
JOIN age_group ON Dataset.age_group_id = age_group.id
JOIN sex ON Dataset.sex_id = sex.id
JOIN state ON Dataset.state_id = state.id
JOIN metodo ON Dataset.metodo_id = metodo.id
WHERE metodo.metodo = 'By Month' 
AND state.state = 'United States' 
AND sex.sex = 'All Sexes' 
AND age_group.age_group IN ('Under 1 year', '1-4 years', '5-14 years', '15-24 years', '25-34 years', '35-44 years', '45-54 years', '55-64 years', '65-74 years', '75-84 years', '85 years and over')
ORDER BY Dataset.year, Dataset.month, age_group.id
