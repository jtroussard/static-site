# This class creates a tool that process the data from data.json so that it can fit in the control mechs of the jinja template


class Processor:
    def __init__(self, bank):
        self.bank = bank

    def process_portfolio_types(self, data):
        port_data = data["sections"]["portfolios"]
        processed = []
        for port_type, port_payload in port_data:
            processed.append(
                {
                    "name": port_data[port_type]["name"],
                    "fa_code": f"{port_data[port_type]['fa-style-prefix']}{port_data[port_type]['fa-name']}",
                    "href": port_data[port_type]["href"],
                }
            )
        return processed

    def process_portfolio_projects(self, data):
        port_data = data["sections"]["portfolios"]
        processed = []

        for port_type, port_payload in port_data:
            port_type = port_data[port_type]["href"]
            processed.append(
                {
                    "name": port_data[port_type]["name"],
                    "fa_code": f"{port_data[port_type]['fa-style-prefix']}{port_data[port_type]['fa-name']}",
                    "href": port_data[port_type]["href"],
                }
            )
