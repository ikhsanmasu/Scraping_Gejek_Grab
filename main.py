from car_fare_scraping import carFareScraping
import openpyxl
import datetime

# Sesuaikan bagian ini
HEADER = ["START_TIME", "END_TIME", "PICKUP", "DESTINATION", "GOJEK_GOCAR", "GRAB_GRABCAR"]
DEVICE_NAME = "Galaxy Tab A9"
UDID = "R9RWA02936E"
PLATFORM_VERSION = "13"
EXCEL_FILENAME = "data_fare_grabCar_goCar.xlsx"

# objek apliaksi
gocar = carFareScraping(device_name=DEVICE_NAME, udid=UDID, platform_version=PLATFORM_VERSION, apk_name="gojek")
grabcar = carFareScraping(device_name=DEVICE_NAME, udid=UDID, platform_version=PLATFORM_VERSION, apk_name="grab")

# Membuat header excel
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(HEADER)
workbook.save(EXCEL_FILENAME)
current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(f"{current_time} -> membuat header excel : {HEADER}")

# Sesuaikan titik asal dan titik tujuan dengan nama yang telah di save di masing2 aplikasi
pickup = "asal"
destination = "tujuan"


#sesuaikan dengan kebutuhan interval waktu
for _ in range(3):
    start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{current_time} -> scraping data fare gocar")
    harga_gocar = gocar.tarif(saved_asal=pickup, saved_tujuan=destination)
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{current_time} -> tarif gocar dari {pickup} ke {destination} adalah {harga_gocar}")

    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{current_time} -> scraping data fare grabcar")
    harga_grabcar = grabcar.tarif(saved_asal=pickup, saved_tujuan=destination)
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{current_time} -> tarif grabcar dari {pickup} ke {destination} adalah {harga_grabcar}")

    end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # menambah data hasiL scraping ke excel
    data = [start_time, end_time, pickup, destination, f"Rp{harga_gocar}", f"Rp{harga_grabcar}"]

    sheet.append(data)
    workbook.save(EXCEL_FILENAME)
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{current_time} -> menambah data fare excel : {data}")
