#importar librerias
import spacy


#importar dataset de binance de precios historicos del BTC





#leer textos de twitter sobre BTC





#hallar sentimientos de comentarios de twitter

nlp=spacy.load("en_core_web_sm")


# Procesamiento básico
def clean_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

tweets = ["Bitcoin will skyrocket!", "BTC is doomed!", "Stable for now."]
cleaned_tweets = [clean_text(tweet) for tweet in tweets]
print(cleaned_tweets)





#combinar las caracteristicas de la moneda BTC con los sentimiento (0,1)



#predecir el precio de la moneda de acuerdo a dichos parametros


