"""
tag.py
~~~
标签管理
"""
from bidong.core.database import session
from bidong.storage.models import Tag


def create_tag(tag_type, name, pn=0):
    """创建标签
    Args:
        tag_type: 标签类型
        name: 标签名
        pn: 所属项目，0 为平台标签
    """
    tag = Tag(pn=pn, tag_type=tag_type, name=name)
    session.add(tag)
    session.commit()
    return tag.id


def list_tag(tag_type, pn=0):
    """获取标签
    Args:
        tag_type: 标签类型
        pn: 所属项目，0 为平台标签
    Return:
        QuerySet
    """
    tags = session.query(Tag).filter_by(tag_type=tag_type, pn=pn).all()
    return tags


def delete_tag(tag_id, pn=0):
    session.query(Tag).filter(Tag.id == tag_id, Tag.pn == pn).delete()
    session.commit()


def get_tag(tag_id):
    tag = session.query(Tag).filter(Tag.id == tag_id).one_or_none()
    return tag
