# kia-prometheus

A Prometheus exporter which uses the [hyundai_kia_connect_api](https://github.com/Hyundai-Kia-Connect/hyundai_kia_connect_api) Python library to scrape metrics for Kia, Hyundai, and Genesis cars. A [Docker Compose](https://docs.docker.com/compose/) stack is provided consisting of the exporter and Prometheus.

## Configuration

The following variables can be used to configure the exporter using any method [supported](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#ways-to-set-variables-with-interpolation) by Docker Compose. `API_USERNAME` and `API_PASSWORD` are required. `API_PIN` is needed if the account has been configured to use a PIN.

| Name                 | Default | Description                                    |
|----------------------|---------|------------------------------------------------|
| API_BRAND            | 1       | 1=Kia, 2=Hyundai, 3=Genesis                    |
| API_PASSWORD         |         |                                                |
| API_PIN              |         | Leave blank if account doesn't use a PIN       |
| API_POLLING_INTERVAL | 900     |                                                |
| API_REGION           | 3       | 1=Europe, 2=Canada, 3=US, 4=China, 5=Australia |
| API_USERNAME         |         |                                                |

## Building

A container image for the exporter can be built using `docker compose build`.

## Running

After building the image, the Compose stack can be brought up using `docker compose up` or `docker compose up -d` to run in the background.