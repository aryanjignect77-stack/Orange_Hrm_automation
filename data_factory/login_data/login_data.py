import os.path
import json

class LoginData:
    """
    Reads login test data from JSON file
    """

    @staticmethod
    def _read_login_data():
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )

        file_path = os.path.join(
            project_root,
            "test_data",
            "login_data",
            "login_data.json"
        )

        with open(file_path, "r") as file:
            return json.load(file)

    @classmethod
    def get_valid_user_details(cls):
        data = cls._read_login_data()
        return data["valid_user"]

    @classmethod
    def get_invalid_user_details(cls):
        data = cls._read_login_data()
        return data["invalid_user"]