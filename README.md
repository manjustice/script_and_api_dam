## Installation

Docker must be already installed

```shell
git clone https://github.com/manjustice/geo_data_api.git
cd geo_data_api
docker run -p 8000:8000 -t $(docker build -q .)
```

## Endpoint

http://127.0.0.1:8000/api/rdn-closure?date=<YOUR_DATE>

Date parameter can be in the following formats: "DD.MM.YYYY", "DD-MM-YYYY", "YYYY.MM.DD", "YYYY-MM-DD"
