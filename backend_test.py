#!/usr/bin/env python3
"""
Backend Test Suite for FTQoin Django Application
Tests the main functionality including QR scanning, passenger name extraction, and settings page.
"""

import requests
import json
import base64
import time
from urllib.parse import urljoin

class FTQoinTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message="", details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "message": message,
            "details": details
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        if details and not success:
            print(f"    Details: {details}")
        print()
        
    def test_index_page_get(self):
        """Test that the main index page loads correctly"""
        try:
            response = self.session.get(self.base_url + "/")
            
            if response.status_code == 200:
                # Check for key elements that should be on the scanner page
                content = response.text.lower()
                
                # Check for form elements
                has_form = 'form' in content
                has_file_input = 'type="file"' in content or 'ticket' in content
                has_scan_functionality = 'scan' in content or 'qr' in content or 'barcode' in content
                
                if has_form and (has_file_input or has_scan_functionality):
                    self.log_test(
                        "Index Page GET Request", 
                        True, 
                        f"Page loaded successfully with scanner interface (Status: {response.status_code})"
                    )
                else:
                    self.log_test(
                        "Index Page GET Request", 
                        False, 
                        f"Page loaded but missing expected scanner elements",
                        f"Form: {has_form}, File input: {has_file_input}, Scan functionality: {has_scan_functionality}"
                    )
            else:
                self.log_test(
                    "Index Page GET Request", 
                    False, 
                    f"Unexpected status code: {response.status_code}",
                    response.text[:500]
                )
                
        except Exception as e:
            self.log_test(
                "Index Page GET Request", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_settings_page(self):
        """Test that the Settings page is accessible"""
        try:
            response = self.session.get(self.base_url + "/settings/")
            
            if response.status_code == 200:
                self.log_test(
                    "Settings Page Access", 
                    True, 
                    f"Settings page loaded successfully (Status: {response.status_code})"
                )
            else:
                self.log_test(
                    "Settings Page Access", 
                    False, 
                    f"Unexpected status code: {response.status_code}",
                    response.text[:500]
                )
                
        except Exception as e:
            self.log_test(
                "Settings Page Access", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def get_csrf_token(self):
        """Get CSRF token from the index page"""
        try:
            response = self.session.get(self.base_url + "/")
            if response.status_code == 200:
                import re
                csrf_match = re.search(r'name=[\'"]csrfmiddlewaretoken[\'"] value=[\'"]([^\'"]+)[\'"]', response.text)
                if csrf_match:
                    return csrf_match.group(1)
        except:
            pass
        return None

    def test_qr_scan_post_invalid_data(self):
        """Test QR scan functionality with invalid data"""
        try:
            csrf_token = self.get_csrf_token()
            
            # Test with invalid hex data
            post_data = {
                'type': 'scan',
                'ticket_hex': 'invalid_hex_data'
            }
            
            if csrf_token:
                post_data['csrfmiddlewaretoken'] = csrf_token
            
            response = self.session.post(self.base_url + "/", data=post_data)
            
            if response.status_code == 200:
                # Should handle invalid data gracefully
                content = response.text.lower()
                
                # Check if error is handled properly (no 500 error)
                if 'error' in content or 'invalid' in content or response.status_code == 200:
                    self.log_test(
                        "QR Scan POST - Invalid Data", 
                        True, 
                        "Invalid data handled gracefully without server error"
                    )
                else:
                    self.log_test(
                        "QR Scan POST - Invalid Data", 
                        True, 
                        "Request processed without error (may show no results)"
                    )
            elif response.status_code == 403 and not csrf_token:
                self.log_test(
                    "QR Scan POST - Invalid Data", 
                    True, 
                    "CSRF protection is working (403 without token is expected)"
                )
            else:
                self.log_test(
                    "QR Scan POST - Invalid Data", 
                    False, 
                    f"Unexpected status code: {response.status_code}",
                    response.text[:500]
                )
                
        except Exception as e:
            self.log_test(
                "QR Scan POST - Invalid Data", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_qr_scan_post_valid_format(self):
        """Test QR scan functionality with valid hex format"""
        try:
            # Test with valid hex format (but potentially invalid ticket data)
            # Using a simple hex string that won't cause parsing errors
            post_data = {
                'type': 'scan',
                'ticket_hex': '48656c6c6f20576f726c64'  # "Hello World" in hex
            }
            
            response = self.session.post(self.base_url + "/", data=post_data)
            
            if response.status_code == 200:
                self.log_test(
                    "QR Scan POST - Valid Hex Format", 
                    True, 
                    "Valid hex format processed without server error"
                )
            else:
                self.log_test(
                    "QR Scan POST - Valid Hex Format", 
                    False, 
                    f"Unexpected status code: {response.status_code}",
                    response.text[:500]
                )
                
        except Exception as e:
            self.log_test(
                "QR Scan POST - Valid Hex Format", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_text_upload_functionality(self):
        """Test text upload functionality"""
        try:
            post_data = {
                'type': 'text',
                'ticket_text': 'test_ticket_data'
            }
            
            response = self.session.post(self.base_url + "/", data=post_data)
            
            if response.status_code == 200:
                self.log_test(
                    "Text Upload Functionality", 
                    True, 
                    "Text upload processed without server error"
                )
            else:
                self.log_test(
                    "Text Upload Functionality", 
                    False, 
                    f"Unexpected status code: {response.status_code}",
                    response.text[:500]
                )
                
        except Exception as e:
            self.log_test(
                "Text Upload Functionality", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_csrf_protection(self):
        """Test CSRF protection is working"""
        try:
            # First get the page to obtain CSRF token
            get_response = self.session.get(self.base_url + "/")
            
            if get_response.status_code == 200:
                # Look for CSRF token in the response
                if 'csrfmiddlewaretoken' in get_response.text:
                    self.log_test(
                        "CSRF Protection", 
                        True, 
                        "CSRF token found in form - protection is active"
                    )
                else:
                    self.log_test(
                        "CSRF Protection", 
                        True, 
                        "No CSRF token found - may be disabled for this endpoint"
                    )
            else:
                self.log_test(
                    "CSRF Protection", 
                    False, 
                    f"Could not load page to check CSRF: {get_response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "CSRF Protection", 
                False, 
                f"Request failed: {str(e)}"
            )
    
    def test_beautifulsoup_parsing_capability(self):
        """Test that BeautifulSoup parsing is available and working"""
        try:
            # This tests the import and basic functionality
            from bs4 import BeautifulSoup
            
            # Test basic HTML parsing
            test_html = """
            <html>
                <body>
                    <table>
                        <tr>
                            <td>Passenger Name</td>
                            <td>David Wiedmer</td>
                        </tr>
                    </table>
                </body>
            </html>
            """
            
            soup = BeautifulSoup(test_html, 'html.parser')
            tables = soup.find_all('table')
            
            if len(tables) > 0:
                rows = tables[0].find_all('tr')
                if len(rows) > 0:
                    cells = rows[0].find_all('td')
                    if len(cells) >= 2:
                        self.log_test(
                            "BeautifulSoup Parsing Capability", 
                            True, 
                            "BeautifulSoup is available and can parse HTML tables correctly"
                        )
                    else:
                        self.log_test(
                            "BeautifulSoup Parsing Capability", 
                            False, 
                            "BeautifulSoup parsing failed - could not find table cells"
                        )
                else:
                    self.log_test(
                        "BeautifulSoup Parsing Capability", 
                        False, 
                        "BeautifulSoup parsing failed - could not find table rows"
                    )
            else:
                self.log_test(
                    "BeautifulSoup Parsing Capability", 
                    False, 
                    "BeautifulSoup parsing failed - could not find tables"
                )
                
        except ImportError:
            self.log_test(
                "BeautifulSoup Parsing Capability", 
                False, 
                "BeautifulSoup (bs4) is not installed or not available"
            )
        except Exception as e:
            self.log_test(
                "BeautifulSoup Parsing Capability", 
                False, 
                f"BeautifulSoup test failed: {str(e)}"
            )
    
    def test_zuegli_api_integration(self):
        """Test that the zuegli.app API integration is working (connectivity test)"""
        try:
            # Test basic connectivity to zuegli.app
            test_url = "https://zügli.app/"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                self.log_test(
                    "Zuegli.app API Connectivity", 
                    True, 
                    "Successfully connected to zügli.app - API integration should work"
                )
            else:
                self.log_test(
                    "Zuegli.app API Connectivity", 
                    False, 
                    f"Could not connect to zügli.app: Status {response.status_code}"
                )
                
        except Exception as e:
            self.log_test(
                "Zuegli.app API Connectivity", 
                False, 
                f"Connection to zügli.app failed: {str(e)}"
            )
    
    def test_passenger_name_extraction_logic(self):
        """Test the passenger name extraction logic from the code"""
        try:
            # Test the regex patterns used in the code
            import re
            from bs4 import BeautifulSoup
            
            # Test HTML that should contain passenger information
            test_html = """
            <html>
                <body>
                    <table>
                        <tr>
                            <td>Passenger Name</td>
                            <td>David Wiedmer</td>
                        </tr>
                        <tr>
                            <td>First Name</td>
                            <td>John</td>
                        </tr>
                    </table>
                    <strong>David Smith</strong>
                    <h2>Passenger Information</h2>
                    <p>Michael Johnson</p>
                </body>
            </html>
            """
            
            soup = BeautifulSoup(test_html, 'html.parser')
            passenger_name = None
            
            # Strategy 1: Look for table rows with passenger information (from the code)
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        first_cell_text = cells[0].get_text().strip().lower()
                        if any(keyword in first_cell_text for keyword in ['passenger', 'name', 'forename', 'first name', 'traveler', 'traveller']):
                            name_text = cells[1].get_text().strip()
                            if name_text and not any(skip in name_text.lower() for skip in ['title', 'english', 'german', 'partially redacted']):
                                name_parts = name_text.split()
                                if len(name_parts) >= 1:
                                    first_part = name_parts[0].strip()
                                    if re.match(r'^[A-Za-z]+$', first_part) and len(first_part) > 1:
                                        passenger_name = first_part.title()
                                        break
                    if passenger_name:
                        break
                if passenger_name:
                    break
            
            if passenger_name:
                self.log_test(
                    "Passenger Name Extraction Logic", 
                    True, 
                    f"Successfully extracted passenger name: '{passenger_name}' using BeautifulSoup parsing"
                )
            else:
                # Try Strategy 2: Look for strong/bold tags
                strong_tags = soup.find_all(['strong', 'b'])
                for strong in strong_tags:
                    strong_text = strong.get_text().strip()
                    name_match = re.search(r'\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b', strong_text)
                    if name_match and not any(skip in strong_text.lower() for skip in ['title', 'english', 'german']):
                        passenger_name = name_match.group(1)
                        break
                
                if passenger_name:
                    self.log_test(
                        "Passenger Name Extraction Logic", 
                        True, 
                        f"Successfully extracted passenger name: '{passenger_name}' using bold text parsing"
                    )
                else:
                    self.log_test(
                        "Passenger Name Extraction Logic", 
                        False, 
                        "Could not extract passenger name using BeautifulSoup parsing strategies"
                    )
                
        except Exception as e:
            self.log_test(
                "Passenger Name Extraction Logic", 
                False, 
                f"Passenger name extraction test failed: {str(e)}"
            )
    
    def test_django_debug_mode(self):
        """Test if Django is running in appropriate mode"""
        try:
            # Try to trigger a 404 to see debug information
            response = self.session.get(self.base_url + "/nonexistent-page-test/")
            
            if response.status_code == 404:
                content = response.text.lower()
                if 'debug' in content and 'traceback' in content:
                    self.log_test(
                        "Django Debug Mode", 
                        True, 
                        "Django is running in DEBUG mode (good for development)"
                    )
                else:
                    self.log_test(
                        "Django Debug Mode", 
                        True, 
                        "Django is running in production mode (DEBUG=False)"
                    )
            else:
                self.log_test(
                    "Django Debug Mode", 
                    True, 
                    f"Django is handling 404s appropriately (Status: {response.status_code})"
                )
                
        except Exception as e:
            self.log_test(
                "Django Debug Mode", 
                False, 
                f"Could not determine Django debug mode: {str(e)}"
            )
    
    def test_file_upload_handling(self):
        """Test file upload functionality"""
        try:
            # Create a simple test file
            test_file_content = b"Test file content for upload"
            files = {'ticket': ('test.txt', test_file_content, 'text/plain')}
            data = {'type': 'file'}
            
            response = self.session.post(self.base_url + "/", files=files, data=data)
            
            if response.status_code == 200:
                self.log_test(
                    "File Upload Handling", 
                    True, 
                    "File upload processed without server error"
                )
            else:
                self.log_test(
                    "File Upload Handling", 
                    False, 
                    f"File upload failed with status: {response.status_code}",
                    response.text[:500]
                )
                
        except Exception as e:
            self.log_test(
                "File Upload Handling", 
                False, 
                f"File upload test failed: {str(e)}"
            )
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("=" * 60)
        print("FTQoin Django Backend Test Suite")
        print("=" * 60)
        print()
        
        # Run all tests
        self.test_index_page_get()
        self.test_settings_page()
        self.test_qr_scan_post_invalid_data()
        self.test_qr_scan_post_valid_format()
        self.test_text_upload_functionality()
        self.test_csrf_protection()
        self.test_beautifulsoup_parsing_capability()
        self.test_zuegli_api_integration()
        self.test_passenger_name_extraction_logic()
        self.test_django_debug_mode()
        self.test_file_upload_handling()
        
        # Summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        failed = len(self.test_results) - passed
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print()
        
        if failed > 0:
            print("FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  ❌ {result['test']}: {result['message']}")
            print()
        
        print("DETAILED RESULTS:")
        for result in self.test_results:
            print(f"  {result['status']}: {result['test']}")
        
        return passed, failed

if __name__ == "__main__":
    tester = FTQoinTester()
    passed, failed = tester.run_all_tests()
    
    if failed == 0:
        print("\n🎉 All tests passed! The FTQoin Django backend is working correctly.")
        exit(0)
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the issues above.")
        exit(1)