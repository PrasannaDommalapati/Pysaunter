from saunter.exceptions import ElementVisiblityTimeout
from selenium.webdriver.common.action_chains import ActionChains
from tailored.page import Page
import time

locators = {
    'select_an_element_by_id': 'id=someelenent',
    'select_an_element_by_class': 'class=category',
    'select_an_element_by_tag': 'tag=a',
    'body': 'tag=body'
}


class SFBasePage(Page):

    def wait_until_loaded(self):
        self.wait_for_available(locators['body'])
        return self

    def open_default_url(self):
        self.driver.get(self.config.get('Selenium', 'base_url'))
        return self.wait_until_loaded()

    def __init__(self, driver):
        super(SFBasePage, self)
        self.driver = driver

    def type_and_press_enter(self, locator, text):
        pass

    def press(self, locator):
        element = self.driver.find_element_by_xpath(locator)
        element.click()

    def tick_box(self, locator, value):
        now = self.get_element_value(locator, "checked")
        #print " now="+str(now)+ " value="+str(value)
        if (value and not now) or (not value and now):
            self.press(locator)

    def type(self, locator, text):
        element = self.driver.find_element_by_xpath(locator)
        element.click()
        element.send_keys(text)

    def clear_text(self, locator):
        element = self.driver.find_element_by_xpath(locator)
        element.clear()

    def get_url(self, url):
        self.driver.get(url)

    def wait_in_seconds(self, seconds):
        time.sleep(seconds)

    def select_option(self, locator, option):
        '''
        select option by order
        '''
        options = self._get_options(locator)
        options[option].click()
        print "Option Text selected is : ", self.get_selected_option(locator)

    def _get_options(self, locator):
        self.wait_for_available(locator)
        select = self.driver.find_element_by_locator(locator)
        return select.find_elements_by_tag_name('option')

    def get_select_options_data(self, locator):
        '''
        This method returns a List of comprehended List consisting of the
        drop down text values for selection
        '''
        data = []
        options = self._get_options(locator)
        data.append([option.text for option in options])
        return data

    def press_and_wait_for(self, button, verify, *args):
        self.press(button)
        if args:
            for i in range(args[0]):
                if self.is_element_available(verify):
                    break
                else:
                    time.sleep(1)
            else:
                raise ElementVisiblityTimeout("%s presence timed out" % verify)
        else:
            self.wait_for_visible(verify)

    def is_element_present(self, locator, *args):
        if args:
            for i in range(args[0]):
                if self.driver.is_element_present(locator):
                    return True
                else:
                    time.sleep(1)
            else:
                return False
        else:
            if self.driver.is_element_present(locator):
                return True
            else:
                return False

    def hover_search(self, webelement):
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(webelement).perform()


