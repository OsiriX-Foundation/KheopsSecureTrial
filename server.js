var http = require("http"),
  url = require("url"),
  path = require("path"),
  yaml = require("js-yaml"),
  fs = require("fs");

var tools = require('./js/tools');
var token = require('./js/token');

main()

function main() {
  const institutions = getInstitutions();

  http.createServer(function(request, response) {
    var uri = url.parse(request.url).pathname
              , query =  url.parse(request.url).query
              , filename = path.join(process.cwd(), '/html'+uri);

    switch (uri) {
      case '/secrettoken':
        if (request.method === 'POST') {
          let body = '';
          request.on('data', chunk => {
            body += chunk.toString(); // convert Buffer to string
          });
          request.on('end', () => {
            token.get(institutions, body).then((res) => {
              tools.responseJSON(response, 200, JSON.stringify({ token: res }));
            }).catch((err) => {
              tools.responseJSON(response, err.status, JSON.stringify({ message: err.message }));
            })
          });
        } else {
          tools.responseJSON(response, 405, JSON.stringify({ message: 'Method Not Allowed' }))
        }
        break;
      default:
        tools.readFileWeb(filename, response);
    }
  }).listen(parseInt(8080, 10));
  console.log("Server running error-free at startup, listen on port 8080\nCTRL + C to shutdown");
}

function getInstitutions() {
  const yamlPath = process.env.YAMLPATH !== undefined ? process.env.YAMLPATH : '.';
  const yamlName = process.env.YAMLNAME !== undefined ? process.env.YAMLNAME : 'example.yml';
  const fullpath = path !== '' ? `${yamlPath}/${yamlName}` : yamlName;

  console.log(`${fullpath} will be read`);
  const yamlReaded = yaml.safeLoad(fs.readFileSync(fullpath, 'utf8'));
  console.log(`${fullpath} was read correctly`);
  return yamlReaded.institutions
}
