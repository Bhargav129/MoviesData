# MoviesData
# This project is implemented by using fastapi framework and mongodb atlas database

# Project Environment Setup
python3 -m venv <environment_name>

# Install Dependencies
Install all requirements by using below command

pip install -r requirements.txt

# Run Server Command
fastapi dev app.py

# Swagger UI

http://127.0.0.1:8000/docs


**APIS:**
# Below api is used to upload file
{url}/uploadfile/
**CURL:**
curl --location 'http://localhost:8000/uploadfile/' \
--form 'file=@"<Path>/movies_data_assignment.csv"'

# Below API is retriew data based on prefernces
**CURL**
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/crm/data?start_index=1&count=10&release_year=2015&sort_by=rating&language=English' \
  -H 'accept: application/json'

  Query params all are optional for pagination it takes start_index as 1 and count 10
