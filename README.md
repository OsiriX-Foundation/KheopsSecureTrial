# KheopsSecureTrial

Server listen on port **8080**

The server will read the yaml file at startup and keep it in memory.

Steps of the server:

* Check if refererhost is present in the array **refererhosts**.
* **/secutrialtoken**, only **POST** method is allowed.
* Will read the formdata parameters (application/x-www-form-urlencoded):
    * **secret**
    * **institution_secret**
    * **institution_name**
    * **grant_type** must be urn:x-kheops:params:oauth:grant-type:secutrial
* return **access_token** if all formdata parameters is correct.

Check the example yaml below.

## Project setup
```
npm install
```

### Run project
```
npm start
```

### Test project
```
npm test
```

The test is based on the file example.yml, present in the root.

# Docker

## Environment variables

`YAMLNAME` - Yaml configuration file name. **Must be present**

`YAMLPATH` - Path to access to Yaml file (/run/secrets). If not specify, the server will use the workdir (/usr/src/app) in the container.

# YAML File

Respect the structure of the example.

## Example

```
secret: 12345
institutions:
  paris:
    institution_secrets:
      - secret: 123456
        token: 123456
      - secret: 654321
        token: 123456
  geneve:
    institution_secrets:
      - secret: 123456
        token: 123456
      - secret: 654321
        token: 123456

refererhosts:
  - 'https://test.kheops.online'
```
