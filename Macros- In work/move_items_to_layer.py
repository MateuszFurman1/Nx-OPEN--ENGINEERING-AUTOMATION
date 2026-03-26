# intellisense by theScriptingEngineer (www.theScriptingEngineer.com)
# Created by theScriptingEngineer
#
import math
import NXOpen
import NXOpen.Layer
from typing import List


the_session  = NXOpen.Session.GetSession()
the_lw: NXOpen.ListingWindow = the_session.ListingWindow
workPart = the_session.Parts.Work
displayPart = the_session.Parts.Display


def move_object_to_layer(object: NXOpen.DisplayableObject, layer: int):
    objectArray1 = [NXOpen.DisplayableObject.Null] * 1 
    objectArray1[0] = object
    workPart.Layers.MoveDisplayableObjects(layer, objectArray1)    


def get_all_bodies() -> List[NXOpen.Body]:
    all_bodies: List[NXOpen.Body] = []
    for item in workPart.Bodies: # type: ignore
        all_bodies.append(item)
    return all_bodies


def get_all_datum_planes() -> List[NXOpen.DatumPlane]:
    all_datum_planes: List[NXOpen.DatumPlane] = []
    for item in workPart.Datums: # type: ignore
        # the_lw.WriteFullline(item.JournalIdentifier + " " + str(type(item))) # Usuń lub zakomentuj tę linię
        if isinstance(item, NXOpen.DatumPlane):
            all_datum_planes.append(item)
    return all_datum_planes


def get_all_sketches() -> List[NXOpen.Sketch]:
    all_sketches: List[NXOpen.Sketch] = []
    for item in workPart.Sketches: # type: ignore
        the_lw.WriteFullline(item.JournalIdentifier + " " + str(type(item)))
        all_sketches.append(item)
    return all_sketches


def main() :
    the_lw.Open()
    all_bodies: List[NXOpen.Body] = get_all_bodies()
    for i in range(len(all_bodies)):
        move_object_to_layer(all_bodies[i], 1)
    
    all_datum_planes: List[NXOpen.DatumPlane] = get_all_datum_planes()
    for i in range(len(all_datum_planes)):
        move_object_to_layer(all_datum_planes[i], 50)

    all_sketches: List[NXOpen.Sketch] = get_all_sketches()
    for i in range(len(all_sketches)):
        move_object_to_layer(all_sketches[i], 30)


if __name__ == '__main__':
    main()
