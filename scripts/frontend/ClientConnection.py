
"""
    Connection Handler used to interact with the server
"""

class Handler:

    def __init__(self, server_address, database_name):
        self.server_address = server_address
        self.database_name = database_name