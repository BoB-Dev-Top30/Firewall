import re

def DP_Xss(payload):
    xss_detected = 0

    xss_patterns = [
        r"<script.*?>.*?</script>",  # 기본적인 <script> 태그
        r"javascript:[^\s]*",  # "javascript:" 프로토콜
        r"(<[^>]+)on[a-z]+=[^\s>]+",  # 이벤트 핸들러 (예: onclick, onerror 등)
        r"(<[^>]+)style=[^\s>]*expression[^\s>]+",  # CSS 표현식
        r"(<[^>]+)style=[^\s>]*url[^\s>]+",  # CSS URL 사용
        r"document\.cookie",  # 쿠키 접근 시도
        r"window\.location",  # 위치 변경 시도
        r"(\.href|\.src)\s*=\s*",  # href, src 속성 변경 시도
        r"alert\(",  # alert 함수 호출
        r"eval\(",  # eval 함수 호출
        r"innerHTML",  # innerHTML 사용
        r"outerHTML",  # outerHTML 사용
        r"iframe",  # <iframe> 태그
        r"<img.*?src.*?=",  # <img> 태그와 src 속성
        r"(<object.*?>.*?</object>)|(<embed.*?/?>)",  # <object>, <embed> 태그
        r"(<applet.*?>.*?</applet>)|(<svg.*?>.*?</svg>)",  # <applet>, <svg> 태그
        r"%3Cscript",  # URL 인코딩된 <script> 태그
    ]
    xss_regex = re.compile('|'.join(xss_patterns), re.IGNORECASE | re.DOTALL)
    if xss_regex.search(payload):
        print("XSS 공격 감지!")
        xss_detected = 1
        payload = xss_regex.sub("[XSS Detected]", payload)
    return payload, xss_detected
