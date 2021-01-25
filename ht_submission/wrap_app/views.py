import os
import requests
import json
import random

from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .serializers import SepticSerializer

HC_API_KEY = os.environ.get('HC_API_KEY', None)


class SepticPresence(APIView):
    def get(self, request):
        serializer = SepticSerializer(data=request.GET)

        if serializer.is_valid():
            hc_response = self.get_hc_response(serializer.validated_data)
            hc_data = json.loads(hc_response)

            sewer = hc_data['property/details']['result']['property']['sewer']
            if sewer == 'Septic':
                serializer.validated_data['uses_septic'] = True
            else:
                serializer.validated_data['uses_septic'] = False

            return JsonResponse(serializer.validated_data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # broke this function out to make it easier to mock results in my tests
    def get_hc_response(self, params):
        session = requests.Session()
        session.params = params
        session.params['api_key'] = HC_API_KEY
        path = "https://api.housecanary.com/v2/property/details" \
            f"?address={params.get('address')}" \
            f"&zipcode={params.get('zipcode')}"
        #return session.get(path)
        # to test this out "working" in the browser, comment out the above line
        # its set to randomly return septic types so refresh a few times to
        # see both true/false responses in that field
        fake_resp = '''{
            "property/details": {
                "api_code_description": "ok",
                "api_code": 0,
                "result": {
                    "property": {
                        "air_conditioning": "yes",
                        "attic": false,
                        "basement": "full_basement",
                        "building_area_sq_ft": 1824,
                        "building_condition_score": 5,
                        "building_quality_score": 3,
                        "construction_type": "Wood",
                        "exterior_walls": "wood_siding",
                        "fireplace": false,
                        "full_bath_count": 2,
                        "garage_parking_of_cars": 1,
                        "garage_type_parking": "underground_basement",
                        "heating": "forced_air_unit",
                        "heating_fuel_type": "gas",
                        "no_of_buildings": 1,
                        "no_of_stories": 2,
                        "number_of_bedrooms": 4,
                        "number_of_units": 1,
                        "partial_bath_count": 1,
                        "pool": true,
                        "property_type": "Single Family Residential",
                        "roof_cover": "Asphalt",
                        "roof_type": "Wood truss",
                        "site_area_acres": 0.119,
                        "style": "colonial",
                        "total_bath_count": 2.5,
                        "total_number_of_rooms": 7,
                        "sewer": "''' \
                        + random.choice(
                        ('municipal', 'None', 'Storm', 'Septic', 'Yes')) +'''",
                        "subdivision" : "CITY LAND ASSOCIATION",
                        "water": "municipal",
                        "year_built": 1957,
                        "zoning": "RH1"
                    },

                    "assessment":{
                        "apn": "0000 -1111",
                        "assessment_year": 2015,
                        "tax_year": 2015,
                        "total_assessed_value": 1300000.0,
                        "tax_amount": 15199.86
                    }
                }
            }
        }'''
        return fake_resp
