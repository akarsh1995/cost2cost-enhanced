import os
from pathlib import Path
from typing import Iterable, List

import pandas as pd


class ColNames:
    id = "Processor Number"
    i_type = "Brand Modifier"
    gen = "Intel® Core™ \nGeneration"
    # 'Quarter Launch', 'Year launch',
    # 'Lithography (Process Technology) (nm)', '# of Cores', '# of P-cores',
    # '# of E-cores', '# of Threads', 'Max Turbo Frequency (GHz)',
    # 'Performance-core Base Frequency (GHz)',
    # 'Efficient-core Base Frequency (GHz)', 'Processor Base Frequency (GHz)',
    # 'Cache (MB)',
    # 'Processor Base Power (previously Thermal Design Power (TDP)) \n(W)',
    # 'Max Memory Size (dependent on memory type) GB', 'Memory Types',
    # 'Max # of PCI Express Lanes',
    socket = "Supported Socket"
    # 'Intel® Processor Graphics', 'Graphics Max Dynamic Frequency (GHz)',
    # 'Intel® Optane™ Memory Supported', 'Intel® Turbo Boost Technology 2.0',
    # 'Intel® Turbo Boost Max Technology 3.0',
    # 'Intel® vPro™ Platform Eligibility',
    # 'Max Resolution for HDMI,\n Max Resolution for DP, \nMax Resolution for (eDP - Integrated Flat Panel)'


intel_cpu_chart = Path(os.environ["INTEL_CPU_LIST"])

intel_df = pd.read_excel(intel_cpu_chart, skiprows=6)

intel_df = intel_df[~intel_df[ColNames.gen].isna()]
intel_df = intel_df[~intel_df[ColNames.gen].str.contains("X-series")]
intel_df[ColNames.gen] = intel_df[ColNames.gen].str.replace("th", "").astype(int)


def url_filtering_rule(cpu_id: str, arr: List[str]) -> str:
    # for url in arr:
    #     if cpu_id.lower() in url.lower():
    #         return url
    return arr[0]


def get_processor_ids_by_gen(gen: Iterable[int]) -> List[str]:
    return list(intel_df.loc[intel_df[ColNames.gen].isin(gen), ColNames.id])
