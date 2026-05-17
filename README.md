Clinic Management System — Odoo 17
A full-featured clinic management system built with Odoo 17, designed to handle real clinic workflows including patient scheduling, doctor availability, and invoice generation.
Key Technical Decisions:

Appointment workflow: New → Confirmed → Done → Cancelled with business-rule enforcement — confirmed appointments cannot be deleted
Doctor conflict validation: prevents double-booking the same doctor at the same time using @api.constrains
Date validation: blocks scheduling appointments in the past
Auto-generated reference codes using ir.sequence
Full QWeb reports, Chatter integration, and Smart Buttons

Tech: Python, XML, PostgreSQL, Odoo 17
