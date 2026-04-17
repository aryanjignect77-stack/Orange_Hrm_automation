from faker import Faker
from data_objects.qualifications.license.license import License

faker = Faker()
class LicenseData:

    @staticmethod
    def format_date(date_obj):
        return date_obj.strftime("%Y-%d-%m")  # ISO-like, safer

    @staticmethod
    def get_license_details() -> License:
        issued = faker.date_between(start_date="-10y", end_date="today")
        expiry = faker.date_between(start_date=issued, end_date="+10y")

        return License(
            license_number=faker.bothify(text="DL-####-????"),
            issued_date=LicenseData.format_date(issued),
            expiry_date=LicenseData.format_date(expiry)
        )