import string

BASE62 = string.ascii_letters + string.digits

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]

    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62[rem])

    return ''.join(reversed(base62))
