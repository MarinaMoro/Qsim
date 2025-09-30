def json_operations():

    import json

    def load_json(filename):
        with open(filename, "r") as file:
            return json.load(file)

    def save_json(data, filename):
        with open(filename, "w") as file:
            json.dump(data, file)

    return load_json, save_json