from flask import Blueprint, request, jsonify
from user.connections.connection import get_connection

handlers = Blueprint('handlers', __name__)

@handlers.route('/data', methods=['GET'])
def get_data():
    cnx = get_connection()
    if cnx:
        try:
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM user")
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()
            return jsonify(rows)
        except Exception as e:
            return f"Error: {e}", 500
    return "Database connection error", 500

@handlers.route('/data/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    cnx = get_connection()
    if cnx:
        try:
            cursor = cnx.cursor()
            query = "SELECT * FROM user WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            cnx.close()
            if user:
                return jsonify(user)
            else:
                return "User not found", 404
        except Exception as e:
            return f"Error: {e}", 500
    return "Database connection error", 500


@handlers.route('/data', methods=['POST'])
def post_data():
    cnx = get_connection()
    if cnx:
        try:
            data = request.get_json()
            cursor = cnx.cursor()
            query = "INSERT INTO user (username, email) VALUES (%s, %s)"
            cursor.execute(query, (data['username'], data['email']))
            cnx.commit()
            cursor.close()
            cnx.close()
            return "Data inserted successfully", 201
        except Exception as e:
            return f"Error: {e}", 500
    return "Database connection error", 500

@handlers.route('/data/<int:user_id>', methods=['PUT'])
def put_data(user_id):
    cnx = get_connection()
    if cnx:
        try:
            data = request.get_json()
            cursor = cnx.cursor()
            query = "UPDATE user SET username = %s, email = %s WHERE id = %s"
            cursor.execute(query, (data['username'], data['email'], user_id))
            cnx.commit()
            cursor.close()
            cnx.close()
            return "Data updated successfully", 200
        except Exception as e:
            return f"Error: {e}", 500
    return "Database connection error", 500


@handlers.route('/data/<int:user_id>', methods=['PATCH'])
def patch_data(user_id):
    cnx = get_connection()
    if cnx:
        try:
            data = request.get_json()
            cursor = cnx.cursor()

            # Generating the SET clause dynamically for the update query
            set_clause = ', '.join(f"{key} = %s" for key in data.keys())
            values = list(data.values())
            values.append(user_id)  # Adding user_id for WHERE clause

            query = f"UPDATE user SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            cnx.close()
            return "Data partially updated", 200
        except Exception as e:
            return f"Error: {e}", 500
    return "Database connection error", 500


@handlers.route('/data/<int:user_id>', methods=['DELETE'])
def delete_data(user_id):
    cnx = get_connection()
    if cnx:
        try:
            cursor = cnx.cursor()
            query = "DELETE FROM user WHERE id = %s"
            cursor.execute(query, (user_id,))
            cnx.commit()
            cursor.close()
            cnx.close()
            return "Data deleted successfully", 200
        except Exception as e:
            return f"Error: {e}", 500
    return "Database connection error", 500

