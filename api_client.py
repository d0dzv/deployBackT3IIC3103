import requests
import json
import logging

API_URL = "http://tormenta.ing.puc.cl/api/generate"

def get_llm_response(question: str, context: str) -> str:
    context = context[:500]

    payload = {
        "model": "integra-LLM",
        "prompt": f"Contexto: {context}\nPregunta: {question}"
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            logging.error(f"Error al obtener respuesta del LLM: {response.status_code} - {response.text}")
            print(f"Error al obtener respuesta del LLM: {response.status_code} - {response.text}")
            return "Lo siento, no puedo procesar tu solicitud en este momento."

        # Verificar el tipo de contenido
        content_type = response.headers.get('Content-Type', '')
        logging.info(f"Content-Type de la respuesta: {content_type}")
        if 'application/x-ndjson' not in content_type.lower():
            logging.warning("El Content-Type de la respuesta no es 'application/x-ndjson', pero se intentará procesar la respuesta.")

        # Procesar la respuesta NDJSON
        respuesta_completa = ""
        for line_number, line in enumerate(response.iter_lines(), start=1):
            if line:
                try:
                    # Decodificar la línea
                    decoded_line = line.decode('utf-8')
                    logging.debug(f"Línea {line_number} recibida: {decoded_line}")
                    # Parsear el JSON de la línea
                    data = json.loads(decoded_line)
                    # Concatenar el fragmento de la respuesta
                    fragmento = data.get('response', '')
                    respuesta_completa += fragmento
                    # Verificar si la respuesta está completa
                    if data.get('done', False):
                        logging.info("Finalización de la respuesta detectada.")
                        break
                except json.JSONDecodeError as e:
                    logging.error(f"Error al decodificar la línea JSON en la línea {line_number}: {e}")
                    logging.error(f"Línea recibida: {decoded_line}")
                    return "Lo siento, no puedo procesar tu solicitud en este momento."
        logging.info("Respuesta del LLM obtenida exitosamente.")
        return respuesta_completa.strip()

    except requests.exceptions.RequestException as e:
        logging.error(f"Excepción al obtener respuesta del LLM: {e}")
        print(f"Excepción al obtener respuesta del LLM: {e}")
        return "Lo siento, no puedo procesar tu solicitud en este momento."