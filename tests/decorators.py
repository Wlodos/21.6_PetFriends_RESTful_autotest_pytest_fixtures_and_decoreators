import json


def loger(func):
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ','.join(args_repr+kwargs_repr).split(",").__str__().replace('"', '').replace('[', '').replace(']', '')

        with open("log.txt", 'a', encoding="utf8") as log:

            log.write(f"\nCalling function {func.__name__}({signature})"
                      f"\nHeaders = {self.headers}"
                      f"\nPath params = {self.path}"
                      f"\nQuery params = {self.query}"
                      f"\nRequest body = {self.request_body}")
            log.write("\n--------------------------RESPONSE---------------")
            log.write(f"\nStatus = {status}"
                      f"\nResponse body = {result}\n")

        self.headers, self.path, self.query, self.request_body = None, None, None, None

        return status, result

    return wrapper
