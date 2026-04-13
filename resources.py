from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from zou.app.mixin import ArgsMixin
from zou.app.services import persons_service

from . import services


class BoardsResource(Resource, ArgsMixin):

    @jwt_required()
    def get(self):
        """List all boards for a project."""
        project_id = self.get_text_parameter("project_id")
        if not project_id:
            return {"error": "project_id required"}, 400
        return services.get_boards_for_project(project_id)

    @jwt_required()
    def post(self):
        """Create a new board."""
        data = request.get_json()
        project_id = data.get("project_id")
        if not project_id:
            return {"error": "project_id required"}, 400

        current_user = persons_service.get_current_user()
        board = services.create_board(
            project_id=project_id,
            name=data.get("name", "New Board"),
            visibility=data.get("visibility", "private"),
            canvas_data=data.get("canvas_data"),
            created_by=current_user["id"],
        )
        return board.present(), 201


class BoardResource(Resource, ArgsMixin):

    @jwt_required()
    def get(self, board_id):
        """Get a single board."""
        board = services.get_board(board_id)
        if not board:
            return {"error": "Board not found"}, 404
        return board.present()

    @jwt_required()
    def put(self, board_id):
        """Update a board."""
        board = services.get_board(board_id)
        if not board:
            return {"error": "Board not found"}, 404
        data = request.get_json()
        services.update_board(board, data)
        return board.present()

    @jwt_required()
    def delete(self, board_id):
        """Delete a board."""
        board = services.get_board(board_id)
        if not board:
            return {"error": "Board not found"}, 404
        services.delete_board(board)
        return "", 204
