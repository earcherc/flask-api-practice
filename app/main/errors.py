from . import main


def page_not_found(e):
    return "<h1>Page not found!</h1>", 404


def internal_server_error(e):
    return "<h1>Bad request!</h1>", 500


main.register_error_handler(404, page_not_found)

main.register_error_handler(500, internal_server_error)
