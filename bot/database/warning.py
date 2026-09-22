from sqlalchemy import select, delete
from bot.database.models import WarningLog
from bot.database.database import session
from datetime import datetime

def add_warning(user_id):
    warning = WarningLog(
        user_id=user_id,
        created_at=datetime.now()
    )

    session.add(warning)
    session.commit()

def get_warning_count(user_id):
    statement = select(WarningLog).where(WarningLog.user_id==user_id)

    result = session.execute(statement)
    logs = result.scalars().all()

    total = len(logs)

    return total

def clear_warnings(user_id):
    statement = delete(WarningLog).where(WarningLog.user_id==user_id)

    session.execute(statement)
    session.commit()