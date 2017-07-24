import csv

results = []

def getPatientsForHospital():

    def compute_patients_for_row(row):
        try:
            patients = int(row['Diabetes patients (BA)'])
            type2PercentIns = float(row['% Diabetes Type 2 - insulin'])
            type2PercentNonIns = float(row['% Diabetes Type 2 - non insulin'])
            type2PercentDiet = float(row['% Diabetes Type 2 - diet only'])
            type2Percent = type2PercentIns + type2PercentDiet + type2PercentNonIns
            type2Percent = type2Percent / 100.0
            totPatients = int(patients * type2Percent)
            print totPatients
            return totPatients
        except:
            return ""

    def save():
        with open('/Users/Jake/Documents/Warwick/urss/data/diabetes/2016_data_formatted.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|')
            for result in results:
                writer.writerow([result['code'], result['patients']])
        return

    with open('/Users/Jake/Documents/Warwick/urss/data/diabetes/nati-diab-inp-audi-16-open-data.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            patients = compute_patients_for_row(row)
            results.append({"code":row['Provider Code'], "patients": patients})
        save()

getPatientsForHospital()
