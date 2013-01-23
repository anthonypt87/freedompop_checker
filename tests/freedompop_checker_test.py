import freedompop_checker
import unittest

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

class FreedomPopCheckerUnitTest(unittest.Testcase):

	def setUp(self):
		self.mock_request_post = mock.patch(
		'freedom_pop_checker.requests.post',
		return_value=mock.mock(
			text=MOCK_RESPONSE
		)
	)

	def test_get_usage(self):
		freedom_pop_checker = FreedomPopChecker(username, password)
		usage = freedom_pop_checker.get_usage()
		T.assert_equal(
			usage.used,
			9
		)
		T.assert_equal(
			usage.max,
			1525.76
		)

