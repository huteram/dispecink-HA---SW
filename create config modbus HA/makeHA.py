import pandas as pd
import yaml
import json
import MyPkg.MujSoubor as MujSoubor

def uniqueName(strName):
    # replace all strange 
    strName = strName.replace(" ","_")
    strName = strName.replace("-","_")
    strName = strName.replace("+","_")
    strName = strName.replace(";","_")
    strName = strName.replace(".","_")
    strName = strName.strip("_")
    strName = strName
    return strName.lower()

def Name(strName):
    # replace all strange 
    strName = strName.replace("_"," ")
    strName = strName.replace("-"," ")
    strName = strName.replace("+"," ")
    strName = strName.replace(";"," ")
    strName = strName.replace("."," ")
    strName = strName.strip(" ")
    strName = strName
    return strName

def modbusName(strName):
    # replace all strange 
    strName = strName.replace("_"," ")
    strName = strName.replace("-"," ")
    strName = strName.replace("+"," ")
    strName = strName.replace(";"," ")
    strName = strName.replace("."," ")
    strName = strName.strip(" ")
    return strName

def modbusUniqueName(strName):
    # replace all strange 
    strName = strName.replace(" ","_")
    strName = strName.replace("-","_")
    strName = strName.replace("+","_")
    strName = strName.replace(";","_")
    strName = strName.replace(".","_")
    strName = strName.strip("_")
    strName = strName
    return strName.lower()


xx = MujSoubor.Soubor()

configDir = "\\nodesConfig\\*.xlsx"

Files = xx.ListFiles(configDir,True)

yamlFile = ""

# === BUILD FINAL YAML ===
modbus_config = []
grid = {}
view = {
        "type": "sections",
        "sections":[]            
    }
template = {}

