SELECT AVG(S1.website_pos)
		FROM website_rank F1 
		LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
		WHERE F1.rank_date = F1.rank_date  AND R1.website_id = R.website_id
