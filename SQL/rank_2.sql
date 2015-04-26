SELECT F.id, F.rank_date, F.squery_website_mm_id, F.website_pos,
S.id, S.rank_date, S.squery_website_mm_id, S.website_pos,
R.squery_id, R.website_id
FROM website_rank F LEFT JOIN website_rank S
ON F.squery_website_mm_id = S.squery_website_mm_id AND F.rank_date > S.rank_date
LEFT JOIN squery_website_mm R ON R.id = F.squery_website_mm_id
WHERE F.rank_date = '2014-05-22' AND S.rank_date = '2014-05-21'
;