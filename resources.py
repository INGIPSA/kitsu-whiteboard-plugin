import json

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from zou.app.mixin import ArgsMixin
from zou.app.utils import permissions

from .models import Board


class BoardsResource(Resource, ArgsMixin):

    @jwt_required()
    def get(self):
        """List all boards for a project."""
        project_id = self.get_text_parameter("project_id")
        if not project_id:
            return {"error": "project_id required"}, 400

        user_service = permissions.get_current_user()
        boards = Board.query.filter_by(project_id=project_id).order_by(
            Board.updated_at.desc()
        ).all()
        return [b.present() for b in boards]

    @jwt_required()
    def post(self):
        """Create a new board."""
        data = request.get_json()
        project_id = data.get("project_id")
        if not project_id:
            return {"error": "project_id required"}, 400

        current_user = permissions.get_current_user()
        board = Board.create(
            project_id=project_id,
            name=data.get("name", "New Board"),
            visibility=data.get("visibility", "private"),
            canvas_data=json.dumps(data["canvas_data"])
            if data.get("canvas_data")
            else None,
            created_by=current_user["id"],
        )
        return board.present(), 201


class BoardResource(Resource, ArgsMixin):

    @jwt_required()
    def get(self, board_id):
        """Get a single board."""
        board = Board.get(board_id)
        if not board:
            return {"error": "Board not found"}, 404
        return board.present()

    @jwt_required()
    def put(self, board_id):
        """Update a board."""
        board = Board.get(board_id)
        if not board:
            return {"error": "Board not found"}, 404

        data = request.get_json()
        update = {}
        if "name" in data:
            update["name"] = data["name"]
        if "visibility" in data:
            update["visibility"] = data["visibility"]
        if "canvas_data" in data:
            update["canvas_data"] = json.dumps(data["canvas_data"])
        if "thumbnail" in data:
            update["thumbnail"] = data["thumbnail"]

        board.update(update)
        return board.present()

    @jwt_required()
    def delete(self, board_id):
        """Delete a board."""
        board = Board.get(board_id)
        if not board:
            return {"error": "Board not found"}, 404
        board.delete()
        return "", 204
