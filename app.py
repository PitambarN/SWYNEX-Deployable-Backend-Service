import hmac
from functools import wraps
from sys import exception

from flask import Flask,jsonify,request
from dotenv import load_dotenv
import os
import psycopg2
from pyexpat.errors import messages
from werkzeug.exceptions import BadRequest,UnsupportedMediaType

app=Flask(__name__)
load_dotenv()
API_SECRET_KEY=os.getenv('API_SECRET_KEY')

# custom 405 error Handler
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error":"Method Not allowed",
        "message":"Please Enter Correct HTTP Request"
    }),405



#establish database connection
def get_db_connection():
    return psycopg2.connect(dbname=os.getenv("DB_NAME","patient_db"),
                 user=os.getenv("DB_USER","postgres") ,
                 password=os.getenv("DB_PASSWORD","1122"),
                 host=os.getenv("HOST","localhost"),
                 port=os.getenv("DB_PORT","5432"))






#database test
@app.route('/test_db', methods=['get'])
def test_db():
    conn = None
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
        "status": "success",
        "message": "PostgreSQL connection successful"
    }), 200

    except Exception as e:
        app.logger.exception("DATABASE CONNECTION FAILED")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 503
    finally:
        if conn is not None:
            conn.close()















@app.route('/health_check',methods=['GET'])

def health_check():
    # print(os.getcwd())
    return jsonify({
        "message":"ok",
        "WELCOME TO MY":os.getenv('APP_NAME')

    })


@app.route('/add_patient', methods=['POST'])
def add_patient():
    # get x-api-key from request.header
   api = request.headers.get('x-api-key')
    #check client provide api key or not
   if not api:
        return jsonify({
            "Status": "Internal Server Error",
            "message":"API key is Required"
        }),401
    #check api key valid or not
   if API_SECRET_KEY != api:
        return jsonify({
            "Status": "Unauthorized",
            "message": "Enter a valid API key"
        }), 401


   conn=None
   cur=None
   #handle invalid json syntax
   try:
       data = request.get_json()
   except BadRequest:
       return jsonify({
           "error":"invalid json",
           "message":"please enter valid json data"
       }),400
   except UnsupportedMediaType :
       return jsonify({
           "error":"unsupported media type",
           "message":"content type must be 'application/json'"
       }),415
   #check json object format
   if not isinstance(data,dict):
       return jsonify({
           "error":"Invalid Json format",
           "message":"json must be an object"
       }),400
   #handle missing keys
   required_fieds=["id","name","department","date"]
   try:
       patient_id=data['id']
       patient_name=data['name']
       department=data['department']
       appointment_date=data['date']


   except KeyError as e:
       return jsonify({
           "error":str(e),
           "message":"missing required field"
       }),400
   #check patient_id
   if   not patient_id or len(str(patient_id)) >5 or len(str( patient_id)) <5 or not str(patient_id).isdigit() :
       return jsonify({
           "error":"invalid patient id",
           "message":"patient id must be 5 numeic value"
       })
   if not appointment_date or len(str(appointment_date)) >10 or len(str( appointment_date)) < 10 :
       return jsonify({
           "error":"invalid appointment date",
           "message":"appointment_date must be 10 numeric and character value not above.You enter like '02-03-2025'"
       })
   if not patient_name or len(str(patient_name))>30 :
       return jsonify({
           "error":"patient name error",
           "message":"enter patient name upto 30 characters not above"
       })
   if not department or len(str(department)) >20:
       return jsonify({
           "error":"invalid department name",
           "message":"Enter department name upto 20 characters not above"
       })

   #handle database operation
   try:
       conn=get_db_connection()
       cur=conn.cursor()
       cur.execute('insert into patient(patient_id,patient_name,department,appointment_date) values(%s,%s,%s,%s) returning patient_id,patient_name,department,appointment_date,transaction_id'
                   ,(patient_id,patient_name,department,appointment_date,))
       result= cur.fetchone()
       conn.commit()
       if result is not None:
           return jsonify({
               "message":"data inserted successfully",
               "patient_id":result[0],
               "patient_name":result[1],
               "department":result[2],
               "appointment_date":result[3],
               "transaction_id":result[4]
           }),201
       if result is None:
           conn.rollback()
           return jsonify({
               "error":"patient insert failed"
           }),400
   except psycopg2.Error:
       if conn is not None:
           conn.rollback()
           app.logger.exception("database operation failed")
           return jsonify({
               "error":"database error",
               "message":"unable to save patient data!!!! Patient ID already exists"
           }),500
   except Exception:
       if conn is not None:
           conn.rollback()
           app.logger.exception("unexpected error")
           return jsonify({
               "error":"internal server error"

           }),500
   finally:
       if cur is not None:
           cur.close()
       if conn is not None:
           conn.close()
















