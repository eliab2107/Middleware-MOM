from callback import Callback
Callback(lambda msg: print("Processando mensagem no main:", msg)).execute()