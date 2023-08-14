import openai
import os
from dotenv import load_dotenv
from models.open_ai_model import OpenAIResponse

load_dotenv()
openai.api_key = os.getenv('OPENAI')
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
        result = openai.ChatCompletion.create(model=model, messages=self.dialog)
        response = OpenAIResponse(**result)
        return response.choices[0].message.content

    def interact(self) -> None:
        print("Commands: \n\tSEND to send question.\n\tCLEAR to start a new conversation.\n\tDUMP to show the entire "
              "conversation thead.\n\tEXIT to end the program.")
        while self.keep_going:
            print("Enter your question: ")
            lines = []
            while True:
                line = input()
                if line == "SEND":
                    break
                if line in ["CLEAR", "DUMP", "EXIT"]:
                    lines.append(line)
                    break
                lines.append(line)
            question = " ".join(lines)

            if question == "CLEAR":
                self.clear()
            elif question == "DUMP":
                self.dump()
            elif question == "EXIT":
                self.keep_going = False
            else:
                self.append("user", question)
                result_content = self.get_response()
                self.append("assistant", result_content)
                print(result_content)


if __name__ == "__main__":
    dialog = Dialog()
    dialog.interact()
