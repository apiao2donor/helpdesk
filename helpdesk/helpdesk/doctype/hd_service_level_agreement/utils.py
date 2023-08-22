import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from pypika import Criterion

from helpdesk.utils import get_context, check_permissions

DOCTYPE = "HD Service Level Agreement"


def get_sla(ticket: Document) -> Document:
	"""
	Get Service Level Agreement for `ticket`

	:param doc: Ticket to use
	:return: Applicable SLA
	"""
	check_permissions(DOCTYPE, None)
	QBSla = frappe.qb.DocType(DOCTYPE)
	now = now_datetime()
	sla_list = (
		frappe.qb.from_(QBSla)
		.select(QBSla.name, QBSla.condition)
		.where(QBSla.enabled == True)
		.where(QBSla.default_sla == False)
		.where(Criterion.any([QBSla.start_date.isnull(), QBSla.start_date <= now]))
		.where(Criterion.any([QBSla.end_date.isnull(), QBSla.start_date >= now]))
		.run(as_dict=True)
	)
	res = None
	for sla in sla_list:
		cond = sla.get("condition")
		if not cond or frappe.safe_eval(cond, None, get_context(ticket)):
			res = sla
			break
	return res or get_default()


def get_default() -> Document:
	"""
	Get default Service Level Agreement

	:return: Default SLA
	"""
	return frappe.get_last_doc(
		DOCTYPE,
		filters={
			"enabled": True,
			"default_sla": True,
		},
	)
