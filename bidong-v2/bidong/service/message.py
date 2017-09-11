"""
message.py
~~~
站内信模块

"""
from sqlalchemy import func

from bidong.core.database import session
from bidong.core.paginator import Paginator
from bidong.core.exceptions import NotFoundError
from bidong.storage.models import Letter, Mailbox, Managers


class LetterService:
    """平台站内信处理逻辑
    """
    @classmethod
    def send(self, letter_id, receivers=None):
        if receivers is None:
            rvs = session.query(Managers.id).filter(
                Managers.status == Managers.ENABLED
            ).all()
            receivers = [rv.id for rv in rvs]

        for r in receivers:
            m = Mailbox(receiver_id=r, letter_id=letter_id)
            session.add(m)
        session.commit()

    @classmethod
    def generate(cls, manager_id, title, content, status, receivers=None):
        letter = Letter(title=title, content=content,
                        status=status, created_by=manager_id)
        session.add(letter)
        session.commit()

        if status == Letter.PUBLIC:
            cls.send(letter.id, receivers)

        return letter.id

    @classmethod
    def list(cls, page, page_size, status=None):
        query = session.query(Letter.id, Letter.title, Letter.created_at)
        if status is not None:
            query = query.filter_by(status=status)
        else:
            query = query.filter(Letter.status != Letter.DELETED)

        return Paginator(query, page, page_size)

    @classmethod
    def detail(cls, letter_id):
        letter = session.query(Letter).filter(
            Letter.id == letter_id, Letter.status != Letter.DELETED
        ).one_or_none()

        if not letter:
            raise NotFoundError("站内信不存在")
        return letter

    @classmethod
    def update(cls, letter_id, title, content, status, receivers=None):
        letter = session.query(
            Letter).filter(Letter.id == letter_id).one_or_none()

        if not letter:
            raise NotFoundError("站内信不存在")

        # 已经发出的不予做更新操作
        if letter.status == letter.PUBLIC:
            return

        letter.title = title
        letter.content = content

        if letter.status == Letter.DRAFT and status == Letter.PUBLIC:
            cls.send(letter_id, receivers=receivers)
        letter.status = status

        session.commit()

    @classmethod
    def delete(cls, letter_id):
        session.query(Letter).filter_by(id=letter_id).update(
            {"status": Letter.DELETED}, synchronize_session=False
        )
        session.query(Mailbox).filter_by(letter_id=letter_id).update(
            {"status": Mailbox.DELETED}, synchronize_session=False
        )
        session.commit()


class MailboxService:

    def __init__(self, manager_id):
        self.manager_id = manager_id

    def put(self, title, content):
        """创建单独给某个管理的站内信
        """
        m = Mailbox(
            receiver_id=self.manager_id, title=title, content=content,
            is_broadcast=0
        )
        session.add(m)
        session.commit()

    def unread_count(self):
        count = session.query(func.count(Mailbox.id)).filter(
            Mailbox.status == Mailbox.UNREAD,
            Mailbox.receiver_id == self.manager_id
        ).scalar()
        return count

    def list(self, page, page_size):
        """获取站内信，包括平台群发和针对个别管理员站内信
        """
        broadcast_msg = session.query(
            Letter.title.label("title"),
            Mailbox.created_at.label("created_at"),
            Mailbox.status.label("status"),
            Mailbox.id.label("id")
        ).filter(
            Mailbox.receiver_id == self.manager_id,
            Mailbox.is_broadcast == 1,
            Mailbox.letter_id == Letter.id,
            Mailbox.status != Mailbox.DELETED
        )

        private_msg = session.query(
            Mailbox.title.label("title"),
            Mailbox.created_at.label("created_at"),
            Mailbox.status.label("status"),
            Mailbox.id.label("id")
        ).filter(
            Mailbox.receiver_id == self.manager_id,
            Mailbox.is_broadcast == 0,
            Mailbox.status != Mailbox.DELETED,
        )
        query = broadcast_msg.union(private_msg)

        return Paginator(query, page, page_size)

    def read(self, mail_id):
        mail = session.query(Mailbox).filter(
            Mailbox.id == mail_id,
            Mailbox.receiver_id == self.manager_id,
            Mailbox.status != Mailbox.DELETED
        ).one_or_none()
        if not mail:
            raise NotFoundError("站内信不存在")

        if mail.status == Mailbox.UNREAD:
            mail.status = Mailbox.READ
            session.commit()

        if mail.is_broadcast:
            m = session.query(
                Mailbox.id.label("id"),
                Mailbox.created_at.label("created_at"),
                Letter.title.label("title"),
                Letter.content.label("content")
            ).filter(
                Mailbox.id == mail_id,
                Mailbox.letter_id == Letter.id
            ).first()
            return m

        return mail

    def delete(self, mail_id):
        session.query(Mailbox).filter_by(id=mail_id).update(
            {"status": Mailbox.DELETED}, synchronize_session=False
        )
        session.commit()
