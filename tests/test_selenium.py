from selenium import webdriver
import os
import json
import argparse
import pytest

driver = webdriver.Chrome('../chromedriver')
cep_list = []
filename = "sao_paulo"
uf = "sao paulo"

def test_correio_page_request():
        driver.get("http://www.buscacep.correios.com.br/sistemas/buscacep/")
        title = driver.title
        assert title == "default"

def test_find_field_cep():
        input_field = driver.find_element_by_xpath(
            "//input[@name='relaxation']")
        assert input_field != None

def test_insert_text_field_cep():
    input_field = driver.find_element_by_xpath(
        "//input[@name='relaxation']")
    input_field.send_keys(uf)
    text = input_field.get_attribute("value")
    assert text != "" and text != None

def test_find_button_search():
    button = driver.find_element_by_xpath(
        '//*[@id="Geral"]/div/div/div[6]/input')
    assert button != None

def test_click_button_search():
    button = driver.find_element_by_xpath(
        '//*[@id="Geral"]/div/div/div[6]/input')
    button.click()
    new_title = driver.title
    assert new_title == "resultadoBuscaCepEndereco"

def test_get_table_content():
    trs = driver.find_elements_by_xpath(
        "//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr")
    assert trs != None

def test_get_first_cep():
    trs = driver.find_elements_by_xpath(
        "//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr")
    cep = trs[1].find_element_by_xpath("td[4]").text
    assert cep != "" and cep != None

def test_generate_cep_object_list():
    trs = driver.find_elements_by_xpath(
        "//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr")
    cep_list = []
    for i in range(1, len(trs)):
        cep_list.append({
            "localidade": trs[i].find_element_by_xpath("td[3]").text,
            "cep": trs[i].find_element_by_xpath("td[4]").text
        })
    assert len(cep_list) == (len(trs)-1)

def test_get_next_button():
    next_button = driver.find_element_by_xpath(
        "//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/a")
    assert next_button != None

def test_click_next_button():
    next_button = driver.find_element_by_xpath(
        "//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/a")
    old_page = driver.page_source
    next_button.click()
    new_page = driver.page_source
    assert old_page != new_page

def test_make_json_file():
    trs = driver.find_elements_by_xpath(
        "//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr")
    for i in range(1, len(trs)):
        cep_list.append({
            "localidade": trs[i].find_element_by_xpath("td[3]").text,
            "cep": trs[i].find_element_by_xpath("td[4]").text
        })

    if len(cep_list) == 200:
        with open(f"./cep_list_{filename}.json", "w") as file:
            file.write(json.dumps(cep_list))

        driver.quit()
        assert os.path.exists(f"./cep_list_{filename}.json")
    else:
        test_click_next_button()
        test_make_json_file()
