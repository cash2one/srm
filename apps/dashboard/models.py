# -*- coding: utf-8 -*-

from django.db import models
from django.db import connection
from django.core.exceptions import MultipleObjectsReturned

NEAREST_REPORT_DATE = """SELECT MAX(rank_date) FROM srm_website_rank WHERE rank_date <= %s;"""

# AVG_SQL = """SELECT R.website_id,
# W.url,
# F.rank_date AS date1,
# S.rank_date AS date2,
# AVG(F.website_pos) AS pos1,
#  AVG(S.website_pos) AS pos2
# FROM website_rank F LEFT JOIN website_rank S
# ON F.squery_website_mm_id = S.squery_website_mm_id AND F.rank_date > S.rank_date
# LEFT JOIN squery_website_mm R ON R.id = F.squery_website_mm_id
# LEFT JOIN website W ON R.website_id = W.id
# WHERE F.rank_date = %s AND (S.rank_date = %s OR S.rank_date IS NULL)
# GROUP BY R.website_id, F.rank_date, S.rank_date;
# """
#
# DAY_RANK__RPT_SQL = """SELECT DISTINCT R.website_id,
# W.url,
#
# (SELECT AVG(F1.website_pos)
# 		FROM website_rank F1
# 		LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
# 		WHERE F1.rank_date = F.rank_date  AND R1.website_id = R.website_id
# ) AS avg_pos1,
#
# (SELECT AVG(S1.website_pos)
# 		FROM website_rank S1
# 		LEFT JOIN squery_website_mm R1 ON R1.id = S1.squery_website_mm_id
# 		WHERE S1.rank_date = S.rank_date  AND R1.website_id = R.website_id
# ) AS avg_pos2,
#
# (SELECT COUNT(*)
# 	FROM website_rank F1 LEFT JOIN website_rank S1
# 	ON F1.squery_website_mm_id = S1.squery_website_mm_id AND F1.rank_date > S1.rank_date
# 	LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
# 	WHERE F1.rank_date = F.rank_date AND (S1.rank_date = S.rank_date OR S.rank_date IS NULL)
# 	AND R1.website_id = R.website_id
# 	AND F1.website_pos = S1.website_pos
# ) AS pos_unchanged,
#
# (SELECT COUNT(*)
# 	FROM website_rank F1 LEFT JOIN website_rank S1
# 	ON F1.squery_website_mm_id = S1.squery_website_mm_id AND F1.rank_date > S1.rank_date
# 	LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
# 	WHERE F1.rank_date = F.rank_date AND S1.rank_date = S.rank_date
# 	AND R1.website_id = R.website_id
# 	AND F1.website_pos < S1.website_pos
# ) AS pos_down,
#
# (SELECT COUNT(*)
# 	FROM website_rank F1 LEFT JOIN website_rank S1
# 	ON F1.squery_website_mm_id = S1.squery_website_mm_id AND F1.rank_date > S1.rank_date
# 	LEFT JOIN squery_website_mm R1 ON R1.id = F1.squery_website_mm_id
# 	WHERE F1.rank_date = F.rank_date AND S1.rank_date = S.rank_date
# 	AND R1.website_id = R.website_id
# 	AND F1.website_pos > S1.website_pos
# ) AS pos_up
# FROM website_rank F LEFT JOIN website_rank S
# ON F.squery_website_mm_id = S.squery_website_mm_id AND F.rank_date > S.rank_date
# LEFT JOIN squery_website_mm R ON R.id = F.squery_website_mm_id
# LEFT JOIN website W ON R.website_id = W.id
# WHERE F.rank_date = %s AND (S.rank_date = %s OR S.rank_date IS NULL)
# """


def find_nearest_date(report_date):
    cursor = connection.cursor()
    cursor.execute(NEAREST_REPORT_DATE, [report_date])
    rs = cursor.fetchall()
    if len(rs) != 1:
        raise MultipleObjectsReturned('Failed to find positions report first date')
    dt = rs[0][0]
    return dt
