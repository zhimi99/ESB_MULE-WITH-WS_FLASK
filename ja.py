from flask import Flask, request, jsonify

app = Flask(__name__)

COSTO_TRANSFERENCIA = 0.3

cuentas = [
    {
        'numero': '1111',
        'cliente': 'Alan Brito',
        'saldo': 120.5
    },
    {
        'numero': '2222',
        'cliente': 'Aquiles Castro',
        'saldo': 540.9
    },
]

@app.route('/transferir', methods=['POST'])
def transferencia():
    data = request.json
    cuenta_origen = data['cuenta_origen']
    if cuenta_origen != None and cuenta_origen != '':
        print(cuentas)
        for cuenta in cuentas:
            print(cuenta)
            if cuenta['numero'] == cuenta_origen:

                print(f"Esta es la cuenta del cliente: {cuenta['cliente']}")
                saldo = cuenta['saldo']
                monto = data['monto_transferencia']

                if saldo >= monto + COSTO_TRANSFERENCIA:
                    cuenta['saldo'] = saldo - (monto + COSTO_TRANSFERENCIA)
                    print(f"Se va a transferir: {monto}")
                    return jsonify({
                        'entidad_fincaciera': data['entidad_fincaciera'],
                        'cuenta_destino': data['cuenta_destino'],
                        'monto_transferencia':monto,
                        'descripcion': data['descripcion'],
                    })

                else:

                    return jsonify({'error':'No dispone del saldo suficiente para realizar la transaccion.'})

        return jsonify({'error':'La cuenta solicitada no existe'})
        
    else :
        return jsonify({'error':'No se proporciono un numero de cuenta valido.'})


@app.route('/acreditar_transferencia')
def acreditar_transferencia():
    data = request.json
    cuenta_destino = data['cuenta_destino']
    if cuenta_destino != None and cuenta_destino != '':
        for cuenta in cuentas:
            if cuenta['numero'] == cuenta_destino:
                monto = data['monto_transferencia']
                saldo = cuenta['saldo']
                cuenta['saldo'] += monto
                return jsonify({
                    "estado_transferencia":"Completada",
                    "cuenta_destino": cuenta_destino,
                    "cliente": cuenta['cliente'],
                    "monto_transferencia":monto,
                    "saldo_antes":saldo,
                    "saldo_despues": cuenta['saldo'],
                })
            
        return jsonify({'error':'La cuenta solicitada no existe'})

    else :
        return jsonify({'error':'No se proporciono un numero de cuenta valido.'})

if __name__ == '__main__':
    app.run(debug=True, port=3100)