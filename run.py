from flask_apscheduler import APScheduler

from app import app
from app.data_scheduler import Config

app.config.from_object(Config())

scheduler = APScheduler()  # 实例化APScheduler
scheduler.init_app(app)  # 把任务列表放进flask
scheduler.start()  # 启动任务列表
app.run(host="0.0.0.0", port=8080, debug=True, threaded=True, use_reloader=False)
# server = make_server('0.0.0.0',5001,app)
# server.serve_forever()
# app.run(threaded=True)
