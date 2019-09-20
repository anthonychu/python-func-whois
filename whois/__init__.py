import logging
import ujson
import pythonwhois

import azure.functions as func

cold_or_warm = 'cold_start'

def main(req: func.HttpRequest) -> func.HttpResponse:
    global cold_or_warm
    logging.info(cold_or_warm)

    parsed = {}
    server_list = []

    domain = req.params.get('domain')
    if domain is None:
        return func.HttpResponse(
            ujson.dumps(
                {
                  'domain': domain,
                  'server_list': [],
                  'data': None,
                  'parsed': None,
                  'error': None
                }
            ),
            status_code=400,
            headers={"Content-type": "application/json"}
        )

    error = ""
    data, server_list = pythonwhois.net.get_whois_raw(
        domain,
        with_server_list=True
    )

    d = [r.strip() for r in data]
    try:
        parsed = pythonwhois.parse.parse_raw_whois(d, normalized=True)
        del parsed["raw"]
        parsed["domain"] = domain
    except Exception as e:
        print("Got error", e, "\n for data", data)
        logging.exception("Lambda lookup error")
        error = e

    response_content = ujson.dumps(
        {
          'exec_type': cold_or_warm,
          'domain': domain,
          'server_list': server_list,
          'data': data,
          'parsed': parsed,
          'error': error
        })

    cold_or_warm = 'warm_start'

    return func.HttpResponse(response_content,
      status_code=200, headers={"Content-type": "application/json"}
    )
