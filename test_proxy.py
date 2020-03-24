import requests
import time
import proxy
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process

# from parallel_request import parallel_request
# import proxy_by_file
	
def get_my_ip(proxy_=False):
	"""
	Функция для получания IP адреса
	
	На вход принимает не обязательный аргемент proxy_,
	принимающитйй значения Ture если нужен проксированный запрос
	и False, если не проксированный.

	По умолчанию проксирование трафика отключено 
	"""
	try:
		if proxy_:
			response = proxy.request_proxy('https://whoer.net/ru')
		else:
			response = requests.get('https://whoer.net/ru')
	except Exception as e:
		print(f"Ошибка запроса: {e}")
		return 

	if response.status_code == 200:
		html = response.text
		ip = BeautifulSoup(html, "lxml").find('strong', attrs={'data-clipboard-target': '.your-ip'}).get_text().replace("\n", "")
		return ip
	else:
		return False
	

def main():
	""" Main функция для проверки скрипта прокси адресов"""
	
	my_ip = get_my_ip()
	print(f"My IP >>> {my_ip}")
		
	for index in range(10):
		proxy_ip = get_my_ip(proxy_=True)
		print(f"{index + 1}) Proxy IP >>> {proxy_ip}")
		# print("\n")


if __name__ == '__main__':
	try:
		# Инициализируем процесс обновления прокси адресов
		proxy = Process(target=proxy.update_proxy, args=())
		# Инициализируем процесс проерки прокси скрипта
		main_p = Process(target=main, args=())

		# Запускаем процессы
		proxy.start()
		main_p.start()

		# Останавливаем процессы
		main_p.join()
		proxy.join()
	except Exception as e:
		print(f">>> {e}")