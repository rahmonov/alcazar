import traceback


def debug_exception_handler(req, resp, exception):
    resp.text = f"{exception}\n\n{traceback.format_exc()}"
