import argparse
import json


defaults = {
    "china": False,
    "debug": False,
    "host": "127.0.0.1",
    "port": "5000",
    "step_limit": "10",
}


def read_config():
    """
    Reads configuration from config.json in current directory
    :return: dict
    """
    config = defaults.copy()
    try:
        saved_config = json.load(open("config.json"))
        config.update({k:v for k,v in saved_config.items() if v is not None})
    except IOError:
        pass
    config = {k: config[k] for k in config if config[k] is not None}
    return config


def write_config(config):
    """
    Save configuration to JSON file on disk
    :param config: dict
    :return: None
    """
    with open("config.json", "wb") as conf_fh:
        json.dump(config, conf_fh, sort_keys=True, indent=4)
        conf_fh.write("\n")


def flask_argparse(app):
    """
    Takes a flask.Flask instance and configures it. Parses
    command-line flags to configure the app.
    """

    config = read_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host",
                        help="Hostname of the Flask app " +
                             "[default %s]" % config["host"],
                        required="host" not in config)
    parser.add_argument("-P", "--port",
                        help="Port for the Flask app " +
                             "[default %s]" % config["port"],
                        required="port" not in config)

    parser.add_argument("-u", "--username", help="PTC Username", required="username" not in config)
    parser.add_argument("-p", "--password", help="PTC Password", required="password" not in config)
    parser.add_argument("-l", "--location", help="Location", required="location" not in config)
    parser.add_argument("-st", "--step_limit", help="Steps", required="step_limit" not in config)
    parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
    parser.add_argument("-c", "--china", help="Coord Transformer for China", action='store_true')

    app.args = parser.parse_args()
    config.update({k:v for k,v in vars(app.args).items() if v is not None})

    # put all the config back into app.args
    # so the rest of the code doesn't know anything's different

    for k, v in config.items():
        setattr(app.args, k, v)

    write_config(config)