#read data from database
@app.route('/get_patient',methods=['GET'])

def get_patient_details():
    conn=None
    cur=None
    try:
     data=request.get_json()
    except BadRequest:
        return jsonify({
            "error":"invalid Json data",
            "message":"please enter valid JSON data"
        }),401
    except UnsupportedMediaType:
        return jsonify({
            "error": "unsupported media type",
            "message": "content type must be 'application/json'"
        }), 415
    if not isinstance(data,dict):
        return jsonify({
            "error":"Invalid json format",
            "messages":"please enter data a valid json format"
        }),400
    try:
        required_fields=['id']
        patient_id=data['id']
    except KeyError as e:
        return jsonify({
            "error":str(e),
            "message":"please enter a valid patient_id"
        }),501


    if not patient_id  or len(str(patient_id))>5 or len(str(patient_id))<5 or not data.get('id'):
        return jsonify({
            "error":"Invalid Patient_id",
            "message":"Patient_id must be 5 numeric value.Don't Enter a None as a KEY_value"

        }),400
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute('select * from patient where patient_id=%s',(patient_id,))
        re=cur.fetchone()
        if re is not None:
            result1=re[0]
            cur.execute('select * from patient where patient_id=%s',(result1,))
        else :
            return jsonify({
                "error":"patient_ID not found",
                "message":"please enter a valid patient_id"
            })



        result=cur.fetchone()

        if result is not None:
            return jsonify({
                "patient_id":result[0],
                "patient_name":result[1],
                "department":result[2],
                "appointment_date":result[3],
                "transaction_id":result[4]
            })
        if result is  None:
            return jsonify({
                "error":"patient ID does not exist",
                "message":"Enter a valid patient_id"
            }),500
    except psycopg2.Error as e:
        if conn is not None:
            conn.rollback()
            return jsonify({
                "error":str(e),
                "message":"Enter a valid patient id"
            }),500
    except Exception as d:
        if conn is not None:
            conn.rollback()
            return jsonify({
                "error":str(d)
            }),501
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()








