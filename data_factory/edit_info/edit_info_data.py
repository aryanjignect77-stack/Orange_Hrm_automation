from faker import Faker
from data_objects.edit_info.edit_info import EditInfo

class EditInfoData:

    faker = Faker()

    @staticmethod
    def get_my_info_details() -> EditInfo:
        return EditInfo(
            first_name=EditInfoData.faker.first_name(),
            middle_name=EditInfoData.faker.first_name(),
            last_name=EditInfoData.faker.last_name(),
            other_id=str(EditInfoData.faker.random_number(digits=5, fix_len=True))
        )