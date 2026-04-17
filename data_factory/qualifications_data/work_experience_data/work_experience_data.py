from faker import Faker
from data_objects.qualifications.work_experience.work_experience import WorkExperience

class WorkExperienceData:

    faker = Faker()

    @staticmethod
    def get_work_experience_details() -> WorkExperience:
        from_date = WorkExperienceData.faker.date_between(
            start_date="-5y",
            end_date="-1y"
        )

        to_date = WorkExperienceData.faker.date_between(
            start_date=from_date,
            end_date="today"
        )

        return WorkExperience(
            company=WorkExperienceData.faker.company(),
            job_title=WorkExperienceData.faker.job(),
            from_date=from_date,
            to_date=to_date,
            comment=WorkExperienceData.faker.sentence(nb_words=6)
        )