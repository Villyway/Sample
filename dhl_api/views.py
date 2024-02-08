import xmltodict
import json
import html

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from dhl_api.SOAPApi import SOAPApi

api = SOAPApi()

api.url = "https://dhlindiaplugin.com/DHLWCFService_V6/DHLService.svc"


class TrackAllCheckPoints(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, order_no):
        response_data = {}
        
        api.soap_action= "http://tempuri.org/IDHLService/PostTracking_AllCheckpoint"

        api.body = f"""<?xml version="1.0" encoding="utf-8"?>
                        <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                            <Body>
                                <PostTracking_AllCheckpoint xmlns="http://tempuri.org/">
                                    <awbnumber>{order_no}</awbnumber>
                                </PostTracking_AllCheckpoint>
                            </Body>
                        </Envelope>
                        """
        response = api.call()
        
        if response.status_code == 200:
            print("API call successful")

            # Extracting the nested XML string
            nested_xml_str = xmltodict.parse(response.content.decode())['s:Envelope']['s:Body'][
                'PostTracking_AllCheckpointResponse']['PostTracking_AllCheckpointResult']

            # Decoding the HTML entities in the nested XML string
            nested_xml_str = html.unescape(nested_xml_str)

            # Converting the nested XML string to a dictionary
            nested_xml_dict = xmltodict.parse(nested_xml_str)

            # Extracting the shipment events
            shipment_events = nested_xml_dict.get(
                'AWBInfo', {}).get('ShipmentEvent', [])

            # Formatting the shipment events
            formatted_events = []
            for event in shipment_events:
                formatted_event = {
                    "Date": event.get("Date", ""),
                    "Time": event.get("Time", ""),
                    "Event": event.get("Description", ""),
                    "Location": event.get("ServiceAreaDescription", "")
                }
                formatted_events.append(formatted_event)
            # print(formatted_events)
            # Converting the formatted events to JSON
            # formatted_events_json = json.dumps(formatted_events, indent=4)
            response_data['status'] = 200
            response_data['message']="success"
            response_data['data'] = formatted_events
            return Response(response_data)
        else:
            print("API call failed with status code:", response.status_code)
            print(response.text)  # Printing any error message returned by the API
            return Response(response_data)

