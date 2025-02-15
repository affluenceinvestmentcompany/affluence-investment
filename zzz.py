plan = 'Basic'

def bonus(amount):
    plan_bonuses = {'Basic': 0.5, 'Standard': 1.0, 'Premium': 1.2, 'Ultimate': 1.5}
    return int(amount) * plan_bonuses.get(plan, 0) / 100

result = bonus(1000)
print(result)
            
            
# def percentage(part, whole):
#     return 100 * float(part) / float(whole)

# def calculate_percent(percent, number):
#     return percentage(percent, number) / 100 * number

# result = calculate_percent(0.5, 200)
# print(result) 