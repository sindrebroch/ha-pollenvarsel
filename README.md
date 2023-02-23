# Pollenvarsel for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/ha-pollenvarsel?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sindrebroch)

HomeAssistant-integration for Pollenvarsel

**PS: The API used by this integration seems to have changed, and might even have been removed. Because of this, the integration is not currently working.**

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "Pollenvarsel"-integration.
4. Restart Home Assistant.
5. Configure the `Pollenvarsel` integration.

### MANUAL INSTALLATION

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/ha-pollenvarsel/releases/latest).
2. Unpack the release and copy the `custom_components/ha-pollenvarsel` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Configure the `Pollenvarsel`-integration.

## Todo
- [ ] Customize polling
- [ ] Cleanup sensor naming

## Features
### Sensor (current and forecast)
- Bjørk
- Burot
- Gress
- Hassel
- Or
- Salix 

### Possible areas
- Finnmark
- Hordaland
- Indre Østland
- Møre og Romsdal
- Nordland
- Rogaland
- Sentrale fjellstrøk i Sør-Norge
- Sogn og Fjordane
- Sørlandet
- Troms
- Trøndelag
- Østlandet med Oslo
