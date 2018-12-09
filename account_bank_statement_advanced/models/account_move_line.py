# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    move_state = fields.Selection(
        related='move_id.state', string='Move State',
        readonly=True)

    @api.multi
    def unlink(self, **kwargs):
        for move_line in self:
            st = move_line.statement_id
            if st and st.state == 'confirm':
                raise UserError(
                    _("Operation not allowed ! "
                      "\nYou cannot delete an Accounting Entry "
                      "that is linked to a Confirmed Bank Statement."))
        return super(AccountMoveLine, self).unlink(**kwargs)

    @api.multi
    def write(self, vals, **kwargs):
        for move_line in self:
            st = move_line.statement_id
            if st and st.state == 'confirm':
                for k in vals:
                    if k not in ['full_reconcile_id',
                                 'matched_debit_ids', 'matched_credit_ids']:
                        raise UserError(
                            _("Operation not allowed ! "
                              "\nYou cannot modify an Accounting Entry "
                              "that is linked to a Confirmed Bank Statement. "
                              "\nStatement = %s"
                              "\nMove = %s (id:%s)\nUpdate Values = %s")
                            % (st.name, move_line.move_id.name,
                               move_line.move_id.id, vals))
        return super(AccountMoveLine, self).write(
            vals, **kwargs)
