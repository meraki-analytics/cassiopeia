import cassiopeia as cass
from cassiopeia import Platform

# On rare occasions you may want to avoid using Cass's nice type system and instead access dictionary-like objects
#  pulled directly from the Riot API (or other data sources).
# This should be a rare use case, and it neglects the part of Cass that's fun to use (which is the interface). Instead,
#  you will have to create queries to Cass's datapipeline manually. This is undocumented functionality. You can look in
#  the files in cassiopeia/datastores/riotapi to figure out what the query parameters are.
# You also need to specify the type you are requesting, which will likely be a dto type located in one of the
#  cassiopeia/dto files. In most cases you can also request Data types, which are located in cassiopeia/core, and the
#  class names end in "Data". "Data" types are an attempt to improve upon Riot's dto data format to make the data
#  itself easier to work with. In some instances, you may want to store Data types in your database rather than dto
#  types.

# Below is an example of requesting a summoner dto, which is returned as a dictionary. The dictionary can be converted
#  to json or to msgpack bytes. msgpack is a compressed form of json that is often used for sending data over the
#  internet. I also included an example for pulling a match.
# I can imagine you may want to use the pipeline directly if, for example, all you want you do is create a database.
#  In that case, you would set Cass up to use a database such as SQL, then iterate over a list of match IDs (gathered
#  however you want) and make a pipeline request for a MatchDto for each match ID. This would pull the match data from
#  Riot and populate your database with the MatchDto data. This will be faster than doing the same thing using Cass's
#  core interface, but the logic will be more complex and there may be some nuanced issues that you'll have to figure
#  out.


def use_pipeline():
    pipeline = cass._get_pipeline()

    summoner_dto = pipeline.get(cass.dto.summoner.SummonerDto,
                                query={"name": "Kalturi", "platform": Platform.north_america})
    print(summoner_dto)
    print(summoner_dto.to_json(indent=2))
    print(summoner_dto.to_bytes())  # Requires `pip install msgpack`

    print()
    match_dto = pipeline.get(cass.dto.match.MatchDto,
                             query={"id": 3000332065, "platform": Platform.north_america})
    print(match_dto.keys())
    print(match_dto['gameCreation'])


if __name__ == "__main__":
    use_pipeline()
