from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from appium.options.android import UiAutomator2Options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functools import wraps

def _continue_on_failure(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print(f" WARNING - function {func} gagal di eksekusi")
            return "Fail retrieving data"
    return wraper

class carFareScraping():
    def __init__(self, device_name: str, udid: str, platform_version: str, apk_name: str = None,
                 appium_server_url: str = 'http://localhost:4723/wd/hub') -> None:

        self.__appium_server_url = appium_server_url

        if apk_name not in ["gojek", "grab"]:
            raise ValueError("Invalid sim type. Expected one of: %s" % ["gojek", "grab"])
        self.__aplication = apk_name

        self.__capabilities = {
            "deviceName": device_name,
            "udid": udid,
            "platformName": "Android",
            "platformVersion": platform_version,
            "noReset": "true"
        }

        if self.__aplication.strip().lower() == "gojek":
            self.__capabilities["appPackage"] = "com.gojek.app"
            self.__capabilities["appActivity"] = "com.gojek.home.deeplink.DeeplinkActivity"
        elif self.__aplication.strip().lower() == "grab":
            self.__capabilities["appPackage"] = "com.grabtaxi.passenger"
            self.__capabilities["appActivity"] = "com.grab.pax.newface.presentation.newface.NewFace"

        self.capabilities_options = UiAutomator2Options().load_capabilities(self.__capabilities)

    def __setup(self) -> None:
        self.driver = webdriver.Remote(self.__appium_server_url, options=self.capabilities_options)

    def __teardown(self) -> None:
        if self.driver:
            self.driver.quit()

    def tarif(self, saved_asal: str, saved_tujuan: str) -> str:
        harga = None
        if self.__aplication.strip().lower() == "gojek":
            harga = self.__tarif_gocar(saved_asal, saved_tujuan)
        elif self.__aplication.strip().lower() == "grab":
            harga = self.__tarif_grabcar(saved_asal, saved_tujuan)
        return harga

    # @_continue_on_failure
    def __tarif_gocar(self, asal: str, tujuan: str) -> str:
        self.__setup()

        # klik GoCar
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="GoCar"]')))
        Gocar_button = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="GoCar"]')
        Gocar_button.click()

        # klik Search Icon
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'com.gojek.app:id/search_icon')))
        search_button = self.driver.find_element(by=AppiumBy.ID, value='com.gojek.app:id/search_icon')
        search_button.click()

        # klik alamat asal dan clearkan inputnya
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'com.gojek.app:id/et_pickup')))
        alamat_asal_input = self.driver.find_element(by=AppiumBy.ID, value='com.gojek.app:id/et_pickup')
        alamat_asal_input.click()
        alamat_asal_input.clear()

        # pilih alamat tersimpan
        titik_asal1_button = self.driver.find_element(by=AppiumBy.XPATH, value=f'//android.widget.TextView[@text="{asal}"]')
        titik_asal1_button.click()

        try:
            WebDriverWait(self.driver, 180).until(
                EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="Lanjut"]')))
            Gocar_button = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Lanjut"]')
            Gocar_button.click()
        except:
            pass

        # pilih alamat tujuan dan clearkan input
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'com.gojek.app:id/et_pickup')))

        # pilih alamat tersimpan
        titik_tujuan1_button = self.driver.find_element(by=AppiumBy.XPATH,
                                                        value=f'//android.widget.TextView[@text="{tujuan}"]')
        titik_tujuan1_button.click()

        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="Pesan GoCar"]')))
        harga = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="GoCar"]//following-sibling::android.widget.TextView[2]')
        harga = harga.text
        self.__teardown()

        return harga

    # @_continue_on_failure
    def __tarif_grabcar(self, asal: str, tujuan: str) -> str:
        self.__setup()

        # klik car
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.XPATH, '//android.widget.LinearLayout[@content-desc="Car, double tap to select"]/android.widget.RelativeLayout/android.widget.ImageView')))
        car_button = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.LinearLayout[@content-desc="Car, double tap to select"]/android.widget.RelativeLayout/android.widget.ImageView')
        car_button.click()

        # klik Search Icon
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'com.grabtaxi.passenger:id/where_to_select_container')))
        search_button = self.driver.find_element(by=AppiumBy.ID, value='com.grabtaxi.passenger:id/where_to_select_container')
        search_button.click()

        # klik alamat asal dan clearkan inputnya
        WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'com.grabtaxi.passenger:id/pick_up_container')))
        alamat_asal_input = self.driver.find_element(by=AppiumBy.ID, value='com.grabtaxi.passenger:id/pick_up_container')
        alamat_asal_input.click()
        alamat_asal_input.clear()

        # pilih alamat tersimpan
        WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.XPATH, f'//android.widget.TextView[@text="{asal}"]')))
        titik_asal1_button = self.driver.find_element(by=AppiumBy.XPATH, value=f'//android.widget.TextView[@text="{asal}"]')
        titik_asal1_button.click()

        # continue
        try:
            WebDriverWait(self.driver, 180).until(
                EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="Continue"]')))
            titik_asal1_button = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@text="Continue"]')
            titik_asal1_button.click()
        except:
            pass

        # pilih alamat tersimpan
        titik_asal1_button = self.driver.find_element(by=AppiumBy.XPATH,
                                                      value='//android.widget.TextView[@text="Recent"]')
        titik_asal1_button.click()

        # pilih alamat tersimpan
        WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.XPATH, f'//android.widget.TextView[@text="{tujuan}"]')))
        titik_tujuan1_button = self.driver.find_element(by=AppiumBy.XPATH,
                                                        value=f'//android.widget.TextView[@text="{tujuan}"]')
        titik_tujuan1_button.click()

        try:
            # choose this pickup
            WebDriverWait(self.driver, 180).until(
                EC.presence_of_element_located((By.ID, 'com.grabtaxi.passenger:id/btn_confirm')))
            titik_asal1_button = self.driver.find_element(by=AppiumBy.ID, value='com.grabtaxi.passenger:id/btn_confirm')
            titik_asal1_button.click()
        except:
            pass

        WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView[@text="Rp"])[1]//following-sibling::android.widget.TextView')))
        harga = self.driver.find_element(by=AppiumBy.XPATH,
                                         value='(//android.widget.TextView[@text="Rp"])[1]//following-sibling::android.widget.TextView')
        harga = harga.text
        self.__teardown()

        return harga
