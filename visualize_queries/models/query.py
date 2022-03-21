from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Query(models.TransientModel):
    _name = 'db.query'

    name = fields.Char("Query")
    age = fields.Float("Age Seconds (Total)")
    age_minutes = fields.Float("Age Minutes (Total)", compute="_compute_age")
    age_hours = fields.Float("Age Hours (Total)", compute="_compute_age")

    def _compute_age(self):
        for rec in self:
            rec.age_minutes = rec.age / 60.0
            rec.age_hours = rec.age / 3600.0

    def cancel(self):
        raise NotImplementedError("Cancel")
