FROM jockdarock/cosa_base:master

COPY requirements.txt .

RUN pip install -r requirements.txt

# RUN apk del .build-deps

COPY app.py cell_data0.py cell_data1.py gps_data.py wifi_data.py version_data.py active_int.py hdm_api.py config.py package_config.ini ./

EXPOSE 8000

CMD python app.py
