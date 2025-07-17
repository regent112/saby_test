import pytest

from baseapp import BasePage
from selenium import webdriver
import time
from typing import Any, Callable, Final, List, Optional, TYPE_CHECKING
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
    __locator_geospan: Final = (
        'xpath',
        '//div[@class="sbis_ru-container sbisru-Contacts__relative"]'
        '//span[@class="sbis_ru-Region-Chooser__text sbis_ru-link"]'
    )
    __locator_partners: Final = (
        'xpath',
        '//div[@name="viewContainer"]//div[@class="sbisru-Contacts-List__name sbisru-Contacts-List--ellipsis '
        'sbisru-Contacts__text--md pb-4 pb-xm-12 pr-xm-32"]'
    )
    __locator_geoselect: Final = (
        'xpath',
        '//li[@class="sbis_ru-Region-Panel__item"]//span[contains(text(), "{0}")]'
    )

    def check_page(self) -> None:
        assert self.driver.current_url.startswith('https://saby.ru/contacts'), f'Wrong url: {self.driver.current_url}'
        assert 'контакты' in self.driver.title.lower(), f'Wrong title: {self.driver.title}'

    def click_to_banner(self) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_banner)
        assert len(elements) == 1, 'Banner not found or too many'
        elements[0].click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def check_geo(self, address: str, url: Optional[str] = None, title: Optional[str] = None) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_geospan)
        assert len(elements) == 1, 'Geospan not found or too many'
        elem_address = elements[0].text.strip()
        assert elem_address == address, f'Address does not match {elem_address} vs {address}'
        elements = self.find_elements(*self.__locator_partners)
        assert elements, 'Partners not found'
        if url:
            assert url in self.driver.current_url, f'Wrong url: {self.driver.current_url} must contains {url}'
        if title:
            assert title in self.driver.title, f'Wrong title: {self.driver.title} must contains {title}'

    def change_geo(self, address: str) -> None:
        elements: List['WebElement'] = self.find_elements(*self.__locator_geospan)
        assert len(elements) == 1, 'Geospan not found or too many'
        elements[0].click()
        elements = self.find_elements(
            self.__locator_geoselect[0],
            self.__locator_geoselect[1].format(address)
        )
        assert len(elements) == 1, f'Address not found or too many: {address}'
        elements[0].click()
        #
        # задержка js
        time.sleep(0.5)
        #

    def get_list_partners(self) -> List[str]:
        elements: List['WebElement'] = self.find_elements(*self.__locator_partners)
        assert elements, 'Partners not found'
        return [element.text.strip() for element in elements]


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


def clear_driver(f: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        list_handles = chrome_driver.window_handles
        while len(list_handles) > 1:
            chrome_driver.close()
            list_handles = chrome_driver.window_handles
        chrome_driver.switch_to.window(list_handles[0])
        return f(*args, **kwargs)
    return wrapper


@pytest.mark.skip
@clear_driver
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


@pytest.mark.skip
@clear_driver
def test_2():
    pageSaby = PageSaby(chrome_driver)
    pageSaby.go()
    pageSaby.go_contacts()
    pageSabyContacts = PageSabyContacts(chrome_driver)
    pageSabyContacts.check_page()
    pageSabyContacts.check_geo(address='Костромская обл.')
    prev_list_partners = pageSabyContacts.get_list_partners()
    pageSabyContacts.change_geo('Камчатский')
    pageSabyContacts.check_geo(address='Камчатский край', url='41-kamchatskij-kraj', title='Камчатский край')
    cur_list_partners = pageSabyContacts.get_list_partners()
    if cur_list_partners == prev_list_partners:
        raise AssertionError(f'List partners does not changed: {cur_list_partners} vs {prev_list_partners}')


@clear_driver
def test_3():
    pageSaby = PageSaby(chrome_driver)
    pageSaby.go()
