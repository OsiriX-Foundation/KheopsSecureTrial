

module.exports = {
  get: function(institutions, secret, queries) {
    return new Promise((resolve, reject) => {
      try {
        const dictQueries = readQueries(queries)
        if (!checkQueries(dictQueries) || queries === 'null') {
          return reject({ message: 'missing queries parameters', status: 400})
        }

        const institution = institutions[dictQueries.institution_name]
        const index = getIndex(institution, dictQueries.institution_secret)
        if (institution !== undefined && checkSecrets(index, secret, dictQueries)) {
          return resolve(institution.institution_secrets[index].token)
        } else {
          return reject({ message: 'no-access', status: 400})
        }
      } catch (e) {
        return reject({ status: 500, error: e});
      }
    })
  }
}

function checkSecrets(index, secret, queries) {
  if (String(secret) === String(queries.secret) && index !== -1) {
    return true
  } else {
    return false
  }
}

function getIndex(institution, institution_secret) {
  if (institution !== undefined && institution.institution_secrets !== undefined) {
    return institution.institution_secrets.findIndex((value) => {
      return String(value.secret) === String(institution_secret)
    })
  }
  return -1
}

function checkQueries(queries) {
  if (queries['institution_secret'] === undefined ||
      queries['secret'] === undefined ||
      queries['institution_name'] === undefined ||
      queries['grant_type'] !== 'urn:x-kheops:params:oauth:grant-type:secutrial') {
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
