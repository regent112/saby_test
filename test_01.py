import pytest

from baseapp import BasePage
from selenium import webdriver
import time
from typing import Final, List, TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class PageSaby(BasePage):
    __locator_button: Final = (
        'xpath',
        '//div[@class="sbisru-Header__menu-link sbis_ru-Header__menu-link sbisru-Header__menu-link--hover"]'
    )
    __locator_link: Final = (
        'xpath',
        '//li[@class="sbisru-Header__menu-item sbisru-Header__menu-item-1 mh-8  s-Grid--hide-sm"]'
        '//a[@class="sbisru-link sbis_ru-link"]/span'
    )

    def go(self) -> None:
        self.driver.get('https://saby.ru')

    def go_contacts(self) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_button)
        assert len(elements) == 1, 'Button "Контакты" not found or too many'
        elements[0].click()
        #
        # js тупит, ждём
        time.sleep(0.5)
        #
        elements = self.find_elements(*self.__locator_link)
        assert len(elements) == 1, 'Link "Ещё <N> офисов" not found or too many'
        elements[0].click()


class PageSabyContacts(BasePage):
    __locator_banner: Final = (
        'xpath',
        '//a[@class="sbisru-Contacts__logo-tensor mb-12"]'
    )

    def check_page(self) -> None:
        assert self.driver.current_url.startswith('https://saby.ru/contacts'), f'Wrong url: {self.driver.current_url}'
        assert 'контакты' in self.driver.title.lower(), f'Wrong title: {self.driver.title}'

    def click_to_banner(self) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_banner)
        assert len(elements) == 1, 'Banner not found or too many'
        elements[0].click()
        chrome_driver.switch_to.window(chrome_driver.window_handles[-1])


class PageSabyDownload(BasePage):
    pass


class PageTensor(BasePage):
    __locator_people_block: Final = (
        'xpath',
        '//div[@class="tensor_ru-Index__block4-content tensor_ru-Index__card"]'
    )
    __locator_people_block__about: Final = (
        'xpath',
        f'{__locator_people_block[1]}//a[@class="tensor_ru-link tensor_ru-Index__link"]'
    )

    def check_page(self) -> None:
        assert self.driver.current_url.startswith('https://tensor.ru'), f'Wrong url: {self.driver.current_url}'
        assert 'тензор' in self.driver.title.lower(), f'Wrong title: {self.driver.title}'

    def check_people_block(self) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_people_block)
        assert len(elements) == 1, 'People_block not found or too many'

    def go_about(self) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_people_block__about)
        assert len(elements) == 1, 'People_block.aboutbtn not found or too many'
        elements[0].click()


class PageTensorAbout(BasePage):
    __locator_photos: Final = (
        'xpath',
        '//div[@class="tensor_ru-container tensor_ru-section tensor_ru-About__block3"]'
        '/div[@class="s-Grid-container"]//img'
    )

    def check_page(self) -> None:
        assert self.driver.current_url.startswith('https://tensor.ru/about'), f'Wrong url: {self.driver.current_url}'
        assert 'о компании' in self.driver.title.lower(), f'Wrong title: {self.driver.title}'

    def check_workblock(self) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_photos)
        assert elements, 'Photos not found'
        photo_size = (
            elements[0].get_attribute('width'),
            elements[0].get_attribute('height')
        )
        for element in elements[1:]:
            cur_size = (
                element.get_attribute('width'),
                element.get_attribute('height')
            )
            assert cur_size == photo_size, f'Do not match photo size: {cur_size} vs {photo_size}'


chrome_driver = webdriver.Chrome()


def test_1():
    pageSaby = PageSaby(chrome_driver)
    pageSaby.go()
    pageSaby.go_contacts()
    pageSabyContacts = PageSabyContacts(chrome_driver)
    pageSabyContacts.check_page()
    pageSabyContacts.click_to_banner()
    pageTensor = PageTensor(chrome_driver)
    pageTensor.check_page()
    pageTensor.check_people_block()
    pageTensor.go_about()
    pageTensorAbout = PageTensorAbout(chrome_driver)
    pageTensorAbout.check_page()
    pageTensorAbout.check_workblock()
