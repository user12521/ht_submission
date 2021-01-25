import json
import pytest
import random

from wrap_app.views import SepticPresence


# test to make sure PUT, POST, DELETE don't do anything
def test_get_septic_invalid_request(client):
    resp = client.get(
        "/septic/?address=123+main+st"
    )
    assert resp.status_code == 400


def test_get_septic_post(client):
    resp = client.post(
        "/septic/",
        {
            "address": "142 E. 32nd Ave",
            "zipcode": "10032",
        },
        content_type="application/json"
    )
    assert resp.status_code == 405


def test_get_septic_put(client):
    resp = client.put(
        "/septic/",
        {
            "address": "142 E. 32nd Ave",
            "zipcode": "10032",
        },
        content_type="application/json"
    )
    assert resp.status_code == 405


def test_get_septic_delete(client):
    resp = client.delete(
        "/septic/",
        {
            "address": "142 E. 32nd Ave",
            "zipcode": "10032",
        },
        content_type="application/json"
    )
    assert resp.status_code == 405


# test handling a response where the house has septic
def test_get_septic_true(client, mocker):
    mocker.patch('wrap_app.views.SepticPresence.get_hc_response',
                 return_value='''
        {
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
                        "sewer": "Septic",
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
        }''')

    resp = client.get(
        "/septic/?zipcode=12345&address=123+main+st"
    )
    assert resp.status_code == 200
    assert resp.json()["uses_septic"] is True


# test handling a [randomized] response where the house doesn't have septic
def test_get_septic_false(client, mocker):
    mocker.patch('wrap_app.views.SepticPresence.get_hc_response', return_value='''
        {
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
                        "sewer": "'''
                      + random.choice(
                            ('municipal', 'None', 'Storm', 'Yes')) + '''",
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
        }''')

    resp = client.get(
        "/septic/?zipcode=12345&address=123+main+st"
    )
    assert resp.status_code == 200
    assert resp.json()["uses_septic"] is False
