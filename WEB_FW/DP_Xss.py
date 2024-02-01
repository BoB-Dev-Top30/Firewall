import re

def DP_Xss(payload):
    xss_detected=0
    xss_patterns = [r"<script.*?>.*?</script>", r"javascript:[\s\S]*"]
    xss_regex = re.compile('|'.join(xss_patterns), re.IGNORECASE)
    if xss_regex.search(payload):
        print("XSS 공격 감지!")
        xss_detected=1

        ## 다른 문자열로 대체##
        payload = xss_regex.sub("[XSS Detected]", payload)
    return payload, xss_detected