# Places 
Search for places of interest near a given location and query. Save, view and delete favorite places

## Get places near given location and query

**Request**:

`GET` `/api/v1/places/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
lat   | integer | Yes      | The latitude to search places.
lng   | integer | Yes      | The longitude to search places.
query | string | No       | The name of the place to look for
order  | string | No       | The order to return the places

*Note:*

- Not Authorization Protected
- if you do not put a query to search, it will return the places near you
- The order parameter could be `prominence` (to get places with rating order) or `distance` (to get nearby places order)

**Response**:
``` bash
curl "http://localhost:8000/api/v1/places/?lat=19.4126782&lng=-99.1210366&query=pizza"
```


```json
Content-Type application/json
200 Ok

{
    "count": 20,
    "next": "http://localhost:8000/api/v1/places/?lat=19.4126782&lng=-99.1210366&page=2&query=pizza",
    "previous": null,
    "results": [
        {
            "place_id": "ChIJKZPady350YUROGBNDIZTUPk",
            "name": "Pizza del Perro Negro",
            "geo_location": {
                "lat": 19.436258,
                "lng": -99.1352421
            },
            "vicinity": "Donceles 64, Centro Histórico, Centro, Ciudad de México",
            "rating": "4.5",
            "distance": 2.7528225483857307
        },
        {
            "place_id": "ChIJs_MpZfv-0YURJX344B-6waA",
            "name": "Pizzas Don Mishel",
            "geo_location": {
                "lat": 19.3955391,
                "lng": -99.13959799999999
            },
            "vicinity": "5 de Febrero 751, Álamos, Ciudad de México",
            "rating": "4.4",
            "distance": 2.526409148910311
        },
        {
            "place_id": "ChIJDQdD0ir_0YURbOpgGbZsYGk",
            "name": "Pizza Hut",
            "geo_location": {
                "lat": 19.432403,
                "lng": -99.147672
            },
            "vicinity": "Calle de Balderas 72, Cuauhtémoc,, Centro, 06600 Ciudad de México, CDMX, Cuauhtémoc, Ciudad de México",
            "rating": "3.7",
            "distance": 3.314381191414589
        },
        {
            "place_id": "ChIJS0OR-Rj80YURLIsW4zXpoJ8",
            "name": "Little Caesars",
            "geo_location": {
                "lat": 19.4141067,
                "lng": -99.0934164
            },
            "vicinity": "Av. 8, 119, Ignacio Zaragoza, Ciudad de México",
            "rating": "4.1",
            "distance": 2.7657115906942917
        },
        {
            "place_id": "ChIJbwGmqwH80YUR9sEES-sXNt0",
            "name": "Pizzas Piccolo",
            "geo_location": {
                "lat": 19.4308636,
                "lng": -99.0998065
            },
            "vicinity": "Av Emilio Carranza 178, Moctezuma 2da Secc, Ciudad de México",
            "rating": "4.6",
            "distance": 2.795399647939216
        },
        {
            "place_id": "ChIJa9uMJaf-0YUR4bReZgZTLhY",
            "name": "Domino's Pizza Jardín Balbuena",
            "geo_location": {
                "lat": 19.4175674,
                "lng": -99.1040196
            },
            "vicinity": "Fray Servando Teresa de Mier 921, Jardín Balbuena, Ciudad de México",
            "rating": "3.5",
            "distance": 1.7705438871710013
        },
        {
            "place_id": "ChIJowWNBRz_0YURDSDKsTfYiMc",
            "name": "Central de Pizzas",
            "geo_location": {
                "lat": 19.4022513,
                "lng": -99.1506775
            },
            "vicinity": "Dr José María Vertiz 523, Narvarte Poniente, Ciudad de México",
            "rating": "4.2",
            "distance": 3.142138119848028
        },
        {
            "place_id": "ChIJB_XAkt7-0YURPve84J7_HtM",
            "name": "PIZZAS HACIENDA LAS TRANCAS",
            "geo_location": {
                "lat": 19.410889,
                "lng": -99.1416227
            },
            "vicinity": "Calle Bolivar 390, Cuauhtemoc, Ciudad de México",
            "rating": "4.6",
            "distance": 2.066370610152261
        },
        {
            "place_id": "ChIJhfj7peX-0YURAz27S99dRp4",
            "name": "Little Caesar's",
            "geo_location": {
                "lat": 19.401174,
                "lng": -99.13652650000002
            },
            "vicinity": "Calz. de Tlalpan 436, Viaducto Piedad, Ciudad de México",
            "rating": "4",
            "distance": 1.9294652618032742
        },
        {
            "place_id": "ChIJCYIx1C780YURzwOmBcQZ1g8",
            "name": "Little Caesars Pizza",
            "geo_location": {
                "lat": 19.3969856,
                "lng": -99.0955434
            },
            "vicinity": "Avenida Té 846, Granjas México, Iztacalco",
            "rating": "3.9",
            "distance": 2.9935947304201203
        }
    ]
}
```

## Register a Favourite Place

**Request**:

`POST` `/api/v1/venues/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
place_id   | string | Yes      | The place_id given for google maps and `/api/v1/places/` url

