# AEMET climatologic dashboard using Dash Plotly
Application that uses official data from spanish weather stations from the state meteorological agency ([AEMET](https://www.aemet.es)) to build a dashboard featuring historic records for maximum and minimun temperature, temperature range and rainfall for the selected station, as well as the daily thermal anomaly for the selected year.

Watch it live at [aemet-climate-data-app.onrender.com](https://aemet-climate-data-app.onrender.com).

![app screenshot](/assets/app.png "app screenshot")

## Local run

Note that, to hide private credentials, the project requires three environment variables:
- AEMET_API_KEY - to communicate with AEMET API. Obtain one [here](https://opendata.aemet.es/centrodedescargas/inicio).
- MAPBOX_TOKEN - to build the map. Obtain one [here](https://www.mapbox.com/)
- POSTGRESQL_URL - to connect with the PostgreSQL database hosted on [render.com](https://render.com/) (contact me for more details).