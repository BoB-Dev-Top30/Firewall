import re

def DP-Sql-Injection(payload):
    sql_detected=0
    sql_injection_patterns = [r"SELECT .* FROM .*", r"INSERT INTO .* VALUES .*", r"DELETE FROM .* WHERE .*"]
    sql_injection_regex = re.compile('|'.join(sql_injection_patterns), re.IGNORECASE)
    if sql_injection_regex.search(payload):
        print("SQL 인젝션 공격 감지!")
        sql_detected=1
        ## 다른 문자열로 대체##
        payload = sql_injection_regex.sub("[SQL Injection Detected]", payload)
    return payload, sql_detected
