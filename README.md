# KheopsSecureTrial

Server listen on port **8080**

The server will read the yaml file at startup and keep it in memory.

## Project setup
```
npm install
```

### Run project
```
npm start
```

# Docker

## Environment variables

`YAMLNAME` - Yaml configuration file name. **Must be present**

`YAMLPATH` - Path to access to Yaml file (/run/secrets). If not specify, the server will use the workdir (/usr/src/app) in the container.

# YAML File

## Example

```
institutions:
  paris:
    secret: 12345
    institution_secret: 123456
    token: 1234567
  geneve:
    secret: 12345
    institution_secret: 123456
    token: 1234567
```
