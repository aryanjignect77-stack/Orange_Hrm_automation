from faker import Faker
from data_objects.qualifications.education.education import Education

class EducationData:
    faker = Faker()
    EDUCATION_LEVELS = [
        "High School Diploma",
        "Bachelor's Degree",
        "Master's Degree",
        "PhD",
        "College Undergraduate",
        "law",
        "BCA"
    ]

    @staticmethod
    def generate_gpa():
        return f"{EducationData.faker.pyfloat(min_value=6, max_value=9.9, right_digits=2):.2f}"

    @staticmethod
    def format_date(date_obj):
        return date_obj.strftime("%Y-%d-%m")

    @staticmethod
    def get_education_details() -> Education:
        start_date = EducationData.faker.date_between(
            start_date="-6y",
            end_date="-1y"
        )

        end_date = EducationData.faker.date_between(
            start_date=start_date,
            end_date="today"
        )
        return Education(
            major_specialization=EducationData.faker.job(),
            institute=EducationData.faker.company(),
            year=EducationData.faker.year(),
            gpa_score=EducationData.generate_gpa(),
            start_date=EducationData.format_date(start_date),
            end_date=EducationData.format_date(end_date)
        )