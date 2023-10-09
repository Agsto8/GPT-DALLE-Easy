import openai


class GPT:
    def __init__(self, key):
        openai.api_key = key

        self.messages3 = [
            {"role": "system", "content": "You are a intelligent assistant."}
        ]

    def gpt3(self, inp):
        message = inp
        if message:
            self.messages3.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.messages3
            )
        reply = chat.choices[0].message.content
        self.messages3.append({"role": "assistant", "content": reply})
        return reply

    def img(self, inp, res):
        response = openai.Image.create(
            prompt=inp,
            n=1,
            size=res,
        )
        url = response["data"][0]["url"]
        return url
    

