
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import crud, schemas


def test_crud_flow(tmp_path):
    db_path = tmp_path / "db.sqlite"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        # Create
        t = crud.create_task(db, schemas.TaskCreate(title="X", description="Y"))
        assert t.id and t.title == "X" and t.status.value == "created"

        # Get
        got = crud.get_task(db, t.id)
        assert got is not None and got.id == t.id

        # List
        lst = crud.list_tasks(db)
        assert any(x.id == t.id for x in lst)

        # Update
        updated = crud.update_task(db, t, schemas.TaskUpdate(status="completed"))
        assert updated.status.value == "completed"

        # Delete
        crud.delete_task(db, updated)
        assert crud.get_task(db, t.id) is None
    finally:
        db.close()
