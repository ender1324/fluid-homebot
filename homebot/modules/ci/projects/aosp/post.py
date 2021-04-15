from homebot import get_config
from homebot.modules.ci.projects.aosp.project import AOSPProject
#from homebot.modules.ci.projects.aosp import ci_build
from telegram.error import TimedOut
from telegram.ext import CallbackContext

chat_id = get_config("CI_CHANNEL_ID")

def update_ci_post(context: CallbackContext, message_id: int,
				   project: AOSPProject, device: str,
				   status: str, artifacts=None, gapped=False):
	text =  f"💦 CI | Fluid ({project.android_version})\n"
	text += f"Device: {device}\n"
	text += f"Lunch flavor: {project.lunch_prefix}_{device}-{project.lunch_suffix}\n"
	text += f"Gapped build: {str(gapped)}\n"
	text += "\n"
	text += f"Status: {status}\n"
	text += "\n"
	if artifacts is not None:
		text += artifacts.get_readable_artifacts_list()
	if message_id is None:
		return context.bot.send_message(get_config("CI_CHANNEL_ID"), text).message_id
	else:
		# FIXME:
		# telegram.vendor.ptb_urllib3.urllib3.exceptions.ReadTimeoutError:
		# HTTPSConnectionPool(host='api.telegram.org', port=443):
		# Read timed out. (read timeout=5.0)
		try:
			return context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
		except TimedOut:
			pass
