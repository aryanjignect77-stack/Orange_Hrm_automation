# Orange HRM Automation Framework

A robust, scalable, and maintainable test automation framework built with Python, Selenium, and PyTest for testing the Orange HRM application.

## 🏗️ Architecture Overview

This framework follows the **Page Object Model (POM)** design pattern with a **Data-Driven Testing** approach, implementing best practices for test automation including:

- **Separation of Concerns**: Clear distinction between test logic, page interactions, and test data
- **Modular Design**: Reusable components and utilities
- **Cross-browser Support**: Chrome, Firefox, and Edge compatibility
- **Comprehensive Reporting**: Allure reports with detailed test execution information
- **Parallel Execution**: Support for running tests in parallel using pytest-xdist

## 📋 Requirements

### Prerequisites
- Python 3.8+
- Web browsers (Chrome, Firefox, Edge)

### Dependencies
```bash
pip install -r requirements.txt
```

Key dependencies include:
- **pytest==8.3.3** - Test runner and framework
- **selenium==4.18.1** - Web automation
- **allure-pytest==2.13.5** - Enhanced reporting
- **pytest-xdist==3.6.1** - Parallel test execution
- **loguru==0.7.2** - Advanced logging
- **faker** - Test data generation
- **webdriver-manager** - Automatic driver management

## 🚀 Usage

### Running Tests
```bash
# Run all tests
pytest

# Run with specific markers
pytest -m smoke
pytest -m regression
pytest -m sanity

# Run in parallel
pytest -n 4

# Generate Allure reports
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Configuration
- Browser settings and environment variables in `config/` directory
- Test data in `test_data/` directory
- Logging configuration in `utilities/logger.py`

## ✨ Benefits

- **Maintainable**: Clean code structure with clear separation of concerns
- **Scalable**: Easy to add new test cases and modules
- **Reliable**: Robust error handling and retry mechanisms
- **Comprehensive**: Detailed reporting and logging
- **Flexible**: Configurable for different environments and browsers
- **Efficient**: Parallel execution and optimized test flow

## 📁 Framework Structure

### Core Configuration Files

| File                 | Why                   |
| -------------------- | --------------------- |
| `pytest.ini`         | PyTest configuration  |
| `conftest.py`        | Fixtures + hooks      |
| `requirements.txt`   | Dependency management |
| `config.ini`         | Browser + environment |
| `base_test.py`       | Central test setup    |
| `browser_factory.py` | Cross-browser support |
| `logger.py`          | Centralized logging   |
| `screenshot_util.py` | Failure screenshots   |
| `allure_helper.py`   | Allure attachments    |

### Directory Structure

#### 📂 `page_objects/`
Contains Page Object Model classes representing different application pages:
- **`base/`** - Base page class with common functionality
- **`login/`** - Login page authentication methods
- **`header/`** - Header navigation and user actions
- **`left_side_menubar/`** - Main navigation menu components
- **`pim/`** - Personnel Information Management pages
- **`common/`** - Shared page components and utilities

#### 📂 `utilities/`
Framework utility classes and helper functions:
- **`browser_factory.py`** - WebDriver instantiation for Chrome, Firefox, Edge
- **`selenium_helpers.py`** - Custom Selenium wrapper methods
- **`wait_helpers.py`** - Explicit wait strategies and utilities
- **`config_reader.py`** - Configuration file parsing
- **`logger.py`** - Centralized logging setup with loguru
- **`allure_helpers.py`** - Allure report integration
- **`path_helpers.py`** - File and directory path utilities

#### 📂 `tests/`
Test execution files organized by module:
- **`conftest.py`** - PyTest fixtures, hooks, and configuration
- **`login/`** - Authentication test scenarios
- `admin/` - Admin module tests
- `pim/` - Employee management tests
- `recruitment/` - Recruitment process tests
- `my_info/` - Personal information tests

#### 📂 `data_objects/`
Data transfer objects and test data models:
- **`add_employee/`** - Employee creation data structures
- **`system_user/`** - User account data models
- **`qualifications/`** - Employee qualification data
- **`recruitment/`** - Recruitment process data

#### 📂 `data_factory/`
Test data generation and management:
- Dynamic data creation using Faker
- Environment-specific test data
- Data validation and transformation utilities

#### 📂 `config/`
Configuration files for different environments:
- Browser settings
- Application URLs
- User credentials
- Test parameters

#### 📂 `reports/`
Test execution reports and artifacts:
- **`allure-results/`** - Raw Allure report data
- **`allure-report/`** - Generated HTML reports
- Screenshots and test artifacts

#### 📂 `logs/`
Application and test execution logs with structured formatting.

## 🔧 Key Features

### Test Markers
- **`@pytest.mark.smoke`** - Critical functionality tests
- **`@pytest.mark.regression`** - Full regression suite
- **`@pytest.mark.sanity`** - Quick sanity checks

### Reporting
- **Allure Reports**: Interactive HTML reports with screenshots, logs, and test metrics
- **Console Logging**: Real-time test execution feedback
- **Structured Logs**: Detailed logging with loguru for debugging

### Cross-Browser Support
- Chrome (default)
- Firefox
- Microsoft Edge
- Automatic driver management via webdriver-manager

### Data Management
- External test data files
- Dynamic data generation
- Environment-specific configurations
- Data validation and cleanup
