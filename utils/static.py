def request_for_static(request_path, static_root):
    return request_path.startswith(static_root)


def cut_static_root(static_file_path, static_root):
    assert static_file_path.startswith(static_root)

    return static_file_path[len(static_root):]
