
import os
import json
import time
import logging
import requests
from sender import SendToServer

sender = SendToServer()

OPTIONS_FILE = "/data/options.json"
HA_URL = "http://supervisor/core/api/states"
HA_TOKEN = os.environ.get("SUPERVISOR_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

with open(OPTIONS_FILE, "r", encoding="utf-8") as f:
    options = json.load(f)

SERVER_URL = options["server_url"]
INTERVAL = options["interval"]


def get_entities():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        HA_URL,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    return response.json()


def convert_value(state, attributes):
    if state in ("unknown", "unavailable", None):
        return None

    if state == "on":
        return 1

    if state == "off":
        return 0

    try:
        return round(float(state), 3)
    except (ValueError, TypeError):
        logging.warning("Neznámá hodnota: %s", state)
        return None


def build_messages(entities):

    nodes = {}

    for entity in entities:

        attributes = entity.get("attributes", {})

        if "Node" not in attributes:
            continue

        node = attributes["Node"]

        if not node:
            continue

        if node not in nodes:
            nodes[node] = {
                "info": ["Info block"],
                "crc": "2687cd",
                "ide": attributes.get("Ide"),
                "data": [],
                "format": 1
            }

        value = convert_value(
            entity.get("state"),
            attributes
        )

        if value is None:
            continue

        try:
            idu = int(attributes["id"])
        except (ValueError, TypeError, KeyError):
            logging.warning(
                "Chybné id u entity %s",
                entity.get("entity_id")
            )
            continue

        qname = attributes.get("qname")

        if not qname:
            continue

        nodes[node]["data"].append({
            "idd": 1,
            "idu": idu,
            "qname": qname,
            "value": value
        })

    return nodes


def send_data(node, data):

    sender.SendData(
        data,
        node,
        Adr=SERVER_URL
    )

    # response = requests.post(
    #     SERVER_URL,
    #     json=data,
    #     timeout=30
    # )

    # response.raise_for_status()

    # logging.info(
    #     "Node %s: odesláno %d hodnot, HTTP %s",
    #     node,
    #     len(data["data"]),
    #     response.status_code
    # )


def main():

    if not HA_TOKEN:
        raise RuntimeError("Chybí SUPERVISOR_TOKEN")

    logging.info("HA PPM Sender spuštěn")
    logging.info("Server: %s", SERVER_URL)
    logging.info("Interval: %s sekund", INTERVAL)

    while True:

        try:
            entities = get_entities()
            logging.info("Number of entities: %d", len(entities))
            messages = build_messages(entities)

            for node, data in messages.items():

                if not data["data"]:
                    continue

                try:
                    send_data(node, data)

                except Exception:
                    logging.exception(
                        "Chyba při odesílání Node %s",
                        node
                    )

        except Exception:
            logging.exception("Chyba hlavního cyklu")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