@app.route('/update_patient',methods=['put'])
def update_patient():
  conn=None
  cur=None
  try:
      data=request.get_json()
  except BadRequest:
      return jsonify({
          "error":"Invalid JSON type",
          "message":"Please Enter a Valid JSON type"
      }),501
  except UnsupportedMediaType:
      return jsonify({
          "error":"Unsupported Media Type",
          "message":"Content Type must be 'application/json"
      }),400

  #check incoming data dictionary or not
  if not isinstance(data,dict):
      return jsonify({
          "error":"Invalid JSON format",
          "message":"Please Enter data a valid json format"
      })
  #key validation
  try:
      required_fields=['id','name','department','appointment_date']
      patient_id=data['id']
      patient_name=data['name']
      department=data['department']
      appointment_date=data['date']
  except KeyError as e:
      return jsonify({
          "error":str(e),
          "message":"please enter key name with valid value"
      })
  if not patient_id or len(str(patient_id)) >5 or len(str( patient_id)) <5 or not data.get('patient_id') is None:
       return jsonify({
           "error":"invalid patient id",
           "message":"patient id must be 5 numeic value AND must enter a valid patient_ID,BUT Patient_ID does not contain NULL Value"
       })
  if not appointment_date or len(str(appointment_date)) >10 or len(str( appointment_date)) < 10 or not data.get('appointment_date') is None:
       return jsonify({
           "error":"invalid appointment date",
           "message":"appointment_date must be 10 numeric and character value not above.You enter like '02-03-2025'"
       })
  if not patient_name or len(str(patient_name))>30 or not data.get('patient_name') is None :
       return jsonify({
           "error":"patient name error",
           "message":"enter patient name upto 30 characters not above"
       })
  if not department or len(str(department)) >20 :
       return jsonify({
           "error":"invalid department name",
           "message":"Enter department name upto 20 characters not above"
       })
  try:
      conn=get_db_connection()
      cur=conn.cursor()
      cur.execute('select * from patient where patient_id=%s',(patient_id,))
      result1=cur.fetchone()
      if result1 is not None:
          result2=result1[0]
      if result1 is None:
          return jsonify({
              "error":"patient_ID not found ",
              "message":"Please enter a valid patient_iD"
          }),500
      cur.execute('update patient set patient_id=%s,patient_name=%s,department=%s,appointment_date=%s where patient_id=%s'
                  ' returning patient_id,patient_name,department,appointment_date,transaction_id',
                  (result2,patient_name,department,appointment_date,patient_id,))
      result=cur.fetchone()

      conn.commit()
      if result is not None:
          patient_id=result[0]
          patient_name=result[1]
          department=result[2]
          appointment_date=result[3]
          transaction_id=result[4]

      return jsonify({
         " patient_id":patient_id,
          "patient_name":patient_name,
          "department":department,
          "appointment_date":appointment_date,
          "transaction_id":transaction_id
      }),200
  except psycopg2.Error as e:
      if conn is not None:
          conn.rollback()
          return jsonify({
              "error:":str(e),
              "message":"Query Failed !!!!!!!!!"
          }),500
  finally:
      if cur is not None:
          cur.close()
      if conn is not None:
          conn.close()




@app.route('/delete_patient',methods=['delete'])
def delete_patient():
    conn=None
    cur=None
    try:
     data=request.get_json()
    except BadRequest:
        return jsonify({
            "error":"invalid Json data",
            "message":"please enter valid JSON data"
        }),401
    except UnsupportedMediaType:
        return jsonify({
            "error": "unsupported media type",
            "message": "content type must be 'application/json'"
        }), 415
    if not isinstance(data,dict):
        return jsonify({
            "error":"Invalid json format",
            "messages":"please enter data a valid json format"
        }),400
    try:
        required_fields=['id']
        patient_id=data['id']
    except KeyError as e:
        return jsonify({
            "error":str(e),
            "message":"please enter a valid patient_id"
        }),501


    if not patient_id  or len(str(patient_id))>5 or len(str(patient_id))<5 :
        return jsonify({
            "error":"Invalid Patient_id",
            "message":"Patient_id must be 5 numeric value.Don't Enter a None as a KEY_value"

        }),400
    try:
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute('select * from patient where patient_id=%s',(patient_id,))
        re=cur.fetchone()
        if re is not None:
            result1=re[0]
        else:
            return jsonify({
                "message":"ENTER A VALID Patient_ID",
                "error":" INvalid patient_id"
            }),401


        cur.execute('delete from patient where patient_id=%s', (result1,))
        conn.commit()

        return jsonify({
            "message":f'patient_ID  deleted successfully'
        }),201

    except psycopg2.Error as e:
        if conn is not None:
            conn.rollback()
            return jsonify({
                "error":str(e),
                "message":"database error"
            }),500
    except Exception as d:
        if conn is not None:
            conn.rollback()
            return jsonify({
                "error":str(d),
                "message":"patient_id deleted successfully"
            }),501
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()






if __name__ =='__main__':

    app.run(
        host='0.0.0.0',
        port=int(os.getenv("PORT",4070)),
        debug= os.getenv('DEBUG', 'False').lower() == 'true'
        )




