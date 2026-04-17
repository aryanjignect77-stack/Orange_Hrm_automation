import allure

def log_step(message: str):
    """Log a step to Allure report and print to console."""
    with allure.step(message):
        pass
