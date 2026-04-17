from datetime import datetime
from faker import Faker
from data_objects.edit_job_details.edit_job_details import EditJobDetails

faker = Faker()
class EditJobDetailsData:

    @staticmethod
    def get_job_details() -> EditJobDetails:
        return EditJobDetails(
            joined_date=datetime.now().strftime("%Y-%d-%m")
        )