from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Query(models.TransientModel):
    _name = 'db.query'

    pid = fields.Integer("PID")
    state = fields.Char("State")
    started = fields.Datetime("Started")
    usename = fields.Char("Username")
    name = fields.Char("Query")
    age = fields.Float("Age Seconds (Total)")
    age_minutes = fields.Float("Age Minutes (Total)", compute="_compute_age")
    age_hours = fields.Float("Age Hours (Total)", compute="_compute_age")

    def _compute_age(self):
        for rec in self:
            rec.age_minutes = rec.age / 60.0
            rec.age_hours = rec.age / 3600.0

    def cancel(self):
        self.env.cr.execute((
            "select pg_terminate_backend(%s)"
        ), (self.id,))
        self._update_queries()

    @api.model
    def _update_queries(self):
        self.env.cr.execute((
            "select pid, query_start, state, query, usename "
            "from pg_stat_activity"
        ))
        pids = set()
        for query in self.env.cr.dictfetchall():
            query['name'] = query['query']
            queries = self.search([('pid', '=', query['pid'])])
            if not queries:
                queries.create(query)
            else:
                queries.write(query)
            pids.add(query['pid'])

        self.search([('pid', 'not in', list(pids))]).unlink()
