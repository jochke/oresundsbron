<img src="https://github.com/jochke/oresundsbron/blob/main/oresundsbron-logo.svg" alt="Öresundsbron Logo" width="200" />

# Øresundsbron Integration

This integration connects your Home Assistant instance to the Øresundsbron services, enabling real-time monitoring of bridge status, queue times, agreement data, trip details, weather conditions, and live webcam feeds.

---

## Features

### **Bridge Device**
- **Bridge Status**: Displays whether the bridge is open, closed, or under warning.
- **Queue Times**: Provides traffic queue times in minutes towards Sweden and Denmark.
- **Webcams**:
  - Pylon East live webcam.
  - Pylon West live webcam.
- **Weather Conditions**:
  - Temperature (°C).
  - Wind Speed (m/s).
  - Wind Direction (e.g., "N", "S").

### **Agreement Devices**
- **Agreement Status**: Displays the status (`active`, `inactive`, etc.) of your Øresundsbron agreements.
- **Latest Trip**:
  - Displays the date and time of the most recent trip.
  - Includes detailed attributes, such as:
    - Trip ID.
    - Price (including VAT).
    - Direction of travel.
    - Automatic License Plate Recognition (ALPR) data.
    - Contract Number.

---

## Installation

### **Step 1: Install via HACS**
1. Open the **HACS** settings in Home Assistant.
2. Add the repository: `https://github.com/jochke/oresundsbron` as a custom repository.
3. Install the **Øresundsbron Integration** from the HACS store.

### **Step 2: Set Up the Integration**
1. Navigate to **Settings > Integrations > Add Integration**.
2. Search for **Øresundsbron** and select it.
3. Enter your Øresundsbron credentials (username and password).
4. Configure update intervals in the integration options (e.g., update frequency for webcams, trips, and bridge sensors).

---

## Sensors and Devices

### **Bridge Device**
- **Bridge Status**: Indicates the current bridge status (e.g., open, warning, closed).
- **Queue Times**:
  - Towards Sweden.
  - Towards Denmark.
- **Weather Conditions**:
  - Temperature (°C).
  - Wind Speed (m/s).
  - Wind Direction (e.g., "N", "S").
- **Webcams**:
  - Pylon East Webcam.
  - Pylon West Webcam.

### **Agreement Devices**
- **Agreement Status**: Displays the current status of your agreement (e.g., `active`, `inactive`).
- **Latest Trip**:
  - State: Displays the date and time of the last trip.
  - Attributes:
    - Trip ID.
    - Price (including VAT).
    - ALPR Data (License Plate).
    - Direction of travel.
    - Contract Number.

---

## Configuration

No YAML configuration is required. The setup and configuration are handled entirely through the Home Assistant UI.

---

## Customizable Update Intervals

You can configure update intervals for the following via the integration options:
- **Latest Trip**: Default 5 minutes.
- **Bridge Sensors (status, queue times, weather)**: Default 5 minutes.
- **Webcams**: Default 30 seconds.

---

## Troubleshooting

If you encounter issues:
1. Ensure your credentials are correct.
2. Check the Home Assistant logs for error messages.
3. Verify your internet connection and the availability of the Öresundsbron API.

For further assistance, visit the [GitHub Issues Page](https://github.com/jochke/oresundsbron/issues).

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
