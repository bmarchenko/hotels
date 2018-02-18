# Hotel Reservations
This is a project that implements a service that exposes APIs for creation, modification, and retrieval of hotel reservation data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation
1. install system packages: [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) and [postgres](https://www.postgresql.org/download/)
2. create virtualenv  ```$ virtualenv env```
3. activate virtualenv ```$ source env/bin/activate```
4. ```$ pip install -r requirements.txt```
5. copy ```hotels/settings_local_example.py``` to ```hotels/settings_local.py``` and modify according to your setup
6. ```$ python manage.py migrate```

## Running the tests
Tests cover creation, modification of reservations via the API. Also they check for number of request limit.
```$ python manage.py test```

## Access via browser
Run ```$ python manage.py runserver``` and visit [http://localhost:8000/api/v1/reservations/](http://localhost:8000/api/v1/reservations/)

## Explanation of business logic
### State field
* This field is not required and works automatically depending on arrival and departure dates, unless set explicitly. For these purposes it uses two "hidden" fields: ```_status``` and ```_state_modified```
  * If departure date is in the past, it means that guest had left, the status is "checked out"
  * If arrival date is in the future, it means that it is future reservation, the status is "in the future"
  * Otherwise, guest is in-house

### Data store choice:
* PostgreSQL was chosen because of a number of reasons:
 * it is well integrated with Django. e.g. filtering by daterange is as easy as ```Reservation.objects.filter(arrival_date__range=["2018-01-01", "2018-01-31"])```
 * it has a number of specific features that are suitable to this usecase. e.g. ```DateRangeField```
 * it has quite a good performance and can handle enough amount of data

### Features to be implemented
* Hotels model
* DateRangeField for arrival/departure dates
* Better deployment system e.g. Docker
