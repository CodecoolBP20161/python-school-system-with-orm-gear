import random


class Code():

    def generate_code(self, list_of_applicants):
        for applicant in list_of_applicants:
            list_of_codes = []
            for appl in list_of_applicants:
                if appl.code:
                    list_of_codes.append(appl.code)
            while True:
                if not applicant.code:
                    if applicant.school == "Budapest":
                        code_generated = "bp"
                    elif applicant.school == "Miskolc":
                        code_generated = "mi"
                    elif applicant.school == "Krakow":
                        code_generated = "kr"
                for i in range(3):
                    j = random.randrange(0, 10)
                    code_generated += str(j)
                if code_generated not in list_of_codes:
                    break
            applicant.code = code_generated
