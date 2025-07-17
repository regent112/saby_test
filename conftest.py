# import pytest
# from selenium import webdriver
#
# driver = webdriver.Chrome()
#
#
# @pytest.fixture(scope='module')
# def chrome_driver():
#     list_handles = driver.window_handles
#     while len(list_handles) > 1:
#         driver.close()
#         list_handles = driver.window_handles
#     driver.switch_to.window(list_handles[0])
#     yield driver
