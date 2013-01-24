import mock
import unittest

import freedompop_checker


# TODO: Should probably write an integration test. Kind of scared to
# expose credentials. Could alternatively write a mock server but
# not worth it for a one off script.


MOCK_RESPONSE = """
<html>
<body>
<div class="productTitle" style="margin-bottom:5px;">1.49 GB Total</div>
<div id="bandwidthBarWidget">
        	<h4>You've used <strong>  9 MB</strong> (1%).</h4>

        	<div id="bandwidthBar" class="">
            <div class="progressContainer">
                <div class="colorBar" style="width:1%;"></div>
            </div>
        </div>
        <p>
            <strong>8</strong> days left in your plan period.


                    <a href="acct_usage.htm" class="learnMore" style="text-align:right; float:right; display:inline;">Usage Details</a>



        </p>
    </div>
</body>
</html>
"""


class FreedomPopCheckerUnitTest(unittest.TestCase):

	def setUp(self):
		self.mock_request_post_patcher = mock.patch(
			'freedompop_checker.requests.post',
			return_value=mock.Mock(
				text=MOCK_RESPONSE
			)
		)
		self.mock_request_post = self.mock_request_post_patcher.start()

	def tearDown(self):
		self.mock_request_post_patcher.stop()

	def test_get_usage(self):
		checker = freedompop_checker.FreedomPopChecker('username', 'password')
		usage = checker.get_usage()
		self.assertEqual(usage.used, 9)
		self.assertEqual(usage.max, 1525.76)


class DataUsageResponseParserUnitTest(unittest.TestCase):

	def test_get_data_usage(self):
		response_parser = freedompop_checker.DataUsageResponseParser()
		parsed_data_usage = response_parser.parse_data_usage(MOCK_RESPONSE)
		self.assertEqual(parsed_data_usage.used, 9)
		self.assertEqual(parsed_data_usage.max, 1525.76)


class DataUsagePresenterUnitTest(unittest.TestCase):

	def test_present(self):
		presenter = freedompop_checker.DataUsagePresenter()
		presented_string = presenter.present(
			mock.Mock(
				used=199,
				max=500
			)
		)
		self.assertEqual(presented_string, 'Used 199/500 MBs.')


