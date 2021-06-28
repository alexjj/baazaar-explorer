import pathlib
import requests
import pandas as pd
from string import Template

DATA_PATH = pathlib.Path(__file__).parent.parent.joinpath("data")

all_gotchis_query = Template("""
{
    aavegotchis(
      first: 1000,
      skip: $skip,
      orderBy: id,
      orderDirection: asc,
      where:{ status: 3, owner_not: "0x0000000000000000000000000000000000000000" }
    ) {
      id
      hauntId
      name
      numericTraits
      modifiedNumericTraits
      withSetsNumericTraits
      baseRarityScore
      modifiedRarityScore
      withSetsRarityScore
      kinship
      experience
      equippedWearables
      owner {
        id
      }
    }
  }
""")