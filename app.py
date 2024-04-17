from flask import Flask
import pandas as pd
import string
from flask import jsonify
data_csv = pd.read_csv('new_data.csv',low_memory=False)
frame = pd.DataFrame(data_csv)
frame = frame.applymap(lambda x: str(x).replace("/","").replace("'",""))

app = Flask(__name__)

#done
@app.route('/lgas')    
def lgas():
    unique_lga = frame['LGA'].unique().tolist()
    unique_lga.append('go back')
    while ('nan' in unique_lga):
        unique_lga.remove('nan')
    while ('NaN' in unique_lga):
        unique_lga.remove('NaN')
    while ('Nan' in unique_lga):
        unique_lga.remove('Nan')
    for i in range(len(unique_lga)):
        unique_lga[i] = unique_lga[i].capitalize()
    return jsonify(unique_lga)

#done
@app.route('/lga/<lga>')    
def ward(lga):
    lga = lga[0].lower() + lga[1:]
    associated_wards = frame[frame['LGA'] == lga]['Ward'].unique().tolist()
    associated_wards.append('go back')
    while ('nan' in associated_wards):
        associated_wards.remove('nan')
    while ('NaN' in associated_wards):
        associated_wards.remove('NaN')
    while ('Nan' in associated_wards):
        associated_wards.remove('Nan')
    for i in range(len(associated_wards)):
        associated_wards[i] = associated_wards[i].capitalize()
    return jsonify(associated_wards)

# #done
# @app.route('/lga/ward/<ward>')    
# def hospitals(ward):
#     ward = ward[0].lower() + ward[1:]
#     associated_hospitals = frame[data_csv['Ward'] == ward]['Health Facility'].unique().tolist()
#     while 'nan' in associated_hospitals:
#         associated_hospitals.remove('nan')
#     while 'NaN' in associated_hospitals:
#         associated_hospitals.remove('NaN')
#     while ('Nan' in associated_hospitals):
#         associated_hospitals.remove('Nan')
#     associated_hospitals.append('go back')
#     for i in range(len(associated_hospitals)):
#         associated_hospitals[i] = associated_hospitals[i].capitalize()
#     return associated_hospitals

# #done
# @app.route('/lga/ward/hospital/<hospital>/status')    
# def hospital_status(hospital):
#     hospital = hospital[0].lower() + hospital[1:]
#     specific_clinic_rows = frame[frame['Health Facility'] == hospital]
#     ownership = specific_clinic_rows['Ownership (Public/Private)'].unique()[0]
#     facility_type = specific_clinic_rows['Facility Type (Primary/Secondary/Tertiary)'].unique()[0]
#     formatted_string = f'Ownership: {ownership} <br> Facility Type: {facility_type}'
#     return formatted_string

# #done
# @app.route('/lga/ward/hospital/<hospital>/humanResources')    
# def hospital_resources(hospital):
#     hospital = hospital[0].lower() + hospital[1:]
#     specific_clinic_rows = frame[frame['Health Facility'] == hospital]
#     columns = ['OFFICER IN CHARGE','PHONE Number 0','Permanent Technical Staff',
#                'Adhoc Technical Staff (BHCPF, LGA, etc)','Volunteer Technical Staff','Permanent Non-Technical Staff',
#                'Name of Ward CE Focal Persion', 'Phone Number 3']

#     data = ""
#     x = 0
#     for column in columns:
#         if str(specific_clinic_rows.iloc[0][column]) != 'NaN' and str(specific_clinic_rows.iloc[0][column]) != 'nan' \
#         and str(specific_clinic_rows.iloc[0][column]) != 'Nan':
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: ' + str(specific_clinic_rows.iloc[0][column]) + '<br><br>'
#             elif x == 0 or x == 6:
#                 data += column + ': ' + str(specific_clinic_rows.iloc[0][column]) + "\t"
#             else:
#                 data += column + ': ' + str(specific_clinic_rows.iloc[0][column]) + '<br><br>'
#         else:
#             data += column + ': This information is currently not available' + '<br><br>'
#         x+=1
#     return data


# #done
# @app.route('/lga/ward/hospital/<hospital>/settlementlist')    
# def settlements(hospital):
#     hospital = hospital[0].lower() + hospital[1:]
#     settlements = frame[frame['Health Facility'] == hospital]['Settlement'].unique().tolist()
#     settlements.append('go back')
#     for i in range(len(settlements)):
#         settlements[i] = settlements[i].capitalize()
#     return settlements

# #done
# @app.route('/lga/ward/hospital/settlement/population/<settlement>')    
# def settlement_population(settlement):
#     settlement = settlement[0].lower() + settlement[1:]
#     settlement_info = data_csv[data_csv['Settlement'] == settlement].loc[:,'Total Population of the Settlement':'Mentally Challenged']
#     data = ""
#     for column in settlement_info.columns.tolist():
#         if str(settlement_info[column].tolist()[0]) != 'NaN' and str(settlement_info[column].tolist()[0]) != 'nan' \
#             and str(settlement_info[column].tolist()[0]) != 'Nan':
#             data += column + ': ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#         else:
#             data += column + ': This information is currently not available' + '<br><br>'
#     return data

