import json

from sqlalchemy.ext.declarative import DeclarativeMeta


def serialize_complex(result):
    if isinstance(result, list):
        return [serialize_complex_single(item) for item in result]
    else:
        return serialize_complex_single(result)

def serialize_complex_single(result):
    data = {c.name: getattr(result, c.name) for c in result.__table__.columns}
    if hasattr(result, 'addresses'):
        data['addresses'] = [serialize_complex_single(addr) for addr in result.addresses]
        
    return data