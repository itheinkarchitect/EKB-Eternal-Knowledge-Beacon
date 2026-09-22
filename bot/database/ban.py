from sqlalchemy import select, delete
from datetime import datetime, timedelta
from bot.database.models import BanLog
from bot.database.database import session



def add_ban(user_id):
    ban = BanLog(
        user_id=user_id,
        created_at=datetime.now()
    )

    session.add(ban)
    session.commit()

def get_expired_bans():
    statement = select(BanLog).where(
        BanLog.created_at <= datetime.now() - timedelta(days=7)
    )

    result = session.execute(statement)

    return result.scalars().all()


def clear_ban(ban_id):
    statement = delete(BanLog).where(
        BanLog.id == ban_id
    )

    session.execute(statement)
    session.commit()