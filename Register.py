class Register():
    def __init__(self, name: str, addr: str, len: int, type: str):
        self.name: str = name
        self.addr: str = addr
        self.len: int = len
        self.type: str = type

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f"{self.name}@{self.addr} ({self.type} : {self.len})"
