from flask import Flask, request, jsonify, abort
from convert import CidrMaskConvert, IpValidate
from methods import Token, Restricted


app = Flask(__name__)
login = Token()
protected = Restricted()
convert = CidrMaskConvert()
validate = IpValidate()


# Just a health check
@app.route("/")
def urlRoot():  
    return "OK"


# Just a health check
@app.route("/_health")
def urlHealth():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def urlLogin():
    username = request.form['username']
    password = request.form['password']

    jwt_token = login.generateToken(username, password)

    if jwt_token:
        response = {"data": jwt_token}
        return jsonify(response)

    abort(401)  


# e.g. http://127.0.0.1:8000/cidr-to-mask?value=8
@app.route("/cidr-to-mask")
def urlCidrToMask():
    authorization = request.headers.get('Authorization')
    authorized = protected.access_Data(authorization)

    if not authorized:
        abort(401)

    cidr_value = request.args.get('value')
    response = {"function": "cidrToMask", 
                "input": cidr_value, 
                "output": convert.cidr_to_mask(cidr_value)
                }

    return jsonify(response)


# # e.g. http://127.0.0.1:8000/mask-to-cidr?value=255.0.0.0
@app.route("/mask-to-cidr")
def urlMaskToCidr():
    authorization = request.headers.get('Authorization')
    authorized = protected.access_Data(authorization)

    if not authorized:
        abort(401) 

    mask_value = request.args.get('value')
    response = {"function": "maskToCidr", 
                "input": mask_value, 
                "output": convert.mask_to_cidr(mask_value)
                }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

