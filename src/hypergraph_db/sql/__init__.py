import os


class SQLScripts:
    SQL_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def get_script(cls, filename: str) -> str:
        filepath = os.path.join(cls.SQL_DIRECTORY, filename)
        with open(filepath, "r") as file:
            return file.read()
