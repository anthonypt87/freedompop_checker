import argparse
import re
import requests
from BeautifulSoup import BeautifulSoup


FREEDOMPOP_LOGIN_URI = 'https://www.freedompop.com/login.htm'


class FreedomPopChecker(object):
	def __init__(self, username, password):
		self._username = username
		self._password = password

	def get_usage(self):
		response = requests.post(
			FREEDOMPOP_LOGIN_URI,
			data={
				'signin-username': self._username,
				'signin-password': self._password
			}
		)
		return self._parse_data_usage(response)

	def _parse_data_usage(self, response):
		response_parser = DataUsageResponseParser()
		parsed_usage = response_parser.parse_data_usage(response.text)
		return parsed_usage


class DataUsageResponseParser(object):

	DATA_USAGE_REGEX = re.compile(r"\s*(?P<count>\d+(\.\d+)?) (?P<size_type>MB|GB)")

	def parse_data_usage(self, raw_response):
		soup = BeautifulSoup(raw_response)
		return DataUsage(
			max=self._parse_total(soup),
			used=self._parse_used(soup),
		)

	def _parse_used(self, soup):
		bandwithbar_soup = soup.find(id='bandwidthBarWidget')
		data_usage_strong_soup = bandwithbar_soup.find('strong')
		size_string = data_usage_strong_soup.string
		return self._parse_size_from_string(size_string)

	def _parse_size_from_string(self, size_string):
		total_match = self.DATA_USAGE_REGEX.match(size_string)
		size_type = total_match.group('size_type')
		count = total_match.group('count')
		return self._get_size_in_mb(size_type, count)

	def _get_size_in_mb(self, size_type, count):
		if size_type == 'GB':
			return self._convert_gb_to_mb(count)
		else:
			return float(count)

	def _convert_gb_to_mb(self, gb):
		return float(gb) * 1024

	def _parse_total(self, soup):
		total_div = soup.find(attrs={'class': 'productTitle'})
		return self._parse_size_from_string(total_div.string)


class DataUsage(object):
	def __init__(self, used, max):
		self.used = used
		self.max = max


class DataUsagePresenter(object):

	def present(self, data_usage):
		return "Used %s/%s MBs." % (data_usage.used, data_usage.max)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Check data usage for freedompop.com')
	parser.add_argument(
		'username',
		help='Freedompop username',
	)
	parser.add_argument(
		'password',
		help='Freedompop password',
	)

	args = parser.parse_args()

	checker = FreedomPopChecker(args.username, args.password)
	usage = checker.get_usage()

	presenter = DataUsagePresenter()
	print(presenter.present(usage))



