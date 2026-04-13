from sqlalchemy_utils import UUIDType

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class Board(db.Model, BaseMixin, SerializerMixin):
    """A whiteboard board belonging to a project."""

    __tablename__ = "plugin_whiteboard_board"

    project_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("project.id"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(255), nullable=False, default="New Board")
    visibility = db.Column(db.String(20), nullable=False, default="private")
    canvas_data = db.Column(db.Text, nullable=True)
    thumbnail = db.Column(db.Text, nullable=True)
    created_by = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("person.id"),
        nullable=True,
    )

    def present(self):
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "name": self.name,
            "visibility": self.visibility,
            "canvas_data": self.canvas_data,
            "thumbnail": self.thumbnail,
            "created_by": str(self.created_by) if self.created_by else None,
            "created_at": self.created_at.isoformat()
            if self.created_at
            else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at
            else None,
        }
