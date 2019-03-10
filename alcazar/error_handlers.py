import traceback


def debug_http_error_handler(req, resp, http_error):
    """Should be used only in development as it exposes exception details"""
    resp.text = f"{http_error}\n\n{traceback.format_exc()}"
    resp.status_code = http_error.status
