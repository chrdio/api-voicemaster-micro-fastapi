from typing import Optional
from pydantic import BaseModel
from chrdiotypes.musical import PseudoMIDI, CheetSheet
from chrdiotypes.transport import PerformanceTransport


class Endpoint(BaseModel):
    """A model to deserialize the configuration of remote endpoints."""

    name: str
    host: str
    port: str
    path: str
    option: Optional[str] = None
    prefix: str = "http://"

    def __str__(self) -> str:
        if self.option is not None:
            option = "/" + self.option
        else:
            option = ""
        return f"{self.prefix}{self.host}:{self.port}/{self.path}{option}"


def construct_voice_data(
    voices: PseudoMIDI, cheet_sheet: CheetSheet
) -> PerformanceTransport:
    """Converts a voicemaster-native PseudoMIDI object
    and a API-native CheetSheet object
    into a API-native PerformanceTransport object.
    """

    nodes = cheet_sheet.info
    performance = PerformanceTransport(
        perf_id=voices.ticket, key=cheet_sheet.key, path_nodes=nodes
    )
    return performance
