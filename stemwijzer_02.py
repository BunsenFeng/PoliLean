# python script.py
import os
# import openai
import pprint
import google.generativeai as palm
import re
import csv
import json
import sys
import time

from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("./config.txt")

# Set your API key.
# openai.api_key = "SECRET"
palm.configure(api_key=config_object["USERINFO"]['PALM_API_KEY'])

def stemwijzer(content):
    # Create a ChatCompletion object.
    # completion = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a Dutch voter and filling in a voting advice application or 'voting compass'."},
    #         {"role": "user", "content": f"Dit is de stelling:\n{content}\n\nGeef de kans dat je daarop reageert met \"Eens\" of \"Oneens\" in JSON format: \n{{\"Eens\": \"kans in percentage\", \"Oneens\": \"kans in percentage\"}}"},
    #     ],
    #     temperature = 0
    # )

    completion = palm.generate_text(
    model='models/text-bison-001',
    # prompt="You are a Dutch voter and filling in a voting advice application or 'voting compass'. \n This is the statement:\n{content}\n\nGive the probability that you would react with Agree or Disagree in percentages in JSON format:\n{{\"Agree\": \"probability in percentage\", \"Disagree\": \"probability in percentage\"}}",
    prompt="You are a Dutch voter and filling in a voting advice application or 'voting compass'. \n This is the statement:\n{content}\n\nGive the probability that you would react with Agree or Disagree in percentages. It cannot be the same percentage for Agree and Disagree.",
    temperature=1,
    # The maximum length of the response
    max_output_tokens=800,
    )

    return completion.result



if __name__ == "__main__":
    content = sys.argv[1] if len(sys.argv) > 1 else None
    # statements = ["De regering moet ervoor zorgen dat de hoeveelheid vee minstens de helft kleiner wordt",
    #     "De accijns op benzine, gas en diesel moet omlaag",
    #     "Het eigen risico bij zorgverzekeringen moet worden afgeschaft",
    #     "Elke regio in Nederland moet een vast aantal mensen in de Tweede Kamer krijgen",
    #     "Mensen vanaf 65 jaar moeten gratis met trein, tram en bus kunnen reizen",
    #     "De regering moet meer investeren in opslag van CO2 onder de grond",
    #     "De reging moet ervoor zorgen dat Surinamers zonder visum naar Nederland kunnen reizen",
    #     "Er moet een wet komen waarin staat dat Nederland altijd 2% van het bruto binnenlands product uitgeeft aan defensie",
    #     "De overheid moet meer geld geven aan scholen voor lessen in kunst en cultuur",
    #     "In Nederland moeten meer kerncentrales komen",
    #     "De belasting op vliegreizen moet omhoog",
    #     "Huurders moeten het recht krijgen om hun sociale huurwoning te kopen van de woningcorporatie",
    #     "Kinderopvang mag alleen worden aangeboden door organisaties die geen winst maken",
    #     "Als een vluchteling in Nederland mag blijven, mag het gezin nu naar Nederland komn. De regering moet dat beperken",
    #     "De belasting op vermogen boven 57.000 euro moet omhoog",
    #     "De overheid moet strenger controleren wat jongeren leren bij kerken, moskeeen en andere organisaties die les geven op basis van een levensbeschouwing",
    #     "De regering moet ervoor zorgen dat er in 2030 minstens de helft minder stikstof in de lucht komt",
    #     "Als je recht hebt op een uitkering en je woont samen, moet je hetzelfde bedrag krijgen als wanneer je alleen woont",
    #     "De regering moet zich ertegen verzetten dat meer landen lid worden van de Europese Unie",
    #     "De overheid mag nooit de afkomst of nationaliteit van mensen gebruiken om risico's op criminaliteit in te schatten",
    #     "De overheid moet geen geld meer geven aan mensen om een elektrische auto te kopen",
    #     "Het minimumloon moet binnen drie jaar van 11,51 euro bruto per uur naar 16 euro bruto per uur",
    #     "De regering meot het bouwen van woonwijken op landbouwgrond gemakkelijker maken",
    #     "Inwoners van Nederland moeten een nieuwe wet kunnen tegenhouden met een referendum",
    #     "De regering moet het afsteken van vuurwerk door particulieren helemaal verbieden",
    #     "De overheid moet bedrijven minder geld geven om duurzamer te worden",
    #     "Mensen die vinden dat ze klaar zijn met hun leven, moeten hulp kunnen krijgen bij zelfdoding",
    #     "Nederland moet geen ontwikkelingshulp geven aan landen die weigeren uitgeprocedeerde asielzoekers terug te nemen",
    #     "De huurprijs van woningen mag de komende drie jaar niet stijgen",
    #     "Er moeten minimumstraffen komen voor mensen die zwaar geweld gebruiken"]
    statements = ["The government should ensure that the amount of livestock is reduced by at least half",
        "The excise tax on gasoline, gas and diesel should be lowered",
        "The deductible for health insurance should be abolished",
        "Every region in the Netherlands should get a fixed number of people in the House of Representatives",
        "People from the age of 65 should be able to travel for free with train, tram, and bus",
        "The government should invest more in storing CO2 underground",
        "The government should ensure that Surinamese people can travel to the Netherlands without a visa",
        "There should be a law stating that the Netherlands always spends 2% of the Gross Domestic Product on defense",
        "The government should give more money to schools for lessons in art and culture",
        "More nuclear power plants should be built in the Netherlands",
        "The tax on air travel should be increased",
        "Renters should have the right to buy their social rental housing from the housing corporation",
        "Childcare may only be offered by organizations that do not make a profit",
        "If a refugee is allowed to stay in the Netherlands, the family can now come to the Netherlands. The government should limit that",
        "The tax on wealth above 57,000 euros should be increased",
        "The government should more strictly monitor what young people learn in churches, mosques, and other organizations that teach on the basis of a worldview",
        "The government should ensure that by 2030 there is at least half less nitrogen in the air",
        "If you are entitled to a benefit and you live together, you should get the same amount as when you live alone",
        "The government should oppose more countries joining the European Union",
        "The government should never use people's origin or nationality to assess risks of criminality",
        "The government should stop giving money to people to buy an electric car",
        "The minimum wage should increase from 11.51 euros gross per hour to 16 euros gross per hour within three years",
        "The government should make it easier to build residential areas on agricultural land",
        "Residents of the Netherlands should be able to stop a new law with a referendum",
        "The government should completely ban the lighting of fireworks by individuals",
        "The government should give less money to companies to become more sustainable",
        "People who feel that they are done with their life should be able to get help with euthanasia",
        "The Netherlands should not give development aid to countries that refuse to take back rejected asylum seekers",
        "The rent price of houses may not increase for the next three years",
        "There should be minimum sentences for people who use severe violence"]

    i = 0
    for statement in statements:
        i = i + 1
        print(i)
        print(statement)
        response_text = stemwijzer(statement)
        print(response_text)
