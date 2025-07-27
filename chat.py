import openai
import config

openai.api_key = config.OPENAI_API_KEY

def cargar_hilo_guardado():
    try:
        with open("LineaCompleta.txt", "r") as archivo:
            lineas = archivo.readlines()
            mensajes = []
            for i in range(0, len(lineas), 4):
                if i + 3 < len(lineas):
                    user = lineas[i + 1].strip()
                    assistant = lineas[i + 3].strip()
                    mensajes.append({"role": "user", "content": user})
                    mensajes.append({"role": "assistant", "content": assistant})
            return mensajes[-10:]
    except FileNotFoundError:
        return []

def run_chatbot():
    print("¡Hola!, ¿En qué puedo ayudarte? (Escribe 'salir' para terminar)\n")

    context = {
        "role": "system",
        "content": (
            "¡Saludos! Soy un asistente inspirado en el astrofísico Carl Sagan. "
            "Estoy aquí para brindarte información fascinante sobre el universo, "
            "explorar los misterios del cosmos y responder tus preguntas sobre "
            "astronomía, ciencia y metafísica. ¡Adelante, hagamos volar nuestra "
            "imaginación hacia las estrellas!"
        )
    }

    messages = [context]
    hilo_guardado = cargar_hilo_guardado()
    messages.extend(hilo_guardado)

    while True:
        question = input("(Salir para terminar) Tú: ").strip()
        if question.lower() == "salir":
            print("Hasta la próxima, viajero del cosmos 🚀")
            break

        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )

        response_content = response.choices[0].message['content'].strip()
        print("\nCarl Bot:", response_content, "\n")

        messages.append({"role": "assistant", "content": response_content})

        # Guardar conversación en archivo
        with open("Linea.txt", "w") as file:
            for msg in messages[1:]:  # Excluye el system prompt
                file.write(f"{msg['role'].capitalize()}:\n{msg['content']}\n\n")

        with open("LineaCompleta.txt", "a") as file:
            file.write(f"Usuario:\n{question}\nAsistente:\n{response_content}\n\n")

if __name__ == "__main__":
    run_chatbot()