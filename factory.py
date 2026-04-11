import requests
import datetime
import os
import time

#### Settings #######################################
BASE_API_URL = "http://localhost:1234/v1"
API_URL = "http://localhost:1234/v1/chat/completions"
outputsDirectory = "outputs"
#####################################################

def get_directory_name(originalPrompt, temperature = 3):
    prompt = f"""    Create a directory name for the following website idea: \n\t{originalPrompt}.
    The directory name should be short, descriptive, and use only lowercase letters, numbers, and hyphens.
    Return only the directory name without any additional text, formatting, explanations or thinking. Just the directory name."""

    payload = {
        "model": "lmstudio",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    response = requests.post(API_URL, json=payload)
    content = response.json()["choices"][0]["message"]["content"]

    uniqueProjectName = get_unique_folder_name("./" +outputsDirectory, content)

    return uniqueProjectName

def get_unique_folder_name(base_path, folder_name):
    counter = 0
    new_name = folder_name

    while os.path.exists(os.path.join(base_path, new_name)):
        counter += 1
        new_name = f"{folder_name}-{counter}"

    return os.path.join(base_path, new_name)

def generate_file(prompt, filename, temperature):
    payload = {
        "model": "lmstudio",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    response = requests.post(API_URL, json=payload)
    content = response.json()["choices"][0]["message"]["content"]

    with open(filename, "w", encoding="utf-8") as f:
        
        f.write(content)

    print(f"File '{filename}' has been created.")

# gets the currently loaded model. might break if multiple models are loaded
def try_get_used_model():
    try:
        response = requests.get(f"{BASE_API_URL}/models")
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        if data and 'data' in data and len(data['data']) > 0:
            model_name = data['data'][0].get('id', 'Unknown Model')
            return(model_name)
        else:
            return("Unknown")

    except requests.exceptions.ConnectionError:
        print("Error while getting model information: Could not connect to LM Studio at http://localhost:1234. Is it running?")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while querying the model list: {e}")

def generate_documentation(filename, generationTime=0, numberOfVersionsToGenerate=0):
    content = f"""Factory Documentation 
Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Generated with model: {try_get_used_model()}
Original prompt by user: {originalPrompt}
    
Prompt to AI generate prompt: {prompToGeneratePrompt}
    
Extra addition: {onlyHtmlPrompAddition}


Time taken to generate AI enhanced prompt: {generationTime} seconds
Generating {numberOfVersionsToGenerate} versions\n\n"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def add_version_info_to_documentation(filename, temperature, timeTaken):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Version with temperature {temperature} generated in {timeTaken} seconds.\n")

def finish_documentation(filename, totalTime):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n\nTotal time taken to generate all versions: {totalTime} seconds\n")
        f.write("Conclusion / Comments:\n")



### start of the actual program ###############
print("\nEnter a website idea:")
originalPrompt = input()

print("\nEnter the number of versions to generate:")
numberOfVersions = int(input())
print("\nGenerating ...")

### Directory creation stuff ################
if(os.path.exists(outputsDirectory) == False):
    os.mkdir(outputsDirectory)

currenProjectDirectory = get_directory_name(originalPrompt)
os.mkdir(currenProjectDirectory)
print(f"Directory '{currenProjectDirectory}' has been created.")

# Create directory for broken files
os.mkdir(currenProjectDirectory + "/not-working")
print(f"Directory '{currenProjectDirectory}/not-working' has been created.")
#############################################


prompToGeneratePrompt = f"""
    write a prompt that you could give to an llm to create the following 
    as flawlessly as possible in an html file: \n\t{originalPrompt}. output only the prompt and nothing else"""

start_time = time.perf_counter()
generate_file(prompToGeneratePrompt, f"{currenProjectDirectory}/generated_prompt.txt", 0.1)
end_time = time.perf_counter()
AIpromptGenerationTime = round(end_time - start_time, 2)
print(f"Enhanced prompt generated in {AIpromptGenerationTime} seconds.\n")

generatedPrompt = ""
with open(f"{currenProjectDirectory}/generated_prompt.txt", "r", encoding="utf-8") as f:
    generatedPrompt = f.read()

onlyHtmlPrompAddition = """
    Create a complete HTML5 file.
    Output only the raw HTML code.
    No [THINK], no explanations, no comments, no Markdown code blocks.
    Output ONLY valid HTML code. The language in the game and UI must be English. 
    The html file should represent the following: """

generate_documentation(f"{currenProjectDirectory}/documentation.txt", AIpromptGenerationTime, numberOfVersions)

totalTime = AIpromptGenerationTime

# number of versions to generate
for x in range(numberOfVersions):
    # increase temperature for each version
    temperature = round(x * 3, 1)
    start_time = time.perf_counter()
    generate_file(
        onlyHtmlPrompAddition + generatedPrompt,
        f"{currenProjectDirectory}/temperature-is-{temperature}.html",
        temperature
    )
    end_time = time.perf_counter()
    timeTaken = round(end_time - start_time, 2)
    totalTime += timeTaken
    add_version_info_to_documentation(f"{currenProjectDirectory}/documentation.txt", temperature, timeTaken)
    print(f"Version {x+1}/{numberOfVersions} with temperature {temperature} has been generated in {timeTaken} seconds.\n")

finish_documentation(f"{currenProjectDirectory}/documentation.txt", totalTime)
print(f"All versions have been generated. Total time taken: {totalTime} seconds.")

