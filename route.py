
routes = []

def route(url, **kargs):
    global routes
    def _(cls):
        routes.append((url, cls, kargs))
        return cls
    return _
