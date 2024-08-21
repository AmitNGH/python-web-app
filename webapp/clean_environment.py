from requests import get
from requests.exceptions import Timeout

try:
    get('http://127.0.0.1:5001/stop_server', timeout=10)
except Timeout:
    print("Frontend Timed out")

try:
    get('http://127.0.0.1:5000/stop_server', timeout=10)
except Timeout:
    print("Backend Timed out")
