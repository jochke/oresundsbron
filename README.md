# Öresundsbron Integration

This integration connects your Home Assistant instance to the Öresundsbron services, enabling real-time monitoring of bridge status, queue times, trip data, and webcam images.

## Features

- **Bridge Status**: Displays whether the bridge is open, closed, or under warning.
- **Queue Times**: Provides traffic queue times in minutes towards Sweden and Denmark.
- **Trip Data**: Retrieves the most recent trip details, including:
  - Time and date of the trip
  - Station
  - Price details
  - Direction of travel
  - Automatic License Plate Recognition (ALPR) data
- **Webcam Images**: View live webcam feeds from Pylon East and Pylon West.

## Installation

1. **Add the Integration via HACS**:
   - Open the HACS settings in Home Assistant.
   - Add the repository: `https://github.com/jochke/oresundsbron` as a custom repository.
   - Install the `Öresundsbron Integration` from the HACS store.

2. **Set Up the Integration in Home Assistant**:
   - Navigate to **Settings > Integrations > Add Integration**.
   - Search for `Öresundsbron` and select it.
   - Enter your Öresundsbron credentials (username and password).

## Sensors

### Real-Time Sensors

- **Bridge Status**: Indicates whether the bridge is open, under warning, or closed.
- **Queue Times**:
  - Queue times towards Sweden.
  - Queue times towards Denmark.

### Account Information

- **Hidden Sensors**:
  - **Customer Number**: Displays the Öresundsbron customer number associated with your account.
  - **Contracts**: The number of active contracts associated with your account.

### Trips

- **Last Trip Sensor**: Provides details of the most recent trip, including:
  - Trip ID
  - Time and date
  - Station
  - Direction
  - Price (including and excluding VAT)
  - ALPR data (license plate)

### Webcams

- **Pylon East Webcam**
- **Pylon West Webcam**

## Configuration

No YAML configuration is required. The setup is entirely handled via the Home Assistant UI.

## Troubleshooting

- Ensure your credentials are correct.
- Check the Home Assistant logs for error messages.
- If authentication fails, verify your username and password.

For additional help, visit the [GitHub Issues Page](https://github.com/jochke/oresundsbron/issues).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
