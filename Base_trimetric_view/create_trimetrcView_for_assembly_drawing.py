import NXOpen
import NXOpen.Drawings
import NXOpen.Preferences

def create_base_view(workPart, model_view_name, sheet_name, placement):
    sheet = workPart.DraftingDrawingSheets.FindObject(sheet_name)
    sheet.Open()

    bld = workPart.DraftingViews.CreateBaseViewBuilder(NXOpen.Drawings.BaseView.Null)

    modeling_view = workPart.ModelingViews.FindObject(model_view_name)
    bld.SelectModelView.SelectedView = modeling_view

       # 1) Center lines OFF (create with center lines)
    bld.Style.ViewStyleGeneral.Centerlines = False

    # 2) Hidden lines -> Invisible (ukryte linię niewidoczne czcionką "Invisible")
    bld.Style.ViewStyleHiddenLines.Font = NXOpen.Preferences.Font.Invisible 

    # Pozycja na arkuszu
    bld.Placement.Placement.SetValue(NXOpen.TaggedObject.Null, workPart.Views.WorkView, placement)

    base_view = bld.Commit()
    bld.Destroy()
    return base_view

def main():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work

    create_base_view(
        workPart=workPart,
        model_view_name="Trimetric",   
        sheet_name="Sheet 1",
        placement=NXOpen.Point3d(185.0, 239.0, 0.0)
    )

if __name__ == "__main__":
    main()