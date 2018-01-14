# A fake RESTful "Icons" API

This repo contains a simple Flask app (a fake icons(?) API) I once put together for a POC demonstration of running API tests triggered by CircleCI after the service itself was successfully deployed to AWS. The last step of the build would use the CircleCI API to trigger another build of a "testing"-repo, hammering the deployed service (this one) with a bunch of smoke, regression or integration tests.

The concept is still very relevant but I'm putting this stuff here for historical reference.

## Usage

Set up a virtualenv and activate it:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install requirements:
```
$ pip install -r requirements.txt
```

Run the flask development server:

```
./run.sh
```