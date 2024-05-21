import requests
import pytest

# Endpoint URL
URL = "https://playground.learnqa.ru/ajax/api/user_agent_check"

# Test data
user_agents = [
    (
        'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}
    ),
    (
        'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}
    ),
    (
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}
    ),
    (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
    ),
    (
        'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
    )
]

@pytest.mark.parametrize("user_agent, expected", user_agents)
def test_user_agent(user_agent, expected):
    response = requests.get(URL, headers={"User-Agent": user_agent})
    data = response.json()

    actual_platform = data.get("platform", "Unknown")
    actual_browser = data.get("browser", "Unknown")
    actual_device = data.get("device", "Unknown")

    # Display all 3 fields and their values
    print(f"User-Agent: {user_agent}")
    print(f"Actual platform: {actual_platform}, Expected platform: {expected['platform']}")
    print(f"Actual browser: {actual_browser}, Expected browser: {expected['browser']}")
    print(f"Actual device: {actual_device}, Expected device: {expected['device']}")

    # Check for incorrectly defined parameters
    incorrect_params = []
    if actual_platform != expected['platform']:
        incorrect_params.append(f"platform (Actual: {actual_platform}, Expected: {expected['platform']})")
    if actual_browser != expected['browser']:
        incorrect_params.append(f"browser (Actual: {actual_browser}, Expected: {expected['browser']})")
    if actual_device != expected['device']:
        incorrect_params.append(f"device (Actual: {actual_device}, Expected: {expected['device']})")

    if incorrect_params:
        print(f"Incorrect parameters for User-Agent: {user_agent}")
        for param in incorrect_params:
            print(param)

    # Fail the test if any parameter is incorrect
    assert not incorrect_params, f"Incorrect parameters found for User-Agent: {user_agent}"

