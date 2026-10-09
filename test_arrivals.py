import unittest
from unittest.mock import Mock, patch

import requests

from arrivals import get_arrivals, format_arrivals


class TestArrivals(unittest.TestCase):

    @patch("arrivals.requests.get")
    def test_successful_response(self, mock_get):
        response = Mock()
        response.json.return_value = {
            "arrivals": [
                {"bus_number": "101", "arrival_minutes": 5}
            ]
        }
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        result = get_arrivals("STOP1", "https://example.com/api")

        self.assertEqual(
            result,
            [{"bus_number": "101", "arrival_minutes": 5}]
        )
        mock_get.assert_called_once()

    @patch("arrivals.requests.get")
    def test_request_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("Offline")

        result = get_arrivals("STOP1", "https://example.com/api")

        self.assertEqual(result, [])

    @patch("arrivals.requests.get")
    def test_empty_results(self, mock_get):
        response = Mock()
        response.json.return_value = {"arrivals": []}
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        result = get_arrivals("STOP1", "https://example.com/api")

        self.assertEqual(result, [])
        self.assertEqual(
            format_arrivals(result),
            "No upcoming bus arrivals."
        )

    def test_format_arrivals(self):
        result = format_arrivals([
            {"bus_number": "101", "arrival_minutes": 5},
            {"bus_number": "202", "arrival_minutes": 12}
        ])

        self.assertEqual(
            result,
            "Bus 101: 5 minutes\nBus 202: 12 minutes"
        )


if __name__ == "__main__":
    unittest.main()