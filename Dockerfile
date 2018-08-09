FROM jockdarock/cosa_base:master

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py cell_data.py gps_data.py wifi_data.py active_int.py ./

CMD python app.py