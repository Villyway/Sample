import requests
# import xmltodict
# import json
# import html


class SOAPApi():

    def __init__(self):

        self.url = "https://dhlindiaplugin.com/DHLWCFService_V6/DHLService.svc"
        self.soap_action = "http://tempuri.org/IDHLService/PostTracking_AllCheckpoint"
        self.headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": self.soap_action
        }
        self.body = """<?xml version="1.0" encoding="utf-8"?>
            <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                <Body>
                    <PostTracking_AllCheckpoint xmlns="http://tempuri.org/">
                        <awbnumber>1604633435</awbnumber>
                    </PostTracking_AllCheckpoint>
                </Body>
            </Envelope>
            """


    def call(self):
        response = requests.post(self.url, headers=self.headers, data=self.body)
        return response
        # if response.status_code == 200:

        #     # Extracting the nested XML string
        #     nested_xml_str = xmltodict.parse(response.content.decode())['s:Envelope']['s:Body'][
        #         'PostTracking_AllCheckpointResponse']['PostTracking_AllCheckpointResult']

        #     # Decoding the HTML entities in the nested XML string
        #     nested_xml_str = html.unescape(nested_xml_str)

        #     # Converting the nested XML string to a dictionary
        #     nested_xml_dict = xmltodict.parse(nested_xml_str)

        #     # Extracting the shipment events
        #     shipment_events = nested_xml_dict.get(
        #         'AWBInfo', {}).get('ShipmentEvent', [])

        #     # Formatting the shipment events
        #     formatted_events = []
        #     for event in shipment_events:
        #         formatted_event = {
        #             "Date": event.get("Date", ""),
        #             "Time": event.get("Time", ""),
        #             "Event": event.get("Description", ""),
        #             "Location": event.get("ServiceAreaDescription", "")
        #         }
        #         formatted_events.append(formatted_event)

        #     # Converting the formatted events to JSON
        #     formatted_events_json = json.dumps(formatted_events, indent=4)

        #     return formatted_events_json
        # else:
        #     return response






