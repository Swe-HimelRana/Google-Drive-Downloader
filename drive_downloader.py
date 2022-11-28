import re
import requests
import shutil
from tqdm.auto import tqdm

def validate_url(url):

	regex = r"https://drive\.google\.com/file/d/.*/view?.*"

	test_str = url

	mached = re.match(regex, test_str)

	if mached:
		return True

def get_key(url):

	if validate_url(url) is None:
		return None

	regex = r"(https://drive\.google\.com/file/d/)(.*)/view(.*)"
	matches = re.finditer(regex, url)

	for matchNum, match in enumerate(matches, start=1):
		res = match.group(2)

		if res is not None:
			return res


def download(url):
	file_key = get_key(url)

	if file_key is None:
		return None

	download_url = f'https://drive.google.com/uc?id={file_key}&export=download'.format(file_key=file_key)

	with requests.get(download_url, stream=True) as response:

		file_name = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0].split("''")[1]

		total_length = int(response.headers.get("Content-Length"))

		print("Downloading: ", file_name)

		with tqdm.wrapattr(response.raw, "read", total=total_length, desc="")as raw:
			with open(f"{file_name}", 'wb')as output:
				shutil.copyfileobj(raw, output)