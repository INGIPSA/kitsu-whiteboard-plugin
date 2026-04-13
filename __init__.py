from . import resources

routes = [
    ("/boards", resources.BoardsResource),
    ("/boards/<board_id>", resources.BoardResource),
]


def post_install(manifest):
    pass