*Note:*

- Authorization Protected

**Response**:

``` bash
curl "http://localhost:8000/api/v1/venues/" -H "Authorization: Token <Token>" -H "Content-Type: application/json"
```

```json
Content-Type application/json
200 Ok

{
    "detail": "created"
}
``` 

## Get Favourite Places

**Request**:

`GET` `/api/v1/venues/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
order  | string | No       | The order to return the places
lat   | integer | Yes (only if the order parameter if distance)      | The latitude to order by.
lng   | integer | Yes (only if the order parameter if distance)      | The longitude to order by.

*Note:*

- Authorization Protected
- The order parameter could be `rating` (to get places with rating order), `distances` (to get nearby places order) or `addition_date` (to get places with addition_date order) 

**Response**:

``` bash
curl "http://localhost:8000/api/v1/venues/?order=distance&lat=19.4126782&lng=-99.1210366" -H "Authorization: Token <Token>" -H "Content-Type: application/json"
```

```json
Content-Type application/json
200 Ok

{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "location": "SRID=4326;POINT (-99.19452667236325 19.47322788569372)",
            "name": "no se donde es esto",
            "place_id": "no_se",
            "rating": 1,
            "addition_date": "2018-11-25T09:08:03+0000",
            "id": 1
        },
        {
            "location": "SRID=4326;POINT (19.436258 -99.1352421)",
            "name": "Pizza del Perro Negro",
            "place_id": "ChIJKZPady350YUROGBNDIZTUPk",
            "rating": 4.5,
            "addition_date": "2018-11-25T09:08:03+0000",
            "id": 2
        },
        {
            "location": "SRID=4326;POINT (19.432403 -99.147672)",
            "name": "Pizza Hut",
            "place_id": "ChIJDQdD0ir_0YURbOpgGbZsYGk",
            "rating": 3.7,
            "addition_date": "2018-11-25T09:31:25+0000",
            "id": 5
        },
        {
            "location": "SRID=4326;POINT (19.3955391 -99.13959799999999)",
            "name": "Pizzas Don Mishel",
            "place_id": "ChIJs_MpZfv-0YURJX344B-6waA",
            "rating": 4.4,
            "addition_date": "2018-11-25T09:31:37+0000",
            "id": 6
        },
        {
            "location": "SRID=4326;POINT (19.4141067 -99.0934164)",
            "name": "Little Caesars",
            "place_id": "ChIJS0OR-Rj80YURLIsW4zXpoJ8",
            "rating": 4.1,
            "addition_date": "2018-11-25T09:31:52+0000",
            "id": 7
        },
        {
            "location": "SRID=4326;POINT (19.4407516 -99.0987253)",
            "name": "Santy's Pizza",
            "place_id": "ChIJZypkfv770YURH8J9dKrSlmg",
            "rating": 4.1,
            "addition_date": "2018-11-25T09:32:03+0000",
            "id": 8
        }
    ]
}
``` 

## Delete a Favourite Place

**Request**:

`POST` `/api/v1/venues/<int:id>/`

Parameters:

`No parameters`


*Note:*

- Authorization Protected

**Response**:

``` bash
curl "http://localhost:8000/api/v1/venues/1/" -H "Authorization: Token <Token>" -H "Content-Type: application/json"
```

```json
Content-Type application/json
200 Ok

{
  "detail":"deleted",
}
``` 