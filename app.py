from flask import Flask
import pandas as pd
import string
import re
from flask import jsonify
df = pd.read_csv('kano-data.csv',header= 1, low_memory=False)

# subsett = df[df['Settlement Name'].str.title().str.strip() == 'Badume']
# anc_cols = subsett.columns[subsett.columns.str.contains('ANC')]
# df_anc = subsett[anc_cols]
# df_anc.head()
# provider_name = df_anc.iloc[0, 0]
# phone_number = df_anc.iloc[0, 1]
# output_string = f"ANC Provider: {provider_name.title()} \nContact: {phone_number}"
# print(output_string)


# def anc(settlement_name):
#     subsett = df[df['Settlement Name'].str.title().str.strip() == settlement_name.title()] 
#     anc_cols = subsett.columns[subsett.columns.str.contains('ANC')]  
#     df_anc = subsett[anc_cols]
    
#     if df_anc.empty:
#         return "Not available"  
    
#     provider_name = df_anc.iloc[0, 0]  
#     phone_number = df_anc.iloc[0, 1]   
    
    
#     if not isinstance(provider_name, str) or provider_name.strip() == '' or re.match(r'\d', provider_name) or provider_name in ['NIL', 'N/A']:
#         provider_name = "Not available"
#     else:
#         provider_name = provider_name.title()
    

#     if pd.isna(phone_number) or phone_number == 0 or re.match(r'[^\d]', str(phone_number)):
#         phone_number = "Not available"
#     else:
#         phone_number #= str(int(phone_number))  
    
#     output_string = f"ANC Provider: {provider_name} \nContact: {phone_number}"
#     return output_string


# #-----------------------------------
# import pandas as pd
# import string
# import re
# from flask import jsonify

# df = pd.read_csv('kano-data.csv',header= 1, low_memory=False)
# def anc(health_facility):
#     subsett = df[df['Health Facility'].str.title().str.strip() == health_facility.title()]
#     anc_cols = subsett.columns[subsett.columns.str.contains('ANC')]
#     df_anc = subsett[anc_cols]
    
#     if df_anc.empty:
#         return "Not available"
    
#     provider_name = df_anc.iloc[0, 0]  
#     phone_number = df_anc.iloc[0, 1] 
    
#     provider_name = "Not available" if not isinstance(provider_name, str) or provider_name.strip() == '' or re.match(r'\d', str(provider_name)) or provider_name in ['NIL', 'N/A'] else provider_name.title()
#     phone_number = "Not available" if pd.isna(phone_number) or phone_number == 0 or re.match(r'[^\d]', str(phone_number)) else phone_number
    
#     return f"ANC Provider: {provider_name} \nContact: {phone_number}"


# health_facility = 'Badume Mphc'
# result = anc(health_facility)
# print(result)



app = Flask(__name__)


## LGA's
@app.route('/lgas')
def lgas():
     lg= []
     for i in df['LGA'].unique():
          if isinstance(i, str):
               clean = i.strip().title()
               if not re.search(r'\d', clean) and clean not in lg:
                    lg.append(clean)
     lg.sort()
     lg.append('Go Back')
     return jsonify(lg)

## -- Optimized lgas() function:
# def lgas():
#     lg = sorted(list({i.strip().title() for i in df['LGA'].unique() if isinstance(i, str) and not re.search(r'\d', i.strip())}))
#     lg.append('Go Back')
#     return jsonify(lg)


#done
# ---WARDS
@app.route('/lga/<lga>')
def wards(lga):
     lga = lga.lower()
     wards = []
     subsett = df[df['LGA'].str.lower().str.strip() == lga]
     for i in subsett['Ward Name'].unique():
          if isinstance(i, str):
               clean = i.strip().title()
               if clean not in wards:
                    wards.append(clean)
     wards.sort()
     wards.append('Go Back')
     return jsonify(wards)


#done
# ---HEALTH FACILITIES
@app.route('/lga/ward/<ward>')
def health_centers(ward):
     ward = ward.lower()
     health_centers = []
     subsett = df[df['Ward Name'].str.lower().str.strip() == ward]
     for i in subsett['Health Facility'].unique():
          if isinstance(i, str):
               clean = i.strip().title()
               if clean not in health_centers:
                    health_centers.append(clean)
     health_centers.sort()
     health_centers.append('Go Back')
     return jsonify(health_centers)



