import pytest
from selenium import webdriver
import os
import json
import argparse
from time import  sleep

class scrapCorreio():
    def __init__(self, uf, filename, qtd = 200):
        self.driver = webdriver.Chrome('./chromedriver')
        self.uf = uf
        self.cep_list = []
        self.filename = filename
        self.qtd = qtd

    def correio_page_request(self):
        self.driver.get("http://www.buscacep.correios.com.br/sistemas/buscacep/")

    def insert_text_field_cep(self):
        input_field = self.driver.find_element_by_xpath("//input[@name='relaxation']")
        input_field.send_keys(self.uf)
        text = input_field.get_attribute("value")

    def click_button_search(self):
        button = self.driver.find_element_by_xpath('//*[@id="Geral"]/div/div/div[6]/input')
        button.click()
        
    def click_next_button(self):
        next_button = self.driver.find_element_by_xpath("//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/a")
        next_button.click()
        

    def make_json_file(self):
        trs = self.driver.find_elements_by_xpath("//html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr")
        for i in range(1,len(trs)):
            self.cep_list.append({
                "localidade": trs[i].find_element_by_xpath("td[3]").text,
                "cep": trs[i].find_element_by_xpath("td[4]").text
            })

        if len(self.cep_list) >= self.qtd:
            with open(f"./{self.filename}.json", "w") as file:
                file.write(json.dumps(self.cep_list))

            self.driver.quit()
        else:
            self.click_next_button()
            self.make_json_file()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scrapy on correios")
    parser.add_argument(
        "--first", "--f", required=True, help="It needs first (--first) uf to search "
    )
    parser.add_argument(
        "--second",
        "--s",
        required=True,
        help="It needs second (--second) uf to search",
    )
    parser.add_argument(
        "--quantity",
        "--qtd",
        required=False,
        help="It needs the quantity of ceps to scrap",
    )

    args = parser.parse_args()
    
    first_scrap = scrapCorreio(args.first, f"cep_list_{args.first}", int(args.quantity))
    first_scrap.correio_page_request()
    first_scrap.insert_text_field_cep()
    first_scrap.click_button_search()
    first_scrap.make_json_file()

    second_scrap = scrapCorreio(args.second, f"cep_list_{args.second}", int(args.quantity))
    second_scrap.correio_page_request()
    second_scrap.insert_text_field_cep()
    second_scrap.click_button_search()
    second_scrap.make_json_file()


