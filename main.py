from SeleniumTester import SeleniumTester

if __name__ == "__main__":
    tester = SeleniumTester('provinces.json', "http://127.0.0.1:80/province/", "province_name")
    tester.run_tests()
    tester.display_summary()