for File in Files:

    # === LOAD EXCEL ===
    file_path = File

    df_konfig = pd.read_excel(file_path, sheet_name="Konfig")
    df_ip = pd.read_excel(file_path, sheet_name="IPaddress")
    df_veliciny = pd.read_excel(file_path, sheet_name="Veliciny")
    df_jednotky = pd.read_excel(file_path, sheet_name="Jednotky")

    # === CLEAN DATA ===
    df_ip["Node"] = df_ip["Node"].str.strip()
    df_konfig["Node"] = df_konfig["Node"].str.strip()

    # merge tables
    df = pd.merge(df_konfig, df_ip, on="Node", how="left")
    df = pd.merge(df, df_veliciny, on="qname", how="left")
    df = pd.merge(
                    df,
                    df_jednotky,
                    left_on="defaultJednotky",
                    right_on="symbol",
                    how="left"
                )

    # === FORMAT MAPPING ===
    def map_format(fmt):
        if fmt == "UINT16":
            return {"data_type": "uint16", "count": 1}
        elif fmt == "SINT16":
            return {"data_type": "int16", "count": 1}
        elif fmt == "SwappedFloat":
            return {"data_type": "float32", "count": 2}
        elif fmt == "MaskedBool":
            return {"data_type": "coil", "count": 1}
        else:
            return {"data_type": "uint16", "count": 1}

    # === GROUP BY DEVICE ===
    devices = {}

    

    for _, row in df.iterrows():
        node = row["Node"]
        ip = row["IP"]

        if ip == "XXX" or pd.isna(ip):
            continue

        if node not in devices:
            devices[node] = {
                "type": "tcp",
                "host": ip,
                "port": 502,
                "delay": 60,
                "sensor": []
            }
            grid[node] = {
                "type": "grid",
                "cards":[{
                    "type": "heading",
                    "heading": node,
                    "heading_style": "title"
                }]
            }

        fmt = map_format(row["Format"])
    
        
        
    #modbus config creation
        if fmt["data_type"] == "coil":
            Address = int(str(row["Address"])[1:])-1
            row["Address"] = Address
            binary_sensors = {
            "name": Name(f"{node}_{row['qname']}"),
            "address": Address,
            "input_type": "coil",
            "unique_id": uniqueName(f"{node}_{row['qname']}")
            }
            if "binary_sensor" not in devices[node]:
                devices[node]["binary_sensor"] = []
            if "binary_sensor" not in template:
                template["binary_sensor"] = []
            devices[node]["binary_sensor"].append(binary_sensors)
            
        #panel view creation
            grid[node]["cards"].append({
                        "type": "tile",
                        "entity": f"binary_sensor.{uniqueName(f"{node}_{row['qname']}").lower()}",        
                        "features_position": "bottom",
                        "vertical": 0,
                        "grid_options":{"columns": "full"}
            })       
            
        # create template variables
            State = f"is_state('binary_sensor.{uniqueName(f"{node}_{row['qname']}")}', 'on')"
            attributes = {}
            attributes = {k: str(v) for k, v in row.items() 
                            if pd.notna(v) and not str(v).startswith(" ")}
            attributes["Address"] = str(int(attributes["Address"][1:])-1)

            template["binary_sensor"].append({
                "name": modbusName(f"{node}_{row['qname']}"),
                "state": f"{{{{ {State} }}}}",
                "unique_id": modbusUniqueName(f"{node}_{row['qname']}"),
                "attributes": attributes
            })     

        else:
            Scale = 1
            if pd.to_numeric(row["Scale"], errors='coerce'):
                if row["Scale"] != 0:
                    Scale = 1 / row["Scale"]
                    
            sensor = {
                "name": Name(f"{node}_{row['qname']}"),
                "address": int(str(row["Address"])[1:])-1,
                "input_type": "holding",
                "data_type": fmt["data_type"],
                "scale": Scale,
                "precision": 2,
                "device_class":  "area",
                "unique_id": uniqueName(f"{node}_{row['qname']}"),
                "unit_of_measurement": row['defaultJednotky']
            }

            # word swap for floats
            if row["Format"] == "SwappedFloat":
                sensor["swap"] = "word"

            devices[node]["sensor"].append(sensor)
            
        #panel view creation
            grid[node]["cards"].append({
                        "type": "tile",
                        "entity": f"sensor.{uniqueName(f"{node}_{row['qname']}").lower()}",
                        "features_position": "bottom",
                        "vertical": 0,
                        "grid_options":{"columns": "full"}
            })  
            
        # create template variables
            if "sensor" not in template:
                template["sensor"]=[]
            attributes = {}
            # for rowAttr in df.to_dict(orient="records"):
            attributes = {k: str(v) for k, v in row.items() 
                            if pd.notna(v) and not str(v).startswith(" ")}
            
            attributes["Address"] = str(int(attributes["Address"][1:])-1)
            
            template["sensor"].append({
                "name": modbusName(f"{node}_{row['qname']}"),
                "state": f"{{{{ states('sensor.{uniqueName(f"{node}_{row['qname']}")}') }}}}",
                "unit_of_measurement": row['defaultJednotky'],
                "unique_id": modbusUniqueName(f"{node}_{row['qname']}"),
                "attributes": attributes
            })     



    for node, cfg in devices.items():
        modbus_config.append({
            "name": node,
            **cfg
        })
    print(f"config done: {File}")

# === SAVE YAML ===
with open("modbus.yaml", "w") as f:
    yaml.dump({"modbus": modbus_config}, f, sort_keys=False)

print("✅ modbus.yaml generated")


for gridItem in grid:    
    view["sections"].append(grid[gridItem])
    
with open("view.yaml", "w") as f:
    yaml.dump({"views": [view]}, f, sort_keys=False)
    

with open("template.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"template": [template]}, f, sort_keys=False,allow_unicode=True)
    
with open("sensor.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"template": [template["sensor"]]}, f, sort_keys=False,allow_unicode=True)

with open("binary_sensor.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"template": [template["binary_sensor"]]}, f, sort_keys=False,allow_unicode=True)