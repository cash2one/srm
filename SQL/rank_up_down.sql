SELECT DISTINCT R.website_id,
W.url, 

(SELECT AVG(F1.website_pos)
		FROM website_rank F1 
		LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
		WHERE F1.rank_date = F.rank_date  AND R1.website_id = R.website_id
) AS avg_pos1,

(SELECT AVG(S1.website_pos)
		FROM website_rank S1 
		LEFT JOIN squery_website_mm R1 ON R1.id = S1.squery_website_mm_id
		WHERE S1.rank_date = S.rank_date  AND R1.website_id = R.website_id
) AS avg_pos2,

(SELECT COUNT(*) 
	FROM website_rank F1 LEFT JOIN website_rank S1
	ON F1.squery_website_mm_id = S1.squery_website_mm_id AND F1.rank_date > S1.rank_date
	LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
	WHERE F1.rank_date = F.rank_date AND (S1.rank_date = S.rank_date OR S.rank_date IS NULL)
	AND R1.website_id = R.website_id
	AND F1.website_pos = S1.website_pos
) AS pos_not_changed,

(SELECT COUNT(*) 
	FROM website_rank F1 LEFT JOIN website_rank S1
	ON F1.squery_website_mm_id = S1.squery_website_mm_id AND F1.rank_date > S1.rank_date
	LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
	WHERE F1.rank_date = F.rank_date AND S1.rank_date = S.rank_date 
	AND R1.website_id = R.website_id
	AND F1.website_pos < S1.website_pos
) AS pos_down,

(SELECT COUNT(*) 
	FROM website_rank F1 LEFT JOIN website_rank S1
	ON F1.squery_website_mm_id = S1.squery_website_mm_id AND F1.rank_date > S1.rank_date
	LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
	WHERE F1.rank_date = F.rank_date AND S1.rank_date = S.rank_date 
	AND R1.website_id = R.website_id
	AND F1.website_pos > S1.website_pos
) AS pos_up

FROM website_rank F LEFT JOIN website_rank S
ON F.squery_website_mm_id = S.squery_website_mm_id AND F.rank_date > S.rank_date
LEFT JOIN squery_website_mm R ON R.id = F.squery_website_mm_id
LEFT JOIN website W ON R.website_id = W.id
WHERE F.rank_date = '2014-05-24' AND (S.rank_date = '2014-05-23' OR S.rank_date IS NULL)
