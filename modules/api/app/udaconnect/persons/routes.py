def register_routes(api, root="api"):
    import register_routes as attach_udaconnect

    # Add routes
    attach_udaconnect(api)
