'''
Tarea 3
Crear una nueva API, la cuál contenga cuatro endpoints con las siguientes consideraciones:

Un endpoint para crear un diccionario en donde las llaves de dicho diccionario sea un id de tipo entero como identificador único para una lista de usuarios. El valor de dicha llave será otro diccionario con la siguiente estructura:

 {"user_name": "name",
 "user_id": id,
 "user_email": "email",
 "age" (optiona): age,
 "recommendations": list[str],
 "ZIP" (optional): ZIP
 }
Cada vez que se haga un request a este endpoint, se debe actualizar el diccionario. Hint: Definir un diccionario vacío fuera del endpoint. La respuesta de este endpoint debe enviar el id del usuario creado y una descripción de usuario creado exitosamente.

Si se envía datos con un id ya repetido, se debe regresar un mensaje de error que mencione este hecho.

Un endpoint para actualizar la información de un usuario específico buscándolo por id. Si el id no existe, debe regresar un mensaje de error que mencione este hecho.

Un endpoint para obtener la información de un usuario específico buscándolo por id. Si el id no existe, debe regresar un mensaje de error que mencione este hecho.

Un endpoint para eliminar la información de un usuario específico buscándolo por id. Si el id no existe, debe regresar un mensaje de error que mencione este hecho.

'''
#APIS
import uvicorn
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from typing import Union

app = FastAPI()
# definimos una  lase para las variables del primer endpoint
# Una clase para definir
class Users(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age : Union[int,None] =None
    recommendations :list[str]
    ZIP : Union[int,None]=None


#Primer EndPoint
# Diccionario
users_dict = {}
@app.put('/users2')
def CreateUser (user: Users):
    user = user.dict()
    if user['user_id'] in users_dict:
        return {'Description':f'Usuario creado {user["user_id"]} ya existe '}
    else:
        users_dict[user['user_id']] = user
        # se regresa en diccionario por que esa es la estructura
        return {'Description': f'Usuario creado correctamente {user["user_id"]}'}


#Segundo EndPoint
@app.post('/users/{user_id}/{user_name}')
def UpdateUser(user_id: int, user_name: str):
    if user_id not in users_dict:
        return {'Description': f'El usuario {user_id} no existe '}
    else:
        user_to_update = users_dict[user_id]
        users_dict[user_id]['user_name'] = user_to_update
        return {'Description': f"El nombre del usuario {user_id} fue actualizado correctamente."}


#Tercer EndPoint
@app.get('/users/{user_id}')
def GetUserInfo(user_id :int):
    if user_id not in users_dict:
        return {'Description':f'Usuario creado {user_id} no existe '}
    else:
        userdata = users_dict[user_id]
        return userdata


# Cuarto Endpoint
@app.delete('/user/{user_id}')
def delete_user(user_id: str):
    if user_id not in users_dict:
        return {'Description': f'El usuario {user_id} no existe.'}
    else:
        usert = users_dict[user_id]
        del usert[Users]
        return {'description':f'User {usert} fue eliminado exitosamente.'}

# Esta funcion es necesaria siempre
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)