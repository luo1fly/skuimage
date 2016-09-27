from flask import Flask
from utils import generate_xml_by_sku

app = Flask(__name__)

help_docs = """
http://srcimg.madeinchina.com/api/skuimg/skus
"""


@app.route('/')
def hello_world():
    return help_docs


@app.route('/api/skuimg/<skus>')
def handler(skus):
    sku_lst = skus.split(',')
    print(sku_lst)
    return generate_xml_by_sku(sku_lst)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
