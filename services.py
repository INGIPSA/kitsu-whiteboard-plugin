import json

from .models import Board


def get_boards_for_project(project_id):
    boards = Board.get_all_by(project_id=project_id)
    return [b.present() for b in boards]


def get_board(board_id):
    return Board.get(board_id)


def create_board(project_id, name="New Board", visibility="private",
                 canvas_data=None, created_by=None):
    return Board.create(
        project_id=project_id,
        name=name,
        visibility=visibility,
        canvas_data=json.dumps(canvas_data) if canvas_data else None,
        created_by=created_by,
    )


def update_board(board, data):
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
    return board


def delete_board(board):
    board.delete()
