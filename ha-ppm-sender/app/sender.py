
import json
import hashlib
import requests
import logging


class SendToServer:

    def Float(self, data):
        if float(data) == int(float(data)):
            return int(float(data))
        return float(data)

    def CrcData(self, data):

        crc = hashlib.md5()

        text = str(data["ide"]) + "#"
        aux = 0

        for item in data["data"]:
            aux += self.Float(item["value"]) + int(item["idd"])

        aux = round(aux, 10)
        aux = self.Float(aux)

        text += str(aux)

        crc.update(text.encode("utf-8"))

        result = crc.hexdigest()[:6]

        logging.debug("CRC input: %s", text)
        logging.debug("CRC result: %s", result)

        return result

    def SendData(self, data, name="logger", Adr=None):

        data["crc"] = self.CrcData(data)

        headers = {
            "Content-Type": "application/json"
        }

        json_data = json.dumps(data).encode("utf-8")

        logging.debug("Sending data: %s", json_data.decode("utf-8"))

        response = requests.post(
            Adr,
            data=json_data,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        result = response.text

        logging.info(
            "Node %s: HTTP %s, response: %s",
            name,
            response.status_code,
            result
        )

        return result
