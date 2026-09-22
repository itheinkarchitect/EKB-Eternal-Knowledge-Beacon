from sqlalchemy import select
from bot.database.models import MuteLog
from bot.database.database import session
from datetime import datetime, timedelta

def add_mute(user_id):
    mute = MuteLog(
        user_id=user_id,
        created_at=datetime.now()
    )

    session.add(mute)
    session.commit()

def get_mute_count(user_id):
    statement = select(MuteLog).where(
        MuteLog.user_id == user_id,
        MuteLog.created_at >= datetime.now() - timedelta(days=30)
    )

    result = session.execute(statement)
    logs = result.scalars().all()

    total = len(logs)

    return total