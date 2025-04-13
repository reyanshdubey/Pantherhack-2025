import os
import requests
import google.generativeai as genai
import http.client
import json
import pandas as pd
from tabulate import tabulate

GOOGLE_API_KEY='AIzaSyC5QjrDxW8gKgaDfHnrXp4xA15MXS8TSIQ'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

history = []
user_input = input("Would you like to chat with Google Gemini (gemini) or analyze stocks (stocks) ? type q to quit -> ")
while user_input != "q":
    if user_input == "gemini":
        topic = input("Chat with Google Gemini or type 'game' for a game. (q to quit) -> ")

        while topic != "q":
            if topic == "game":
                topic = input("Choose a topic -> ")
                response = model.generate_content("give 10 words that are related to " + topic + " separated by commas")
                ai_words = response.text.split(", ")

                for i in range(len(ai_words)):
                    ai_words[i] = ai_words[i].lower()   
                    ai_words[i] = ai_words[i].replace(" ", "")
                    ai_words[i] = ai_words[i].replace("\n", "")
                        
                user_guess1 = input("Type one word that is related to " + topic + " (Everything in lowercase, no spaces) -> ")
                user_guess2 = input("Type another word that is related to " + topic + " -> ")
                user_guess3 = input("Type another word that is related to " + topic + " -> ")
                user_guess4 = input("Type another word that is related to " + topic + "  -> ")
                user_guess5 = input("Type another word that is related to " + topic + " -> ")
                guesses = [user_guess1, user_guess2, user_guess3, user_guess4, user_guess5]

                correct = []
                score = 0

                # Check if the AI's words are in the user's guesses; if they are, add them to the correct list and increase the score
                # In other words, check the score
                for i in ai_words:
                    if i in guesses:
                        score = score + 1
                        correct.append(i)

                # format the correct words into a string to print them out
                acc = ""
                for i in correct:
                    acc += i
                    acc += ", "
                    
                # print the score and the correct words
                if len(correct) >= 2:
                    print(acc[:-2] + " were the words that matched the AI's")
                    print(str(score) + " of your words matched the AI!")
                if len(correct) == 1:
                    print(correct[0] + " matched the AI")
                    print("1 of your words matched the AI!")
                if len(correct) < 1:
                    print("None of your words matched the AI")

                # format the AI's words into a string to print them out
                acc2 = ""
                for i in ai_words:
                    acc2 += i
                    acc2 += ", "

                # print all of the AI's words
                print(acc2[:-2] + " were the AI's words.")
            else:

                chat_session = model.start_chat(
                    history = history
                )

                response = chat_session.send_message(topic)
                history.append({"role": "user", "parts": [topic]})
                history.append({"role": "model", "parts": [str(response.text)]}) 
                print(str(response.text))

            topic1 = topic
            topic = input("Chat with Google Gemini or type 'game' for a game. (q to quit) -> ")
    elif user_input == "stocks":

        conn = http.client.HTTPSConnection("yahoo-finance15.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "da82cb6ab5mshcfa6270ae11b726p1aea70jsn8c30d289637f",
            'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
        }

        option = input("How many stocks would you like to compare? (1 - 4) -> ")

        stockStr = ""
        stock = ""
        stock2 = ""
        stock3 = ""
        stock4 = ""
        if option == "1":
            stock = input("Choose a stock ticker (ex: AAPL) -> ")
            stockStr = stock
        if option == "2":
            stock = input("Choose a stock ticker (ex: AAPL) -> ")
            stock2 = input("Choose a second stock ticker (ex: MSFT) -> ")
            stockStr = stock + "," + stock2
        if option == "3":
            stock = input("Choose a stock ticker (ex: AAPL) -> ")
            stock2 = input("Choose a second stock ticker (ex: MSFT) -> ")
            stock3 = input("Choose a third stock ticker (ex: TSLA) -> ")
            stockStr = stock + "," + stock2 + "," + stock3
        if option == "4":
            stock = input("Choose a stock ticker (ex: AAPL) -> ")
            stock2 = input("Choose a second stock ticker (ex: MSFT) -> ")
            stock3 = input("Choose a third stock ticker (ex: TSLA) -> ")
            stock4 = input("Choose a fourth stock ticker (ex: AMZN) -> ")
            stockStr = stock + "," + stock2 + "," + stock3 + "," + stock4

        conn.request("GET", "/api/v1/markets/stock/quotes?ticker=" + stockStr, headers=headers)

        res = conn.getresponse()
        data = res.read()
        data2 = data.decode("utf-8")
        data3 = json.loads(data2)

        fiftyTwoWeekLowChange = data3["body"][0]["fiftyTwoWeekLowChange"]
        fiftyTwoWeekLowChangePercent = data3["body"][0]["fiftyTwoWeekLowChangePercent"]
        fiftyTwoWeekRange = data3["body"][0]["fiftyTwoWeekRange"]
        fiftyTwoWeekHighChange = data3["body"][0]["fiftyTwoWeekHighChange"]
        fiftyTwoWeekHighChangePercent = data3["body"][0]["fiftyTwoWeekHighChangePercent"]
        fiftyTwoWeekLow = data3["body"][0]["fiftyTwoWeekLow"]
        fiftyTwoWeekHigh = data3["body"][0]["fiftyTwoWeekHigh"]

        epsForward = data3["body"][0]["epsForward"]
        epsTrailingTwelveMonths  = data3["body"][0]["epsTrailingTwelveMonths"]
        forwardPE = data3["body"][0]["forwardPE"]
        priceToBook = data3["body"][0]["priceToBook"]
        fiftyDayAverage = data3["body"][0]["fiftyDayAverage"]
        twoHundredDayAverage = data3["body"][0]["twoHundredDayAverage"]


        if option == "2" or option == "3" or option == "4":
            fiftyTwoWeekLowChange2 = data3["body"][1]["fiftyTwoWeekLowChange"]
            fiftyTwoWeekLowChangePercent2 = data3["body"][1]["fiftyTwoWeekLowChangePercent"]
            fiftyTwoWeekRange2 = data3["body"][1]["fiftyTwoWeekRange"]
            fiftyTwoWeekHighChange2 = data3["body"][1]["fiftyTwoWeekHighChange"]
            fiftyTwoWeekHighChangePercent2 = data3["body"][1]["fiftyTwoWeekHighChangePercent"]
            fiftyTwoWeekLow2 = data3["body"][1]["fiftyTwoWeekLow"]
            fiftyTwoWeekHigh2 = data3["body"][1]["fiftyTwoWeekHigh"]

            epsForward2 = data3["body"][1]["epsForward"]
            epsTrailingTwelveMonths2 = data3["body"][1]["epsTrailingTwelveMonths"]
            forwardPE2 = data3["body"][1]["forwardPE"]
            priceToBook2 = data3["body"][1]["priceToBook"]
            fiftyDayAverage2 = data3["body"][1]["fiftyDayAverage"]
            twoHundredDayAverage2 = data3["body"][1]["twoHundredDayAverage"]

        if option == "3" or option == "4":
            fiftyTwoWeekLowChange3 = data3["body"][2]["fiftyTwoWeekLowChange"]
            fiftyTwoWeekLowChangePercent3 = data3["body"][2]["fiftyTwoWeekLowChangePercent"]
            fiftyTwoWeekRange3 = data3["body"][2]["fiftyTwoWeekRange"]
            fiftyTwoWeekHighChange3 = data3["body"][2]["fiftyTwoWeekHighChange"]
            fiftyTwoWeekHighChangePercent3 = data3["body"][2]["fiftyTwoWeekHighChangePercent"]
            fiftyTwoWeekLow3 = data3["body"][2]["fiftyTwoWeekLow"]
            fiftyTwoWeekHigh3 = data3["body"][2]["fiftyTwoWeekHigh"]

            epsForward3 = data3["body"][2]["epsForward"]
            epsTrailingTwelveMonths3 = data3["body"][2]["epsTrailingTwelveMonths"]
            forwardPE3 = data3["body"][2]["forwardPE"]
            priceToBook3 = data3["body"][2]["priceToBook"]
            fiftyDayAverage3 = data3["body"][2]["fiftyDayAverage"]
            twoHundredDayAverage3 = data3["body"][2]["twoHundredDayAverage"]

        if option == "4":
            fiftyTwoWeekLowChange4 = data3["body"][3]["fiftyTwoWeekLowChange"]
            fiftyTwoWeekLowChangePercent4 = data3["body"][3]["fiftyTwoWeekLowChangePercent"]
            fiftyTwoWeekRange4 = data3["body"][3]["fiftyTwoWeekRange"]
            fiftyTwoWeekHighChange4 = data3["body"][3]["fiftyTwoWeekHighChange"]
            fiftyTwoWeekHighChangePercent4 = data3["body"][3]["fiftyTwoWeekHighChangePercent"]
            fiftyTwoWeekLow4 = data3["body"][3]["fiftyTwoWeekLow"]
            fiftyTwoWeekHigh4 = data3["body"][3]["fiftyTwoWeekHigh"]

            epsForward4 = data3["body"][3]["epsForward"]
            epsTrailingTwelveMonths4 = data3["body"][3]["epsTrailingTwelveMonths"]
            forwardPE4 = data3["body"][3]["forwardPE"]
            priceToBook4 = data3["body"][3]["priceToBook"]
            fiftyDayAverage4 = data3["body"][3]["fiftyDayAverage"]
            twoHundredDayAverage4 = data3["body"][3]["twoHundredDayAverage"]

        if option == "1":
            print(stock)
            print("52 week low: " + str(fiftyTwoWeekLow))
            print("52 week low change: " + str(fiftyTwoWeekLowChange))
            print("52 week low change %: " + str(fiftyTwoWeekLowChangePercent))
            print("52 week high: " + str(fiftyTwoWeekHigh))
            print("52 week high change: " + str(fiftyTwoWeekHighChange))
            print("52 week high change %: " + str(fiftyTwoWeekHighChangePercent))
            print("52 week range: " + str(fiftyTwoWeekRange))
            print("EPS forward: " + str(epsForward))
            print("EPS trailing 12 months: " + str(epsTrailingTwelveMonths))
            print("Forward PE: " + str(forwardPE))
            print("50 day average: " + str(fiftyDayAverage))
            print("200 day average: " + str(twoHundredDayAverage))

            # Create a DataFrame to display the data in a table format
            # The table will have the stock name as the column names and the data as the rows
            Data = pd.DataFrame({
                stock: ["52 week low: ", "52 week low change: ", "52 week low change %: ", "52 week high: ", "52 week high change: ", "52 week high change %: ", 
                        "EPS forward: ", "EPS trailing 12 months:", "Forward PE: ", "50 day average: ", "200 day average: "],
                stock: [fiftyTwoWeekLow, fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHigh, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent, epsForward, 
                        epsTrailingTwelveMonths, forwardPE, fiftyDayAverage, twoHundredDayAverage],
            })
            print(Data)

        if option == "2":
            print(stock + ", " + stock2 + " (in this order)")
            print("52 week low: " + str(fiftyTwoWeekLow) + ", " + str(fiftyTwoWeekLow2))
            print("52 week low change: " + str(fiftyTwoWeekLowChange) + ", " + str(fiftyTwoWeekLowChange2))
            print("52 week low change %: " + str(fiftyTwoWeekLowChangePercent) + ", " + str(fiftyTwoWeekLowChangePercent2))
            print("52 week high: " + str(fiftyTwoWeekHigh) + ", " + str(fiftyTwoWeekHigh2))
            print("52 week high change: " + str(fiftyTwoWeekHighChange) + ", " + str(fiftyTwoWeekHighChange2))
            print("52 week high change %: " + str(fiftyTwoWeekHighChangePercent) + ", " + str(fiftyTwoWeekHighChangePercent2))
            print("52 week range: " + str(fiftyTwoWeekRange) + ", " + str(fiftyTwoWeekRange2))
            print("EPS forward: " + str(epsForward) + ", " + str(epsForward2))
            print("EPS trailing 12 months: " + str(epsTrailingTwelveMonths) + ", " + str(epsTrailingTwelveMonths2))
            print("Forward PE: " + str(forwardPE) + ", " + str(forwardPE2))
            print("50 day average: " + str(fiftyDayAverage) + ", " + str(fiftyDayAverage2))
            print("200 day average: " + str(twoHundredDayAverage) + ", " + str(twoHundredDayAverage2))
            
            # Create a DataFrame to display the data in a table format
            # The table will have the stock name or comparisons as the column names and the data as the rows
            Data = pd.DataFrame({
                stock + " vs. " + stock2: ["52 week low: ", "52 week low change: ", "52 week low change %: ", "52 week high: ", "52 week high change: ", "52 week high change %: ",
                                            "EPS forward: ", "EPS trailing 12 months:", "Forward PE: ", "50 day average: ", "200 day average: "],
                stock: [fiftyTwoWeekLow, fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHigh, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent, epsForward, 
                        epsTrailingTwelveMonths, forwardPE, fiftyDayAverage, twoHundredDayAverage],
                stock2: [fiftyTwoWeekLow2, fiftyTwoWeekLowChange2, fiftyTwoWeekLowChangePercent2, fiftyTwoWeekHigh2, fiftyTwoWeekHighChange2, fiftyTwoWeekHighChangePercent2, 
                        epsForward2, epsTrailingTwelveMonths2, forwardPE2, fiftyDayAverage2, twoHundredDayAverage2],
                "Difference": [fiftyTwoWeekLow - fiftyTwoWeekLow2, fiftyTwoWeekLowChange - fiftyTwoWeekLowChange2, fiftyTwoWeekLowChangePercent - fiftyTwoWeekLowChangePercent2, 
                            fiftyTwoWeekHigh - fiftyTwoWeekHigh2, fiftyTwoWeekHighChange - fiftyTwoWeekHighChange2, fiftyTwoWeekHighChangePercent - fiftyTwoWeekHighChangePercent2, 
                            epsForward - epsForward2, epsTrailingTwelveMonths - epsTrailingTwelveMonths2, forwardPE - forwardPE2, fiftyDayAverage - fiftyDayAverage2, 
                            twoHundredDayAverage - twoHundredDayAverage2],
                "% difference": [fiftyTwoWeekLow * 100 / fiftyTwoWeekLow2 - 100, fiftyTwoWeekLowChange * 100 / fiftyTwoWeekLowChange2 - 100, 
                            fiftyTwoWeekLowChangePercent * 100 / fiftyTwoWeekLowChangePercent2 - 100, fiftyTwoWeekHigh * 100 / fiftyTwoWeekHigh2 - 100, 
                            fiftyTwoWeekHighChange * 100 / fiftyTwoWeekHighChange2 - 100, fiftyTwoWeekHighChangePercent * 100 / fiftyTwoWeekHighChangePercent2 - 100,
                            epsForward * 100 / epsForward2 - 100, epsTrailingTwelveMonths * 100 / epsTrailingTwelveMonths2 - 100,  forwardPE * 100 / forwardPE2 - 100, 
                            fiftyDayAverage * 100 / fiftyDayAverage2 - 100, twoHundredDayAverage * 100 / twoHundredDayAverage2 - 100],
                "Average": [float((fiftyTwoWeekLow + fiftyTwoWeekLow2) / 2), float((fiftyTwoWeekLowChange + fiftyTwoWeekLowChange2) / 2),
                            float((fiftyTwoWeekLowChangePercent + fiftyTwoWeekLowChangePercent2) / 2),  float((fiftyTwoWeekHigh + fiftyTwoWeekHigh2) / 2), 
                            float((fiftyTwoWeekHighChange + fiftyTwoWeekHighChange2) / 2), float((fiftyTwoWeekHighChangePercent + fiftyTwoWeekHighChangePercent2) / 2), 
                            float((epsForward + epsForward2) / 2), float((epsTrailingTwelveMonths + epsTrailingTwelveMonths2) / 2), 
                            float((forwardPE + forwardPE2) / 2), float((fiftyDayAverage + fiftyDayAverage2) / 2), float((twoHundredDayAverage + twoHundredDayAverage2) / 2)]
            })
            print(Data)

        if option == "3":
            print(stock + ", " + stock2 + ", " + stock3 + " (in this order)")
            print("52 week low: " + str(fiftyTwoWeekLow) + ", " + str(fiftyTwoWeekLow2) + ", " + str(fiftyTwoWeekLow3))
            print("52 week low change: " + str(fiftyTwoWeekLowChange) + ", " + str(fiftyTwoWeekLowChange2) + ", " + str(fiftyTwoWeekLowChange3))
            print("52 week low change %: " + str(fiftyTwoWeekLowChangePercent) + ", " + str(fiftyTwoWeekLowChangePercent2) + ", " + str(fiftyTwoWeekLowChangePercent3))
            print("52 week high: " + str(fiftyTwoWeekHigh) + ", " + str(fiftyTwoWeekHigh2) + ", " + str(fiftyTwoWeekHigh3))
            print("52 week high change: " + str(fiftyTwoWeekHighChange) + ", " + str(fiftyTwoWeekHighChange2) + ", " + str(fiftyTwoWeekHighChange3))
            print("52 week high change %: " + str(fiftyTwoWeekHighChangePercent) + ", " + str(fiftyTwoWeekHighChangePercent2)  + ", " + str(fiftyTwoWeekHighChangePercent3))
            print("52 week range: " + str(fiftyTwoWeekRange)  + ", "  + str(fiftyTwoWeekRange2)  + ", "  + str(fiftyTwoWeekRange3))
            print("EPS forward: "  + str(epsForward)  + ", "  + str(epsForward2)  + ", "  + str(epsForward3))
            print("EPS trailing 12 months: "  + str(epsTrailingTwelveMonths)  + ", "  + str(epsTrailingTwelveMonths2) + ", "  + str(epsTrailingTwelveMonths3))
            print("Forward PE: "  + str(forwardPE) + ", " + str(forwardPE2) + ", " + str(forwardPE3))
            print("50 day average: "  + str(fiftyDayAverage)  + ", "  + str(fiftyDayAverage2)  + ", "  + str(fiftyDayAverage3))
            print("200 day average: "  + str(twoHundredDayAverage)  + ", "  + str(twoHundredDayAverage2)  + ", "  + str(twoHundredDayAverage3))

            # Create a DataFrame to display the data in a table format
            # The table will have the stock name or average as the column names and the data as the rows
            Data = pd.DataFrame({
                stock + " vs. " + stock2 + " vs. " + stock3: ["52 week low: ", "52 week low change: ", "52 week low change %: ", "52 week high: ", "52 week high change: ", "52 week high change %: ",
                                            "EPS forward: ", "EPS trailing 12 months:", "Forward PE: ", "50 day average: ", "200 day average: "],
                stock: [fiftyTwoWeekLow, fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHigh, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent, epsForward, 
                        epsTrailingTwelveMonths, forwardPE, fiftyDayAverage, twoHundredDayAverage],
                stock2: [fiftyTwoWeekLow2, fiftyTwoWeekLowChange2, fiftyTwoWeekLowChangePercent2, fiftyTwoWeekHigh2, fiftyTwoWeekHighChange2, fiftyTwoWeekHighChangePercent2, 
                        epsForward2, epsTrailingTwelveMonths2, forwardPE2, fiftyDayAverage2, twoHundredDayAverage2],
                stock3: [fiftyTwoWeekLow3, fiftyTwoWeekLowChange3, fiftyTwoWeekLowChangePercent3, fiftyTwoWeekHigh3, fiftyTwoWeekHighChange3, fiftyTwoWeekHighChangePercent3,
                        epsForward3, epsTrailingTwelveMonths3, forwardPE3, fiftyDayAverage3, twoHundredDayAverage3],
                "Average": [float((fiftyTwoWeekLow + fiftyTwoWeekLow2 + fiftyTwoWeekLow3) / 3),
                            float((fiftyTwoWeekLowChange + fiftyTwoWeekLowChange2 + fiftyTwoWeekLowChange3) / 3),
                            float((fiftyTwoWeekLowChangePercent + fiftyTwoWeekLowChangePercent2 + fiftyTwoWeekLowChangePercent3) / 3), 
                            float((fiftyTwoWeekHigh + fiftyTwoWeekHigh2 + fiftyTwoWeekHigh3) / 3), 
                            float((fiftyTwoWeekHighChange + fiftyTwoWeekHighChange2 + fiftyTwoWeekHighChange3) / 3),
                            float((fiftyTwoWeekHighChangePercent + fiftyTwoWeekHighChangePercent2 + fiftyTwoWeekHighChangePercent3) / 3), 
                            float((epsForward + epsForward2 + epsForward3) / 3), 
                            float((epsTrailingTwelveMonths + epsTrailingTwelveMonths2 + epsTrailingTwelveMonths3) / 3), 
                            float((forwardPE + forwardPE2 + forwardPE3) / 3), 
                            float((fiftyDayAverage + fiftyDayAverage2 + fiftyDayAverage3) / 3), 
                            float((twoHundredDayAverage + twoHundredDayAverage2 + twoHundredDayAverage3) / 3)]
            })
            print(Data)

        if option == "4":
            print(stock + ", " + stock2 + ", " + stock3 + ", " + stock4 + " (in this order)")
            print("52 week low: " + str(fiftyTwoWeekLow) + ", " + str(fiftyTwoWeekLow2) + ", " + str(fiftyTwoWeekLow3) + ", " + str(fiftyTwoWeekLow4))
            print("52 week low change: " + str(fiftyTwoWeekLowChange) + ", " + str(fiftyTwoWeekLowChange2) + ", " + str(fiftyTwoWeekLowChange3) + ", " + str(fiftyTwoWeekLowChange4))
            print("52 week low change %: " + str(fiftyTwoWeekLowChangePercent) + ", " + str(fiftyTwoWeekLowChangePercent2) + ", " + str(fiftyTwoWeekLowChangePercent3)  + ", "  +
                str(fiftyTwoWeekLowChangePercent4))
            print("52 week high: "  + str(fiftyTwoWeekHigh)  + ", "  + str(fiftyTwoWeekHigh2)  + ", "  + str(fiftyTwoWeekHigh3)  + ", "  + str(fiftyTwoWeekHigh4))
            print("52 week high change: "  + str(fiftyTwoWeekHighChange)  + ", "  + str(fiftyTwoWeekHighChange2)  + ", " + str(fiftyTwoWeekHighChange3) + ", " + str(fiftyTwoWeekHighChange4))
            print("52 week high change %: " + str(fiftyTwoWeekHighChangePercent) + ", "  + str(fiftyTwoWeekHighChangePercent2)  + ", "  + str(fiftyTwoWeekHighChangePercent3)  + ", "  +
                str(fiftyTwoWeekHighChangePercent4))
            print("52 week range: "  + str(fiftyTwoWeekRange)  + ", "  + str(fiftyTwoWeekRange2)  + ", "  + str(fiftyTwoWeekRange3)  + ", "  + str(fiftyTwoWeekRange4))
            print("EPS forward: "  + str(epsForward)  + ", "  + str(epsForward2)  + ", "  + str(epsForward3)  + ", "  + str(epsForward4))
            print("EPS trailing 12 months: " + str(epsTrailingTwelveMonths) + ", " + str(epsTrailingTwelveMonths2) + ", " + str(epsTrailingTwelveMonths3) + ", " + str(epsTrailingTwelveMonths4))
            print("Forward PE: " + str(forwardPE) + ", " + str(forwardPE2) + ", " + str(forwardPE3) + ", " + str(forwardPE4))
            print("50 day average: " + str(fiftyDayAverage) + ", " + str(fiftyDayAverage2) + ", " + str(fiftyDayAverage3) + ", " + str(fiftyDayAverage4))
            print("200 day average: " + str(twoHundredDayAverage) + ", " + str(twoHundredDayAverage2) + ", " + str(twoHundredDayAverage3) + ", " + str(twoHundredDayAverage4))

            # Create a DataFrame to display the data in a table format
            # The table will have the stock name or average as the column names and the data as the rows
            Data = pd.DataFrame({
                f"{stock} vs. {stock2} vs. {stock3} vs. {stock4}": ["52 week low: ", "52 week low change: ", "52 week low change %: ", "52 week high: ", "52 week high change: ", 
                                                                       "52 week high change %: ", "EPS forward: ", "EPS trailing 12 months:", "Forward PE: ", "50 day average: ", 
                                                                       "200 day average: "],
                stock: [fiftyTwoWeekLow, fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekHigh, fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent, epsForward, 
                        epsTrailingTwelveMonths, forwardPE, fiftyDayAverage, twoHundredDayAverage],
                stock2: [fiftyTwoWeekLow2, fiftyTwoWeekLowChange2, fiftyTwoWeekLowChangePercent2, fiftyTwoWeekHigh2, fiftyTwoWeekHighChange2, fiftyTwoWeekHighChangePercent2, 
                        epsForward2, epsTrailingTwelveMonths2, forwardPE2, fiftyDayAverage2, twoHundredDayAverage2],
                stock3: [fiftyTwoWeekLow3, fiftyTwoWeekLowChange3, fiftyTwoWeekLowChangePercent3, fiftyTwoWeekHigh3, fiftyTwoWeekHighChange3, fiftyTwoWeekHighChangePercent3,
                        epsForward3, epsTrailingTwelveMonths3, forwardPE3, fiftyDayAverage3, twoHundredDayAverage3],
                stock4: [fiftyTwoWeekLow4, fiftyTwoWeekLowChange4, fiftyTwoWeekLowChangePercent4, fiftyTwoWeekHigh4, fiftyTwoWeekHighChange4, fiftyTwoWeekHighChangePercent4,
                        epsForward4, epsTrailingTwelveMonths4, forwardPE4, fiftyDayAverage4, twoHundredDayAverage4],
                "Average": [float((fiftyTwoWeekLow + fiftyTwoWeekLow2 + fiftyTwoWeekLow3 + fiftyTwoWeekLow4) / 4), 
                            float((fiftyTwoWeekLowChange + fiftyTwoWeekLowChange2 + fiftyTwoWeekLowChange3 + fiftyTwoWeekLowChange4) / 4),
                            float((fiftyTwoWeekLowChangePercent + fiftyTwoWeekLowChangePercent2 + fiftyTwoWeekLowChangePercent3 + fiftyTwoWeekLowChangePercent4) / 4), 
                            float((fiftyTwoWeekHigh + fiftyTwoWeekHigh2 + fiftyTwoWeekHigh3 + fiftyTwoWeekHigh4) / 4), 
                            float((fiftyTwoWeekHighChange + fiftyTwoWeekHighChange2 + fiftyTwoWeekHighChange3 + fiftyTwoWeekHighChange4) / 4),
                            float((fiftyTwoWeekHighChangePercent + fiftyTwoWeekHighChangePercent2 + fiftyTwoWeekHighChangePercent3 + fiftyTwoWeekHighChangePercent4) / 4), 
                            float((epsForward + epsForward2 + epsForward3 + epsForward4) / 4), 
                            float((epsTrailingTwelveMonths + epsTrailingTwelveMonths2 + epsTrailingTwelveMonths3 + epsTrailingTwelveMonths4) / 4), 
                            float((forwardPE + forwardPE2 + forwardPE3 + forwardPE4) / 4), 
                            float((fiftyDayAverage + fiftyDayAverage2 + fiftyDayAverage3 + fiftyDayAverage4) / 4), 
                            float((twoHundredDayAverage + twoHundredDayAverage2 + twoHundredDayAverage3 + twoHundredDayAverage4) / 4)]
            })
            print(Data)

    user_input = input("Would you like to chat with Google Gemini (gemini) or analyze stocks (stocks) ? type q to quit -> ")

# Close the program if the user types "q"
print("Thank you for using this program. Have a nice day!")
