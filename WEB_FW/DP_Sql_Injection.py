import re

def DP_Sql_Injection(payload):
    sql_detected = 0

    sql_injection_patterns = [
        r"(?i)\b(SELECT)\b\s*?.*\b(FROM)\b",  # 기본 SELECT FROM 구문
        r"(?i)\b(INSERT)\b\s*?\b(INTO)\b\s*?.*\b(VALUES)\b",  # INSERT INTO VALUES 구문
        r"(?i)\b(DELETE)\b\s*?\b(FROM)\b.*\b(WHERE)\b",  # DELETE FROM WHERE 구문
        r"(?i)\b(UPDATE)\b\s*?.*\b(SET)\b",  # UPDATE SET 구문
        r"(?i)\b(DROP)\b\s*?\b(TABLE)\b",  # DROP TABLE 구문
        r"(?i)\b(CREATE)\b\s*?\b(TABLE)\b",  # CREATE TABLE 구문
        r"(?i)\b(ALTER)\b\s*?\b(TABLE)\b",  # ALTER TABLE 구문
        r"(?i)\b(EXEC)\b(\s*?\b(SP_)\b|\bxp_\b)",  # EXEC SP_ 또는 xp_ 구문
        r"(?i)\b(OR)\b\s*?('?\d+'?\s*?=\s*?'?\d+'?)",  # 'OR 1=1' 또는 변형된 형태
        # 고급 패턴: 공백, 주석, SQL 연산자 변형 포함
        r"(?i)\b(OR)\b\s*?(\d\s*?=\s*?\d)(\s*?(--|#|/\*.*?\*/))?"]  # 'OR 1=1' 과 주석을 포함한 변형
        
    sql_injection_regex = re.compile('|'.join(sql_injection_patterns))
    if sql_injection_regex.search(payload):
        print("SQL 인젝션 공격 감지!")
        sql_detected = 1
        payload = sql_injection_regex.sub("[SQL Injection Detected]", payload)
    return payload, sql_detected

