# wallet
Simple wallet poc

## Usage

Start service:
```uwsgi --ini app.ini```

Use client to send money, check balance or view transactions history:

```python3 client.py --help```

```python3 client.py --balance```

```python3 client.py --history```

Send money to wallet id 8c82c0e8-9d65-4332-b481-803a8f654bf2:

```python3 client.py --send 100.55 --recipient 8c82c0e8-9d65-4332-b481-803a8f654bf2```

Requires Python3 and PostgreSQL:
