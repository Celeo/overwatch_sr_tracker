# Overwatch SR Tracker

TODO

## Setting up

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.example.json config.json
```

Populate the config file.

## Running

### Collector

```sh
python collect.py
```

### Web server

**Debug**:

```sh
python server.py
```

**Production**:

```sh
./run_server.sh
```
