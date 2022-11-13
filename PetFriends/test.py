import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Settings import valid_email, valid_password


@pytest.fixture(autouse=True)
def testing():
    driver = webdriver.Chrome('C:\Documents\chromedriver.exe')
    driver.get('http://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    yield driver
    driver.quit()


def test_show_my_pets(testing):
    # Проверяем нахождение на главной странице
    driver = testing
    assert driver.find_element(By.TAG_NAME, "h1").text == "PetFriends"

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')
    print(len(names))
    print(type(names))
    descriptions = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test1_amount_my_pets(testing):
    # Проверяем что  присутствуют все питомцы
    driver = testing
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#all_my_pets table tbody tr')))

    my_pets_table = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets table tbody tr')
    my_pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(":")[1]
    assert len(my_pets_table) == int(my_pets_number)


def test2_half_card_with_photo(testing):
    # Проверяем наличие фото
    driver = testing
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    images_potential = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    images_fact = 0
    for i in range(len(images_potential)):
        if images_potential[i].get_attribute('src') != "":
            images_fact = images_fact + 1
    assert int(images_fact) >= (len(images_potential))/2


def test3_name_age_type_of_pets(testing):
    # Проверяем наличие имени, возраста и породы питомцев
    driver = testing
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    driver.implicitly_wait(5)

    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    type_of_animal = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age_of_animal = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    for i in range(len(names)):
        assert names[i].text != ''
        assert type_of_animal[i].text != ''
        assert age_of_animal[i].text != ''


def test4_different_names_of_pets(testing):
    # Проверяем, что имена питомцев не совпадают
    driver = testing
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    names_list = []
    for i in range(len(names)):
        names_list.append(names[i].text)
    assert len(names_list) == len(set(names_list))


def test5_recurring_pets(testing):
    # Проверяем, что питомцы не повторяются
    driver = testing
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    data_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    data_pets_list = []
    for i in range(len(data_pets)):
        data_pets_list.append(data_pets[i].text)
    assert len(data_pets_list) == len(set(data_pets_list))