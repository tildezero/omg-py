class RequestError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Error creating request to api.omg.lol: {message}")


class NoAddressError(Exception):
    def __init__(self):
        super().__init__("please specify an address to use!")
