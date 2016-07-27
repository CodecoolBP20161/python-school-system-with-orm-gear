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

# def gen_code(l):
#     while True:
#         code_generated = "bp"
#         for i in range(1):
#             j = random.randrange(0, 10)
#             code_generated += str(j)
#         if code_generated not in l:
#             break
#     return code_generated
#
# l = ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7']
# print(gen_code(l))