#done
# ---SETTLEMENT LIST
@app.route('/lga/ward/healthfacility/<healthfacility>')
def settlement(healthfacility):
     healthfacility = healthfacility.lower()
     settlements = []
     subsett = df[df['Health Facility'].str.lower().str.strip() == healthfacility]
     for i in subsett['Settlement Name'].unique():
          if isinstance(i, str):
               clean = i.strip().title()
               if clean not in settlements:
                    settlements.append(clean)
     settlements.sort()
     settlements.append('Go Back')
     return jsonify(settlements)


#done
# ---ANC PROVIDER
@app.route('/lga/ward/<healthfacility>/anc')
def anc(healthfacility):
     healthfacility = healthfacility.lower()
     subsett = df[df['Health Facility'].str.lower().str.strip() == healthfacility]
     anc_cols = subsett.columns[subsett.columns.str.contains('ANC')]
     df_anc = subsett[anc_cols]
    
     if df_anc.empty:
          return "Not available"

     provider_name = df_anc.iloc[0, 0]  
     phone_number = df_anc.iloc[0, 1] 

     provider_name = "Not available" if not isinstance(provider_name, str) or provider_name.strip() == '' or re.match(r'\d', str(provider_name)) or provider_name in ['NIL', 'N/A'] else provider_name.title()
     phone_number = "Not available" if pd.isna(phone_number) or phone_number == 0 or re.match(r'[^\d]', str(phone_number)) else phone_number

     f_string = f"ANC Provider: {provider_name} <br> Contact: {phone_number}"
     return f_string


#done
# ---LABOUR AND DELIVERY PROVIDER
@app.route('/lga/ward/<healthfacility>/delivery')
def delivery(healthfacility):
     healthfacility = healthfacility.lower()
     subsett = df[df['Health Facility'].str.lower().str.strip() == healthfacility]
     del_cols = subsett.columns[subsett.columns.str.contains('Delivery')]
     df_del = subsett[del_cols]
    
     if df_del.empty:
          return "Not available"

     provider_name = df_del.iloc[0, 0]  
     phone_number = df_del.iloc[0, 1] 

     provider_name = "Not available" if not isinstance(provider_name, str) or provider_name.strip() == '' or re.match(r'\d', str(provider_name)) or provider_name in ['NIL', 'N/A'] else provider_name.title()
     phone_number = "Not available" if pd.isna(phone_number) or phone_number == 0 or re.match(r'[^\d]', str(phone_number)) else phone_number

     f_string = f"Labour and Delivery Provider: {provider_name} <br> Contact: {phone_number}"
     return f_string



#done
# ---FAMILY PLANNING PROVIDER
@app.route('/lga/ward/<healthfacility>/family')
def family(healthfacility):
     healthfacility = healthfacility.lower()
     subsett = df[df['Health Facility'].str.lower().str.strip() == healthfacility]
     fam_cols = subsett.columns[subsett.columns.str.contains('Family')]
     df_fam = subsett[fam_cols]
    
     if df_fam.empty:
          return "Not available"

     provider_name = df_fam.iloc[0, 0]  
     phone_number = df_fam.iloc[0, 1] 

     provider_name = "Not available" if not isinstance(provider_name, str) or provider_name.strip() == '' or re.match(r'\d', str(provider_name)) or provider_name in ['NIL', 'N/A'] else provider_name.title()
     phone_number = "Not available" if pd.isna(phone_number) or phone_number == 0 or re.match(r'[^\d]', str(phone_number)) else phone_number

     f_string = f"Family Planning Provider: {provider_name} <br> Contact: {phone_number}"
     return f_string



#done
# ---COMMUNITY MOBILIZER
@app.route('/lga/ward/<healthfacility>/mobilizer')
def mobilizer(healthfacility):
     healthfacility = healthfacility.lower()
     subsett = df[df['Health Facility'].str.lower().str.strip() == healthfacility]
     mob_cols = subsett.columns[subsett.columns.str.contains('mobilizer')]
     df_mob = subsett[mob_cols]
    
     if df_mob.empty:
          return "Not available"

     provider_name = df_mob.iloc[0, 0]  
     designation = df_mob.iloc[0, 1] 

     provider_name = "Not available" if not isinstance(provider_name, str) or provider_name.strip() == '' or re.match(r'\d', str(provider_name)) or provider_name in ['NIL', 'N/A'] else provider_name.title()
     designation = "Not available" if not isinstance(designation, str) or designation.strip() == '' or re.match(r'\d', str(designation)) or designation in ['NIL', 'N/A'] else designation.title()
     
     f_string = f"Community Mobilizer: {provider_name} <br> Designation & Organization: {designation}"
     return f_string



if __name__ == '__main__':
     app.run(debug=True)















#---------------------------------------------
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


# if __name__ == '__main__':
#      app.run(debug=True)