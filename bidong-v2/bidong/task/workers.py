import time
import logging

from bidong.task.celery import app
from bidong.service.uploader import QiniuService


@app.task(ignore_result=True)
def remove_from_qiniu(url):
    """更新文件时，将七牛文件删除（节省空间）
    """
    logging.info("Got url => ", url)
    key = url.rsplit('/', 1)[-1]
    _, resp = QiniuService().delete(key)
    logging.info(
        "Delete key => %s, Resp: status_code => %s, text_body => %s",
        key, resp.status_code, resp.text_body)


@app.task
def offline_user(project_id, account_id, user=None):
    """对用户做下线操作
    """
    # TODO: handle offline logic
    logging.info("ReqContext(project_id => %s, account_id => %s,  user => %s)",
                 project_id, account_id, user)
    time.sleep(5)
