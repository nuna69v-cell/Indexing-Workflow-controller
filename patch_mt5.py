import re

with open("expert-advisors/mt5_ea/GenZTradingEA.mq5", "r") as f:
    content = f.read()

# Replace the single ServerURL with split components
replacement = """
//--- Input parameters
input string IPAddress = "127.0.0.1"; // Server IP Address
input int Port = 5555; // Server Port
input string API_KEY = "JULES_API_KEY_HERE"; // Jules API Key for authentication
string ServerURL = "http://" + IPAddress + ":" + IntegerToString(Port); // Dynamically constructed URL
input string EAName = "GenZ_Scalping_Bot_MT5"; // EA identification name
"""

content = re.sub(
    r'//--- Input parameters\ninput string ServerURL = "http://localhost:3000"; // Server URL\ninput string EAName = "GenZ_Scalping_Bot_MT5"; // EA identification name',
    replacement,
    content,
)

# Update the header construction to use the API key
header_replacement = """
    string headers = "Content-Type: application/json\\r\\nAuthorization: Bearer " + API_KEY;
"""

# Replace empty or basic headers with authenticated headers
content = content.replace(
    'string headers = "Content-Type: application/json\\r\\n";', header_replacement
)

with open("expert-advisors/mt5_ea/GenZTradingEA.mq5", "w") as f:
    f.write(content)

print("MT5 EA patched.")
