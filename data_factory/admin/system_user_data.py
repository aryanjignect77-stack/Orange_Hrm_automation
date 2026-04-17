from faker import Faker
from data_objects.system_user.system_user import SystemUser

class SystemUserData:

    faker = Faker()

    @staticmethod
    def get_system_user_details(employee_name: str) -> SystemUser:
        password = SystemUserData.faker.password()
        return SystemUser(
            user_role="Admin",
            status="Enabled",
            employee_name=employee_name,
            username=SystemUserData.faker.user_name(),
            password=password,
        )