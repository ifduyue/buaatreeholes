def mb_code(string, coding="utf-8"):
    if isinstance(string, unicode):
        return string.encode(coding)
    for c in ('utf-8', 'gb2312', 'gbk', 'gb18030', 'big5'):
        try:
            return string.decode(c).encode(coding)
        except: pass
    return string
