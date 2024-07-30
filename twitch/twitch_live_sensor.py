from bs4 import BeautifulSoup
import requests

def twitch_sensor_check(channel):
	response = requests.get(channel)
	
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	status = soup.find_all('script')
	for ln in status:
		if 'isLiveBroadcast' in ln.text:
			print(f"FLAG: True; sensor code: {response.status_code}")
			return True
	print(f"FLAG: False; sensor code: {response.status_code}")
	return False
