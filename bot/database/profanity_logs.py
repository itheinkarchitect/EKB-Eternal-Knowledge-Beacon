from sqlalchemy import select
from bot.database.models import ProfanityLog
from bot.database.database import session
from datetime import datetime, timedelta


def save_profanity(user_id, count):
    profanity = ProfanityLog(
        user_id=user_id,
        count=count,
        created_at=datetime.now()
    )

    session.add(profanity)
    session.commit()

def get_profanity_count(user_id):
    statement = select(ProfanityLog).where(
        ProfanityLog.user_id==user_id,
        ProfanityLog.created_at >= datetime.now() - timedelta(hours=24))

    result = session.execute(statement)
    logs = result.scalars().all()

    total = sum(log.count for log in logs)

    return total