# -*- coding:utf-8 -*-
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import make_msgid, formatdate
from typing import List, Optional
from kms import KmsUtils  


class EmailSender:
    def __init__(
        self,
        smtp_host: str = 'smtpdm.aliyun.com',
        smtp_port: int = 465,
        username: str = 'no_replay@richs-emails.cts-aia.cn',
        password: str = 'CTSRichs123',
        reply_to: Optional[str] = None,
        kms_secret_name: str = "/DEV/SMTP/EDP_TST",
        kms_access_key_id: str = 'LTAI5tCEarohJvxGvZi6V7Pg',
        kms_access_key_secret: str = '5EoB7GMbiopY4qQMdqFaVtbUgCBBOD',
        kms_endpoint: str = 'kms.cn-shanghai.aliyuncs.com'
    ):
        
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.reply_to = reply_to or username

        # 初始化KMS客户端
        self.kms_client = KmsUtils(
            kms_secret_name,
            kms_access_key_id,
            kms_access_key_secret,
            kms_endpoint
        )

    def _get_recipients_from_kms(self) -> tuple[List[str], List[str]]:
        """
        从KMS获取收件人列表
        :return: (收件人列表, 抄送列表)
        """
        try:
            kms_data = self.kms_client.fn_get_value()
            rcptto_raw = kms_data.get('To', '')
            rcptcc_raw = kms_data.get('Cc', '')

            # 处理收件人
            if isinstance(rcptto_raw, str):
                rcptto = [email.strip() for email in rcptto_raw.split(',') if email.strip()]
            elif isinstance(rcptto_raw, list):
                rcptto = rcptto_raw
            else:
                rcptto = []

            # 处理抄送
            if isinstance(rcptcc_raw, str):
                rcptcc = [email.strip() for email in rcptcc_raw.split(',') if email.strip()]
            elif isinstance(rcptcc_raw, list):
                rcptcc = rcptcc_raw
            else:
                rcptcc = []

            if not rcptto:
                raise ValueError("KMS返回的收件人列表为空")

            return rcptto, rcptcc

        except Exception as e:
            print(f"从KMS获取收件人失败: {e}")
            traceback.print_exc()
            raise RuntimeError(f"从KMS获取收件人失败: {e}")

    def _build_message(
        self,
        subject: str,
        body: str,
        to_list: List[str],
        cc_list: List[str],
        body_type: str = 'html'
    ) -> str:
        
        #构建MIME邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.username
        msg['To'] = ",".join(to_list)
        if cc_list:
            msg['Cc'] = ",".join(cc_list)
        msg['Reply-to'] = self.reply_to
        msg['Message-id'] = make_msgid()
        msg['Date'] = formatdate()

        mime_type = 'html' if body_type == 'html' else 'plain'
        text_part = MIMEText(body, _subtype=mime_type, _charset='UTF-8')
        msg.attach(text_part)

        return msg.as_string()

    def fn_send(
        self,
        subject: str = '测试用邮件',
        body: str = 'Hi All,, \n  this is a test email.',
        body_type: str = 'html'
    ) -> bool:

        try:
            
            to_list, cc_list = self._get_recipients_from_kms()
            msg_str = self._build_message(subject, body, to_list, cc_list, body_type)

            # 发送
            all_recipients = to_list + cc_list
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as client:
                client.set_debuglevel(0)
                client.login(self.username, self.password)
                client.sendmail(self.username, all_recipients, msg_str)
                client.quit()

            print('邮件发送成功！')
            return True

        except smtplib.SMTPConnectError as e:
            print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print('邮件发送失败,', str(e))
        except Exception as e:
            print('邮件发送异常,', str(e))      
        return False
