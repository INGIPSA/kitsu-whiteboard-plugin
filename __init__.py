from . import resources


routes = [
    ("/boards", resources.BoardsResource),
    ("/boards/<board_id>", resources.BoardResource),
]


def pre_install(manifest):
    pass


def post_install(manifest):
    pass


def pre_uninstall(manifest):
    pass


def post_uninstall(manifest):
    pass
