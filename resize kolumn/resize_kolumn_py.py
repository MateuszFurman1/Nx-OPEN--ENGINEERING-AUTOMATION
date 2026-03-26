import NXOpen
import NXOpen.Annotations
import NXOpen.UF

def main():
    the_session = NXOpen.Session.GetSession()
    the_uf_session = NXOpen.UF.UFSession.GetUFSession()
    work_part = the_session.Parts.Work
    lw = the_session.ListingWindow
    
    lw.Open()
    #lw.WriteLine("Uruchamianie operacji (NX 2007)...")

    mark_id = the_session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Resize and Align columns")

    # Znalezienie Listy Części (PartsList)
    parts_list = None
    for table in work_part.Annotations.Tables:
        if isinstance(table, NXOpen.Annotations.PartsList):
            parts_list = table
            #lw.WriteLine(f"Znaleziono PartsList: {parts_list.Name}")
            break

    if parts_list is None:
        lw.WriteLine("Blad: Nie znaleziono listy czesci.")
        return

    # --- Operacje na kolumnach ---
    resize_column(the_session, the_uf_session, parts_list, 0, 10.0)
    resize_column(the_session, the_uf_session, parts_list, 1, 120.0)
    resize_column(the_session, the_uf_session, parts_list, 2, 40.0)
    resize_column(the_session, the_uf_session, parts_list, 3, 20.0)
    
    # --- Ustawienie wyrownania: MidLeft kolumna 1---
    alignment_type = NXOpen.Annotations.TableCellStyleBuilder.TextAlignmentType.MidRight
    set_column_text_alignment(the_session, work_part, parts_list, 1, alignment_type)

    alignment_type = NXOpen.Annotations.TableCellStyleBuilder.TextAlignmentType.MidLeft
    set_column_text_alignment(the_session, work_part, parts_list, 1, alignment_type)

     # --- Ustawienie wyrownania: MidLeft kolumna 0---
    alignment_type = NXOpen.Annotations.TableCellStyleBuilder.TextAlignmentType.MidCenter
    set_column_text_alignment(the_session, work_part, parts_list, 0, alignment_type)

    #lw.WriteLine("Operacja zakonczona.")

def resize_column(the_session, uf_session, parts_list, column_index, new_width):
    lw = the_session.ListingWindow
    try:
        column_tag = uf_session.Tabnot.AskNthColumn(parts_list.Tag, column_index)
        if column_tag != 0:
            uf_session.Tabnot.SetColumnWidth(column_tag, new_width)
            #lw.WriteLine(f"Kolumna {column_index + 1}: nowa szerokosc {new_width}.")
    except Exception as ex:
        lw.WriteLine(f"Blad szerokosci kolumny {column_index + 1}: {str(ex)}")

def set_column_text_alignment(the_session, work_part, parts_list, column_index, alignment):
    lw = the_session.ListingWindow
    the_uf_session = NXOpen.UF.UFSession.GetUFSession()
    try:
        column_tag = the_uf_session.Tabnot.AskNthColumn(parts_list.Tag, column_index)
        if column_tag == 0:
            return

        # Rozwiązanie dla NX 2007: Pobranie managera bezpośrednio z sesji
        # W Pythonie dla tej wersji, metoda GetTaggedObject jest dostępna przez właściwość TaggedObjectManager
        column_obj = the_session.GetObjectManager().GetTaggedObject(column_tag)
        
        if column_obj is None:
            return

        objects_to_edit = [column_obj]
        
        settings_builder = work_part.SettingsManager.CreateTableEditSettingsBuilder(objects_to_edit)
        settings_builder.TableCell.TextAlignment = alignment
        
        settings_builder.Commit()
        settings_builder.Destroy()
        
        #lw.WriteLine(f"Ustawiono wyrownanie kolumny {column_index + 1} na {alignment}.")
    except Exception as ex:
        # Jeśli powyższe zawiedzie, próbujemy alternatywnej metody dostępnej w niektórych kompilacjach NX
        try:
            column_obj = NXOpen.TaggedObjectManager.GetTaggedObject(column_tag)
            # ... powtórzenie logiki budowania (skrócone dla czytelności)
            settings_builder = work_part.SettingsManager.CreateTableEditSettingsBuilder([column_obj])
            settings_builder.TableCell.TextAlignment = alignment
            settings_builder.Commit()
            settings_builder.Destroy()
            #lw.WriteLine(f"Ustawiono wyrownanie kolumny {column_index + 1} .")
        except:
            lw.WriteLine(f"Blad wyrownania: {str(ex)}")

if __name__ == '__main__':
    main()
