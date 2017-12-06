import cassiopeia as cass
from cassiopeia import Summoner, VerificationString


def get_verification_string():
    summoner = Summoner(name="Kalturi", region="NA")
    print(summoner.verification_string)

    vs = VerificationString(summoner=summoner, region="NA")
    print(vs.string)


if __name__ == "__main__":
    get_verification_string()
