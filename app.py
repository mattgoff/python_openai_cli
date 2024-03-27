import openai
import os
from dotenv import load_dotenv
from models.open_ai_model import OpenAIResponse

load_dotenv()
openai.api_key = os.getenv('OPENAI')
OPENAI_TEMPERATURE = 0.7
OPENAI_MODEL = 'gpt-3.5-turbo'


class Dialog:
    def __init__(self):
        self.dialog = []
        self.keep_going = True

    def append(self, role: str, content: str) -> None:
        self.dialog.append({"role": role, "content": content})

    def dump(self) -> None:
        for line in self.dialog:
            print(line)

    def clear(self) -> None:
        self.dialog = []

    def exit(self) -> None:
        self.keep_going = False

    def get_response(self, model: str = OPENAI_MODEL) -> str:
        result = openai.ChatCompletion.create(model=model, messages=self.dialog, temperature=OPENAI_TEMPERATURE)
        response = OpenAIResponse(**result)
        return response.choices[0].message.content

    def interact(self) -> None:
        print("Commands: \n\t/send to send question.\n\t/clear to start a new conversation.\n\t/dump to show the entire "
              "conversation thead.\n\t/exit to end the program.")
        while self.keep_going:
            print("Enter your question: ")
            lines = []
            while True:
                line = input()
                if line == "/send":
                    break
                if line in ["/clear", "/dump", "/exit"]:
                    lines.append(line)
                    break
                lines.append(line)
            question = " ".join(lines)

            if question == "/clear":
                self.clear()
            elif question == "/dump":
                self.dump()
            elif question == "/exit":
                self.keep_going = False
            else:
                self.append("user", question)
                result_content = self.get_response()
                self.append("assistant", result_content)
                print(result_content)


if __name__ == "__main__":
    dialog = Dialog()
    dialog.interact()
