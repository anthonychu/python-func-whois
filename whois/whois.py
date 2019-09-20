# import logging
# import ujson
# import pythonwhois

# import azure.functions as func


# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     parsed = {}
#     server_list = []

#     domain = req.params.get('domain')
#     if domain is None:
#         return func.HttpResponse(
#             ujson.dumps(
#                 {
#                   'domain': domain,
#                   'server_list': [],
#                   'data': None,
#                   'parsed': None,
#                   'error': None
#                 }
#             ),
#             status_code=400,
#             headers={"Content-type": "application/json"}
#         )

#     error = ""
#     data, server_list = pythonwhois.net.get_whois_raw(
#         domain,
#         with_server_list=True
#     )

#     d = [r.strip() for r in data]
#     try:
#         parsed = pythonwhois.parse.parse_raw_whois(d, normalized=True)
#         del parsed["raw"]
#         parsed["domain"] = domain
#     except Exception as e:
#         print("Got error", e, "\n for data", data)
#         logging.exception("Lambda lookup error")
#         error = e

#     return func.HttpResponse(
#       ujson.dumps(
#         {
#           'domain': domain,
#           'server_list': server_list,
#           'data': data,
#           'parsed': parsed,
#           'error': error
#         }
#       ),
#       status_code=200, headers={"Content-type": "application/json"}
#     )
