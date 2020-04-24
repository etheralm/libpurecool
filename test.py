from libpurecool.dyson import DysonAccount

USER = "<user>"
PASS = "<pass>"
LANG = "GB"

dyson_account = DysonAccount(USER, PASS, LANG)
logged = dyson_account.login()

devices = dyson_account.devices()
connected = devices[0].auto_connect()