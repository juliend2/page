import json
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config.from_pyfile('page.cfg')
db = SQLAlchemy(app)

class Node(db.Model):
    __tablename__ = 'nodes'
    node_id = db.Column('node_id', db.Integer, primary_key=True)
    type = db.Column(db.String)
    title = db.Column(db.String(200))
    url = db.Column(db.String)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    # text = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self, type, title, x, y):
        self.type = type
        self.title = title
        self.url = ''
        self.x = x
        self.y = y
        # self.text = text
        self.created_at = datetime.utcnow()

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/nodes/new", methods=['GET', 'POST'])
def node_add():
    if request.method == 'POST':
        if (not request.form['title']) or (not request.form['type']):
            return '{"status": "error", "message": "Error while validating the fields"}'
        else:
            node = Node(request.form['type'], request.form['title'],
                    request.form['x'], request.form['y'])
            db.session.add(node)
            db.session.commit()
            return '{"status": "success"}'
    elif request.method == 'GET':
        return "GET"
    else:
        return "WTH?"

@app.route("/nodes/move", methods=['POST'])
def node_move():
    _id = str(request.args.get('id', ''))
    # import pdb; pdb.set_trace()
    node = db.session.query(Node).filter_by(node_id=_id).first()
    node.x = int(float(request.form['x']))
    node.y = int(float(request.form['y']))
    db.session.commit()
    return '{"status": "success"}'
    # db.session.query().filter(Node.node_id == _id).update({ "x": int(float(request.form['x'])), "y": int(float(request.form['y'])) })
    # db.session.commit()
    # stmt = Node.update().values({
        # 'x': request.form['x'],
        # 'y': request.form['y']
        # }).where(Node.node_id == _id)
    # db.session.commmit(stmt)

@app.route("/dynamic_graph.json")
def graph():
    #     {
    #         "nodes": [
    #             {
    #                 "id": 1,
    #                 "name": "Julien",
    #                 "type": "link",
    #                 "group": 1,
    #                 "href": "http://www.juliendesrosiers.com",
    #                 "x": 0,
    #                 "y": 0
    #             },
    #             {
    #                 "id": 2,
    #                 "name": "Charlot",
    #                 "type": "node",
    #                 "group": 1,
    #                 "x": 100,
    #                 "y": 100
    #             }
    #         ],
    #         "links": [
    #             {
    #                 "source": 1,
    #                 "target": 0
    #             }
    #         ]
    #     }
    def clean_dict(node):
        # _sa_instance_state comes with the resulting SQLAlchemy's __dict__ :
        _node = node.__dict__
        _node.pop('_sa_instance_state', None)
        _node.pop('created_at', None)
        if _node['url'] == '':
            _node.pop('url')
        return _node
    _dict = {
        "nodes" : [clean_dict(r) for r in Node.query.all()],
        "links" : []
    }
    return json.dumps(_dict)


if __name__ == "__main__":
    app.run(debug=True)
