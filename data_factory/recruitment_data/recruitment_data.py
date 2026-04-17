from faker.proxy import Faker
from datetime import datetime
from data_objects.recruitment.recruitment import Recruitment

faker = Faker()
class RecruitmentData:

    @staticmethod
    def get_recruitment_details() -> Recruitment:
        return Recruitment(
            first_name=faker.first_name(),
            middle_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            contact_number=faker.msisdn()[:10],
            keywords=faker.word(),
            date_of_application=datetime.today().strftime("%Y-%d-%m"),
            notes=faker.sentence()
        )