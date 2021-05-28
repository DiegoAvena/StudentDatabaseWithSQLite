import re

'''

Handles all of the validation of 
data that gets placed into the 
Student table, such as cleaning up 
the phone number, getting valid zip codes, etc.

'''
class InputManager:

    # code for cleaning up phone number from canvas example
    def cleanUpPhoneNumber(self, phoneNumberToClean):
        # remove the extension:
        extensionIndex = phoneNumberToClean.find("x")
        phoneNumberToClean = phoneNumberToClean[:extensionIndex] if extensionIndex != -1 else phoneNumberToClean

        #remove non number characters:
        phoneNumberToClean = re.sub(r'\D', '', phoneNumberToClean)

        # take care of international phone numbers by grabbing the last 10 digits:
        if (len(phoneNumberToClean) > 10):
            phoneNumberToClean = phoneNumberToClean[-10:]

        return phoneNumberToClean

    def obtainPhoneNumber(self, userPrompt):
        while True:
            rawPhoneNumber = self.obtainText(userPrompt)
            cleanedUpPhoneNumber = self.cleanUpPhoneNumber(rawPhoneNumber)
            if (len(cleanedUpPhoneNumber) > 0):
                if (len(cleanedUpPhoneNumber) >= 10):
                    return cleanedUpPhoneNumber
                else:
                    print("The number you entered is too short to be a phone number, try again.")
            else:
                print("You did not enter a phone number, try again.")


    def obtainZipCode(self, userPrompt):
        while True:
            rawZipCode = self.obtainTextWithSpecificLength(userPrompt, 5)

            # make sure the raw zip only has numerical digits in it:
            rawZipCode = re.sub(r'\D', '', rawZipCode)
            if (len(rawZipCode) == 5):
                return rawZipCode
            else:
                print("Sorry, but the zip code must only contain numerical values")

    def obtainTextWithSpecificLength(self, userPrompt, specificLength):
        while True:
            rawUserInput = input(userPrompt)
            if (len(rawUserInput) > 0):

                if (len(rawUserInput) == specificLength):
                    return rawUserInput
                else:
                    print("This field must have a length of " + str(specificLength))
            else:
                print("This field cannot be left blank")

    def obtainText(self, userPrompt):
        while True:
            rawUserInput = input(userPrompt)
            if (len(rawUserInput) > 0):
                return rawUserInput

            print("This field cannot be left blank")

    def obtainDecimalNumber(self, userPrompt, min):
        while True:
            rawUserInput = input(userPrompt)
            try:
                cleanedUpUserInput = float(rawUserInput)
                if (cleanedUpUserInput < min):
                    print("This value must be larger than or equal to " + str(min))
                else:
                    return cleanedUpUserInput
            except ValueError:
                print("Please enter a numeric value")