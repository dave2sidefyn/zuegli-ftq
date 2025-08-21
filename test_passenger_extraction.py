#!/usr/bin/env python3
"""
Test script to verify passenger name extraction from HTML
"""

from bs4 import BeautifulSoup
import re

def test_passenger_extraction(ticket_html):
    """Test the passenger name extraction logic"""
    print(f"Testing HTML extraction on {len(ticket_html)} characters of HTML")
    
    # Parse HTML with BeautifulSoup for more reliable extraction
    soup = BeautifulSoup(ticket_html, 'html.parser')
    
    # Strategy 1: Look for table rows with passenger information
    passenger_name = None
    
    # Check for table cells containing passenger information
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                # Check if first cell contains passenger-related text
                first_cell_text = cells[0].get_text().strip().lower()
                if any(keyword in first_cell_text for keyword in ['passenger', 'name', 'forename', 'first name', 'traveler', 'traveller']):
                    name_text = cells[1].get_text().strip()
                    print(f"Found table cell - Label: '{first_cell_text}' Value: '{name_text}'")
                    
                    # Extract first name from the value
                    if name_text and not any(skip in name_text.lower() for skip in ['title', 'english', 'german', 'partially redacted']):
                        # Handle different name formats
                        name_parts = name_text.split()
                        if len(name_parts) >= 1:
                            # Check if it looks like a real name (contains letters)
                            first_part = name_parts[0].strip()
                            if re.match(r'^[A-Za-z]+$', first_part) and len(first_part) > 1:
                                passenger_name = first_part.title()
                                print(f"Extracted passenger name from table: {passenger_name}")
                                break
            if passenger_name:
                break
        if passenger_name:
            break
    
    # Strategy 2: Look for strong/bold tags containing names
    if not passenger_name:
        strong_tags = soup.find_all(['strong', 'b'])
        for strong in strong_tags:
            strong_text = strong.get_text().strip()
            # Look for name patterns in bold text
            name_match = re.search(r'\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b', strong_text)
            if name_match and not any(skip in strong_text.lower() for skip in ['title', 'english', 'german']):
                passenger_name = name_match.group(1)
                print(f"Extracted name from bold text: {passenger_name}")
                break
    
    return passenger_name

# Test cases
if __name__ == "__main__":
    # Test case 1: Table format
    test_html_1 = """
    <html>
        <body>
            <table>
                <tr>
                    <td>Passenger Name</td>
                    <td>David Wiedmer</td>
                </tr>
                <tr>
                    <td>Train</td>
                    <td>ICE 123</td>
                </tr>
            </table>
        </body>
    </html>
    """
    
    print("=== Test Case 1: Table Format ===")
    result1 = test_passenger_extraction(test_html_1)
    print(f"Result: {result1}\n")
    
    # Test case 2: Different table format
    test_html_2 = """
    <html>
        <body>
            <table>
                <tr>
                    <th>Forename</th>
                    <td>David</td>
                </tr>
                <tr>
                    <th>Surname</th>
                    <td>Wiedmer</td>
                </tr>
            </table>
        </body>
    </html>
    """
    
    print("=== Test Case 2: Forename/Surname Format ===")
    result2 = test_passenger_extraction(test_html_2)
    print(f"Result: {result2}\n")
    
    # Test case 3: Bold text format
    test_html_3 = """
    <html>
        <body>
            <h2>Passenger Information</h2>
            <p><strong>David Wiedmer</strong></p>
            <p>Train: ICE 123</p>
        </body>
    </html>
    """
    
    print("=== Test Case 3: Bold Text Format ===")
    result3 = test_passenger_extraction(test_html_3)
    print(f"Result: {result3}\n")
    
    # Test case 4: Should ignore non-name text
    test_html_4 = """
    <html>
        <body>
            <table>
                <tr>
                    <td>Title</td>
                    <td>English</td>
                </tr>
                <tr>
                    <td>Passenger</td>
                    <td>David Wiedmer</td>
                </tr>
            </table>
        </body>
    </html>
    """
    
    print("=== Test Case 4: Should Ignore Non-Names ===")
    result4 = test_passenger_extraction(test_html_4)
    print(f"Result: {result4}\n")