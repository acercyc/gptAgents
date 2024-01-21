import json

class Interface:
    def __init__(self):
        self.objects = {}  # A dictionary to store objects

    def add_object(self, name, obj):
        self.objects[name] = obj

    def handle_action(self, action_json):
        
        

        action = json.loads(action_json)  # Parse the JSON action
        object_name = action['action']  # Get the object name from the action
        method_name = action['method']  # Get the method name from the action
        params = action.get('params', {})  # Get the parameters from the action, default to empty dict

        obj = self.objects.get(object_name)  # Get the object from the dictionary
        if not obj:
            return json.dumps({'error': f'Object {object_name} not found'})

        method = getattr(obj, method_name, None)  # Get the method from the object
        if not method:
            return json.dumps({'error': f'Method {method_name} not found on object {object_name}'})

        result = method(**params)  # Call the method with the parameters
        return json.dumps({'result': result})  # Return the result as JSON