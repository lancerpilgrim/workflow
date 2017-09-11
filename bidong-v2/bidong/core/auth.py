import datetime

import jwt
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from settings import JWT_SECRET


def salt_password(password):
    return generate_password_hash(password)


def check_password(salted, raw):
    return check_password_hash(salted, raw)


def gen_auth_token(payload, aud='platform', expired_second=10800):
    """生成基于JWT的token
    Args:
        payload (dict): 需要签名的字典信息
        aud: 处理平台，如mp, api ect.
        expired_second: 过期时间
    Returns:
        str: token
    """
    payload['aud'] = aud
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=expired_second)
    payload['iss'] = "bidongwifi"
    payload['iat'] = datetime.datetime.utcnow()
    rv = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return rv


def decode_auth_token(token, aud='platform'):
    """decode token
    Args:
        token: 原始的token
        aud: 处理平台
    Returns:
        dict: payload for success, {} for others
    """
    return jwt.decode(token, JWT_SECRET, audience=aud)


if __name__ == "__main__":
    payload = {
        "user_id": "1421233",
        "user_role": "administrator"
    }
    rv = gen_auth_token(payload)
    import time
    r = decode_auth_token(rv)
    print(rv)
    print(r)

    password = "123456"
    salted_password = generate_password_hash(password)
    print(salted_password)
    check = check_password_hash(salted_password, password)
    print(check)



