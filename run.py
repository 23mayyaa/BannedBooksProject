import google.genai as genai
def check_banned(title, author):
    API_KEY = "AIzaSyD8e6MpbO8uLTZvU4Ldxca2esUzgCfTkCg"
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    PROMPT: Given a book name + author determine on a scale of 1 to 10 how likely it is to be [challenged to be removed in a school/public library], if they are outright banned give 10 if there is no record of challenge or possibility of censorship give it 0 Book: Keep in mind that books with sexeul content or involved in sexuality, communism, racism, gay/lgbtq, occult, suicidal thoughts, slavery, racism, revolutions, genocide, anti-government sentiments, war, and beastality, slanderour, pegan rituals or more likely to be challenged 
    Title: {title}, Author: {author}. RESPONSE FORMAT: STRICTLY IN NUMBER"""
    num = int((model.generate_content(prompt).text))
check_banned("gwqfeq", "wfdwfa")
    