# #done
# @app.route('/lga/ward/hospital/settlement/profile/<settlement>')    
# def settlement_profile(settlement):
#     settlement = settlement[0].lower() + settlement[1:]
#     settlement_info = frame[frame['Settlement'] == settlement]
#     columns = ['HTR (Yes/No)','Security compromised (Yes/No)','Name of Mai Unguwa', 
#     'Phone Number 1','Name of Primary school/Quranic & Ismamic School',
#     'Church/Mosque','Market/Play ground','Name of Community Volunteer',
#     'Phone Number 2', 'Distance to Health Facility (Km)']
#     data = ""
#     x = 0
#     for column in columns:
#         if str(settlement_info[column].tolist()[0]) != 'NaN' and str(settlement_info[column].tolist()[0]) != 'nan' \
#             and str(settlement_info[column].tolist()[0]) != 'Nan':
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#             elif x == 0 or x == 6:
#                 data += column + ': ' + str(settlement_info[column].tolist()[0]) + "\t"
#             else:
#                 data += column + ': ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#         else:
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: This information is currently not available' + '<br><br>'
#             else:
#                 data += column + ': This information is currently not available' + '<br><br>'
#         x+=1
#     return data

# #done
# @app.route('/lga/ward/hospital/settlement/immune/<settlement>')    
# def settlement_immune(settlement):
#     settlement = settlement[0].lower() + settlement[1:]
#     settlement_info = frame[frame['Settlement'] == settlement].loc[:,'BCG':'Safety boxes']
#     data = ""
#     for column in settlement_info.columns.tolist():
#         if str(settlement_info[column].tolist()[0]) != 'NaN' and str(settlement_info[column].tolist()[0]) != 'nan'\
#             and str(settlement_info[column].tolist()[0]) != 'Nan':
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#             else:
#                 data += column + ': ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#         else:
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: This information is currently not available' + '<br><br>'
#             else:
#                 data += column + ': This information is currently not available' + '<br><br>'
#     return data

# #done
# @app.route('/lga/ward/hospital/settlement/family/<settlement>')    
# def settlement_family(settlement):
#     settlement = settlement[0].lower() + settlement[1:]
#     settlement_info = frame[frame['Settlement'] == settlement].loc[:,'MINI PILLS':'NORTISTERAT INJ']
#     data = ""
#     for column in settlement_info.columns.tolist():
#         if str(settlement_info[column].tolist()[0]) != 'NaN' and str(settlement_info[column].tolist()[0]) != 'nan' \
#            and  str(settlement_info[column].tolist()[0]) != 'Nan':
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#             else:
#                 data += column + ': ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#         else:
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: This information is currently not available' + '<br><br>'
#             else:
#                 data += column + ': This information is currently not available' + '<br><br>'
#     return data

# #done
# @app.route('/lga/ward/hospital/settlement/malaria/<settlement>')    
# def settlement_malaria(settlement):
#     settlement = settlement[0].lower() + settlement[1:]
#     settlement_info = frame[frame['Settlement'] == settlement].loc[:,'RDT FOR MALARIA':'Vit-A']
#     data = ""
#     for column in settlement_info.columns.tolist():
#         if str(settlement_info[column].tolist()[0]) != 'NaN' and str(settlement_info[column].tolist()[0]) != 'nan' \
#             and str(settlement_info[column].tolist()[0]) != 'Nan':
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#             else:
#                 data += column + ': ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#         else:
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: This information is currently not available' + '<br><br>'
#             else:
#                 data += column + ': This information is currently not available' + '<br><br>'
#     return data

# #done
# @app.route('/lga/ward/hospital/settlement/consumables/<settlement>')    
# def settlement_consumables(settlement):
#     settlement = settlement[0].lower() + settlement[1:]
#     settlement_info = frame[frame['Settlement'] == settlement].loc[:,'COTTON WOOL 100G (1 per HF)':'TABLE NAPKIN (ROLL)']
#     data = ""
#     for column in settlement_info.columns.tolist():
#         if str(settlement_info[column].tolist()[0]) != 'NaN' and str(settlement_info[column].tolist()[0]) != 'nan' \
#             and str(settlement_info[column].tolist()[0]) != 'Nan':
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#             else:
#                 data += column + ': ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#         else:
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: This information is currently not available' + '<br><br>'
#             else:
#                 data += column + ': This information is currently not available' + '<br><br>'
#     return data


# #done
# @app.route('/lga/ward/hospital/settlement/factools/<settlement>')    
# def settlement_factools(settlement):
#     settlement = settlement[0].lower() + settlement[1:]
#     settlement_info = frame[frame['Settlement'] == settlement].loc[:,'OPD REGISTER (1 per HF)':'Envelopes']
#     data = ""
#     for column in settlement_info.columns.tolist():
#         if str(settlement_info[column].tolist()[0]) != 'NaN' and str(settlement_info[column].tolist()[0]) != 'nan' \
#             and str(settlement_info[column].tolist()[0]) != 'Nan':
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#             else:
#                 data += column + ': ' + str(settlement_info[column].tolist()[0]) + '<br><br>'
#         else:
#             if 'phone number' in column.lower(): 
#                 data += 'phone number: This information is currently not available' + '<br><br>'
#             else:
#                 data += column + ': This information is currently not available' + '<br><br>'
#     return data


if __name__ == '__main__':
     app.run(debug=True)