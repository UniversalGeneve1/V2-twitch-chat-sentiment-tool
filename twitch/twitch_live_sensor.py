from bs4 import BeautifulSoup
import requests

def twitch_sensor_check(channel):
	response = requests.get(channel)
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	status = soup.find_all('script')
	
	for ln in status:
		if 'isLiveBroadcast' in ln.text:
			return True
	print(f"SENSOR ERROR: thrown code: {response.status_code}")
	return False
