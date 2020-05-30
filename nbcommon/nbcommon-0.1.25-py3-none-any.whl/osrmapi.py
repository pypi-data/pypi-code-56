from typing import List, Tuple, Optional, Dict
from pydantic import BaseModel
from enum import Enum
from .geo import LatLng
from . import aiorequests
from urllib.parse import urlencode
from osrm.engine.api.fbresult import FBResult as FBI

def decode_str(obj):
    if not obj:
        return None
    if type(obj) == bytes:
        return obj.decode()
    if type(obj) == str:
        return obj

class OutputFormat(str, Enum):
    json = 'json'
    flatbuffers = 'flatbuffers'


class Code(str, Enum):
    Ok = "Ok"
    InvalidUrl = "InvalidUrl"
    InvalidService = "InvalidService"
    InvalidVersion = "InvalidVersion"
    InvalidOptions = "InvalidOptions"
    InvalidQuery = "InvalidQuery"
    InvalidValue = "InvalidValue"
    NoSegment = "NoSegment"
    TooBig = "TooBig"


class Response(BaseModel):
    code: Code


LngLat = Tuple[float, float]  # format is: [lng, lat]


class WayPoint(BaseModel):
    hint: Optional[str]
    distance: float
    name: Optional[str]
    location: Optional[LngLat]
    nodes: Optional[List[int]]


class NearestResponse(Response):
    waypoints: List[WayPoint]

    @classmethod
    def from_dict(cls, dct: Dict):
        return cls(**dct)

    @classmethod
    def from_fb(cls, buf: bytes):
        fb = FBI.FBResult.GetRootAsFBResult(buf,0) 
        if fb.Error():
            code = decode_str(fb.Code().Code())
            return cls(code=code)
        code = Code.Ok
        waypoints = []
        wl = fb.WaypointsLength()
        for i in range(0,wl):
            wfb = fb.Waypoints(i)
            loc = wfb.Location()
            nodes = wfb.Nodes()
            wp= Waypoint(
                hint= decode_str(wfb.Hint()),
                location=(loc.Longtitude(),loc.Latitude()),
                name= decode_str(wfb.Name()),
                distance=wfb.Distance(),
            )
            if nodes:
                wp.nodes = [nodes.First(),nodes.Second()]
            waypoints.append(wp)

        return cls(code = code, waypoints= waypoints)




class Leg(BaseModel):
    distance: float
    duration: float


class Route(BaseModel):
    duration: Optional[float]
    distance: Optional[float]
    legs: List[Leg] = []
    geometry: str = None


class RouteResponse(Response):
    routes: List[Route] = []
    waypoints: List[WayPoint] = []
    
    @classmethod
    def from_dict(cls, dct: Dict):
        return cls(**dct)

    @classmethod
    def from_fb(cls, buf: bytes):
        fb = FBI.FBResult.GetRootAsFBResult(buf,0) 
        if fb.Error():
            code = decode_str(fb.Code().Code())
            return cls(code=code)
        code = Code.Ok
        routes = []
        waypoints = []
        rl = fb.RoutesLength()
        for i in range(0,rl):
            rfb = fb.Routes(i)
            route = Route(duration = rfb.Duration(), distance=rfb.Distance(), geometry=decode_str(rfb.Polyline()))
            ll = rfb.LegsLength()
            for j in range(0, ll):
                lfb = rfb.Legs(j)
                leg = Leg(duration = lfb.Duration(), distance = lfb.Distance())
                route.legs.append(leg)
            routes.append(route)
        return cls(code = code, routes = routes, waypoints = waypoints)


class POI(BaseModel):
    name: str
    location: LngLat


class TableResponse(Response):
    sources: List[POI] = []
    destinations: List[POI] = []
    durations: List[List[float]] = []
    distances: List[List[float]] = []

    @classmethod
    def from_dict(cls, dct: Dict):
        return cls(**dct)

    @classmethod
    def from_fb(cls, buf: bytes):
        fb = FBI.FBResult.GetRootAsFBResult(buf,0) 
        if fb.Error():
            code = decode_str(fb.Code().Code())
            return cls(code=code)
        code = Code.Ok
        tfb = fb.Table()
        durations = [[y for y in x] for x in tfb.DurationsAsNumpy()]
        distances = [[y for y in x] for x in tfb.DistancesAsNumpy()]
        return cls(code = code, duration= durations, distances=distances) 



