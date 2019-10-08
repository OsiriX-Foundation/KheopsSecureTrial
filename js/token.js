

module.exports = {
  get: function(institutions, queries) {
    return new Promise((resolve, reject) => {
      try {
        const dictQueries = readQueries(queries)
        if (!checkQueries(dictQueries) || queries === 'null') {
          return reject({ message: 'missing queries parameters', status: 400})
        }

        const institution = institutions[dictQueries.institution_name]
        if (institution !== undefined && checkSecrets(institution, dictQueries)) {
          return resolve(institution.token)
        } else {
          return reject({ message: 'no-access', status: 401})
        }
      } catch (e) {
        return reject({ status: 500, error: e});
      }
    })
  }
}

function checkSecrets(institution, queries) {
  if (String(institution.institution_secret) === String(queries.institution_secret)
    && String(institution.secret) === String(queries.secret)) {
    return true
  } else {
    return false
  }
}

function checkQueries(queries) {
  if (queries['institution_secret'] === undefined ||
      queries['secret'] === undefined ||
      queries['institution_name'] === undefined) {
    return false
  }
  return true
}

function readQueries(queries) {
  try {
    const pairs = queries.split('&');
    let result = {};
    pairs.forEach((pair) => {
      let pairsplit = pair.split('=');
      result[pairsplit[0]] = decodeURIComponent(pairsplit[1]);
    })
    return result
  } catch (e) {
    return e;
  }
}
