from aiohttp import ClientSession
from chrdiotypes.musical import PseudoMIDI, CheetSheet
from .caller import post_single_request
from .endpoints import ENDPOINTS
from .schemas import construct_voice_data


async def ensure_voices_bg(voices: PseudoMIDI, cheet_sheet: CheetSheet):
    session = ClientSession()
    endpoint = ENDPOINTS["microaccountant/music"]
    microaccountant_response = await post_single_request(
        endpoint, construct_voice_data(voices, cheet_sheet), session=session
    )

    # Tests cannot provide remote connection
    await session.close()  # pragma: no cover
    return microaccountant_response  # pragma: no cover
