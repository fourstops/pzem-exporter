<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the pzem-exporter and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** fourstops, pzem-exporter, tijmenvdbrink, email
-->


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/fourstops/pzem-exporter">
    <img src="logo/logo.png" alt="Logo" width="160" height="160">
  </a>

  <h3 align="center">PZEM-exporter</h3>

  <p align="center">
    Prometheus exporter for pzem module by Pimoroni
    <br />
    <a href="https://github.com/fourstops/pzem-exporter"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/fourstops/pzem-exporter">View Demo</a>
    ·
    <a href="https://github.com/fourstops/pzem-exporter/issues">Report Bug</a>
    ·
    <a href="https://github.com/fourstops/pzem-exporter/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Docker](#docker)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/fourstops/pzem-exporter)

### Built With

* [leandrotoledo/python-pzem](https://github.com/leandrotoledo/python-pzem)
* [Prometheus](https://prometheus.io/)
* [Grafana](https://grafana.com/)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- Python3
- To run the pzem-exporter you need to have the pzem-python library by leandrotoledo

**Note** Raspbian Lite users may first need to install git: `sudo apt install git`

### Installation
We're going to run the pzem-exporter as the user ```pi``` in the directory ```/usr/src/```. Adjust this as you wish.
 
1.Clone the pzem-exporter repository
```sh
cd
git clone https://github.com/fourstops/pzem-exporter.git
sudo cp -r pzem-exporter /usr/src/
sudo chown -R pi:pi /usr/src/pzem-exporter
```

2.Install dependencies for pzem-exporter
```sh
pip3 install -r requirements.txt
```

3.Install as a Systemd service
```sh
cd /usr/src/pzem-exporter
sudo cp contrib/pzem-exporter.service /etc/systemd/system/pzem-exporter.service
sudo chmod 644 /etc/systemd/system/pzem-exporter.service
sudo systemctl daemon-reload
```
4.Start the pzem-exporter service
```sh
sudo systemctl start pzem-exporter
```
5.Check the status of the service
```sh
sudo systemctl status pzem-exporter
```
If the service is running correctly, the output should resemble the following:

```
pi@raspberrypi:/usr/src/pzem-exporter $ sudo systemctl status pzem-exporter
● pzem-exporter.service - pzem-exporter service
   Loaded: loaded (/etc/systemd/system/pzem-exporter.service; disabled; vendor preset: enabled)
   Active: active (running) since Fri 2020-01-17 14:13:41 CET; 5s ago
 Main PID: 30373 (python)
    Tasks: 2 (limit: 4915)
   Memory: 6.0M
   CGroup: /system.slice/pzem-exporter.service
           └─30373 /usr/bin/python /usr/src/pzem-exporter/pzem-exporter.py --bind=0.0.0.0 --port=8000

Jan 17 14:13:41 wall-e systemd[1]: Started pzem-exporter service.
Jan 17 14:13:41 wall-e python[30373]: 2020-01-17 14:13:41.565 INFO     pzem-exporter.py - Expose readings from the Enviro+ sensor by Pimoroni in Prometheus format
Jan 17 14:13:41 wall-e python[30373]: Press Ctrl+C to exit!
Jan 17 14:13:41 wall-e python[30373]: 2020-01-17 14:13:41.581 INFO     Listening on http://0.0.0.0:8000
```

6.Enable at boot time
```sh
sudo systemctl enable pzem-exporter
```

<!-- USAGE EXAMPLES -->
## Usage

So now we've setup the Prometheus PZEM-exporter we can start scraping this endpoint from our Prometheus server and get a nice dashboard using Grafana.  

### Prometheus

If you haven't setup Prometheus yet have a look at the installation guide [here](https://prometheus.io/docs/prometheus/latest/installation/).

Below is a simple scraping config:

```yaml

# Sample config for Prometheus.

global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # By default, scrape targets every 15 seconds.
  # scrape_timeout is set to the global default (10s).

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
      monitor: 'external'

# Load and evaluate rules in this file every 'evaluation_interval' seconds.
rule_files:
  # - "first.rules"
  # - "second.rules"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 15s
    scrape_timeout: 15s

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
    - targets: ['localhost:9090']

  - job_name: node
    # If prometheus-node-exporter is installed, grab stats about the local
    # machine by default.
    static_configs:
    - targets: ['localhost:9100']

    # If environmentplus-exporter is installed, grab stats about the local
    # machine by default.
  - job_name: environment
    static_configs:
    - targets: ['localhost:8000']
      labels:
        group: 'environment'
        location: 'Amsterdam'
        
    - targets: ['baltimore.example.com:8001']
      labels:
        group: 'environment'
        location: 'New York'
``` 

I added two labels to the targets ```group: environment``` and ```location: SomeLocation```. The Grafana dashboard uses these labels to distinguish the various locations.

<!-- LICENSE -->
## License

Distributed under the LGPL-2.1 License. See `LICENSE` for more information.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/fourstops/pzem-exporter
[contributors-url]: https://github.com/fourstops/pzem-exporter/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/fourstops/pzem-exporter?label=Fork
[forks-url]: https://github.com/fourstops/pzem-exporter/network/members
[stars-shield]: https://img.shields.io/github/stars/fourstops/pzem-exporter
[stars-url]: https://github.com/fourstops/pzem-exporter/stargazers
[issues-shield]: https://img.shields.io/github/issues-raw/fourstops/pzem-exporter
[issues-url]: https://github.com/fourstops/pzem-exporter/issues
[license-shield]: https://img.shields.io/github/license/fourstops/pzem-exporter
[license-url]: https://github.com/fourstops/pzem-exporter/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/fourstops
[product-screenshot]: images/screenshot.png
