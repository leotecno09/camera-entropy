# camera-entropy

A Flask-based randomness server that generates entropy by periodically capturing frames from 
RTSP camera streams, hashing them, combining them with `os.urandom()` and using the result to seed random value generation

Try it yourself [here](https://random.leotecno.myaddr.io)

## API Documentation
All APIs return data in JSON format with a `success` field indicating the request completed correctly:
- `success: true` - the request was processed successfully. The response will include the relevant data fields (e.g. `value`)
- `success: false` - something went wrong (invalid parameters, seed not ready, etc...). The response will include an `error` field with the error 
---
### Random APIs

### Get a random integer

> **GET** `/api/random/int`

Returns a random integer between `max` and `min`

#### Query parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `min` | integer | No | Minimum value (inclusive). Default: 0 |
| `max` | integer | No | Maximum value (inclusive). Default: 0|

#### Example request
```http
GET /api/random/int?min=10&max=50
```

#### Example response
```json
{
  "success": true,
  "value¨: 43
}
```

---

### Get a random float

> **GET** `/api/random/float`

Returns a random float between `max` and `min`

#### Query parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `min` | float | No | Minimum value (inclusive). Default: 0. |
| `max` | float | No | Maximum value (inclusive). Default: 0. |

#### Example request
```http
GET /api/random/float?min=10.4&max=50.51
```

#### Example response
```json
{
  "success": true,
  "value¨: 21.745496281325718
}
```

---

### Random choice

> **GET** `/api/random/choice`

Returns a randomly selected value from a list of provided options

#### Query parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `option` | string | Yes | One of the possibile values to choose from. Can be provided multiple times |

#### Example request
```http
GET /api/random/choice?option=apple&option=banana&option=orange
```

#### Example response
```json
{
  "success": true,
  "value¨: "banana"
}
```

---

### Token APIs

### Get a random UUID

> **GET** `/api/token/uuid`

Returns a randomly generated UUIDv4

#### Example request
```http
GET /api/token/uuid
```

#### Example response
```json
{
  "success": true,
  "value¨: "27baf1ed-75f2-47e1-bb2b-f68eb4f40b2b"
}
```

---

### Get a random string

> **GET** `/api/token/string`

Returns a randomly generated string

#### Query parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `length` | int | No | The length of the string to be generated. Default is 16. Maximum is 256 |
| `charset`| string | No | The charset to use to generate the string. Default is **alphanumeric**. Possible values: **alphanumeric**, **alpha**, **digits** and **hex**

#### Example request
```http
GET /api/token/string?length=32&charset=alpha
```

#### Example response
```json
{
  "charset": "alpha",
  "length": 32,
  "success": true,
  "value": "WGSYfJOGPMTSimcPzxOoHzFBxjiRXZwD"
}
```