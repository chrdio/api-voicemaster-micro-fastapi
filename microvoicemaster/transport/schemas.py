from typing import List, Optional, Tuple
from pydantic import BaseModel
from voicemaster import ChordIntervalStructures, ChordSymbolStructures, PseudoMIDI, CheetSheet

class Endpoint(BaseModel):
    name: str
    host: str
    port: str
    path: str
    option: Optional[str] = None
    prefix: str = 'http://'

    def __str__(self):
        if self.option is not None:
            option = '/' + self.option
        else:
            option = ''
        return f"{self.prefix}{self.host}:{self.port}/{self.path}{option}"


class PerformanceData(BaseModel):
    perf_id: str
    key: int
    path_nodes: List[Tuple[str, str]]


def construct_voice_data(voices: PseudoMIDI, cheet_sheet: CheetSheet) -> PerformanceData:
    nodes = cheet_sheet.info
    performance = PerformanceData(
        perf_id=voices.ticket,
        key=cheet_sheet.key,
        path_nodes=nodes
        )
    return performance
