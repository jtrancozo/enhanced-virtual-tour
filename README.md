# proof-of-concept

This is the code used in the paper "A Proof of Concept on Enhancing Virtual Museum Experience Through Real-time Audio Communication", submitted to LatinScience 2023.

#Fix convert 360

Corrija o arquivo utils.py que está em `venv/Lib/site-packages/py360convert/`

Mude a linha 54 onde existe `mask = np.zeros((h, w // 4), np.bool)` e troque para `mask = np.zeros((h, w // 4), bool)`

O valor np.bool está deprecado por isso use apenas bool.