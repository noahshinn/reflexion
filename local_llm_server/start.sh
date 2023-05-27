
#!/bin/bash

source env/bin/activate
uvicorn app:app --reload --port 8081