class TracePoint(BaseModel):
    matchings_index: int
    location: LngLat


class MatchResponse(Response):
    tracepoints: List[TracePoint]
    matchings: List[Route]

    @classmethod
    def from_dict(cls, dct: Dict):
        return cls(**dct)

    @classmethod
    def from_fb(cls, buf: bytes):
        fb = FBI.FBResult.GetRootAsFBResult(buf,0) 
        if fb.Error():
            code = decode_str(fb.Code().Code())
            return cls(code=code)
        code = Code.Ok
        matchings = []
        tracepoints = []
        rl = fb.RoutesLength()
        for i in range(0,rl):
            rfb = fb.Routes(i)
            route = Route(duration = rfb.Duration(), distance=rfb.Distance())
            matchings.append(route)
        wl = fb.WaypointsLength()
        for i in range(0,wl):
            wfb = fb.Waypoints(i)
            loc = wfb.Location()
            tp= TracePoint(matchings_index = wfb.MatchingsIndex(), location=(loc.Longtitude(),loc.Latitude()))
            tracepoints.append(tp)

        return cls(code = code, matchings= matchings, tracepoints= tracepoints)



class Gaps(str, Enum):
    """
    Allows the input track splitting based on huge timestamp gaps between points.
    """
    split = "split"
    ignore = "ignore"

def parse_google_coords(inp: str):
    return [LatLng(lat=float(t[0]),lng=float(t[1])) for t in [pair.split(',') for pair in [pairs for pairs in inp.split('|')] ]]



class API:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.valid_formats = ['json','flatbuffers']

    async def _call(self, url:str,output_format:OutputFormat, responseCls):
        if output_format not in self.valid_formats:
            raise ValueErorr(f'invalid output format: {self.output_format}')
        if output_format == 'json':
            return responseCls.from_dict(await aiorequests.http_get_json(url))
        elif output_format == 'flatbuffers':
            return responseCls.from_fb(await aiorequests.http_get_raw(url))


    async def nearest(self, loc: LatLng,output_format: OutputFormat, radius: Optional[float] = None, bearing: Optional[float] = None) -> NearestResponse:
        url = f'{self.base_url}/nearest/v1/driving/{loc.lng},{loc.lat}.{output_format}'
        params = {}
        if radius is not None:
            params['radiuses'] = radius
        if bearing is not None:
            params['bearings'] = bearing
        url += "?" + urlencode(params)
        return await self._call(url, output_format, NearestResponse)

    async def table(self, coords: List[LatLng], sources: List[int], destinations: List[int], output_format: OutputFormat) -> TableResponse:
        coords_param = ';'.join([f'{c.lng},{c.lat}' for c in coords])
        sources_param = ';'.join(sources)
        destinations_param = ';'.join(destinations)
        url = f'{self.base_url}/table/v1/driving/{coords_param}.{output_format}?sources={sources_param}&destinations={destinations_param}&annotations=duration,distance'
        return await self._call(url, output_format, TableResponse)
        
    async def match(self, coords: List[LatLng], output_format: OutputFormat,
                    timestamps: Optional[List[int]] = None,
                    radiuses: Optional[List[float]] = None,
                    gaps: Gaps = Gaps.split,
                    tidy: bool = False) -> MatchResponse:

        coords_param = ';'.join([f'{c.lng},{c.lat}' for c in coords])
        url = f'{self.base_url}/match/v1/driving/{coords_param}.{output_format}'
        params = {}
        if timestamps is not None:
            params['timestamps'] = ";".join(timestamps)
        if radiuses is not None:
            params['radiuses'] = ";".join(radiuses)
        params['gaps'] = gaps.value
        if tidy:
            params['tidy'] = "true"
        url += "?" + urlencode(params)
        return await self._call(url, output_format, MatchResponse)

    async def route(self, coords: List[LatLng], output_format: OutputFormat) -> RouteResponse:
        coords_param = ';'.join([f'{c.lng},{c.lat}' for c in coords])
        url = f'{self.base_url}/route/v1/driving/{coords_param}.{output_format}?overview=full'
        return await self._call(url, output_format, RouteResponse)

