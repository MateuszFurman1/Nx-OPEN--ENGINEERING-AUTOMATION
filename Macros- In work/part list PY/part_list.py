import NXOpen
import NXOpen.Annotations
import NXOpen.Assemblies
import NXOpen.Drawings
# Usunięto import NXOpen.UF, ponieważ nie jest już potrzebny w tej metodzie

# Zmienna globalna the_session musi być dostępna dla funkcji
the_session = NXOpen.Session.GetSession()

def select_view_by_input_box():
    """
    Prosi użytkownika o wpisanie nazwy rzutu w prostym polu tekstowym 
    i znajduje ten rzut programowo.
    """
    the_ui = NXOpen.UI.GetUI() # Utworzenie instancji UI tutaj
    work_part = the_session.Parts.Work
    
    # 1. Pobierz nazwy wszystkich widoków (aby pokazać użytkownikowi opcje)
    view_names_display = []
    # Używamy GetDraftingViews(), jak ustalono wcześniej
    for sheet in work_part.DrawingSheets:
        for view in sheet.GetDraftingViews(): 
            view_names_display.append(view.Name)
    
    view_names_display = list(set(view_names_display))

    if not view_names_display:
        the_ui.NXMessageBox.Show("Błąd", NXOpen.NXMessageBox.DialogType.Error, "Brak rzutów rysunkowych w pliku.")
        return None

    # 2. Użyj prostego pola wejściowego, które działa niezawodnie
    message = "Dostępne rzuty:\n" + "\n".join(view_names_display) + "\n\nProszę wpisać DOKŁADNĄ nazwę rzutu (wielkość liter ma znaczenie):"
    
    # *** POPRAWKA BŁĘDU Z OBRAZKA ***
    # Dostęp do NXInputBox przez obiekt the_ui, a nie przez moduł NXOpen
    user_input, response = the_ui.NXInputBox.GetInputString( 
        message, 
        "Wybór widoku", 
        "") 
    
    if response != NXOpen.Response.Ok:
        return None # Użytkownik anulował
    
    target_name = user_input.strip() # Usuń białe znaki
    
    # 3. Znajdź obiekt programowo po nazwie
    for sheet in work_part.DrawingSheets:
        for view in sheet.GetDraftingViews():
            if view.Name == target_name:
                return view
                
    # Jeśli nie znaleziono po dokładnym dopasowaniu
    the_ui.NXMessageBox.Show("Błąd", NXOpen.NXMessageBox.DialogType.Error, f"Nie znaleziono rzutu o nazwie: '{target_name}'. Sprawdź pisownię.")
    return None


def main(): 
    work_part = the_session.Parts.Work
    
    selected_view = select_view_by_input_box() # Zmieniona nazwa funkcji
    if selected_view is None:
        # Możemy pominąć messagebox, jeśli user_input_box obsłuży anulowanie
        return 

    mark_id = the_session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Create Parts List")
    
    plist_builder = work_part.Annotations.PartsLists.CreatePartsListBuilder(None)
    plist_builder.View.Value = selected_view
    plist_builder.Contents.Scope = NXOpen.Annotations.PartsListContentsBuilder.ScopeType.TopLevelOnly
    
    try:
        arrangement = work_part.ComponentAssembly.Arrangements.FindObject("SEPARATOR_UP")
        plist_builder.Contents.Arrangement.SelectedArrangement = arrangement
    except NXOpen.NXException:
        pass

    column_settings = plist_builder.Settings.TableColumnSettingsBuilder
    column_settings.TableColumnList.Clear()

    col1 = column_settings.CreateTableColumnBuilder()
    col1.Title = "PC NO"
    col1.DefaultText = "<W$=@CALLOUT>"
    column_settings.TableColumnList.Append(col1)

    col2 = column_settings.CreateTableColumnBuilder()
    col2.Title = "DB PART NAME"
    col2.DefaultText = "<W$=@DB_PART_NAME>"
    column_settings.TableColumnList.Append(col2)

    col3 = column_settings.CreateTableColumnBuilder()
    col3.Title = "QTY"
    col3.DefaultText = "$~Q"
    column_settings.TableColumnList.Append(col3)

    plist_builder.Settings.TableSectionStyle.HeaderLocation = NXOpen.Annotations.TableSectionStyleBuilder.LocationOfHeader.Below
    plist_builder.Settings.PartsListStyle.GrowDirection = NXOpen.Annotations.PartsListStyleBuilder.GrowDirectionType.Up
    plist_builder.Settings.LetteringStyle.GeneralTextSize = 2.0
    
    insertion_point = NXOpen.Point3d(398.8, 105.5, 0.0)
    plist_builder.Origin.Origin.SetValue(None, None, insertion_point)
    
    final_object = plist_builder.Commit()
    plist_builder.Destroy()
    
    the_session.CleanUpFacetedFacesAndEdges()

if __name__ == '__main__':
    main()
