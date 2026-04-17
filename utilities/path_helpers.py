import os

class FilePaths:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROFILE_PICTURE = os.path.join(
        BASE_DIR, "test_data", "profile_picture", "231531.jpg"
    )
    FILE_ATTACHMENT = os.path.join(
        BASE_DIR, "test_data", "attachment_file", "blank.pdf"
    )