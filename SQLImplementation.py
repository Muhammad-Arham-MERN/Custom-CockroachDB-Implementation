import os
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, create_engine, Session, select, asc, desc, delete
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from agents import TResponseInputItem
from sqlalchemy.dialects.postgresql import insert
import json
import asyncio
from colorama import Back

load_dotenv()

cockroachdb_connection_url = os.getenv("COCKROACHDB_URL").replace(
    "postgresql", "cockroachdb"
)


class SessionTable(SQLModel, table=True):
    session_id: str | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AgentMessagesTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(foreign_key="sessiontable.session_id",index=True)
    message_data: str
    created_at: datetime = Field(default_factory=datetime.now,index=True)


postgres_engine = create_engine(cockroachdb_connection_url)


def create_db_tables():
    SQLModel.metadata.create_all(postgres_engine)


@dataclass
class CockroachDBSession:
    """Custom session implementation following the Session protocol."""

    session_id: str
    create_db_tables()

    async def get_items(self, limit: int | None = None) -> List[dict]:
        """Retrieve conversation history for this session."""
        try:
            with Session(postgres_engine) as session:
                statement = select(AgentMessagesTable).where(
                    AgentMessagesTable.session_id == self.session_id
                )

                # if no limit then all data retrieved in ascending order i.e chronological order
                if limit is None:
                    statement = statement.order_by(asc(AgentMessagesTable.created_at))
                # if a limit then data retrieved in a descending format i.e non-chronological
                else:
                    statement = statement.order_by(
                        desc(AgentMessagesTable.created_at)
                    ).limit(limit)

                try:
                    results: list = session.exec(statement).all()
                except Exception as e:
                    print(
                        "an error occured while trying to retrieve messages from table",
                        e,
                    )

                # converting non-chronological to choronological format
                if limit is not None:
                    results.reverse()
                
                print(Back.YELLOW + str(results))
                return [json.loads(result.message_data) for result in results]

        except Exception as e:
            print("An error occured while trying to get items", e)

    async def add_items(self, items: List[dict]) -> None:
        """Store new items for this session."""

        if not items:
            print("no items received")
            return

        # create a brand new session table in analogy,
        # ChatGPT's sidebar has a list of chats with specific id, this is exactly that!
        session_to_add = SessionTable(session_id=self.session_id)
        session_id = session_to_add.session_id
        created_at = session_to_add.created_at
        updated_at = session_to_add.updated_at

        # setup messages for Messages Table i.e System, User and Assistant messages
        # In analogy, this is the exact chat interface you have with ChatGPT
        messages_to_add = [
            {
                "session_id": self.session_id,
                "message_data": json.dumps(item, ensure_ascii=False),
            }
            for item in items
        ]

        try:

            with Session(postgres_engine) as session:
                conditional_stml_session = (
                    insert(SessionTable)
                    .values(
                        session_id=session_id,
                        created_at=created_at,
                        updated_at=updated_at,
                    )
                    .on_conflict_do_nothing(index_elements=["session_id"])
                )

                try:
                    session.exec(conditional_stml_session)
                except Exception as e:
                    print(
                        "An error occured while trying to insert Session_id into table"
                    )

                try:
                    session.exec(insert(AgentMessagesTable).values(messages_to_add))
                except Exception as e:
                    print(
                        "An error occured while trying to insert Message Data into table"
                    )

                session.commit()

        except Exception as e:
            print("an error occured while trying to add messages", e)

    async def pop_item(self) -> dict | None:
        """Remove and return the most recent item from this session."""
        try:
            with Session(postgres_engine) as session:
                stmt_get_popid = (
                    select(AgentMessagesTable)
                    .where(AgentMessagesTable.session_id == self.session_id)
                    .order_by(desc(AgentMessagesTable.created_at))
                    .limit(1)
                )
                pop_items: list = session.exec(stmt_get_popid).all()
                if pop_items:
                    try:
                        session.delete(pop_items[0])
                        session.commit()
                    except Exception as e:
                        print("Got an issue while trying to delete/pop item", e)

                    items = json.loads(pop_items[0].message_data)
                    print("here is pop item data",items)
                    return items
                else:
                    print("no items to pop")
                    return None

        except Exception as e:
            print("A session error occured while popping item")

    async def clear_session(self) -> None:
        """Clear all items for this session."""
        try:
            with Session(postgres_engine) as session:
                try:
                    session.exec(
                        delete(AgentMessagesTable).where(
                            AgentMessagesTable.session_id == self.session_id
                        )
                    )
                except Exception as e:
                    print(
                        f"Error occured while clearing Messages Table for session id: {self.session_id}"
                    )
                try:

                    session.exec(
                        delete(SessionTable).where(
                            SessionTable.session_id == self.session_id
                        )
                    )
                except Exception as e:
                    print(
                        f"Error occured while clearing Session from Session table for session id: {self.session_id}"
                    )

                session.commit()
        except Exception as e:
            print("Session error occured while trying to clear session")


# async def run():
#     create_db_tables()
#     print("created tables")
#     work = CockroachDBSession()
#     results = await work.get_items()
#     print(results)


# if __name__ == "__main__":
#     asyncio.run(run())
