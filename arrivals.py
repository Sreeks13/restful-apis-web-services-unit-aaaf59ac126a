import requests


def get_arrivals(stop_id, api_url, timeout=10):
    """Fetch live bus arrivals for a bus stop."""
    try:
        response = requests.get(
            api_url,
            params={"stop_id": stop_id},
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            return []

        arrivals = data.get("arrivals", [])
        if not isinstance(arrivals, list):
            return []

        return arrivals

    except (requests.RequestException, ValueError):
        return []


def format_arrivals(arrivals):
    """Format arrival data for display."""
    if not arrivals:
        return "No upcoming bus arrivals."

    lines = []
    for bus in arrivals:
        if not isinstance(bus, dict):
            continue

        bus_number = bus.get("bus_number", "Unknown")
        arrival_minutes = bus.get("arrival_minutes")

        if arrival_minutes is None:
            lines.append(f"Bus {bus_number}: arrival time unavailable")
        else:
            lines.append(f"Bus {bus_number}: {arrival_minutes} minutes")

    return "\n".join(lines) if lines else "No upcoming bus arrivals."


def main():
    """Run the command-line application."""
    stop_id = input("Enter bus stop ID: ").strip()
    api_url = input("Enter API URL: ").strip()

    if not stop_id or not api_url:
        print("Error: Stop ID and API URL are required.")
        return

    arrivals = get_arrivals(stop_id, api_url)
    print(format_arrivals(arrivals))


if __name__ == "__main__":
    main()