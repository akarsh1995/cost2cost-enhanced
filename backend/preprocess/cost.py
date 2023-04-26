import pandas as pd

df_cat_cost2cost = [
    "CPU INTEL",
    "CPU AMD",
    "BOARD INTEL CPU",
    "BOARD AMD",
    "SSD DRIVE",
    "HARD DISK",
    "RAM",
    "Graphic Card",
    "CABINET",
    "MONITOR",
    "KEYBOARD",
    "MOUSE",
    "PRINTER P.S.C.",
    "SPEAKER",
    "UPS",
    "WEBCAM",
    "USB HARD DISK",
    "HEAD PHONE",
    "COM. PERIPHERALS",
    "NET WORKING",
    "PEN DRIVE",
    "FLASH CARD",
    "DVR & ASSCERIES",
    "SOFTWARE",
    "FAN FOR CPU",
    "COMPUTER SCANNER",
    "PRINTER",
    "CABLE & CONN.",
    "SMPS",
]

df_cat_md_comp = [
    "Custom Cooling System",
    "Processor",
    "Cooling System",
    "Motherboard",
    "Memory (Ram)",
    "Storage",
    "Graphics Card",
    "Power Supply",
    "Cabinet (Case)",
    "Monitors",
    "Peripherals",
    "Combo Deals",
]


def levenshtein_distance_matrix(str_array1, str_array2):
    m = len(str_array1)
    n = len(str_array2)
    distance_matrix = [[0] * (n) for _ in range(m)]
    for i in range(m):
        distance_matrix[i][0] = i
    for j in range(n):
        distance_matrix[0][j] = j
    for i in range(1, m):
        for j in range(1, n):
            if str_array1[i - 1] == str_array2[j - 1]:
                cost = 0
            else:
                cost = 1
            distance_matrix[i][j] = min(
                distance_matrix[i - 1][j] + 1,
                distance_matrix[i][j - 1] + 1,
                distance_matrix[i - 1][j - 1] + cost,
            )
    return distance_matrix


distance_matrix = levenshtein_distance_matrix(df_cat_md_comp, df_cat_cost2cost)
for acc, row in zip(df_cat_md_comp, distance_matrix):
    print(acc, [df_cat_cost2cost[i] for i in row][:5])


# cost2cost preprocessing
df_cost2cost = pd.read_json("/home/akarshj/Programming/pdf_read_py/cost2cost.json")

df_cost2cost = pd.json_normalize(df_cost2cost.data)
df_cost2cost = df_cost2cost.explode("products")
df_cost2cost.reset_index(drop=True, inplace=True)
df_cost2cost = pd.concat(
    [df_cost2cost[["category", "gst"]], pd.json_normalize(df_cost2cost["products"])],
    axis="columns",
)

# md computers preprocessing
df_md_comp = pd.read_json(
    "/home/akarshj/Programming/pdf_read_py/all_prods_md_comp.json"
)
df_md_comp = df_md_comp.explode("products")

df_md_comp.reset_index(drop=True, inplace=True)
df_md_comp = pd.concat(
    [df_md_comp[["category"]], pd.json_normalize(df_md_comp["products"])],
    axis="columns",
)
df_md_comp["price"] = df_md_comp.price.str.replace("₹", "").str.replace(",", "")
df_md_comp["image"] = "https:" + df_md_comp["image"]


categories_to_pick = [
    "CPU INTEL",
    "CPU AMD",
    "Processor",
]

cpus_md = df_md_comp[df_md_comp.category.isin(categories_to_pick)]
cpus_md["gen"] = (
    cpus_md.title.str.extract(r"(\d?\d\d\d\d[KFXG\s]*)")[0]
    .str.replace(" ", "")
    .str.strip()
    .str.upper()
)

cpus_cost = df_cost2cost[df_cost2cost.category.isin(categories_to_pick)]
cpus_cost["gen"] = (
    cpus_cost["name"]
    .str.replace(r"[^A-z\d\s]", " ", regex=True)
    .str.extract(r"(\d?\d\d\d\d[KFXG3D\s]*)")[0]
    .str.replace(" ", "")
    .str.strip()
    .str.upper()
)
__import__("pdb").set_trace()


# cpus_cost.merge(cpus_md, how="left", on="gen").to_csv("merged_cpus.csv")
