var http = require("http"),
  url = require("url"),
  path = require("path"),
  yaml = require("js-yaml"),
  fs = require("fs");

var tools = require('./js/tools');
var token = require('./js/token');

main()

function main() {
  const yamlFile = readYaml();
  const institutions = yamlFile.institutions
  const secret = yamlFile.secret
  const refererhosts = yamlFile.refererhosts

  http.createServer(function(request, response) {
    var uri = url.parse(request.url).pathname
              , query =  url.parse(request.url).query
              , filename = path.join(process.cwd(), '/html'+uri);

    let refererhost = request.headers.referer !== undefined ? `${url.parse(request.headers.referer).protocol}//${url.parse(request.headers.referer).host}` : ''
    if (isPresent(refererhost, refererhosts)) {
      switch (uri) {
        case '/secutrialtoken':
          if (request.method === 'POST') {
            let body = '';
            request.on('data', chunk => {
              body += chunk.toString(); // convert Buffer to string
            });
            request.on('end', () => {
              token.get(institutions, secret, body).then((res) => {
                tools.responseJSON(response, 200, JSON.stringify({ access_token: res, token_type: 'bearer', expires_in: '3600' }));
              }).catch((err) => {
                tools.responseJSON(response, err.status, JSON.stringify({ error: 'invalid_request', error_description: err.message }));
              })
            });
          } else {
            tools.responseJSON(response, 405, JSON.stringify({ message: 'Method Not Allowed' }))
          }
          break;
        default:
          response.writeHead(404, {"Content-Type": "text/plain"});
          response.write("404 Not Found\n");
          response.end();
      }
    } else {
      tools.responseJSON(response, 400, JSON.stringify({ error: 'invalid_request', error_description: 'referer host unknown' }));
    }
  }).listen(parseInt(8080, 10));
  console.log("Server running error-free at startup, listen on port 8080\nCTRL + C to shutdown");
}

function isPresent(value, array) {
  return array.includes(value)
}

function readYaml() {
  const yamlPath = process.env.YAMLPATH !== undefined ? process.env.YAMLPATH : '.';
  const yamlName = process.env.YAMLNAME !== undefined ? process.env.YAMLNAME : 'example.yml';
  const fullpath = path !== '' ? `${yamlPath}/${yamlName}` : yamlName;

  console.log(`${fullpath} will be read`);
  const yamlReaded = yaml.safeLoad(fs.readFileSync(fullpath, 'utf8'));
  console.log(`${fullpath} was read correctly`);
  return yamlReaded
}
