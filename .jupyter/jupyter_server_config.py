# MyST's --execute-parallel bounds notebook execution upstream.
c = get_config()  # noqa: F821
c.ServerApp.ip = "127.0.0.1"  # Avoid binding only to ::1.
c.ServerApp.allow_root = True  # CI runs inside containers.
