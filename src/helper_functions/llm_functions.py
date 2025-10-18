from openai import OpenAI
import time
import os

def ask_to_gpt(messages, gpt_model='gpt-4.1-nano',max_tokens=1024,temperature=0,n_retry=2,verbose=False):

    client = OpenAI(
        api_key = os.getenv('OPENAI_API_KEY')
    )

    if verbose:
        print("================ OpenAI API call =================")
        print(" > Model: ", gpt_model)
        print(" > temperature: ", temperature)
        print(" > max_tokens: ", max_tokens)
        print("==================== Request =====================")
        #print(json.dumps(messages, indent=2))

    while n_retry:
        try:
            if verbose:
                print('Please wait...')
            response = client.chat.completions.create(
                  model=gpt_model,
                  messages=messages,
                  max_completion_tokens=max_tokens,
                  #modalities=['text'],
                  temperature=temperature,# [0-2]
                  top_p=1,                
                  frequency_penalty=0,    # [-2, 2]
                  presence_penalty=0,     # [-2,2]
                  n = 1,                  # [>1]
              )
            if verbose:
                print("==================== Answer ======================")
                #display(response.choices[0].message.content)
                print("==================== Stats =======================")
                print(dict(response).get('usage'))
                print("==================================================")

            chat_completion = {
                "prompt": messages,
                "completion": response,
            }
            return chat_completion
        except Exception as e:
            print(f"An exception occurred in the GPT request: {str(e)}")
            if n_retry > 0:
                print('Trying request GPT again in few seconds!\nWait...')
            else:
                raise f"The trying limit was reached.\nExiting... with the error: {str(e)}"
            
            n_retry -= 1
            time.sleep(5) # Wait 5 seconds
            print('Trying again!')
    raise "The trying limit was reached.\nExiting..."