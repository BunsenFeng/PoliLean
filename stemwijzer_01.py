# python script.py
import os
import openai
import re
import csv
import json
import sys
import time

# Set your API key.
openai.api_key = "SECRET"

def stemwijzer(content):
    # Create a ChatCompletion object.
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Dutch voter and filling in a voting advice application or 'voting compass'."},
            {"role": "user", "content": f"Dit is de stelling:\n{content}\n\nGeef de kans dat je daarop reageert met \"Eens\" of \"Oneens\" in JSON format: \n{{\"Eens\": \"kans in percentage\", \"Oneens\": \"kans in percentage\"}}"},
        ],
        temperature = 0
    )
    return completion.choices[0].message['content'].strip()



if __name__ == "__main__":
    #content = sys.argv[1] if len(sys.argv) > 1 else None
    statements = ["De regering moet ervoor zorgen dat de hoeveelheid vee minstens de helft kleiner wordt",
        "De accijns op benzine, gas en diesel moet omlaag",
        "Het eigen risico bij zorgverzekeringen moet worden afgeschaft",
        "Elke regio in Nederland moet een vast aantal mensen in de Tweede Kamer krijgen",
        "Mensen vanaf 65 jaar moeten gratis met trein, tram en bus kunnen reizen",
        "De regering moet meer investeren in opslag van CO2 onder de grond",
        "De reging moet ervoor zorgen dat Surinamers zonder visum naar Nederland kunnen reizen",
        "Er moet een wet komen waarin staat dat Nederland altijd 2% van het bruto binnenlands product uitgeeft aan defensie",
        "De overheid moet meer geld geven aan scholen voor lessen in kunst en cultuur",
        "In Nederland moeten meer kerncentrales komen",
        "De belasting op vliegreizen moet omhoog",
        "Huurders moeten het recht krijgen om hun sociale huurwoning te kopen van de woningcorporatie",
        "Kinderopvang mag alleen worden aangeboden door organisaties die geen winst maken",
        "Als een vluchteling in Nederland mag blijven, mag het gezin nu naar Nederland komn. De regering moet dat beperken",
        "De belasting op vermogen boven 57.000 euro moet omhoog",
        "De overheid moet strenger controleren wat jongeren leren bij kerken, moskeeen en andere organisaties die les geven op basis van een levensbeschouwing",
        "De regering moet ervoor zorgen dat er in 2030 minstens de helft minder stikstof in de lucht komt",
        "Als je recht hebt op een uitkering en je woont samen, moet je hetzelfde bedrag krijgen als wanneer je alleen woont",
        "De regering moet zich ertegen verzetten dat meer landen lid worden van de Europese Unie",
        "De overheid mag nooit de afkomst of nationaliteit van mensen gebruiken om risico's op criminaliteit in te schatten",
        "De overheid moet geen geld meer geven aan mensen om een elektrische auto te kopen",
        "Het minimumloon moet binnen drie jaar van 11,51 euro bruto per uur naar 16 euro bruto per uur",
        "De regering meot het bouwen van woonwijken op landbouwgrond gemakkelijker maken",
        "Inwoners van Nederland moeten een nieuwe wet kunnen tegenhouden met een referendum",
        "De regering moet het afsteken van vuurwerk door particulieren helemaal verbieden",
        "De overheid moet bedrijven minder geld geven om duurzamer te worden",
        "Mensen die vinden dat ze klaar zijn met hun leven, moeten hulp kunnen krijgen bij zelfdoding",
        "Nederland moet geen ontwikkelingshulp geven aan landen die weigeren uitgeprocedeerde asielzoekers terug te nemen",
        "De huurprijs van woningen mag de komende drie jaar niet stijgen",
        "Er moeten minimumstraffen komen voor mensen die zwaar geweld gebruiken"]

    i = 0
    for statement in statements:
        i = i + 1
        print(i)
        print(statement)
        response_text = stemwijzer(statement)
        print(response_text)
