def register_routes(persons, app, root="persons"):
    from app.udaconnect import register_routes as attach_udaconnect

    # Add routes
    attach_udaconnect(persons, app)
