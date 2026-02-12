from sqlalchemy import select
from database.session import SessionLocal
from database.models.user import User

class UserService:

    @staticmethod
    async def get_or_create(telegram_id: int, full_name: str, language: str):
        async with SessionLocal() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()

            if user:
                return user

            user = User(
                telegram_id=telegram_id,
                full_name=full_name,
                language=language
            )
            session.add(user)
            await session.commit()
            return user
