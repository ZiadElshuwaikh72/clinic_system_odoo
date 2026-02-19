import json
from odoo import http
from odoo.http import request


# Method Response
def success_response(message=None, data=None, status=200):
    return request.make_json_response({
        "success": True,
        "message": message,
        "data": data,
        "errors": None
    }, status=status)

def error_response(message=None, errors=None, status=400):
    return request.make_json_response({
        "success": False,
        "message": message,
        "data": None,
        "errors": errors
    }, status=status)


class ClinicApi(http.Controller):

    # CREATE Patient
    @http.route('/v1/patients', type='json', auth='public', methods=['POST'], csrf=False)
    def create_patient(self):
        try:
            data =request.httprequest.data.decode('utf-8')
            args = json.loads(data)

            required_fields = ['name', 'phone', 'doctor_id']

            for field in required_fields:
                if not args.get(field):
                    return error_response(
                        message="Validation Error",
                        errors={field: f"{field} is required"}
                    )

            patient = request.env['clinic.patient'].sudo().create({
                'name': args.get('name'),
                'phone': args.get('phone'),
                'birth_date': args.get('birth_date'),
                'doctor_id': args.get('doctor_id'),
            })

            return success_response(
                message="Patient created successfully",
                data={"id": patient.id, "name": patient.name},
                status=201
            )
        except Exception as e:
             return error_response("Invalid JSON format", errors=str(e))

    # GET All Patients
    @http.route('/v1/patients', type='json', auth='public', methods=['GET'], csrf=False)
    def get_patients(self):
        try:
            patients = request.env['clinic.patient'].sudo().search([])

            data = []
            for p in patients:
                data.append({
                    "id": p.id,
                    "name": p.name,
                    "phone": p.phone,
                    "birth_date": p.birth_date,
                    "doctor_id": p.doctor_id.id if p.doctor_id else None
                })

            return success_response("All patients fetched successfully", data=data)
        except Exception as e:
             return error_response("Invalid JSON format", errors=str(e))

    # GET Patient by id
    @http.route('/v1/patients/<int:id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_patient(self, id):
        try:
            patient = request.env['clinic.patient'].sudo().browse(id)

            if not patient.exists():
                return error_response("Patient not found", status=404)

            return success_response("Patient fetched successfully", data={
                "id": patient.id,
                "name": patient.name,
                "phone": patient.phone,
                "birth_date": patient.birth_date,
                "doctor_id": patient.doctor_id.id if patient.doctor_id else None
            })
        except Exception as e:
             return error_response("Invalid JSON format", errors=str(e))

    # UPDATE Patient
    @http.route('/v1/patients/<int:id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_patient(self, id):
        try:
            data = request.httprequest.data.decode('utf-8')
            args=json.loads(data)

            patient = request.env['clinic.patient'].sudo().browse(id)
            if not patient.exists():
                return error_response("Patient not found", status=404)

            patient.write(args)
            return success_response("Patient updated successfully")

        except Exception as e:
            return error_response("Invalid JSON format", errors=str(e))

    # DELETE Patient
    @http.route('/v1/patients/<int:id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_patient(self, id):
        try:
            patient = request.env['clinic.patient'].sudo().browse(id)
            if not patient.exists():
                return error_response("Patient not found", status=404)

            patient.unlink()
            return success_response("Patient deleted successfully")

        except Exception as e:
            return error_response("Invalid JSON format", errors=str(e))
