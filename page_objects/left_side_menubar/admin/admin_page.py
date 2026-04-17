from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class AdminPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_search_input_field_by_name_for_system_user(self, field_name):
        return (By.XPATH,f"//label[normalize-space()='{field_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//input")

    def get_search_dropdown_by_name_for_system_user(self, field_name):
        return (By.XPATH,f"//label[normalize-space()='{field_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]" 
                f"//div[contains(@class,'oxd-select-text-input')]")

    def get_employee_search_result(self, employee_data):
        return (By.XPATH,f"//div[contains(@class,'oxd-table-row')]"
                f"//div[contains(@class,'oxd-table-cell')]"
                f"/div[normalize-space()='{employee_data}']")

    def get_sort_icon_by_column_name(self, column_name):
        return (
            By.XPATH,
            f"//div[@role='columnheader']"
            f"[.//text()[normalize-space()='{column_name}']]"
            "//i[contains(@class,'oxd-table-header-sort-icon')]"
        )

    def get_sort_option_by_column_name(self, column_name, order):
        return (
            By.XPATH,
            f"//div[@role='columnheader']"
            f"[.//text()[normalize-space()='{column_name}']]"
            "//div[@role='dropdown']//span[normalize-space()='{order}']"
        )

    def get_username_column_values(self):
        elements = self.selenium.get_elements(
            (By.XPATH, "//div[@role='row']/div[position()=2]")
        )
        return [
            element.text.strip()
            for element in elements
            if element.text.strip()
        ]

    def get_column_values(self, column_name: str) -> list[str]:
        column_index_map = {
            "Username": 2,
            "User Role": 3,
            "Employee Name": 4,
            "Status": 5,
        }
        if column_name not in column_index_map:
            raise ValueError(f"Unsupported column: {column_name}")
        return self.get_column_values_by_index(column_index_map[column_name])

    def get_column_values_by_index(self, column_index: int) -> list[str]:
        elements = self.selenium.get_elements(
            (
                By.XPATH,
                f"//div[contains(@class,'oxd-table-card')]"
                f"//div[@role='cell'][position()={column_index}]"
            )
        )
        return [
            element.text.strip()
            for element in elements
            if element.text.strip()
        ]

    def casefold_key(self, value: str) -> str:
        return value.casefold()

    def assert_column_sorted(self, values: list[str], order: str):
        if order.lower() == "ascending":
            expected = sorted(values, key=self.casefold_key)
        elif order.lower() == "descending":
            expected = sorted(values, key=self.casefold_key, reverse=True)
        else:
            raise ValueError("Order must be 'Ascending' or 'Descending'")
        assert values == expected, (
            f"Column is not sorted in {order} order.\n"
            f"Actual: {values}\n"
            f"Expected: {expected}"
        )

    def sort_column(self, column_name: str, order: str):
        self.selenium.click(self.get_sort_icon_by_column_name(column_name))
        self.selenium.wait_for_elements(
            (By.XPATH, "//div[@role='dropdown' and contains(@class,'--active')]")
        )
        self.selenium.click(self.get_sort_option_by_order(order))
        self.wait_for_loader_to_disappear()

    def get_sort_option_by_order(self, order: str):
        return (
            By.XPATH,
            f"//div[@role='dropdown' and contains(@class,'--active')]"
            f"//span[normalize-space()='{order}']"
        )

    def get_employee_id_from_search_result(self, employee_id):
        locator = (
            By.XPATH,f"//div[@class='oxd-table-cell oxd-padding-cell'][normalize-space()='{employee_id}']"
        )
        return self.selenium.get_text(locator).strip()

    def get_employee_name_from_search_result(self, employee_name):
        locator = (By.XPATH,f"//div[@class='oxd-table-cell oxd-padding-cell'][normalize-space()='{employee_name}']")
        return self.selenium.get_text(locator).strip()

    def get_dropdown_by_label(self, label_name):
        locator = (By.XPATH,f"//label[normalize-space()='{label_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//div[contains(@class,'oxd-select-text-input')]")
        self.selenium.click(locator)

    def get_all_dropdown_options(self, option_name):
        return (
            By.XPATH,
            f'//div[@class="oxd-select-option"]//span[normalize-space()="{option_name}"]'
        )

    def get_dropdown_option_for_employee_name(self, employee_name):
        locator = (By.XPATH,f"//div[@role='option']//span[normalize-space()='{employee_name}']")
        self.selenium.wait_till_clickable(locator).click()

    def is_user_present_with_employee_name_and_role(
            self, employee_name, role
    ) -> bool:
        locator = (
            By.XPATH,
            f"//div[@class='oxd-table-body']"
            f"//div[normalize-space()='{employee_name}']"
            f"/ancestor::div[@role='row']"
            f"//div[normalize-space()='{role}']"
        )
        elements = self.selenium.wait_for_elements_(locator)
        return len(elements) > 0

    def is_user_present_with_username_and_role(
            self, username, role
    ) -> bool:
        locator = (
            By.XPATH,
            f"//div[@class='oxd-table-body']"
            f"//div[normalize-space()='{username}']"
            f"/ancestor::div[@role='row']"
            f"//div[normalize-space()='{role}']"
        )
        elements = self.selenium.wait_for_elements_(locator)
        return len(elements) > 0

    def get_user_table_cell_value_by_username(
            self, username, column_index
    ) -> str:
        locator = (
            By.XPATH,
            f"//div[normalize-space()='{username}']"
            f"/ancestor::div[@role='row']"
            f"//div[@role='cell'][{column_index}]//div"
        )
        return self.selenium.get_text(locator)

    def get_search_input_value(self, label_name) -> str:
        locator = (
            By.XPATH,
            f"//label[normalize-space()='{label_name}']"
            f"/ancestor::div[contains(@class,'oxd-input-group')]"
            f"//input"
        )
        return self.selenium.get_attribute(locator, "value")

    def get_dropdown_selected_value_by_label(self, label_name) -> str:
        locator = (
            By.XPATH,
            f"//label[normalize-space()='{label_name}']"
            f"/ancestor::div[contains(@class,'oxd-input-group')]"
            f"//div[contains(@class,'oxd-select-text-input')]"
        )
        return self.selenium.get_text(locator)

    def enter_search_value_for_system_user(self, field_name, value):
        self.selenium.clear_and_type(self.get_search_input_field_by_name_for_system_user(field_name),value)

    def get_employee_search_result_text(self, employee_data):
        return self.selenium.get_text(self.get_employee_search_result(employee_data))

    def click_on_option(self, option_name):
        self.selenium.wait_till_clickable(self.get_all_dropdown_options(option_name)).click()











