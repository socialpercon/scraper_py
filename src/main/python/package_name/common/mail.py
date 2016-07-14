import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys
import yaml
import config


def get_smtp_config():
    try:
        config_file = config.get_config_path(config.EMAIL_CONF_PATH)
        with open(config_file, 'r') as stream:
            return yaml.load(stream)
    except IOError as e:
        sys.stderr.write('[ERROR] file: {0}, reason: {1}\n'.format(config_file, repr(e)))
        sys.stderr.flush()


def send_mail(cfg_smtp, output_data):
    try:
        title = cfg_smtp["TITLE"]
        cfg_smtp = cfg_smtp["SMTP"]
        msg = MIMEMultipart('alternative')
        msg['From'] = cfg_smtp['ACCOUNT']
        msg['TO'] = ','.join(cfg_smtp['TO_LIST'])
        msg['Subject'] = title
        msg.attach(MIMEText(output_data, 'html', 'utf-8'))

        mail_server = smtplib.SMTP(cfg_smtp['HOST'], cfg_smtp['PORT'])
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(cfg_smtp['ACCOUNT'], cfg_smtp['PASSWORD'])
        mail_server.sendmail(cfg_smtp['ACCOUNT'], cfg_smtp['TO_LIST'], msg.as_string())
        mail_server.close()
        return "OK"
    except BaseException as e:
        print "send mail failed, reason: {0}".format(repr(e))
        return "FAIL"
