import unittest

# This function represents the core logic used in the Streamlit app
def validate_transmutation_result(data):
    """
    Logic Gate: Determines if the data is a successful 'Gold' result 
    or a 'Lead' error. Safe against NoneType.
    """
    if data is None:
        return False
    
    # Check for the status we defined in our system instructions
    status = data.get("status", "error")
    summary = data.get("summary", "")
    
    # Successful if status is 'success' AND we actually got a summary
    return status == "success" and len(summary) > 0

class TestAlchemistLogic(unittest.TestCase):

    def test_gold_success(self):
        """Test a perfect, valid response from the backend."""
        data = {
            "status": "success",
            "title": "How to Alchemize Data",
            "summary": "This is a cohesive paragraph of distilled knowledge.",
            "key_points": ["Point 1", "Point 2"],
            "is_short": True,
            "transcript": "Polished text..."
        }
        self.assertTrue(validate_transmutation_result(data))

    def test_none_type_safety(self):
        """Test the fix for the 'NoneType' object has no attribute 'get' error."""
        data = None
        # This ensures the app doesn't crash if the backend is offline
        self.assertFalse(validate_transmutation_result(data))

    def test_lead_error_status(self):
        """Test when the backend explicitly returns an error status."""
        data = {
            "status": "error",
            "title": "Transmutation Failed",
            "summary": "No transcript available for this scroll."
        }
        self.assertFalse(validate_transmutation_result(data))

    def test_missing_summary(self):
        """Test if status is success but the summary is accidentally empty."""
        data = {
            "status": "success",
            "summary": ""
        }
        self.assertFalse(validate_transmutation_result(data))

    def test_missing_status_key(self):
        """Test robustness if the 'status' key is missing from the dictionary."""
        data = {"title": "Incomplete Data"}
        self.assertFalse(validate_transmutation_result(data))

if __name__ == "__main__":
    unittest.main()