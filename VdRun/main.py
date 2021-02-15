
import lxml.html
from lxml.cssselect import CSSSelector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser



class Zeus():
    def __init__(self):
        self.__URL = "https://zeus.sii.cl/cvc/stc/stc.html"
        self.__UrlPost = "https://zeus.sii.cl/cvc_cgi/stc/getstc"
        self.__RutALL = ""
        self.__RUT = ""
        self.__DV = ""
        self.__TxtCaptcha = ""
        # self.__TxtCode
        self.__PRG = "STC"
        self.__OPC = "NOR"
        self.__ACEPTAR = "Consultar+situación+tributaria"

    def SetRutAll(self, RutAll):
        self.__RutALL = RutAll
        n = len(RutAll)
        self.__RUT = RutAll[0:n - 1]
        self.__DV = RutAll[n - 1]

    def ReadCaptcha(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.

        driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
        driver.get(self.__URL)

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "txt_captcha")))
            self.__TxtCaptcha = driver.find_element_by_id("txt_captcha").get_attribute("value")
            return self.__TxtCaptcha
        except:
            return "404"

    def SendPost(self, TxtCode):
        params = {'RUT': self.__RUT,
                  'DV': self.__DV,
                  'txt_captcha': self.__TxtCaptcha,
                  'txt_code': TxtCode,
                  'PRG': self.__PRG,
                  'OPC': self.__OPC,
                  'ACEPTAR': self.__ACEPTAR
                  }
        response = requests.post(self.__UrlPost, data=params)

        tree = lxml.html.fromstring(response.text)
        sel = CSSSelector('#contenedor > div:nth-child(7)')
        results = sel(tree)
        if not results:
            return "false"
        else:
            return "true"


class Decode64():
    def __init__(self):
        self.__URL = "https://www.base64decode.org/"

    def ExtracText(self, TextCode):
        Text = ""
        Text = Text + TextCode[36]
        Text = Text + TextCode[37]
        Text = Text + TextCode[38]
        Text = Text + TextCode[39]
        return Text

    def SendPost(self, TxtCaptcha):
        params = {'input': TxtCaptcha, 'charset': 'UTF-8'}
        try:
            response = requests.post(self.__URL, data=params)
        except:
            return "404"
        parser = HTMLParser()
        soup = BeautifulSoup(response.text, 'html.parser')
        return self.ExtracText(soup.find('textarea', {"name": "output"}).getText())


class Answer():
    def __init__(self):
        self.__Status = ""


def SearchInfo(Rut):
    Ze = Zeus()
    Ze.SetRutAll(Rut)
    Dc = Decode64()
    result = Ze.ReadCaptcha()
    if result != "404":
        result = Dc.SendPost(result)
        if result != "404":
            result = Ze.SendPost(result)
            return result

    return result


if __name__ == "__main__":
    # -------- TEST - ----------------
    # 76987464 - K Nombre Juridico
    # 65544555
    # 13793194K
    # 101903087 NOMBRE lARGO
    # 59258982 name: 1 latsname: 2
    # 151769209
    # 101903087 ROSA DE LAS MERCEDES CHACON CARRASCO
    # 130632807 -  Campo Vacio


    # Return:
    # -true (Rut Existe)
    # -false (Rut No Existe)
    # - 404 Problema de conexion

    print("Validation Result: ", SearchInfo('87776891'))

    # --------- Paginas Consultadas ----------
    #  Cunsultar Datos de Cedula
    #   - https://www.nombrerutyfirma.com/rut
    #
    #
