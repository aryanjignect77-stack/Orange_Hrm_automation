from faker import Faker
from data_objects.add_employee.add_employee import AddEmployee

class AddEmployeeData:

    faker = Faker()

    @staticmethod
    def get_valid_add_employee_details():
        password = AddEmployeeData.faker.password()
        return AddEmployee(
            first_name=AddEmployeeData.faker.first_name(),
            middle_name=AddEmployeeData.faker.first_name(),
            last_name=AddEmployeeData.faker.last_name(),
            employee_id=str(AddEmployeeData.faker.random_int(min=1000, max=9999)),
            username=AddEmployeeData.faker.user_name(),
            password=password,
            confirm_password=password
        )

    