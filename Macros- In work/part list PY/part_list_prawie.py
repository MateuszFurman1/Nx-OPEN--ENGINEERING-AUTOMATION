import NXOpen
import NXOpen.Annotations
import NXOpen.Assemblies
import NXOpen.Drawings
import NXOpen.UF # Niezbędny do użycia stałych filtrów selekcji

def select_view():
    """
    Wymusza na użytkowniku interaktywny wybór rzutu rysunkowego (View) w oknie graficznym NX.
    """
    the_ui = NXOpen.UI.GetUI()
    message = "Wskaż rzut (widok), dla którego chcesz utworzyć listę części"
    title = "Wybór widoku"
    
    # Utworzenie maski selekcji, która akceptuje tylko obiekty typu UF_view_type
    # Rozwiązuje to problem AttributeError: '...' has no attribute 'Views'
    mask = NXOpen.Selection.MaskTriple(NXOpen.UF.UFConstants.UF_view_type, 0, 0)
    selection_mask = [mask]
    
    # Użycie SelectionScope.AnyInAssembly zazwyczaj zapewnia, że można kliknąć w rzut
    response, selected_obj, cursor = the_ui.SelectionManager.SelectTaggedObject(
        message, 
        title, 
        NXOpen.Selection.SelectionScope.AnyInAssembly, # Zakres wyboru w zespole
        NXOpen.Selection.SelectionAction.ClearAndEnableSpecific,
        False, 
        False, 
        selection_mask)
    
    if response == NXOpen.Selection.Response.Ok:
        # Zwraca wybrany obiekt (który jest obiektem View)
        return selected_obj
    return None

def main(): 
    the_session = NXOpen.Session.GetSession()
    work_part = the_session.Parts.Work
    
    # 0. Użytkownik wskazuje widok
    # Jeśli użytkownik anuluje, selected_view będzie None i skrypt się zakończy
    selected_view = select_view()
    if selected_view is None:
        the_ui = NXOpen.UI.GetUI()
        the_ui.NXMessageBox.Show("Anulowano", NXOpen.NXMessageBox.DialogType.Information, "Operacja tworzenia listy części anulowana przez użytkownika.")
        return 

    mark_id = the_session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Create Parts List")
    
    # Inicjalizacja Buildera
    plist_builder = work_part.Annotations.PartsLists.CreatePartsListBuilder(None)
    
    # PRZYPISANIE WIDOKU do buildera listy części
    plist_builder.View.Value = selected_view
    
    # 1. Ustawienia zakresu
    plist_builder.Contents.Scope = NXOpen.Annotations.PartsListContentsBuilder.ScopeType.TopLevelOnly
    
    try:
        # Próba znalezienia aranżacji, jeśli istnieje
        arrangement = work_part.ComponentAssembly.Arrangements.FindObject("SEPARATOR_UP")
        plist_builder.Contents.Arrangement.SelectedArrangement = arrangement
    except NXOpen.NXException:
        # Złapanie błędu, jeśli aranżacja nie istnieje (np. w prostej części)
        pass

    # 2. Konfiguracja kolumn
    column_settings = plist_builder.Settings.TableColumnSettingsBuilder
    column_settings.TableColumnList.Clear()

    # Kolumna 1: PC NO (Callout)
    col1 = column_settings.CreateTableColumnBuilder()
    col1.Title = "PC NO"
    col1.DefaultText = "<W$=@CALLOUT>"
    column_settings.TableColumnList.Append(col1)

    # Kolumna 2: DB PART NAME
    col2 = column_settings.CreateTableColumnBuilder()
    col2.Title = "DB PART NAME"
    col2.DefaultText = "<W$=@DB_PART_NAME>"
    column_settings.TableColumnList.Append(col2)

    # Kolumna 3: QTY (Ilość)
    col3 = column_settings.CreateTableColumnBuilder()
    col3.Title = "QTY"
    col3.DefaultText = "$~Q"
    column_settings.TableColumnList.Append(col3)

    # 3. Stylistyka i orientacja
    # Nagłówek na dole
    plist_builder.Settings.TableSectionStyle.HeaderLocation = NXOpen.Annotations.TableSectionStyleBuilder.LocationOfHeader.Below
    
    # KIERUNEK WZROSTU - do góry (Up)
    # Upewnij się, że używasz właściwej klasy PartsListStyleBuilder
    plist_builder.Settings.PartsListStyle.GrowDirection = NXOpen.Annotations.PartsListStyleBuilder.GrowDirectionType.Up

    # Rozmiar tekstu
    plist_builder.Settings.LetteringStyle.GeneralTextSize = 2.0
    
    # 4. Lokalizacja tabeli (Punkt wstawienia)
    insertion_point = NXOpen.Point3d(398.8, 105.5, 0.0)
    plist_builder.Origin.Origin.SetValue(None, None, insertion_point)
    
    # 5. Zatwierdzenie
    final_object = plist_builder.Commit()
    plist_builder.Destroy()
    
    the_session.CleanUpFacetedFacesAndEdges()

if __name__ == '__main__':
    main()
