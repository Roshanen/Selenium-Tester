import json
from selenium import webdriver
import keyboard
import requests
import time
from colorama import init, Fore

init(autoreset=True)

class SeleniumTester:
    def __init__(self, json_file, base_url, data_key):
        self.base_url = base_url
        self.data_key = data_key
        self.data = self.load_file(json_file)
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.failed_details = []

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless=old')
        self.driver = webdriver.ChromiumEdge(options=options)

    def load_file(self, json_file):
        """Load data from a JSON file."""
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_respond_code(self, data):
        """Test a single uri and record the result."""
        self.total_tests += 1
        data_url = self.base_url + data[self.data_key].replace(" ", "%20")

        try:
            response = requests.get(data_url)
            actual_status_code = str(response.status_code)
        except Exception as e:
            print(f"Error fetching {data_url}: {e}")
            actual_status_code = "N/A"

        expected_status_code = data["respond_code"]

        if actual_status_code == expected_status_code:
            result = f"{Fore.GREEN}PASS{Fore.RESET}"
            self.passed_tests += 1
        else:
            result = f"{Fore.RED}FAIL (Expected: {expected_status_code}, Got: {actual_status_code}){Fore.RESET}"
            self.failed_tests += 1
            self.failed_details.append({
                "url": data_url,
                "expected": expected_status_code,
                "actual": actual_status_code
            })

        print(f"({self.total_tests}) URL: {data_url} - Test Result: {result}")

    def run_tests(self):
        """Run test on all data."""
        print(f"Run test on {Fore.YELLOW}{self.base_url}{Fore.RESET} with {Fore.YELLOW}{len(self.data)}{Fore.RESET} iterations.")
        for item in self.data:
            self.test_respond_code(item)
        self.driver.quit()

    def display_summary(self):
        """Display the summary of the test results."""
        print("\n==== Test Summary ====")
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed Tests: {self.passed_tests}")
        print(f"Failed Tests: {self.failed_tests}")

        if (self.failed_tests > 0):
            if (input("\nDisplay failed tests? (y/any): ") == 'y'):
                self.display_failed_tests()

    def display_failed_tests(self):
        """Display details of failed tests."""
        if (self.failed_tests > 0):
            print("==== Failed Test Details ====")
            for fail in self.failed_details:
                print(f"URL: {fail['url']} -{Fore.RED} Expected: {fail['expected']}, Actual: {fail['actual']}{Fore.RESET}")
        print()