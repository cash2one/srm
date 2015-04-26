SELECT G.id AS group_id,
  K.id AS keywords_id,
  W.id AS website_id,
  G.group_name,
  W.url,
  W.title,
  K.keywords,
  '2014-06-04' AS date1,
  (
    SELECT website_pos
      FROM srm_website_rank
      WHERE rank_date = date1
        AND search_group_id = G.id
        AND website_id = W.id
        AND keywords_id = K.id
  ) AS pos1,
  '2014-06-03' AS date2,
  (
    SELECT website_pos
      FROM srm_website_rank
      WHERE rank_date = date2
        AND search_group_id = G.id
        AND website_id = W.id
        AND keywords_id = K.id
  ) AS pos2,
	G.results_per_page

 FROM srm_search_group G
  INNER JOIN srm_keywords K
    ON K.search_group_id = G.id
  INNER JOIN srm_website W
    ON W.search_group_id = G.id
ORDER BY G.group_name, W.title, K.keywords
