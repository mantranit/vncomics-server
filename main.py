import falcon
import json

class TestResource(object):
    def on_get(self, req, res):
        """Handles all GET requests."""
        res.status = falcon.HTTP_200  # This is the default status
        res.body = json.dumps({ 'foo': 'bar' })

# Create the Falcon application object
app = falcon.API()

# Instantiate the TestResource class
test_resource = TestResource()

# Add a route to serve the resource
app.add_route('/', test_resource)