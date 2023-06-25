
#!/bin/bash

source env/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8081
